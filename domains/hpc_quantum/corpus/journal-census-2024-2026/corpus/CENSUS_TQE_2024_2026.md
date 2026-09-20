# TQE Census 2024-2026 — HPC x Quantum-Computing Interface

**Journal:** IEEE Transactions on Quantum Engineering (TQE) · **ISSN** 2689-1808 · **Census date:** 2026-09-17

## 1. Scope and method

This is a **venue census of the HPC x quantum-computing interface**, not a quantum-computing literature review.

**The full population was screened.** All **246** records supplied for TQE volumes 5-7 (2024-2026), i.e. the complete
journal population for those years minus front matter and indexes, were read and classified individually against the
Three-Gate test in `CRITERIA.md`. No sampling, no keyword pre-filter and no seed whitelist were used; every record
carries a verdict and every excluded record carries a reason keyed to a false-positive class.

**Gate justifications.** Every retained record — all 62 INCLUDED and BORDERLINE records, plus the one
record moved out of the census window — carries three explicit per-record fields in `TQE_records.json`, reproduced in
sections 3, 4 and 7 below:

- `gate1` — the concrete classical systems problem that is substantively present (cost, parallelism, memory,
  communication, latency, throughput, scheduling, resource allocation, runtime, scaling, compilation cost,
  data movement, accelerator design or performance modeling);
- `gate2` — the HPC/systems/architecture technique that is a major part of the contribution. Where this gate is
  carried weakly the field says so explicitly (`WEAK:`), which is what separates BORDERLINE from INCLUDED;
- `gate3` — what the record tells us about future CPU/GPU/HPC to QPU heterogeneous computing.

BORDERLINE records additionally carry `borderline_reason_for` and `borderline_reason_against`. Verdicts changed
during verification carry a `notes` field recording the change and its justification.

**Year basis: YEAR_BASIS=ISSUE.** TQE census years rest on the volume cover year (v5 = 2024, v6 = 2025, v7 = 2026),
because IEEE Early Access dates are not available for most TQE records from the metadata sources used. Records with
no volume are IEEE Early Access and are placed by their supplied census year. The years were not re-derived here.
One record (TQE-007) is the exception: an Early Access date of 2023-12-26 was supplied from OpenAlex, which places it
before the census window, so it is marked `OUT_OF_WINDOW` and counts toward no 2024-2026 total.

**Outcome: 183 of 246 records (74.4%) were excluded**, 25 were included, 37 are
borderline and 1 fell outside the window. The high exclusion rate is the expected result and not a failure of
the search. TQE's entire population is quantum, so the binding question is never *is this quantum?* but *is there a
substantial classical computing / systems / HPC contribution?* For the large majority of TQE papers the classical
computer is a tool, not a subject: the paper is about a quantum network, a device, a sensor, a quantum algorithm
applied to a domain problem, a variational method, or a code construction. Those fail Gate 1 or Gate 2 and were
excluded without further analysis.

Abstracts in the dossier are truncated to 700 characters. Where a number or mechanism could not be recovered from the
truncated text it is recorded as `INSUFFICIENT_EVIDENCE`, and unsourced speedup figures are marked `BASELINE_UNCLEAR`.
Eight records carried no abstract at all and are flagged `NO_ABSTRACT`: TQE-143, TQE-156, TQE-236, TQE-241, TQE-242, TQE-244, TQE-245, TQE-246.
Ten records were checked against the publisher DOI or an arXiv abstract page to fill gaps; the IEEE Xplore landing
page for TQE-143 could not be retrieved, so that record stays at title-level evidence.

**Verification pass.** An adversarial verification pass was applied after the first build. Outcomes: TQE-007 moved to OUT_OF_WINDOW; TQE-108 and TQE-163 demoted INCLUDED -> BORDERLINE; TQE-034 challenged on Gate 2 and kept INCLUDED with a written rebuttal in its notes field; gate1/gate2/gate3 fields added to all retained records.

### Population and outcome

| Census year | Records | INCLUDED | BORDERLINE | EXCLUDED | OUT_OF_WINDOW |
|---|---:|---:|---:|---:|---:|
| 2024 | 76 | 7 | 9 | 59 | 1 |
| 2025 | 86 | 12 | 15 | 59 | 0 |
| 2026 | 84 | 6 | 13 | 65 | 0 |
| **Total** | **246** | **25** | **37** | **183** | **1** |

Article types across the whole population: ORIGINAL_RESEARCH 240, REVIEW_SURVEY 5, PERSPECTIVE 1. Included original-research count: **25**.

Scenario tags across INCLUDED + BORDERLINE: HPC_FOR_Q 54, FUTURE_WORKLOAD 13, Q_IN_HPC 5, Q_FOR_HPC 4.

Branch distribution across INCLUDED + BORDERLINE:

| Branch | Records |
|---|---:|
| benchmarking_performance_modeling | 16 |
| architecture_control | 16 |
| compiler_mapping_routing | 15 |
| qec_classical_processing | 11 |
| multi_qpu_distributed_qc | 7 |
| quantum_runtime_orchestration | 5 |
| scientific_workflow_application | 4 |
| distributed_gpu_simulation | 4 |
| qpu_scheduling_resource_mgmt | 3 |
| hybrid_workflow | 3 |
| circuit_cutting_reconstruction | 3 |
| hpc_qpu_integration | 2 |

## 2. Per-year screening tables

All 246 records, in dossier order. `FP` is the false-positive class for excluded records (legend in section 5).

### 2024 (76 records)

| ID | DOI | Vol/pp | Lead author | Title | Type | Verdict | FP |
|---|---|---|---|---|---|---|---|
| TQE-001 | 10.1109/tqe.2023.3333224 | v5/1-24 | Sangwoo Park | Quantum Conformal Prediction for Reliable Uncertainty Quantification in Quantum Machine Lear... | ORIG | EXCLUDED | 5 |
| TQE-002 | 10.1109/tqe.2023.3336514 | v5/1-11 | Mohammad Rezai | Quantum Computation via Multiport Discretized Quantum Fourier Optical Processors | ORIG | EXCLUDED | 6 |
| TQE-003 | 10.1109/tqe.2023.3337328 | v5/1-20 | Ginés Carrascal | Backtesting Quantum Computing Algorithms for Portfolio Optimization | ORIG | EXCLUDED | E8 |
| TQE-004 | 10.1109/tqe.2023.3338970 | v5/1-9 | Soronzonbold Otgonbaatar | Exploiting the Quantum Advantage for Satellite Image Processing: Review and Assessment | REVIEW | BORDERLINE | - |
| TQE-005 | 10.1109/tqe.2023.3341151 | v5/1-18 | Paolo Fittipaldi | A Linear Algebraic Framework for Dynamic Scheduling Over Memory-Equipped Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-006 | 10.1109/tqe.2023.3343625 | v5/1-11 | Fang Qi | Quantum Vulnerability Analysis to Guide Robust Quantum Computing System Design | ORIG | BORDERLINE | - |
| TQE-007 | 10.1109/tqe.2023.3347106 | v5/1-10 | Sebastian Brandhofer | Optimal Partitioning of Quantum Circuits Using Gate Cuts and Wire Cuts | ORIG | OUT_OF_WINDOW | - |
| TQE-008 | 10.1109/tqe.2023.3347476 | v5/1-17 | Jordi Pérez-Guijarro | Relation Between Quantum Advantage in Supervised Learning and Quantum Computational Advantage | ORIG | EXCLUDED | 7 |
| TQE-009 | 10.1109/tqe.2024.3358193 | v5/1-14 | Daniel Volya | State Preparation on Quantum Computers via Quantum Steering | ORIG | EXCLUDED | E11 |
| TQE-010 | 10.1109/tqe.2024.3358674 | v5/1-20 | Bethany Davies | Tools for the Analysis of Quantum Protocols Requiring State Generation Within a Time Window | ORIG | EXCLUDED | 4 |
| TQE-011 | 10.1109/tqe.2024.3359574 | v5/1-11 | Alon Kukliansky | Network Anomaly Detection Using Quantum Neural Networks on Noisy Quantum Computers | ORIG | EXCLUDED | 5 |
| TQE-012 | 10.1109/tqe.2024.3361810 | v5/1-11 | Alberto Tarable | Rateless Protograph LDPC Codes for Quantum Key Distribution | ORIG | EXCLUDED | 4 |
| TQE-013 | 10.1109/tqe.2024.3364546 | v5/1-12 | Shaowen Li | Parallelizing Quantum Simulation With Decision Diagrams | ORIG | INCLUDED | - |
| TQE-014 | 10.1109/tqe.2024.3366696 | v5/1-14 | Gayane Vardoyan | On the Bipartite Entanglement Capacity of Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-015 | 10.1109/tqe.2024.3367234 | v5/1-14 | Ryan L'Abbate | A Quantum-Classical Collaborative Training Architecture Based on Quantum State Fidelity | ORIG | EXCLUDED | 5 |
| TQE-016 | 10.1109/tqe.2024.3368073 | v5/1-13 | Qing Zhou | A Stable Hash Function Based on Parity-Dependent Quantum Walks With Memory (August 2023) | ORIG | EXCLUDED | 7 |
| TQE-017 | 10.1109/tqe.2024.3372880 | v5/1-14 | Marzio Vallero | Understanding Logical-Shift Error Propagation in Quanvolutional Neural Networks | ORIG | EXCLUDED | 5 |
| TQE-018 | 10.1109/tqe.2024.3373903 | v5/1-13 | Wenbin Yu | Application of Quantum Recurrent Neural Network in Low-Resource Language Text Classification | ORIG | EXCLUDED | 5 |
| TQE-019 | 10.1109/tqe.2024.3374251 | v5/1-13 | Giovanni Acampora | Quantum Fuzzy Inference Engine for Particle Accelerator Control | ORIG | EXCLUDED | E8 |
| TQE-020 | 10.1109/tqe.2024.3374879 | v5/1-15 | Sara Ayman Metwalli | Testing and Debugging Quantum Circuits | ORIG | BORDERLINE | - |
| TQE-021 | 10.1109/tqe.2024.3376721 | v5/1-14 | Tatsuhiko Shirai | Postprocessing Variationally Scheduled Quantum Algorithm for Constrained Combinatorial Optim... | ORIG | EXCLUDED | E8 |
| TQE-022 | 10.1109/tqe.2024.3383050 | v5/1-19 | Xia Liu | Mitigating Barren Plateaus of Variational Quantum Eigensolvers | ORIG | EXCLUDED | E9 |
| TQE-023 | 10.1109/tqe.2024.3385372 | v5/1-14 | Gayathree M. Vinod | Simulating Quantum Field Theories on Gate-Based Quantum Computers | ORIG | EXCLUDED | 3 |
| TQE-024 | 10.1109/tqe.2024.3385673 | v5/1-15 | Bagas Prabowo | Modeling and Experimental Validation of the Intrinsic SNR in Spin Qubit Gate-Based Readout a... | ORIG | EXCLUDED | 6 |
| TQE-025 | 10.1109/tqe.2024.3386753 | v5/1-19 | Shao-Hen Chiew | Multiobjective Optimization and Network Routing With Near-Term Quantum Computers | ORIG | EXCLUDED | E8 |
| TQE-026 | 10.1109/tqe.2024.3391654 | v5/1-19 | Elijah Pelofske | Probing Quantum Telecloning on Superconducting Quantum Processors | ORIG | EXCLUDED | 4 |
| TQE-027 | 10.1109/tqe.2024.3392834 | v5/1-10 | David Winderl | A Comparative Study on Solving Optimization Problems With Exponentially Fewer Qubits | ORIG | EXCLUDED | E8 |
| TQE-028 | 10.1109/tqe.2024.3393416 | v5/1-8 | Leonardo Oleynik | Variational Estimation of Optimal Signal States for Quantum Channels | ORIG | EXCLUDED | E12 |
| TQE-029 | 10.1109/tqe.2024.3393437 | v5/1-12 | Yuki Sano | Accelerating Grover Adaptive Search: Qubit and Gate Count Reduction Strategies With Higher O... | ORIG | EXCLUDED | 7 |
| TQE-030 | 10.1109/tqe.2024.3398410 | v5/1-18 | Carlo Mastroianni | Variational Quantum Algorithms for the Allocation of Resources in a Cloud/Edge Architecture | ORIG | BORDERLINE | - |
| TQE-031 | 10.1109/tqe.2024.3399609 | v5/1-13 | Lorenzo Valentini | Reliable Quantum Communications Based on Asymmetry in Distillation and Coding | ORIG | EXCLUDED | 4 |
| TQE-032 | 10.1109/tqe.2024.3401857 | v5/1-30 | Eric Sabo | Trellis Decoding for Qudit Stabilizer Codes and Its Application to Qubit Topological Codes | ORIG | BORDERLINE | - |
| TQE-033 | 10.1109/tqe.2024.3402085 | v5/1-10 | Willers Yang | Harnessing the Power of Long-Range Entanglement for Clifford Circuit Synthesis | ORIG | EXCLUDED | 7 |
| TQE-034 | 10.1109/tqe.2024.3404502 | v5/1-12 | Jordan Hines | Scalable Full-Stack Benchmarks for Quantum Computers | ORIG | INCLUDED | - |
| TQE-035 | 10.1109/tqe.2024.3407236 | v5/1-15 | David Bucher | Incentivizing Demand-Side Response Through Discount Scheduling Using Hybrid Quantum Optimiza... | ORIG | EXCLUDED | E8 |
| TQE-036 | 10.1109/tqe.2024.3408757 | v5/1-18 | Weining Dai | Advanced Shuttle Strategies for Parallel QCCD Architectures | ORIG | INCLUDED | - |
| TQE-037 | 10.1109/tqe.2024.3409309 | v5/1-12 | Zichang He | Distributionally Robust Variational Quantum Algorithms With Shifted Noise | ORIG | EXCLUDED | E9 |
| TQE-038 | 10.1109/tqe.2024.3409811 | v5/1-16 | Mathieu Toubeix | FASQuiC: Flexible Architecture for Scalable Spin Qubit Control | ORIG | INCLUDED | - |
| TQE-039 | 10.1109/tqe.2024.3412165 | v5/1-9 | Ioannis Krikidis | MIMO With 1-b Pre/Postcoding Resolution: A Quantum Annealing Approach | ORIG | EXCLUDED | E8 |
| TQE-040 | 10.1109/tqe.2024.3414264 | v5/1-14 | Matvei Anoshin | Hybrid Quantum Cycle Generative Adversarial Network for Small Molecule Generation | ORIG | EXCLUDED | 5 |
| TQE-041 | 10.1109/tqe.2024.3416836 | v5/1-17 | Luc Enthoven | Optimizing the Electrical Interface for Large-Scale Color-Center Quantum Processors | ORIG | BORDERLINE | - |
| TQE-042 | 10.1109/tqe.2024.3416963 | v5/1-4 | Kiyotaka Mukasa | Superconducting Through-Substrate Vias on Sapphire Substrates for Quantum Circuits | ORIG | EXCLUDED | 6 |
| TQE-043 | 10.1109/tqe.2024.3417816 | v7/1-14 | Vikesh Siddhu | Unital Qubit Queue-Channels: Classical Capacity and Product Decoding | ORIG | EXCLUDED | 4 |
| TQE-044 | 10.1109/tqe.2024.3418094 | v5/1-11 | André Sequeira | On Quantum Natural Policy Gradients | ORIG | EXCLUDED | 5 |
| TQE-045 | 10.1109/tqe.2024.3419773 | v5/1-13 | Hyunwoo Jung | Convolutional Neural Decoder for Surface Codes | ORIG | BORDERLINE | - |
| TQE-046 | 10.1109/tqe.2024.3421294 | v5/1-15 | Bryce Fuller | Approximate Solutions of Combinatorial Problems via Quantum Relaxations | ORIG | EXCLUDED | E8 |
| TQE-047 | 10.1109/tqe.2024.3425969 | v5/1-17 | Kumar Ghosh | Energy Risk Analysis With Dynamic Amplitude Estimation and Piecewise Approximate Quantum Com... | ORIG | EXCLUDED | E8 |
| TQE-048 | 10.1109/tqe.2024.3429451 | v5/1-22 | Nikiforos Paraskevopoulos | BeSnake: A Routing Algorithm for Scalable Spin-Qubit Architectures | ORIG | INCLUDED | - |
| TQE-049 | 10.1109/tqe.2024.3430215 | v5/1-26 | Daniel Hothem | Learning a Quantum Computer's Capability | ORIG | BORDERLINE | - |
| TQE-050 | 10.1109/tqe.2024.3432070 | v5/1-8 | Pasquale Ercolano | Superconducting Nanostrip Photon-Number-Resolving Detector as an Unbiased Random Number Gene... | ORIG | EXCLUDED | 6 |
| TQE-051 | 10.1109/tqe.2024.3432390 | v5/1-16 | Shahrooz Pouryousef | Resource Placement for Rate and Fidelity Maximization in Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-052 | 10.1109/tqe.2024.3435757 | v5/1-14 | Samudra Dasgupta | Improving Probabilistic Error Cancellation in the Presence of Nonstationary Noise | ORIG | EXCLUDED | E9 |
| TQE-053 | 10.1109/tqe.2024.3439135 | v5/1-9 | Kentaro Tamura | Noise Robustness of Quantum Relaxation for Combinatorial Optimization | ORIG | EXCLUDED | E8 |
| TQE-054 | 10.1109/tqe.2024.3440192 | v5/1-17 | Hany Khalifa | Fault-Tolerant One-Way Noiseless Amplification for Microwave Bosonic Quantum Information Pro... | ORIG | EXCLUDED | 6 |
| TQE-055 | 10.1109/tqe.2024.3441229 | v5/1-10 | John D. Malcolm | Multidisk Clutch Optimization Using Quantum Annealing | ORIG | EXCLUDED | E8 |
| TQE-056 | 10.1109/tqe.2024.3443660 | v5/1-14 | Jonathan Wurtz | Solving Nonnative Combinatorial Optimization Problems Using Hybrid Quantum–Classical Algorithms | ORIG | EXCLUDED | E8 |
| TQE-057 | 10.1109/tqe.2024.3445967 | v5/1-14 | Fabian Hader | Simulation of Charge Stability Diagrams for Automated Tuning Solutions (SimCATS) | ORIG | EXCLUDED | 6 |
| TQE-058 | 10.1109/tqe.2024.3447875 | v5/1-12 | Claudio Sanavio | Quantum Circuit for Imputation of Missing Data | ORIG | EXCLUDED | 5 |
| TQE-059 | 10.1109/tqe.2024.3450852 | v5/1-16 | Kein Yukiyoshi | Quantum Speedup of the Dispersion and Codebook Design Problems | ORIG | EXCLUDED | 7 |
| TQE-060 | 10.1109/tqe.2024.3454640 | v5/1-10 | Tong Zhao | Hierarchical Quantum Architecture Search for Variational Quantum Algorithms | ORIG | EXCLUDED | E9 |
| TQE-061 | 10.1109/tqe.2024.3464572 | v5/1-20 | Mohamed Shaban | SPARQ: Efficient Entanglement Distribution and Routing in Space–Air–Ground Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-062 | 10.1109/tqe.2024.3467271 | v5/1-18 | Namitha Liyanage | FPGA-Based Distributed Union-Find Decoder for Surface Codes | ORIG | INCLUDED | - |
| TQE-063 | 10.1109/tqe.2024.3475875 | v5/1-12 | Enrico Zardini | Local Binary and Multiclass SVMs Trained on a Quantum Annealer | ORIG | EXCLUDED | 5 |
| TQE-064 | 10.1109/tqe.2024.3476009 | v5/1-15 | Mohadeseh Azari | Quantum Switches for Gottesman–Kitaev–Preskill Qubit-Based All-Photonic Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-065 | 10.1109/tqe.2024.3476929 | v5/1-23 | Steven Herbert | Noise-Aware Quantum Amplitude Estimation | ORIG | EXCLUDED | E9 |
| TQE-066 | 10.1109/tqe.2024.3481280 | v5/1-19 | Yifeng Peng | HyQ2: A Hybrid Quantum Neural Network for NextG Vulnerability Detection | ORIG | EXCLUDED | 5 |
| TQE-067 | 10.1109/tqe.2024.3484650 | v5/1-12 | Ákos Nagy | Fixed-Point Grover Adaptive Search for Quadratic Binary Optimization Problems | ORIG | EXCLUDED | 7 |
| TQE-068 | 10.1109/tqe.2024.3486546 | v5/1-11 | Benjamin Gys | Hybrid Hamiltonian Simulation Approach for the Analysis of Quantum Error Correction Protocol... | ORIG | BORDERLINE | - |
| TQE-069 | 10.1109/tqe.2024.3488518 | v5/1-15 | Jorge M. Ramirez | Expressiveness of Commutative Quantum Circuits: A Probabilistic Approach | ORIG | EXCLUDED | E9 |
| TQE-070 | 10.1109/tqe.2024.3501683 | v6/1-15 | Miloš Prokop | Grover's Oracle for the Shortest Vector Problem and Its Application in Hybrid Classical–Quan... | ORIG | EXCLUDED | 1 |
| TQE-071 | 10.1109/tqe.2024.3507155 | v6/1-10 | Nishanth Chandra | FPGA-Based Synchronization of Frequency-Domain Interferometer for QKD | ORIG | EXCLUDED | 4 |
| TQE-072 | 10.1109/tqe.2024.3509019 | v6/1-16 | Ilora Maity | TAQNet: Traffic-Aware Minimum-Cost Quantum Communication Network Planning | ORIG | EXCLUDED | 4 |
| TQE-073 | 10.1109/tqe.2024.3511419 | v6/1-12 | Yigal Ilin | Dissipative Variational Quantum Algorithms for Gibbs State Preparation | ORIG | EXCLUDED | E9 |
| TQE-074 | 10.1109/tqe.2024.3512367 | v6/1-15 | Shivendra Singh Parihar | Novel Trade-offs in 5 nm FinFET SRAM Arrays at Extremely Low Temperatures | ORIG | EXCLUDED | 6 |
| TQE-075 | 10.1109/tqe.2024.3521442 | v6/1-17 | Yosuke Ueno | C3-VQA: Cryogenic Counter-Based Coprocessor for Variational Quantum Algorithms | ORIG | INCLUDED | - |
| TQE-076 | 10.1109/tqe.2024.3523889 | v6/1-14 | Sounak Kar | Convexification of the Quantum Network Utility Maximization Problem | ORIG | EXCLUDED | 4 |

### 2025 (86 records)

| ID | DOI | Vol/pp | Lead author | Title | Type | Verdict | FP |
|---|---|---|---|---|---|---|---|
| TQE-077 | 10.1109/tqe.2024.3520805 | v6/1-11 | João Barbosa | RSFQ All-Digital Programmable Multitone Generator for Quantum Applications | ORIG | BORDERLINE | - |
| TQE-078 | 10.1109/tqe.2025.3527399 | v6/1-15 | Sanjiang Li | Benchmarking Quantum Circuit Transformation With QKNOB Circuits | ORIG | INCLUDED | - |
| TQE-079 | 10.1109/tqe.2025.3528238 | v6/1-8 | Kristian S. Jensen | Quantum Two-Way Protocol Beyond Superdense Coding: Joint Transfer of Data and Entanglement | ORIG | EXCLUDED | 4 |
| TQE-080 | 10.1109/tqe.2025.3529868 | v6/1-17 | Chou-Wei Kiang | Wavelet-Based Quantum Sensing of Geomagnetic Fluctuations With Multiple NV Ensembles | ORIG | EXCLUDED | 6 |
| TQE-081 | 10.1109/tqe.2025.3530939 | v6/1-7 | Ryutaroh Matsumoto | Advance Sharing Procedures for the Ramp Quantum Secret Sharing Schemes With the Highest Codi... | ORIG | EXCLUDED | 4 |
| TQE-082 | 10.1109/tqe.2025.3532017 | v6/1-16 | Niclas Schillo | Variational Quantum Algorithms for Differential Equations on a Noisy Quantum Computer | ORIG | EXCLUDED | E9 |
| TQE-083 | 10.1109/tqe.2025.3535823 | v6/1-18 | Alessio Di Santo | Security and Fairness in Multiparty Quantum Secret Sharing Protocol | ORIG | EXCLUDED | 4 |
| TQE-084 | 10.1109/tqe.2025.3538934 | v6/1-14 | Mark A. Webster | Engineering Quantum Error Correction Codes Using Evolutionary Algorithms | ORIG | EXCLUDED | E10 |
| TQE-085 | 10.1109/tqe.2025.3541123 | v6/1-39 | Amar Abane | Entanglement Routing in Quantum Networks: A Comprehensive Survey | REVIEW | EXCLUDED | 4 |
| TQE-086 | 10.1109/tqe.2025.3541882 | v6/1-15 | Diego Alvarez-Estevez | Benchmarking Quantum Machine Learning Kernel Training for Classification Tasks | ORIG | EXCLUDED | 5 |
| TQE-087 | 10.1109/tqe.2025.3542462 | v6/1-38 | Naoto Sato | Generating Shuttling Procedures for Constrained Silicon Quantum Dot Array | ORIG | BORDERLINE | - |
| TQE-088 | 10.1109/tqe.2025.3542484 | v6/1-10 | Marc Jofre | Qubit Rate Modulation-Based Time Synchronization Mechanism for Multinode Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-089 | 10.1109/tqe.2025.3544839 | v6/1-12 | Claudio Sanavio | Explicit Quantum Circuit for Simulating the Advection–Diffusion–Reaction Dynamics | ORIG | EXCLUDED | 7 |
| TQE-090 | 10.1109/tqe.2025.3548423 | v6/1-14 | Che-Ming Chang | Quantum Circuit Compilation for Trapped-Ion Processors With the Drive-Through Architecture | ORIG | INCLUDED | - |
| TQE-091 | 10.1109/tqe.2025.3548706 | v6/1-12 | Rei Sato | Two-Step Quantum Search Algorithm for Solving Traveling Salesman Problems | ORIG | EXCLUDED | 7 |
| TQE-092 | 10.1109/tqe.2025.3549305 | v6/1-10 | Kilian Dremel | Utilizing Quantum Annealing in Computed Tomography Image Reconstruction | ORIG | EXCLUDED | E8 |
| TQE-093 | 10.1109/tqe.2025.3549485 | v6/1-8 | Jiaming Wang | Observing the Poisson Distribution of a Coherent Microwave Field With a Parametric Photon De... | ORIG | EXCLUDED | 6 |
| TQE-094 | 10.1109/tqe.2025.3552006 | v6/1-17 | Xiaojie Fan | Optimized Distribution of Entanglement Graph States in Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-095 | 10.1109/tqe.2025.3552736 | v6/1-16 | Anthony J. Cressman | Emulation of Density Matrix Dynamics With Classical Analog Circuits | ORIG | BORDERLINE | - |
| TQE-096 | 10.1109/tqe.2025.3555145 | v6/1-16 | Maki Arai | Two-Dimensional Beam Selection by Multiarmed Bandit Algorithm Based on a Quantum Walk | ORIG | EXCLUDED | E8 |
| TQE-097 | 10.1109/tqe.2025.3555562 | v6/1-13 | Romain Piron | Mixed Grover: A Hybrid Version to Improve Grover's Algorithm for Unstructured Database Search | ORIG | EXCLUDED | 7 |
| TQE-098 | 10.1109/tqe.2025.3558090 | v6/1-26 | Avimita Chatterjee | A Comprehensive Cross-Model Framework for Benchmarking the Performance of Quantum Hamiltonia... | ORIG | INCLUDED | - |
| TQE-099 | 10.1109/tqe.2025.3560403 | v6/1-40 | Mohammad Amir Dastgheib | Quantum Direct-Sequence Spread-Spectrum CDMA Communication Systems: Mathematical Foundations | ORIG | EXCLUDED | 4 |
| TQE-100 | 10.1109/tqe.2025.3563805 | v6/1-22 | Vahideh Eshaghian | Runtime–Coherence Tradeoffs for Hybrid Satisfiability Solvers | ORIG | BORDERLINE | - |
| TQE-101 | 10.1109/tqe.2025.3567322 | v6/1-13 | Claudio Cicconetti | Modeling and Performance Evaluation of Hybrid Classical–Quantum Serverless Computing Platforms | ORIG | INCLUDED | - |
| TQE-102 | 10.1109/tqe.2025.3568865 | v6/1-13 | XiYuan Liang | Three-Party Controlled Authentication Semiquantum Key Agreement Protocol for Online Joint Co... | ORIG | EXCLUDED | 4 |
| TQE-103 | 10.1109/tqe.2025.3569338 | v6/1-27 | Marzieh Bathaee | Quantum Wavelength-Division Multiplexing and Multiple-Access Communication Systems and Netwo... | ORIG | EXCLUDED | 4 |
| TQE-104 | 10.1109/tqe.2025.3569922 | v6/1-22 | Bacui Li | Computable Model-Independent Bounds for Adversarial Quantum Machine Learning | ORIG | EXCLUDED | 5 |
| TQE-105 | 10.1109/tqe.2025.3571484 | v6/1-12 | Yu Liu | Analysis of Parameterized Quantum Circuits: On the Connection Between Expressibility and Typ... | ORIG | EXCLUDED | E9 |
| TQE-106 | 10.1109/tqe.2025.3572142 | v6/1-16 | Yikai Mao | Q-Gen: A Parameterized Quantum Circuit Generator | ORIG | BORDERLINE | - |
| TQE-107 | 10.1109/tqe.2025.3572764 | v6/1-24 | Pei-Hao Liou | Reducing Quantum Error Correction Overhead With Versatile Flag-Sharing Syndrome Extraction C... | ORIG | BORDERLINE | - |
| TQE-108 | 10.1109/tqe.2025.3574463 | v6/1-12 | Jan Ole Ernst | Memory-Optimized Cubic Splines for High-Fidelity Quantum Operations | ORIG | BORDERLINE | - |
| TQE-109 | 10.1109/tqe.2025.3577769 | v6/1-16 | Jiahan Chen | Improved Belief Propagation Decoding Algorithms for Surface Codes | ORIG | BORDERLINE | - |
| TQE-110 | 10.1109/tqe.2025.3580377 | v6/1-18 | Job van Staveren | Cryo-CMOS Bias-Voltage Generation and Demultiplexing at mK Temperatures for Large-Scale Arra... | ORIG | EXCLUDED | 6 |
| TQE-111 | 10.1109/tqe.2025.3583570 | v6/1-8 | Laura Di Marino | Control of a Josephson Digital Phase Detector via an SFQ-Based Flux Bias Driver | ORIG | EXCLUDED | 6 |
| TQE-112 | 10.1109/tqe.2025.3585413 | v6/1-12 | Michihiko Sugawara | SU(4) Gate Design via Unitary Process Tomography: Its Application to Cross-Resonance-Based S... | ORIG | EXCLUDED | E11 |
| TQE-113 | 10.1109/tqe.2025.3586541 | v6/1-23 | Michael Garn | Quantum Resource Estimates for Computing Binary Elliptic Curve Discrete Logarithms | ORIG | EXCLUDED | 1 |
| TQE-114 | 10.1109/tqe.2025.3588783 | v6/1-18 | Evan Sutcliffe | Fidelity-Aware Multipath Routing for Multipartite State Distribution in Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-115 | 10.1109/tqe.2025.3591213 | v6/1-12 | Kaito Kishi | Simulation of Shor Algorithm for Discrete Logarithm Problems With Comprehensive Pairs of Mod... | ORIG | EXCLUDED | 1 |
| TQE-116 | 10.1109/tqe.2025.3595275 | v6/1-14 | Marco Venere | A Grover-Meets-Simon Approach to Match Vector Boolean Functions | ORIG | EXCLUDED | 7 |
| TQE-117 | 10.1109/tqe.2025.3595703 | v6/1-11 | Alberto Tarable | Generalized Quantum-Assisted Digital Signature | ORIG | EXCLUDED | 4 |
| TQE-118 | 10.1109/tqe.2025.3595706 | v6/1-12 | Swaraj Shekhar Nande | TCEP-Based Synchronization for Practical Communication Network | ORIG | EXCLUDED | 4 |
| TQE-119 | 10.1109/tqe.2025.3595778 | v6/1-26 | Diogo Cruz | Fault-Tolerant Noise Guessing Decoding of Quantum Random Codes | ORIG | BORDERLINE | - |
| TQE-120 | 10.1109/tqe.2025.3595910 | v6/1-13 | Shintaro Fujiwara | Grover Adaptive Search With Spin Variables | ORIG | EXCLUDED | 7 |
| TQE-121 | 10.1109/tqe.2025.3596392 | v6/1-14 | Fabian Hader | Automated Charge Transition Detection in Quantum Dot Charge Stability Diagrams | ORIG | EXCLUDED | 6 |
| TQE-122 | 10.1109/tqe.2025.3596491 | v6/1-7 | Haley A. Weinstein | High-Fidelity Artificial Quantum Thermal State Generation Using Encoded Coherent States | ORIG | EXCLUDED | 4 |
| TQE-123 | 10.1109/tqe.2025.3599670 | v6/1-11 | Xiangjun Tan | Toward Axion Signal Extraction in Semiconductor Spin Qubits via Spectral Engineering | ORIG | EXCLUDED | 6 |
| TQE-124 | 10.1109/tqe.2025.3600216 | v6/1-17 | Christopher G. Yale | Realization and Calibration of Continuously Parameterized Two-Qubit Gates on a Trapped-Ion Q... | ORIG | EXCLUDED | E11 |
| TQE-125 | 10.1109/tqe.2025.3602404 | v6/1-14 | Tatsuhiko Shirai | Compressed Space Quantum Approximate Optimization Algorithm for Constrained Combinatorial Op... | ORIG | EXCLUDED | E8 |
| TQE-126 | 10.1109/tqe.2025.3603459 | v6/1-15 | Muhdin Abdo Wodedo | Amplifying Two-Mode Squeezing in Nanomechanical Resonators | ORIG | EXCLUDED | 6 |
| TQE-127 | 10.1109/tqe.2025.3604712 | v6/1-10 | Giuseppe Di Guglielmo | End-to-End Workflow for Machine-Learning-Based Qubit Readout With QICK and hls4ml | ORIG | INCLUDED | - |
| TQE-128 | 10.1109/tqe.2025.3606123 | v6/1-16 | Chunxiang Song | Fast State Stabilization Using Deep Reinforcement Learning for Measurement-Based Quantum Fee... | ORIG | EXCLUDED | E11 |
| TQE-129 | 10.1109/tqe.2025.3607689 | v6/1-21 | Koffka Khan | DT-QFL: Dual-Timeline Quantum Federated Learning With Time-Symmetric Updates, Temporal Memor... | ORIG | EXCLUDED | 5 |
| TQE-130 | 10.1109/tqe.2025.3608053 | v6/1-14 | Yaniv Kurman | Benchmarking the Ability of a Controller to Execute Quantum Error Corrected Non-Clifford Cir... | ORIG | INCLUDED | - |
| TQE-131 | 10.1109/tqe.2025.3610112 | v6/1-12 | Jannis Ruh | Quantum Circuit Optimization and MBQC Scheduling With a Pauli Tracking Library | ORIG | INCLUDED | - |
| TQE-132 | 10.1109/tqe.2025.3610800 | v6/1-25 | Moritz Schmidt | Exploration of Design Alternatives for Reducing Idle Time in Shor's Algorithm: A Study on Mo... | ORIG | INCLUDED | - |
| TQE-133 | 10.1109/tqe.2025.3611335 | v6/1-15 | Yoshimichi Tanizawa | Quantum Key Distribution Network and Quantum Secure Cloud Technologies for Genome Medicine U... | ORIG | EXCLUDED | 4 |
| TQE-134 | 10.1109/tqe.2025.3615886 | v6/1-17 | Ankit Kulshrestha | Neural Architecture Search Algorithms for Quantum Autoencoders | ORIG | EXCLUDED | 5 |
| TQE-135 | 10.1109/tqe.2025.3616080 | v6/1-8 | Paniz Foshat | Quasiparticle Dynamics in Niobium Nitride Superconducting Microwave Resonators at Single-Pho... | ORIG | EXCLUDED | 6 |
| TQE-136 | 10.1109/tqe.2025.3618295 | v6/1-11 | Hyunju Lee | Quantum Optimization Approaches in Medical Imaging: Advances in Quantum Algorithms for Medic... | ORIG | EXCLUDED | E8 |
| TQE-137 | 10.1109/tqe.2025.3619387 | v6/1-14 | Iago Fernández Llovo | Network-Assisted Collective Operations for Efficient Distributed Quantum Computing | ORIG | INCLUDED | - |
| TQE-138 | 10.1109/tqe.2025.3619944 | v6/1-11 | Shivendra Singh Parihar | Modeling and Evaluating Superconducting Ferroelectric SQUID Circuits | ORIG | EXCLUDED | 6 |
| TQE-139 | 10.1109/tqe.2025.3620104 | v6/1-19 | Miloš Prokop | Heuristic Time Complexity of NISQ Shortest-Vector-Problem Solvers | ORIG | EXCLUDED | 1 |
| TQE-140 | 10.1109/tqe.2025.3620130 | v6/1-18 | Francesco Turro | Toward Practical Application of the Quantum Carleman Lattice Boltzmann Method in Industrial ... | ORIG | BORDERLINE | - |
| TQE-141 | 10.1109/tqe.2025.3620628 | v6/1-20 | Yuhang Yao | On the Capacity of Vector Linear Computation Over a Noiseless Quantum Multiple-Access Channe... | ORIG | EXCLUDED | 4 |
| TQE-142 | 10.1109/tqe.2025.3622495 | v6/1-12 | Alon Kukliansky | Leveraging Quantum Machine Learning Generalization to Significantly Speed up Quantum Compila... | ORIG | INCLUDED | - |
| TQE-143 | 10.1109/tqe.2025.3623158 | v6/1-17 | Eneet Kaur | Optimized Quantum Circuit Partitioning Across Multiple Quantum Processors | ORIG | INCLUDED | - |
| TQE-144 | 10.1109/tqe.2025.3624658 | v7/4100629-4100629 | Thomas R. Beauchamp | A Modular Quantum Network Architecture for Integrating Network Scheduling With Local Program... | ORIG | BORDERLINE | - |
| TQE-145 | 10.1109/tqe.2025.3624699 | v7/1-18 | Zexian Li | Binary Tree Block Encoding of Classical Matrix | ORIG | BORDERLINE | - |
| TQE-146 | 10.1109/tqe.2025.3625774 | v7/1-19 | Jeremy Johnston | Quantum Detection Over Quantum Channels With Uncertainty | ORIG | EXCLUDED | E12 |
| TQE-147 | 10.1109/tqe.2025.3626745 | v7/1-27 | Linzhi Huang | A Dynamic Testing Strategy With Incremental Learning Model for Quantum Programs | ORIG | BORDERLINE | - |
| TQE-148 | 10.1109/tqe.2025.3627918 | v7/1-13 | Fumiyoshi Kobayashi | Erasure-Tolerance Scheme for the Surface Codes on Neutral Atom Quantum Computers | ORIG | EXCLUDED | E10 |
| TQE-149 | 10.1109/tqe.2025.3630201 | v7/1-15 | Benedikt Baier | Combined Physical- and Link-Layer Protocols for Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-150 | 10.1109/tqe.2025.3632540 | v7/1-15 | Miguel Palma | Hardware-Aware and Resource-Efficient Circuit Packing and Scheduling on Trapped-Ion Quantum ... | ORIG | INCLUDED | - |
| TQE-151 | 10.1109/tqe.2025.3633176 | v7/1-8 | Roberto Moretti | Transmon Qubit Modeling and Characterization for Dark Matter Search | ORIG | EXCLUDED | 6 |
| TQE-152 | 10.1109/tqe.2025.3636049 | v7/1-31 | Yannik N. Boeck | Feynman Meets Turing: Computability Aspects of Exact Circuit Synthesis, Gate Efficiency, and... | ORIG | BORDERLINE | - |
| TQE-153 | 10.1109/tqe.2025.3638878 | v7/1-14 | Subhadeep Mondal | Relative Entropy-Based Training of Quantum Neural Networks | ORIG | EXCLUDED | 5 |
| TQE-154 | 10.1109/tqe.2025.3640361 | v7/1-19 | Sana Javed | Low-Complexity Syndrome-Based Linear Programming Decoding of Quantum LDPC Codes | ORIG | BORDERLINE | - |
| TQE-155 | 10.1109/tqe.2025.3641027 | v7/1-14 | Kai Zhang | Optimal Control-Assisted Rapid Quantum State Transfer on 1-D Spin Chain | ORIG | EXCLUDED | E11 |
| TQE-156 | 10.1109/tqe.2025.3641834 | v7/1-30 | Scarlett Gauthier | On-Demand Resource Allocation for a Quantum Network Hub | ORIG | EXCLUDED | 4 |
| TQE-157 | 10.1109/tqe.2025.3642110 | v7/1-14 | Purin Pongpanich | Dual-Discriminator Hybrid Quantum Generative Adversarial Networks for Improved GAN Performance | ORIG | EXCLUDED | 5 |
| TQE-158 | 10.1109/tqe.2025.3645732 | v7/1-25 | Shin-Yi Wen | Robust $H_{\infty }$ Uncertainties-Tolerant Observer-Based Reference Quantum Trajectory Trac... | ORIG | EXCLUDED | E11 |
| TQE-159 | 10.1109/tqe.2025.3646010 | v7/1-12 | Hiromitsu Kigure | Black-Box Optimization of the Storage Location Assignment Problem in Logistics Centers Using... | ORIG | EXCLUDED | E8 |
| TQE-160 | 10.1109/tqe.2025.3646040 | v7/1-19 | Daniele Lizzio Bosco | Integrated Encoding and Quantization to Enhance Quanvolutional Neural Networks | ORIG | EXCLUDED | 5 |
| TQE-161 | 10.1109/tqe.2025.3649561 | v7/1-17 | Dawei Jiao | Quantum Error Correction for Second-Generation Quantum Repeaters | ORIG | EXCLUDED | 4 |
| TQE-162 | 10.1109/tqe.2025.3649709 | v7/1-21 | Marco Passafiume | A Sparse-Event Simulation Engine to Model Coincidence-Based Ranging Architectures in Quantum... | ORIG | EXCLUDED | 6 |

### 2026 (84 records)

| ID | DOI | Vol/pp | Lead author | Title | Type | Verdict | FP |
|---|---|---|---|---|---|---|---|
| TQE-163 | 10.1109/tqe.2025.3649617 | v7/1-18 | Nitish Kumar Chandra | Multiplexed Bilayered Realization of Fault-Tolerant Quantum Computation Over Optically Netwo... | ORIG | BORDERLINE | - |
| TQE-164 | 10.1109/tqe.2026.3653126 | v7/1-15 | Naphan Benchasattabuse | Bridging All-Photonic and Memory-Based Quantum Repeaters | ORIG | EXCLUDED | 4 |
| TQE-165 | 10.1109/tqe.2026.3653200 | v7/1-33 | Ashlesha Patil | A Graphical Rule Book for Clifford Manipulations of Stabilizer States | REVIEW | EXCLUDED | 7 |
| TQE-166 | 10.1109/tqe.2026.3654528 | v7/1-16 | Salahuddin Abdul Rahman | Feedback-Based Quantum Algorithm for Excited States Calculation | ORIG | EXCLUDED | E9 |
| TQE-167 | 10.1109/tqe.2026.3654543 | v7/1-15 | Yusuke Kimura | Improving Decision Diagram-Based Quantum Circuit Simulation Using Static Variable Ordering a... | ORIG | INCLUDED | - |
| TQE-168 | 10.1109/tqe.2026.3654929 | v7/1-16 | Zhen Qin | Optimal Allocation of Pauli Measurements for Low-Rank Quantum State Tomography | ORIG | EXCLUDED | E12 |
| TQE-169 | 10.1109/tqe.2026.3654930 | v7/1-13 | Boris Tsvelikhovskiy | Equivariant Quantum Approximate Optimization Algorithm | ORIG | EXCLUDED | E8 |
| TQE-170 | 10.1109/tqe.2026.3659017 | v7/1-7 | Ioannis Krikidis | Quantum Rotation Diversity in Displaced Squeezed Binary Phase-Shift Keying | ORIG | EXCLUDED | 4 |
| TQE-171 | 10.1109/tqe.2026.3659096 | v7/1-18 | Chenyi Zhang | Encrypted-State Quantum Compilation Scheme Based on Quantum Circuit Obfuscation for Quantum ... | ORIG | BORDERLINE | - |
| TQE-172 | 10.1109/tqe.2026.3659400 | v7/1-52 | Naheel Raza Rizvi | A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits | REVIEW | BORDERLINE | - |
| TQE-173 | 10.1109/tqe.2026.3659730 | v7/1-11 | Sigurd Huber | A Quantum Variational Approach to Phase-Only Pattern Synthesis | ORIG | EXCLUDED | E8 |
| TQE-174 | 10.1109/tqe.2026.3660364 | v7/1-12 | Zhelun Li | Information-Theoretic Analysis of Bayesian Quantum State Search | ORIG | EXCLUDED | E12 |
| TQE-175 | 10.1109/tqe.2026.3661822 | v7/1-11 | Ian Tomeo | Quantum Annealing for Robust Principal Component Analysis | ORIG | EXCLUDED | E8 |
| TQE-176 | 10.1109/tqe.2026.3662339 | v7/1-10 | Michelle Chalupnik | Realistic Quantum Network Simulation for Experimental BBM92 Key Distribution | ORIG | EXCLUDED | 4 |
| TQE-177 | 10.1109/tqe.2026.3663507 | v7/1-17 | Daniel Mastropietro | Parallel Variational Quantum Algorithms With Gradient-Informed Restart to Speed Up Optimizat... | ORIG | BORDERLINE | - |
| TQE-178 | 10.1109/tqe.2026.3664680 | v7/1-12 | Oskar Novak | Explaining Robust Quantum Metrology by Counting Codewords | ORIG | EXCLUDED | 6 |
| TQE-179 | 10.1109/tqe.2026.3665005 | v7/1-14 | Nilesh Sharma | Differential Phase Encoded Plug-and-Play Measurement-Device-Independent Quantum Key Distribu... | ORIG | EXCLUDED | 4 |
| TQE-180 | 10.1109/tqe.2026.3666889 | v7/1-10 | Xing-yu Wu | Accelerating the Max-Cut Problems via Distributed Ising Machine Solvers | ORIG | EXCLUDED | 2 |
| TQE-181 | 10.1109/tqe.2026.3667338 | v7/1-11 | Zhenlin Zhang | A Low Noise Signal Read-Out Circuit for Integrated Quantum Diamond Magnetometers | ORIG | EXCLUDED | 6 |
| TQE-182 | 10.1109/tqe.2026.3668098 | v7/1-10 | Maria Jose Lozano Palacio | Parameter Analysis and Optimization of Layer Fidelity for Quantum Processor Benchmarking at ... | ORIG | BORDERLINE | - |
| TQE-183 | 10.1109/tqe.2026.3669050 | v7/1-13 | Mingqi Zhang | Orthogonal Frequency-Division Multiplexing Continuous-Variable Terahertz QKD for Large-Scale... | ORIG | EXCLUDED | 4 |
| TQE-184 | 10.1109/tqe.2026.3669054 | v7/1-15 | Aditya Sodhani | Encoder Circuit Optimization for Nonbinary Quantum Error Correction Codes in Prime Dimension... | ORIG | EXCLUDED | E10 |
| TQE-185 | 10.1109/tqe.2026.3670136 | v7/1-15 | Sangkeum Lee | Measurement-Informed Safe Reinforcement Learning for Quantum Battery Charging via Harmonic-S... | ORIG | EXCLUDED | E11 |
| TQE-186 | 10.1109/tqe.2026.3670353 | v7/1-7 | Marc-Antoine Roux | Rapid Autotuning of a SiGe Quantum Dot Into the Single-Electron Regime With Machine Learning... | ORIG | BORDERLINE | - |
| TQE-187 | 10.1109/tqe.2026.3671723 | v7/1-13 | Shu Kanno | Efficient Implementation of Randomized Quantum Algorithms With Dynamic Circuits | ORIG | BORDERLINE | - |
| TQE-188 | 10.1109/tqe.2026.3673092 | v7/2100730-2100730 | Theerapat Tansuwannont | Synchronizable Hybrid Subsystem Codes | ORIG | EXCLUDED | E10 |
| TQE-189 | 10.1109/tqe.2026.3674210 | v7/1-26 | Andreea-Iulia Lefterovici | Beyond Asymptotic Scaling: Comparing Functional Quantum Linear Solvers | ORIG | BORDERLINE | - |
| TQE-190 | 10.1109/tqe.2026.3674396 | v7/1-15 | Abubakar Danasabe | QATNet: A Lightweight Quantum–Classical Tabular Network for Low-Latency Intrusion Detection | ORIG | EXCLUDED | 5 |
| TQE-191 | 10.1109/tqe.2026.3674551 | v7/1-15 | Nguyen Hoang Viet | Advanced Quantum Annealing for the Biobjective Traveling Thief Problem: An $\varepsilon$-Con... | ORIG | EXCLUDED | E8 |
| TQE-192 | 10.1109/tqe.2026.3674887 | v7/1-21 | Joaquin Chung | InterQnet: A Heterogeneous Full-Stack Approach to Co-Designing Scalable Quantum Networks | PERSP | EXCLUDED | 4 |
| TQE-193 | 10.1109/tqe.2026.3675340 | EarlyAccess/1-14 | Giuseppe Bisicchia | Cut&amp;shoot: Distributed Execution of Quantum Circuit Fragments | ORIG | INCLUDED | - |
| TQE-194 | 10.1109/tqe.2026.3677420 | v7/1-25 | Hafiz Muhammad Waseem | Quantum-Assisted Optimization and Security for Trustworthy AI-Driven Healthcare | ORIG | EXCLUDED | E8 |
| TQE-195 | 10.1109/tqe.2026.3677541 | v7/1-22 | Jordi Pérez-Guijarro | Extension of Clifford Data Regression Methods for Quantum Error Mitigation | ORIG | EXCLUDED | E9 |
| TQE-196 | 10.1109/tqe.2026.3678760 | v7/1-9 | Jin-Woo Kim | Impact of High-Brightness Entangled Photon Pairs on CHSH Inequality Experiment | ORIG | EXCLUDED | 6 |
| TQE-197 | 10.1109/tqe.2026.3678999 | v7/1-22 | Kentaro Ohno | Mitigating Precision Errors in Quantum Annealing via Coefficient Reduction of Embedded Hamil... | ORIG | EXCLUDED | E8 |
| TQE-198 | 10.1109/tqe.2026.3679863 | v7/1-14 | Ningxiang Chen | Robust Quantum Walk Search on Complete Multipartite Graph With Multiple Marked Vertices | ORIG | EXCLUDED | 7 |
| TQE-199 | 10.1109/tqe.2026.3680641 | v7/1-13 | Maksym Prodius | Robust Design Under Uncertainty in Quantum Error Mitigation | ORIG | EXCLUDED | E9 |
| TQE-200 | 10.1109/tqe.2026.3681202 | v7/1-23 | Xiaodong Zheng | Grover Adaptive Search-Based Hybrid Benders Decomposition for Mixed-Integer Linear Programs | ORIG | EXCLUDED | E8 |
| TQE-201 | 10.1109/tqe.2026.3681530 | v7/1-9 | Arim Ryou | Quantum Compressed Sensing Tomographic Reconstruction Algorithm | ORIG | EXCLUDED | E8 |
| TQE-202 | 10.1109/tqe.2026.3684081 | v7/4101113-4101113 | Mengyao Li | Defending QKD Networks: Routing and Wavelength Assignment to Mitigate Physical-Layer Attacks | ORIG | EXCLUDED | 4 |
| TQE-203 | 10.1109/tqe.2026.3687237 | v7/3103012-3103012 | Sayaki Matsushita | Quantum Communication Complexity of Regularized Linear Regression Protocols | ORIG | BORDERLINE | - |
| TQE-204 | 10.1109/tqe.2026.3688001 | v7/3103116-3103116 | Friedrich Wagner | Quantum Subroutines in Branch-Price-and-Cut for Vehicle Routing | ORIG | EXCLUDED | E8 |
| TQE-205 | 10.1109/tqe.2026.3689570 | v7/1-12 | Yachel Ben-Shalom | Efficient Optical Coupling of Color Center Ensembles in Diamond | ORIG | EXCLUDED | 6 |
| TQE-206 | 10.1109/tqe.2026.3690560 | v7/1-21 | Yuanjie Li | QCHFT: Quantum Cross-Hybrid Fine-Tuning for LLMs | ORIG | EXCLUDED | 5 |
| TQE-207 | 10.1109/tqe.2026.3690593 | v7/3103209-3103209 | Milad Eslaminia | Reducing Maximum Subcircuits Depth in Quantum Circuit Cutting | ORIG | INCLUDED | - |
| TQE-208 | 10.1109/tqe.2026.3690617 | v7/1-6 | Mingwei Lei | Satellite Microwave Detection via Cavity-Coupled Rydberg Atomic Receiver | ORIG | EXCLUDED | 6 |
| TQE-209 | 10.1109/tqe.2026.3691176 | v7/3103316-3103316 | Halima Giovanna Ahmad | Quantum Circuit-Based Adaptation for Credit Risk Analysis | ORIG | EXCLUDED | E8 |
| TQE-210 | 10.1109/tqe.2026.3692012 | v7/2101132-2101132 | Priya J. Nadkarni | Unified and Generalized Approach to Entanglement-Assisted Quantum Error Correction | ORIG | EXCLUDED | E10 |
| TQE-211 | 10.1109/tqe.2026.3693166 | v7/3103409-3103409 | Quinn Langfitt | Extrapolating Pauli Checks for Expectation Value Estimation on Noisy Quantum Devices | ORIG | EXCLUDED | E9 |
| TQE-212 | 10.1109/tqe.2026.3694290 | v7/4101216-4101216 | Shiye Zhang | Perfect Quantum Teleportation in Memory Amplitude-Damping Channels Based on Preflipping and ... | ORIG | EXCLUDED | 4 |
| TQE-213 | 10.1109/tqe.2026.3696519 | v7/3103513-3103513 | Lorenzo Raschi | Single-Hole Spin Qubit Optimization in SOI Quantum Dots via $\boldsymbol {k}\cdot \boldsymbo... | ORIG | EXCLUDED | 6 |
| TQE-214 | 10.1109/tqe.2026.3696707 | v7/3103619-3103619 | Chen Huang | ZAP: Zoned Architecture and Performant Compiler for Field-Programmable Atom Array | ORIG | INCLUDED | - |
| TQE-215 | 10.1109/tqe.2026.3696722 | v7/4101311-4101311 | Harshvardhan Kumar | A Novel n + / i -Well Dot Ge 1− x Sn x -on-Si Single-Photon Avalanche Photodiode for High-Fi... | ORIG | EXCLUDED | 6 |
| TQE-216 | 10.1109/tqe.2026.3697185 | v7/3103814-3103814 | Ali Hassan Homid | Engineering Minimal-Complexity Clifford Circuits Controlled by Microwaves via Coherent Phono... | ORIG | EXCLUDED | 6 |
| TQE-217 | 10.1109/tqe.2026.3697204 | v7/3103728-3103728 | Saleh Almutairi | Quantum Computing for Computational Sciences | REVIEW | BORDERLINE | - |
| TQE-218 | 10.1109/tqe.2026.3698350 | v7/2500608-2500608 | Pilsung Kang | Emergent Bifurcations in Quantum Circuit Stability From Hidden Parameter Statistics | ORIG | EXCLUDED | E9 |
| TQE-219 | 10.1109/tqe.2026.3700568 | v7/5500212-5500212 | Daniel Rocha-Aguilera | Impact of Interface Properties on Direct Tunneling in Al/ALD-Al 2 O 3 /Al Capacitors for Jos... | ORIG | EXCLUDED | 6 |
| TQE-220 | 10.1109/tqe.2026.3702762 | v7/4101412-4101412 | Mughees Ahmed Khan | Quantum Repeater Chains via Cavity–Magnon for Scalable Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-221 | 10.1109/tqe.2026.3702858 | v7/3103913-3103913 | Maher Harb | Quantum-Based Resilient Routing in Networks: Minimizing Latency Under Dual-Link Failures | ORIG | EXCLUDED | E8 |
| TQE-222 | 10.1109/tqe.2026.3703366 | v7/4101522-4101522 | Maxwell Tang | Routing in Nonisotonic Quantum Networks | ORIG | EXCLUDED | 4 |
| TQE-223 | 10.1109/tqe.2026.3705783 | v7/1-10 | Shangshu Li | DAG-Aware Gate Fusion for Efficient State-Vector Quantum-Circuit Simulation | ORIG | INCLUDED | - |
| TQE-224 | 10.1109/tqe.2026.3706630 | v7/1-17 | Tamiya Onodera | Multilevel Gate Set Optimization of Quantum Circuits for Partial Differential Equations | ORIG | BORDERLINE | - |
| TQE-225 | 10.1109/tqe.2026.3707428 | v7/1-12 | Yazan H. Al-Badarneh | Detection Error Probability Analysis Over Atmospheric Quantum Channels With Pointing Errors:... | ORIG | EXCLUDED | 4 |
| TQE-226 | 10.1109/tqe.2026.3707472 | v7/3104427-3104427 | Yifeng Peng | Quantum Squeeze-and-Excitation Networks: Harnessing Quantum Noise for Robust Attention Mecha... | ORIG | EXCLUDED | 5 |
| TQE-227 | 10.1109/tqe.2026.3708537 | v7/3104115-3104115 | Duc-Truyen Le | Variational Quantum Eigensolver: A Comparative Analysis of Classical and Quantum Optimizer M... | ORIG | EXCLUDED | E9 |
| TQE-228 | 10.1109/tqe.2026.3709156 | v7/2101210-2101210 | Rahul Singh | Resource-Efficient Emulation of Majorana Zero Mode Braiding on a Superconducting Trijunction | ORIG | EXCLUDED | 6 |
| TQE-229 | 10.1109/tqe.2026.3709247 | v7/3104025-3104025 | Ridho Nur Rohman Wijaya | Hybrid Quantum Capsule Network: Quantum Transformation Circuit as Vote Transformation in Ima... | ORIG | EXCLUDED | 5 |
| TQE-230 | 10.1109/tqe.2026.3710775 | v7/3104212-3104212 | Pavel Rytir | Topological Quantum Compilation Using Mixed-Integer Programming | ORIG | BORDERLINE | - |
| TQE-231 | 10.1109/tqe.2026.3712194 | v7/4101915-4101915 | Kuan-Wei Hu | Automated Active-Visibility-Control Loop for Stabilized DPS-QKD Decoding Under Dynamic Wavel... | ORIG | EXCLUDED | 4 |
| TQE-232 | 10.1109/tqe.2026.3712782 | v7/3104314-3104314 | Qi Lou | Matrix Low-Dimensional Qubit Casting Based Quantum Electromagnetic Transient Network Simulat... | ORIG | EXCLUDED | E8 |
| TQE-233 | 10.1109/tqe.2026.3714062 | v7/4101717-4101717 | Ange Joel Nounga Njanda | Quantum Communication Infrastructure Cost Optimization Using a Genetic Algorithm | ORIG | EXCLUDED | 4 |
| TQE-234 | 10.1109/tqe.2026.3715957 | v7/4101812-4101812 | Thomas Scarinzi | Boosting Information Reconciliation for Decoy-State Quantum Key Distribution Over a Satellit... | ORIG | EXCLUDED | 4 |
| TQE-235 | 10.1109/tqe.2026.3721256 | EarlyAccess/1-19 | Rodrigo M. Sanz | Efficiently Architecting VQAs: Expressibility–Trainability–Resources Pareto-Optimality | ORIG | EXCLUDED | E9 |
| TQE-236 | 10.1109/tqe.2026.3721271 | EarlyAccess/1-16 | Ashlesha Patil | Clifford Manipulations of Stabilizer States – Application to Linear Optical Qubits | ORIG | EXCLUDED | 7 |
| TQE-237 | 10.1109/tqe.2026.3721420 | v7/1-11 | Neel Malvania | Rydberg Atom Electric Field Sensors as Linear Time-Invariant Systems | ORIG | EXCLUDED | 6 |
| TQE-238 | 10.1109/tqe.2026.3722428 | v7/3104632-3104632 | Soshun Naito | Network-Based Quantum Computing: An Efficient Design Framework for Many-Small-Node Distribut... | ORIG | INCLUDED | - |
| TQE-239 | 10.1109/tqe.2026.3722517 | v7/4102012-4102012 | Amir Mohammad Yaghoobianzadeh | Entanglement Distribution and Teleportation in Assisted and Scalable Quantum Access Networks | ORIG | EXCLUDED | 4 |
| TQE-240 | 10.1109/tqe.2026.3724318 | v7/3500818-3500818 | Yuxuan Zhao | Dissipative Feedback and Hybrid Lyapunov–Reinforcement Learning Control for NV-Center Quantu... | ORIG | EXCLUDED | 6 |
| TQE-241 | 10.1109/tqe.2026.3728701 | EarlyAccess/1-13 | Martin Clason | Field Demonstration of a Passive Phase and Polarization Stabilization Architecture for Sagna... | ORIG | EXCLUDED | 4 |
| TQE-242 | 10.1109/tqe.2026.3728781 | EarlyAccess/1-16 | Mohamed F. Hagag | Integrated Superconducting High-Q Seamless Cavity for Quantum Memory and Qubit Readout Appli... | ORIG | EXCLUDED | 6 |
| TQE-243 | 10.1109/tqe.2026.3728800 | EarlyAccess/1-17 | David Barral | Interconnecting Regional QKD Networks: Hybrid Key Delivery Across Quantum Domains | ORIG | EXCLUDED | 4 |
| TQE-244 | 10.1109/tqe.2026.3729244 | EarlyAccess/1-17 | Rei Kawano | RuleSet Generation Framework for Application Layer Integration in Quantum Internet | ORIG | EXCLUDED | 4 |
| TQE-245 | 10.1109/tqe.2026.3730475 | EarlyAccess/1-15 | Hikaru Wakaura | Noise-model-free versus Bayes-optimal decoding of finite-energy GKP qubits | ORIG | BORDERLINE | - |
| TQE-246 | 10.1109/tqe.2026.3732924 | EarlyAccess/1-16 | Richard A. Brewster | Effect of Nonidealities on Nonlocal Quantum Entanglement Quality as Measured by the CHSH Ine... | ORIG | EXCLUDED | 6 |

## 3. Full records — INCLUDED (25)

Ordered by record id. Every entry passes all three gates, with the gate-by-gate justification stated in the record.

### TQE-013 — Parallelizing Quantum Simulation With Decision Diagrams

- **DOI:** 10.1109/tqe.2024.3364546 · **Census year:** 2024 · **v5**, pp. 1-12 · **Online:** 2024-01-01
- **Lead author:** Shaowen Li (+3 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** distributed_gpu_simulation
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Memory capacity is the binding limit of classical circuit simulation; the paper targets it directly.

**Gate 2 — HPC/systems technique in the contribution.** Parallelization of decision-diagram simulation (concurrent DD node operations under shared-table synchronization).

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows how the dominant HPC_FOR_Q workload behaves on parallel classical hardware and where its parallel efficiency breaks.

**Research question.** Can decision-diagram-based quantum circuit simulation be parallelized to overcome the memory wall of classical simulation?

**Quantum problem.** Simulating quantum state evolution on classical machines for algorithm development and verification.

**Classical / HPC problem.** Memory capacity is the binding constraint for classical simulation; decision diagrams compress state but their manipulation is hard to parallelize (pointer chasing, shared unique tables, dynamic data structures).

**Mechanism.** Parallelizes decision-diagram based simulation so that DD node operations are executed concurrently, trading synchronization cost against reduced wall-clock time while retaining the DD memory advantage.

**Computational bottleneck.** Memory footprint of the state representation; contention/synchronization in shared DD tables limiting parallel speedup.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Simulation runtime/speedup versus sequential DD simulation; specific figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Parallel decision-diagram simulation improves the scalability of classical quantum circuit simulation relative to a sequential DD simulator.

**Limitation.** DD efficiency is circuit-structure dependent; speedup does not transfer to circuits whose DD representation does not compress.

**Relevance.** Directly a classical HPC workload: memory-bound simulation of quantum circuits, the dominant HPC_FOR_Q consumer of cycles today.

### TQE-034 — Scalable Full-Stack Benchmarks for Quantum Computers

- **DOI:** 10.1109/tqe.2024.3404502 · **Census year:** 2024 · **v5**, pp. 1-12 · **Online:** 2024-01-01
- **Lead author:** Jordan Hines (+1 co-authors) · **arXiv:** 2312.14107
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Classical simulation cost of benchmark verification, which the construction is designed to eliminate.

**Gate 2 — HPC/systems technique in the contribution.** Benchmark-construction methodology that scores compiler plus hardware jointly using only efficient classical computation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Gives a way to measure a heterogeneous stack, including its classical compilation stage, past the classically simulable regime.

**Notes.** Verification rebuttal (Gate 2), kept INCLUDED. The systems contribution is not the benchmark scores but the construction itself: the paper's defining constraint is that both the benchmark circuits and their scoring must use only efficient classical computation, which removes the exponential classical-simulation step that every prior full-stack benchmark required. That is a computational-cost-driven methodology, not a device-characterization result. Second, the object measured is explicitly the integrated performance of the processor's classical compilation algorithms together with its low-level operations, so a classical stage of the stack is inside the measurement boundary. Benchmarking infrastructure and quantum performance modeling are named INCLUDE shapes in the criteria, and this record meets both on those grounds rather than on Gate-1 framing alone.

**Research question.** How can full-stack benchmarks be built for quantum processors running circuits that can no longer be classically simulated?

**Quantum problem.** Assessing the error rate of a processor on circuits of practical interest, including the effect of its own compiler.

**Classical / HPC problem.** Existing full-stack benchmarks require classical simulation of the benchmarked circuits, which is exponentially costly; the benchmark construction and scoring must instead use only efficient classical computation.

**Mechanism.** A general construction that turns any set of unitary circuits into a benchmark whose success criterion is computable with efficient classical processing, thereby measuring the integrated performance of the compiler plus the hardware.

**Computational bottleneck.** Classical simulation cost of verification, removed by construction.

**Evaluation platform.** Quantum processors (vendor/model not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Benchmark scores for random circuit families; numeric values not recoverable from the truncated abstract.

**Major claim.** Benchmarks that assess compiler plus hardware jointly can be constructed without classical simulation of the benchmarked circuits.

**Limitation.** Circuit classes must admit an efficiently checkable structure; the benchmark measures aggregate performance, not error localization.

**Relevance.** Benchmarking infrastructure whose design constraint is classical compute cost; also measures the classical compilation stage explicitly.

### TQE-036 — Advanced Shuttle Strategies for Parallel QCCD Architectures

- **DOI:** 10.1109/tqe.2024.3408757 · **Census year:** 2024 · **v5**, pp. 1-18 · **Online:** 2024-01-01
- **Lead author:** Weining Dai (+2 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control, compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Execution time is dominated by serialized ion transport; shuttle movements must be planned and parallelized.

**Gate 2 — HPC/systems technique in the contribution.** Architecture/topology and shuttle-scheduling co-design enabling concurrent transport.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows how architecture choices set the throughput a QPU can offer to a host system.

**Research question.** What trap topology and shuttling strategy reduce ion-movement overhead in QCCD trapped-ion architectures beyond the linear layout?

**Quantum problem.** Trapped-ion scalability is limited by trap capacity, forcing ion shuttling between zones for every non-local operation.

**Classical / HPC problem.** Shuttle scheduling is an architecture-aware routing/scheduling problem: the compiler must plan parallel ion movements over a topology, and execution time is dominated by this movement schedule.

**Mechanism.** Introduces trap topologies supporting parallel shuttling together with shuttle-planning strategies that exploit them, evaluated against the linear QCCD baseline.

**Computational bottleneck.** Serialization of ion transport operations; scheduling of concurrent shuttles without collisions.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in shuttling operations / execution time versus linear QCCD topologies; exact figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Parallel-capable QCCD topologies with matched shuttle strategies reduce movement overhead relative to linear QCCD architectures.

**Limitation.** Topologies are evaluated in simulation; physical feasibility of the proposed trap layouts is assumed.

**Relevance.** Architecture plus scheduling co-design of the kind that will determine QPU throughput inside a heterogeneous system.

### TQE-038 — FASQuiC: Flexible Architecture for Scalable Spin Qubit Control

- **DOI:** 10.1109/tqe.2024.3409811 · **Census year:** 2024 · **v5**, pp. 1-16 · **Online:** 2024-01-01
- **Lead author:** Mathieu Toubeix (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Control channel count, waveform memory and digital feedback latency scale with qubit count.

**Gate 2 — HPC/systems technique in the contribution.** FPGA control architecture (direct digital synthesis, bitstream switching, multichannel synchronization) with a measured latency figure.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Fixes the real-time latency budget (76.8 ns worst case) available to feedback-driven execution models.

**Research question.** Can a single FPGA-based control architecture provide scalable, low-latency multichannel waveform generation for spin qubits?

**Quantum problem.** Spin-qubit control requires precise, synchronized, fast-feedback pulse sequences across many channels.

**Classical / HPC problem.** Control hardware cost, channel count scaling, waveform memory and feedback latency are classical system-design constraints that grow with qubit count.

**Mechanism.** A direct-digital-synthesis architecture on FPGA generating programmable ramps, frequency combs and arbitrary waveforms at 5 GS/s, with bitstream switching for reconfigurability and synchronized multichannel operation.

**Computational bottleneck.** Digital feedback latency and per-channel resource cost in the FPGA fabric.

**Evaluation platform.** FPGA-based control system (FASQuiC).

**Scale.** 5 GS/s generation; multiple synchronized channels (exact count not recoverable from the truncated abstract).

**Performance metrics.** Worst-case digital feedback latency 76.8 ns; 5 GS/s arbitrary waveform generation. Baseline for the latency figure is not stated in the abstract (BASELINE_UNCLEAR).

**Major claim.** A reconfigurable FPGA control architecture delivers 5 GS/s multichannel spin-qubit control with worst-case 76.8 ns digital feedback latency.

**Limitation.** Scalability is argued architecturally; the abstract does not report operation at large channel counts.

**Relevance.** Classical control hardware is the real-time edge of the CPU/GPU-QPU stack; latency budgets here bound what feedback-driven execution models are possible.

### TQE-048 — BeSnake: A Routing Algorithm for Scalable Spin-Qubit Architectures

- **DOI:** 10.1109/tqe.2024.3429451 · **Census year:** 2024 · **v5**, pp. 1-22 · **Online:** 2024-01-01
- **Lead author:** Nikiforos Paraskevopoulos (+2 co-authors) · **arXiv:** 2403.16090
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Routing compile time is treated as a primary metric alongside routed-circuit execution time.

**Gate 2 — HPC/systems technique in the contribution.** Architecture-aware routing algorithm (BFS over SWAP and shuttle primitives) evaluated on compiler runtime as well as output quality.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies compilation scalability, the classical cost of preparing work for a QPU, as arrays grow.

**Research question.** How can qubit routing be performed for scalable spin-qubit architectures that support both SWAP and shuttle operations, at acceptable compile time?

**Quantum problem.** Two-qubit interactions on large spin-qubit arrays require moving qubit state across a constrained topology.

**Classical / HPC problem.** Routing is a classical compilation problem whose runtime must itself stay tractable as array size grows; the paper treats compiler execution time as a primary metric alongside circuit quality.

**Mechanism.** beSnake, a BFS-based routing algorithm that chooses between SWAP and shuttle operations to minimize execution time and fidelity loss while keeping routing computation fast.

**Computational bottleneck.** Compile-time cost of routing search on large architectures.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Routing quality (execution time, fidelity) and routing computation time versus prior SWAP-only methods; exact figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** A BFS-based router that admits shuttle operations improves routed-circuit execution time and fidelity while keeping routing computation fast, relative to SWAP-only routing baselines.

**Limitation.** Targets spin-qubit architectures specifically; shuttle cost model is architecture-dependent.

**Relevance.** Compilation scalability — the classical cost of preparing work for a QPU — is a core Quantum-HPC concern.

### TQE-062 — FPGA-Based Distributed Union-Find Decoder for Surface Codes

- **DOI:** 10.1109/tqe.2024.3467271 · **Census year:** 2024 · **v5**, pp. 1-18 · **Online:** 2024-01-01
- **Lead author:** Namitha Liyanage (+3 co-authors) · **arXiv:** 2406.08491
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Decoding latency must stay ahead of syndrome generation or the computation backs up exponentially.

**Gate 2 — HPC/systems technique in the contribution.** Distributed parallel decoder implemented on FPGA with the Helios hybrid tree-grid processing-element architecture.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Sets the latency and hardware-area budget for the classical real-time processor attached to a fault-tolerant QPU.

**Research question.** Can a Union-Find surface-code decoder be distributed across parallel hardware resources so that decoding latency stops growing with code distance?

**Quantum problem.** Real-time surface-code decoding must keep pace with syndrome generation or the computation suffers exponential backlog slowdown.

**Classical / HPC problem.** Decoding is a latency-critical classical workload; the paper builds a parallel/distributed hardware architecture and studies its time complexity and resource efficiency.

**Mechanism.** A distributed Union-Find decoder on an FPGA using the Helios architecture, which organizes parallel processing elements in a hybrid tree-grid structure so that syndrome data is processed locally and merged hierarchically.

**Computational bottleneck.** Decoding latency per measurement round; parallel resource count scaling as O(d^3); interconnect between processing elements.

**Evaluation platform.** Xilinx VCU129 FPGA.

**Scale.** Code distances up to d=21 in the latency-optimized configuration; d=51 in the resource-efficient configuration.

**Performance metrics.** 11.5 ns average decoding time per measurement round at d=21 under 0.1% phenomenological noise; 23.7 ns at d=17 under circuit-level noise; 544 ns per measurement round at d=51 in the resource-optimized configuration. Baseline: prior decoder implementations (the paper claims it is faster than existing implementations).

**Major claim.** With O(d^3) parallel resources the distributed UF decoder attains sublinear average time complexity in d, with per-round decoding time decreasing as d grows over the measured range.

**Limitation.** Parallel resource demand grows as O(d^3), so the latency result is bought with FPGA area; noise models are phenomenological/circuit-level simulation rather than live hardware syndromes.

**Relevance.** The canonical QEC classical-processing workload; sets the latency and area budget for the classical side of a fault-tolerant machine.

### TQE-075 — C3-VQA: Cryogenic Counter-Based Coprocessor for Variational Quantum Algorithms

- **DOI:** 10.1109/tqe.2024.3521442 · **Census year:** 2024 · **v6**, pp. 1-17 · **Online:** 2024-12-23
- **Lead author:** Yosuke Ueno (+7 co-authors) · **arXiv:** 2409.07847
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch:** architecture_control, hpc_qpu_integration
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Intertemperature wire bandwidth and the cryostat thermal budget bound how many qubits can be wired out.

**Gate 2 — HPC/systems technique in the contribution.** Near-data processing: an in-cryostat SFQ coprocessor performs part of the expectation-value reduction before data crosses the boundary.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Directly informs where classical compute should sit in the temperature/data-movement hierarchy of a hybrid machine.

**Research question.** Can near-data classical processing inside the cryostat reduce the intertemperature wiring bandwidth of a cryogenic quantum computer without adding significant heat?

**Quantum problem.** Variational algorithms require many shots whose measurement results must all be transported out of the cryostat, and every wire carries a passive heat load.

**Classical / HPC problem.** Thermal budget, interconnect bandwidth and near-data processing: a classic accelerator-placement/data-movement trade-off, here with cooling capacity as the constrained resource.

**Mechanism.** C3-VQA, a single-flux-quantum coprocessor at the 4 K stage that precomputes part of the expectation-value accumulation for VQAs and buffers intermediates in counters and bit-operation units, so fewer results cross the temperature boundary.

**Computational bottleneck.** Intertemperature wire bandwidth and the resulting heat dissipation; power of in-cryostat logic.

**Evaluation platform.** Design-level evaluation with workload analysis of VQA execution (SFQ logic at 4 K).

**Scale.** Case study extrapolated to a 10 000-qubit system.

**Performance metrics.** 30% reduction in total 4 K heat dissipation under sequential-shot execution and 81% under parallel-shot execution; 87% in a quantum-chemistry case study at 10 000 qubits. Baseline: the same cryogenic system without the coprocessor.

**Major claim.** Moving part of the expectation-value reduction into ultra-low-power in-cryostat logic reduces 4 K heat dissipation by 30-87% depending on shot execution mode and system size, relative to sending all measurement results out.

**Limitation.** Evaluation is architectural/analytical rather than a fabricated SFQ chip; benefit is specific to VQA-style workloads with large shot counts.

**Relevance.** A textbook near-data-processing argument applied to the quantum-classical interface; directly informs how classical compute should be partitioned across the temperature hierarchy.

### TQE-078 — Benchmarking Quantum Circuit Transformation With QKNOB Circuits

- **DOI:** 10.1109/tqe.2025.3527399 · **Census year:** 2025 · **v6**, pp. 1-15 · **Online:** 2025-01-01
- **Lead author:** Sanjiang Li (+2 co-authors) · **arXiv:** 2301.08932
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling, compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Compiler solution quality cannot be interpreted without a tight reference, so compilation cost is unmeasurable in practice.

**Gate 2 — HPC/systems technique in the contribution.** Benchmark construction with built-in near-optimal transformation cost, used to expose optimality gaps of QCT algorithms.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Provides the measurement basis for comparing the compilation stage of competing quantum software stacks.

**Research question.** How can quantum circuit transformation (qubit mapping and routing) algorithms be evaluated without a bias introduced by unknown optimal solutions?

**Quantum problem.** Connectivity-constrained hardware requires circuit transformation before execution.

**Classical / HPC problem.** Compiler evaluation methodology: without knowing the optimum, reported SWAP-count and depth overheads of competing compilers cannot be interpreted; this is a benchmarking-infrastructure problem for a classical compilation stage.

**Mechanism.** QKNOB constructs benchmark circuits with a built-in transformation of known near-optimal SWAP count and depth overhead, so any compiler's output can be compared to a tight reference.

**Computational bottleneck.** Compiler search cost and solution quality on constructed instances.

**Evaluation platform.** State-of-the-art quantum circuit transformation algorithms evaluated on QKNOB circuits.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Optimality gaps in SWAP count and depth for evaluated QCT algorithms; numeric values not recoverable from the truncated abstract.

**Major claim.** Benchmarks with known near-optimal transformation cost give an unbiased comparison of circuit transformation algorithms, revealing optimality gaps that prior benchmark sets could not expose.

**Limitation.** Constructed circuits may not represent application circuit structure; near-optimality is by construction, not proof of the true optimum.

**Relevance.** Compiler benchmarking infrastructure; underpins claims about compilation cost and quality in a Quantum-HPC software stack.

### TQE-090 — Quantum Circuit Compilation for Trapped-Ion Processors With the Drive-Through Architecture

- **DOI:** 10.1109/tqe.2025.3548423 · **Census year:** 2025 · **v6**, pp. 1-14 · **Online:** 2025-01-01
- **Lead author:** Che-Ming Chang (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing, architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Transport-operation scheduling determines execution time and fidelity on the target architecture.

**Gate 2 — HPC/systems technique in the contribution.** A full compilation flow (mapping, scheduling, transport planning) built for an architecture whose primitive set differs from standard hardware.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows how a change of hardware primitives propagates into the compiler, a recurring issue for heterogeneous back ends.

**Research question.** How should circuits be compiled for a trapped-ion 'drive-through' architecture in which transport gates replace conventional local entangling operations?

**Quantum problem.** A trapped-ion architecture designed to minimize heat generation changes the primitive operation set, so existing compilers do not apply.

**Classical / HPC problem.** Compilation for an architecture with transport-based primitives requires new mapping, scheduling and routing passes; the classical compiler stage determines achievable fidelity and execution time.

**Mechanism.** A compilation system tailored to the drive-through architecture that plans transport-gate sequences and schedules ion movement for the target program.

**Computational bottleneck.** Scheduling of transport operations; compile-time search over movement plans.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Fidelity/execution-time of compiled programs on the drive-through architecture; figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** A compilation flow specific to transport-gate trapped-ion architectures produces executable high-fidelity programs where general-purpose compilers do not apply.

**Limitation.** Single-architecture study; results are simulation-based.

**Relevance.** Architecture-aware compilation with substantial systems content (movement scheduling), one of the INCLUDE shapes.

### TQE-098 — A Comprehensive Cross-Model Framework for Benchmarking the Performance of Quantum Hamiltonian Simulations

- **DOI:** 10.1109/tqe.2025.3558090 · **Census year:** 2025 · **v6**, pp. 1-26 · **Online:** 2025-01-01
- **Lead author:** Avimita Chatterjee (+7 co-authors) · **arXiv:** 2409.06919
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** The classical reference computation (simulation or exact diagonalization) is the cost that limits benchmarking.

**Gate 2 — HPC/systems technique in the contribution.** A benchmarking framework and software implementation with three reference modes, including mirror circuits that need no classical reference.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Enables performance measurement of a quantum workload when the classical cross-check is no longer affordable.

**Research question.** How should Hamiltonian-simulation performance be benchmarked across devices when exact classical reference results are not always available?

**Quantum problem.** Trotterized Hamiltonian evolution is a core workload whose quality on real hardware must be quantified.

**Classical / HPC problem.** Benchmarking methodology and software framework: three benchmark modes trade off against the classical cost of producing a reference (noiseless simulation, exact diagonalization, or mirror circuits that need no reference).

**Mechanism.** A cross-model benchmarking framework and software implementation supporting comparison against a noiseless simulator, against exact diagonalization, and via scalable mirror circuits when classical reference is infeasible.

**Computational bottleneck.** Classical simulation/diagonalization cost of the reference, which is what forces the mirror-circuit mode.

**Evaluation platform.** Gate-based quantum computers plus classical simulators (specific devices not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Fidelity/quality metrics per benchmark mode; numeric values not recoverable from the truncated abstract.

**Major claim.** A single framework with three reference modes allows Hamiltonian-simulation benchmarking to extend past the point where classical reference computation is affordable.

**Limitation.** Mirror-circuit mode measures a proxy for the target workload rather than the workload itself.

**Relevance.** Benchmarking infrastructure explicitly organized around classical reference cost; useful for performance modeling of heterogeneous runs.

### TQE-101 — Modeling and Performance Evaluation of Hybrid Classical–Quantum Serverless Computing Platforms

- **DOI:** 10.1109/tqe.2025.3567322 · **Census year:** 2025 · **v6**, pp. 1-13 · **Online:** 2025-01-01
- **Lead author:** Claudio Cicconetti (+0 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** Q_IN_HPC, FUTURE_WORKLOAD · **Branch:** hpc_qpu_integration, qpu_scheduling_resource_mgmt, quantum_runtime_orchestration
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Queueing, scheduling, resource contention and quality of service for a shared classical-plus-QPU infrastructure.

**Gate 2 — HPC/systems technique in the contribution.** A serverless system model with an analytical/simulation performance evaluation of the hybrid platform under load.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Models QPUs as shared datacenter resources, the core Q_IN_HPC question of how QPU sharing affects user-visible performance.

**Research question.** What does a serverless execution model for hybrid classical-quantum workloads look like, and how does its performance depend on system parameters?

**Quantum problem.** Variational and other hybrid algorithms alternate between classical and quantum execution and need tight, low-overhead coupling of the two resources.

**Classical / HPC problem.** Resource management, queueing, scheduling and quality of service for a shared infrastructure hosting both classical functions and QPUs — a datacenter systems problem.

**Mechanism.** Defines a system model for a hybrid classical-quantum serverless platform together with an analytical/simulation performance evaluation of its behaviour under load.

**Computational bottleneck.** Queueing delay and resource contention at the QPU; invocation overheads of the serverless layer.

**Evaluation platform.** Model-based performance evaluation (analysis and simulation).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Response time / throughput / utilization as functions of system parameters; specific values not recoverable from the truncated abstract.

**Major claim.** A serverless system model captures the performance trade-offs of hybrid classical-quantum platforms and quantifies how QPU sharing affects user-visible quality of service.

**Limitation.** Model-based rather than measured on a deployed platform; QPU service-time assumptions drive the results.

**Relevance.** One of the clearest Q_IN_HPC papers in this venue: middleware, scheduling and QoS for QPUs as shared datacenter resources.

### TQE-127 — End-to-End Workflow for Machine-Learning-Based Qubit Readout With QICK and hls4ml

- **DOI:** 10.1109/tqe.2025.3604712 · **Census year:** 2025 · **v6**, pp. 1-10 · **Online:** 2025-01-01
- **Lead author:** Giuseppe Di Guglielmo (+12 co-authors) · **arXiv:** 2501.14663
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control, qec_classical_processing
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** PARTIAL — https://github.com/openquantumhardware/qick (Builds on the public QICK platform and the public hls4ml package; a paper-specific artifact release was not verified.)
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Real-time inference latency and FPGA resource budget for qubit-state discrimination at scale.

**Gate 2 — HPC/systems technique in the contribution.** Hardware/software codesign toolchain that compiles quantization-aware-trained networks into production control firmware (hls4ml into QICK on RFSoC).

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Establishes a reusable pattern for putting classical accelerators inside the control plane, applicable to decoders and feed-forward logic.

**Research question.** Can neural-network qubit-state discrimination be codesigned into FPGA control firmware to give accurate, low-latency readout at scale?

**Quantum problem.** Superconducting qubit readout must classify measurement traces accurately and fast enough for mid-circuit feedback.

**Classical / HPC problem.** Real-time inference on FPGA under strict latency and resource budgets; an end-to-end hardware/software toolchain from trained model to deployed firmware.

**Mechanism.** An end-to-end workflow embedding quantization-aware-trained neural networks into the QICK firmware on Xilinx RFSoC FPGAs via hls4ml, with Python APIs from model to bitstream.

**Computational bottleneck.** Inference latency and FPGA resource (DSP/LUT) usage; readout data rate.

**Evaluation platform.** Xilinx RFSoC FPGA running QICK; hls4ml toolchain; experimental superconducting qubit readout.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Readout accuracy and inference latency of the deployed model; specific values not recoverable from the truncated abstract.

**Major claim.** ML-based readout discriminators can be compiled into production quantum-control firmware with latency compatible with real-time operation, demonstrated experimentally.

**Limitation.** Demonstration scale (number of qubits/channels) is not stated in the abstract; model complexity is bounded by FPGA resources.

**Relevance.** Classical real-time accelerator design inside the control plane; the same toolchain pattern applies to decoders and feedback logic.

### TQE-130 — Benchmarking the Ability of a Controller to Execute Quantum Error Corrected Non-Clifford Circuits

- **DOI:** 10.1109/tqe.2025.3608053 · **Census year:** 2025 · **v6**, pp. 1-14 · **Online:** 2025-01-01
- **Lead author:** Yaniv Kurman (+6 co-authors) · **arXiv:** 2311.07121
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing, benchmarking_performance_modeling, architecture_control
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Closed-loop mid-circuit latency: readout, decode, decision and feed-forward must fit inside the round budget.

**Gate 2 — HPC/systems technique in the contribution.** A controller-level benchmark suite that exercises the real-time classical subsystem end to end rather than component by component.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Tells us whether a given classical control stack can sustain fault-tolerant execution, which component specifications do not reveal.

**Research question.** How can the classical controller's ability to execute error-corrected non-Clifford circuits — which need mid-circuit decoding and decode-dependent feed-forward — be benchmarked holistically?

**Quantum problem.** Non-Clifford gates under QEC require modifying the physical gate sequence within the same circuit based on decoding results of earlier measurements.

**Classical / HPC problem.** Closed-loop latency of the classical control system: measurement readout, decoding, decision and feed-forward must complete inside the coherence/round budget. The contribution is a benchmark for that classical subsystem.

**Mechanism.** Defines benchmark circuits and metrics that jointly exercise measurement, real-time decoding and conditional gate dispatch, so a controller can be scored end to end rather than component by component.

**Computational bottleneck.** Mid-circuit decode-to-feed-forward latency; controller throughput for conditional instruction streams.

**Evaluation platform.** Quantum control system executing QEC circuits (specific hardware not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Controller latency and success metrics on the proposed benchmarks; numeric values not recoverable from the truncated abstract.

**Major claim.** A controller-level benchmark suite exposes whether a classical control stack can sustain decode-dependent feed-forward, which component-level specifications do not reveal.

**Limitation.** Benchmarks are tied to particular QEC gadget structures; portability across control architectures needs checking.

**Relevance.** Directly measures the classical real-time processing capability that fault-tolerant execution depends on.

### TQE-131 — Quantum Circuit Optimization and MBQC Scheduling With a Pauli Tracking Library

- **DOI:** 10.1109/tqe.2025.3610112 · **Census year:** 2025 · **v6**, pp. 1-12
- **Lead author:** Jannis Ruh (+1 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing, qec_classical_processing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** PARTIAL (The paper states it provides an independent software library for Pauli tracking; the repository URL was not verified.)
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Classical bookkeeping cost plus the measurement-ordering (precedence) scheduling problem it induces.

**Gate 2 — HPC/systems technique in the contribution.** A Pauli-tracking framework with a software library and a numerical study of the resulting scheduling problem.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Characterizes runtime-layer work the classical stack must perform every shot in measurement-based and error-corrected execution.

**Research question.** How can Pauli tracking be used to schedule qubit measurements in measurement-based and error-corrected computation, and what does the resulting scheduling problem cost?

**Quantum problem.** In MBQC and Clifford-implemented error-corrected circuits, byproduct Pauli operators impose a partial order on measurements.

**Classical / HPC problem.** Classical bookkeeping and scheduling: tracking Pauli frames removes gates from the hardware stream and yields precedence constraints that a scheduler must satisfy; the paper investigates the scheduling problem numerically and ships a software library.

**Mechanism.** A framework for commuting Pauli operators through Clifford circuits (Pauli tracking), plus an independent software library implementing it for MBQC, with numerical study of the induced scheduling problem.

**Computational bottleneck.** Classical tracking bookkeeping cost and the measurement-ordering/scheduling search.

**Evaluation platform.** Numerical study using the accompanying software library.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in executed Pauli gates and schedule length/depth; numeric values not recoverable from the truncated abstract.

**Major claim.** Pauli tracking both removes Pauli gates from the hardware instruction stream and exposes the measurement-order constraints needed for MBQC scheduling, implemented in a reusable library.

**Limitation.** Restricted to Clifford-implementable settings; scheduling results are numerical rather than on hardware.

**Relevance.** Runtime/compiler-layer software for fault-tolerant execution; a scheduling problem the classical stack must solve every shot.

### TQE-132 — Exploration of Design Alternatives for Reducing Idle Time in Shor's Algorithm: A Study on Monolithic and Distributed Quantum Systems

- **DOI:** 10.1109/tqe.2025.3610800 · **Census year:** 2025 · **v6**, pp. 1-25 · **Online:** 2025-01-01
- **Lead author:** Moritz Schmidt (+5 co-authors) · **arXiv:** 2503.22564
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch:** multi_qpu_distributed_qc, benchmarking_performance_modeling
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Task serialization produces idle time that dominates overall execution time.

**Gate 2 — HPC/systems technique in the contribution.** Static timing analysis plus task reordering for concurrency, evaluated for monolithic and distributed system organizations.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Exposes the schedule structure of a flagship quantum workload and how it changes when the machine is distributed.

**Research question.** How much idle time does Shor's algorithm contain at the task level, and can reordering tasks (including across distributed nodes) reduce total execution time?

**Quantum problem.** Shor's algorithm implementations are dominated by long sequences of modular-arithmetic tasks with serialization-induced idle qubits.

**Classical / HPC problem.** Execution-flow scheduling and static timing analysis: identify idle time, reorder tasks for concurrency, and evaluate monolithic versus distributed system organizations — a classic parallel-execution scheduling analysis.

**Mechanism.** Adopts a mid-level task abstraction of the algorithm, applies static timing analysis to locate idle intervals, and proposes an alternating design that reorders tasks for simultaneous execution while preserving qubit efficiency; extends the analysis to distributed multi-node systems.

**Computational bottleneck.** Task serialization and resulting qubit idle time; inter-node communication in the distributed variant.

**Evaluation platform.** Static timing analysis across multiple platform models.

**Scale.** Monolithic and distributed configurations (node counts not recoverable from the truncated abstract).

**Performance metrics.** Reduction in idle time and overall execution time; the abstract states a substantial reduction but gives no quantified baseline (BASELINE_UNCLEAR).

**Major claim.** Task-level reordering reduces idle time and overall execution time of Shor's algorithm, with different trade-offs for monolithic versus distributed systems.

**Limitation.** Analysis is at the timing-model level, not measured on hardware; gains depend on the assumed task latencies.

**Relevance.** Schedule/idle-time analysis of a large quantum workload including a distributed configuration — performance modeling for future heterogeneous systems.

### TQE-137 — Network-Assisted Collective Operations for Efficient Distributed Quantum Computing

- **DOI:** 10.1109/tqe.2025.3619387 · **Census year:** 2025 · **v6**, pp. 1-14 · **Online:** 2025-01-01
- **Lead author:** Iago Fernández Llovo (+3 co-authors) · **arXiv:** 2502.19118
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch:** multi_qpu_distributed_qc
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Inter-QPU communication cost (Bell pairs and accompanying classical communication) for non-local gates.

**Gate 2 — HPC/systems technique in the contribution.** Collective-operation design borrowed from HPC interconnects: distributed fan-out to a central node instead of pairwise entanglement swapping.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Informs interconnect topology and collective-operation choices for multi-QPU execution, with an explicit optimality gap of one Bell pair.

**Research question.** Can collective quantum operations be distributed across remote QPUs using HPC-style network topologies instead of full connectivity or entanglement swapping?

**Quantum problem.** Distributed quantum computing needs non-local gates between QPUs, normally realized with pairwise entanglement and swapping.

**Classical / HPC problem.** Communication cost and collective-operation design: the paper borrows the fan-out/reduction pattern used by HPC interconnects and quantifies entanglement (i.e. communication) cost as a function of node count.

**Mechanism.** Distributes a general diagonal gate over any number of nodes via distributed fan-out operations to a central node, requiring only preshared entanglement, local operations and classical communication.

**Computational bottleneck.** Bell-pair (communication resource) consumption and the classical communication rounds that accompany it.

**Evaluation platform.** Analytical construction with protocol cost analysis.

**Scale.** Arbitrary node counts; distributed Grover analysed over multiple partitions.

**Performance metrics.** A general diagonal gate costs one additional Bell pair over the optimum achievable with all-to-all preshared entanglement; distributed Grover's Bell-pair cost grows linearly with the number of Grover iterations and the number of partitions. Baseline: entanglement-swapping-based distribution and the all-to-all-entanglement optimum.

**Major claim.** Central-node fan-out gives near-optimal communication cost for distributed collective quantum operations (one extra Bell pair for a general diagonal gate) without assuming full connectivity.

**Limitation.** Assumes a central node and preshared entanglement supply; does not model entanglement generation rate or failure.

**Relevance.** Directly transplants HPC collective-communication thinking into multi-QPU execution; informs interconnect topology choices.

### TQE-142 — Leveraging Quantum Machine Learning Generalization to Significantly Speed up Quantum Compilation

- **DOI:** 10.1109/tqe.2025.3622495 · **Census year:** 2025 · **v6**, pp. 1-12 · **Online:** 2025-01-01
- **Lead author:** Alon Kukliansky (+3 co-authors) · **arXiv:** 2405.12866
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing, benchmarking_performance_modeling
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** PARTIAL — https://github.com/BQSKit/bqskit (The method is integrated into the public BQSKit compiler; a paper-specific artifact release was not verified.)
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Compiler inner-loop cost: O(4^n) matrix-matrix operations dominate compile time.

**Gate 2 — HPC/systems technique in the contribution.** Replacing the numerical optimizer's linear algebra with O(2^n) sampled circuit simulations inside a production compiler (BQSKit).

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies compilation throughput against a named baseline (average 69x on >8-qubit circuits), the classical stage between an application and a QPU.

**Research question.** Can the numerical optimizer at the heart of a quantum compiler be made to scale better by replacing matrix-matrix algebra with sampled circuit simulation?

**Quantum problem.** Compilation by numerical instantiation of parameterized circuit templates.

**Classical / HPC problem.** Compile time and asymptotic cost of the compiler's inner loop: O(4^n) matrix-matrix operations dominate, and the paper replaces them with O(2^n) circuit simulations on sampled inputs.

**Mechanism.** QFactor-Sample evaluates the objective by simulating the circuit on a set of sample input states rather than forming full unitaries, with the number of samples tied to circuit simplicity; integrated into the BQSKit compiler.

**Computational bottleneck.** Cost of the numerical optimization inner loop; the sample-count versus accuracy trade-off; interaction with partitioning-based compilation.

**Evaluation platform.** BQSKit quantum compiler, compared against a state-of-the-art domain-specific optimizer.

**Scale.** Validated on a large circuit set; speedup reported for circuits with more than 8 qubits.

**Performance metrics.** Average speedup factor of 69 in compile time for circuits with more than 8 qubits, against a state-of-the-art domain-specific optimizer; improved scalability with qubit count.

**Major claim.** Replacing O(4^n) matrix-matrix operations with O(2^n) sampled circuit simulations gives an average 69x compile-time speedup on >8-qubit circuits relative to the prior domain-specific optimizer.

**Limitation.** Sampling introduces a hyperparameter (number of samples) requiring tuning; accuracy depends on circuit simplicity.

**Relevance.** Compilation cost and scalability — the classical compute that stands between an application and a QPU — with a measured speedup and a named baseline.

### TQE-143 — Optimized Quantum Circuit Partitioning Across Multiple Quantum Processors

- **DOI:** 10.1109/tqe.2025.3623158 · **Census year:** 2025 · **v6**, pp. 1-17 · **Online:** 2025-01-01
- **Lead author:** Eneet Kaur (+6 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q, FUTURE_WORKLOAD · **Branch:** multi_qpu_distributed_qc, circuit_cutting_reconstruction
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Evidence flag:** NO_ABSTRACT
- **Abstract status:** NO_ABSTRACT

**Gate 1 — classical systems problem.** Partitioning work across several processors with an inter-processor communication cost (title-level evidence only).

**Gate 2 — HPC/systems technique in the contribution.** Optimization of circuit partitioning across multiple QPUs, structurally the same as graph partitioning for distributed execution.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Bears directly on how a workload is split across several QPUs; details require full-text retrieval (NO_ABSTRACT).

**Research question.** How should a quantum circuit be partitioned across several quantum processors so that the inter-processor communication and reconstruction cost is minimized? (NO_ABSTRACT; question inferred from title only.)

**Quantum problem.** A circuit too large for one QPU must be split across several processors.

**Classical / HPC problem.** Partitioning/placement across compute nodes with an inter-node communication cost — the same optimization shape as classical graph partitioning for distributed execution.

**Mechanism.** NO_ABSTRACT: mechanism not recoverable. The abstract was not retrieved and the IEEE landing page could not be fetched.

**Computational bottleneck.** INSUFFICIENT_EVIDENCE

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** INSUFFICIENT_EVIDENCE

**Major claim.** INSUFFICIENT_EVIDENCE — only the title 'Optimized Quantum Circuit Partitioning Across Multiple Quantum Processors' is available.

**Limitation.** INSUFFICIENT_EVIDENCE

**Relevance.** Title places it squarely in multi-QPU execution and partitioning, an INCLUDE shape; it is retained on that basis and flagged for manual full-text retrieval.

### TQE-150 — Hardware-Aware and Resource-Efficient Circuit Packing and Scheduling on Trapped-Ion Quantum Computers

- **DOI:** 10.1109/tqe.2025.3632540 · **Census year:** 2025 · **v7**, pp. 1-15 · **Online:** 2025-11-14
- **Lead author:** Miguel Palma (+6 co-authors) · **arXiv:** 2512.20554
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** Q_IN_HPC · **Branch:** qpu_scheduling_resource_mgmt, compiler_mapping_routing
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Device utilization and job queueing under single-tenant execution; multi-tenancy is the stated problem.

**Gate 2 — HPC/systems technique in the contribution.** Static scheduling formulated as two-dimensional packing with hardware shuttling constraints, plus balanced scheduling across a module cluster.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Addresses QPU resource management and throughput in a shared service, the scheduling problem a quantum-equipped centre will face.

**Research question.** Can multiple user circuits be packed onto a modular trapped-ion device so that hardware utilization and cloud throughput improve without unacceptable fidelity loss?

**Quantum problem.** Single-tenant execution on quantum cloud services leaves most qubits idle while job queues grow.

**Classical / HPC problem.** Multi-tenancy, packing and scheduling: static circuit scheduling is formulated as a two-dimensional packing problem with hardware shuttling constraints, and balanced scheduling is extended across a cluster of modules.

**Mechanism.** CircPack, a hardware-aware packing framework for QCCD trapped-ion devices that solves 2-D packing with shuttling constraints and balances circuits across independent modules.

**Computational bottleneck.** Device utilization and queue waiting time; shuttling constraints limiting feasible packings; packing search cost.

**Evaluation platform.** Modular QCCD trapped-ion device models; comparison against superconducting-targeted quantum multiprogramming approaches.

**Scale.** Cluster of independent QCCD modules (module count not stated in the abstract).

**Performance metrics.** Up to 70.72% better fidelity, 62.67% higher utilization and 32.80% improved layer reduction, measured against superconducting-oriented quantum-multiprogramming baselines.

**Major claim.** Hardware-aware packing for trapped-ion QCCD devices improves utilization and fidelity over multiprogramming methods designed for superconducting hardware.

**Limitation.** Static (compile-time) scheduling only; results are simulation-based against baselines built for a different hardware class, so the comparison is partly cross-platform.

**Relevance.** QPU resource management and multi-tenancy — the scheduling problem a quantum-equipped HPC centre will face.

### TQE-167 — Improving Decision Diagram-Based Quantum Circuit Simulation Using Static Variable Ordering and Multinode Ring Communication

- **DOI:** 10.1109/tqe.2026.3654543 · **Census year:** 2026 · **v7**, pp. 1-15 · **Online:** 2026-01-01
- **Lead author:** Yusuke Kimura (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** distributed_gpu_simulation
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Memory footprint of the state representation and inter-node communication in distributed simulation.

**Gate 2 — HPC/systems technique in the contribution.** Static variable ordering combined with multinode parallel DD simulation over a ring communication topology.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows how classical quantum-circuit simulation scales across nodes and which communication structure it needs.

**Research question.** How should decision-diagram variable ordering be chosen, and how should DD simulation be parallelized across nodes, to speed up classical quantum circuit simulation?

**Quantum problem.** Classical simulation of quantum circuits is required because large machines are scarce and do not expose state vectors.

**Classical / HPC problem.** Memory-efficient representation plus multinode parallelization: DD processing time depends heavily on variable order, and distributing DD work across nodes requires a communication scheme.

**Mechanism.** A static variable-ordering method with general applicability, combined with multinode parallel DD simulation using ring communication between nodes.

**Computational bottleneck.** DD node count as a function of variable order; inter-node communication in the ring topology; memory per node.

**Evaluation platform.** Multinode classical cluster running a DD-based simulator (node count not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Simulation time/memory improvement from ordering and from multinode execution; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** A generally applicable static variable ordering plus ring-based multinode communication improves DD-based simulation time relative to prior ordering heuristics and single-node execution.

**Limitation.** Static ordering cannot adapt to circuit phases; ring communication may not be the best topology at larger node counts.

**Relevance.** Distributed classical simulation of quantum circuits — a direct HPC workload with a communication-topology design decision.

### TQE-193 — Cut&amp;shoot: Distributed Execution of Quantum Circuit Fragments

- **DOI:** 10.1109/tqe.2026.3675340 · **Census year:** 2026 · **EarlyAccess**, pp. 1-14 · **Online:** 2026-01-01
- **Lead author:** Giuseppe Bisicchia (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q, Q_IN_HPC · **Branch:** circuit_cutting_reconstruction, quantum_runtime_orchestration, hybrid_workflow
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Distributed execution of circuit fragments plus the classical reconstruction cost of recombining them.

**Gate 2 — HPC/systems technique in the contribution.** An orchestration pipeline composing circuit cutting with shot-wise distribution across backends.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Defines a workflow shape that Quantum-HPC middleware must support: fragment dispatch, shot distribution and result aggregation.

**Research question.** Can circuit cutting and shot-wise distribution be combined into one pipeline that distributes circuit fragments and their shots across quantum resources?

**Quantum problem.** NISQ devices limit qubit count and fidelity, so large circuits must be fragmented and their results recombined.

**Classical / HPC problem.** Distributed execution and orchestration: the pipeline must dispatch fragments and shot batches to multiple backends and reconstruct the result, which is a workflow/runtime problem with classical reconstruction cost.

**Mechanism.** Cut&Shoot, a pipeline that composes circuit cutting with shot-wise distribution, orchestrating fragment execution across resources and merging the outcomes.

**Computational bottleneck.** Classical reconstruction cost of cut circuits; distribution and aggregation of shots across backends.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Fidelity/scalability of the combined pipeline versus cutting or shot distribution alone; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Combining circuit cutting with shot-wise distribution in a single orchestrated pipeline improves scalability and reliability relative to applying either technique alone.

**Limitation.** Reconstruction overhead still grows with the number of cuts; evaluation scale not stated in the abstract.

**Relevance.** Quantum software-engineering meets runtime orchestration; the workflow shape a Quantum-HPC middleware would need to support.

### TQE-207 — Reducing Maximum Subcircuits Depth in Quantum Circuit Cutting

- **DOI:** 10.1109/tqe.2026.3690593 · **Census year:** 2026 · **v7**, pp. 3103209-3103209 · **Online:** 2026-01-01
- **Lead author:** Milad Eslaminia (+1 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** circuit_cutting_reconstruction, compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Post-mapping subcircuit depth and the search cost of choosing cut placements.

**Gate 2 — HPC/systems technique in the contribution.** A cutting framework coupled to the mapper's cost model so cut selection anticipates routing overhead.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows how a runtime should plan fragmented execution when the compiler stage, not just qubit count, determines feasibility.

**Research question.** How should cut locations be chosen when the depth of the resulting subcircuits after hardware mapping, not just their qubit count, determines execution quality?

**Quantum problem.** Circuit cutting lets small devices execute large circuits, but deep subcircuits lose fidelity exponentially with depth.

**Classical / HPC problem.** Cut selection as a joint cutting-and-mapping cost optimization: the classical cutter must anticipate the mapping/routing overhead that will inflate subcircuit depth.

**Mechanism.** A circuit-cutting framework that reduces the variance in post-mapping subcircuit depth by taking the target hardware's mapping consequences into account when placing cuts.

**Computational bottleneck.** Post-mapping subcircuit depth; search cost over cut placements.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in maximum subcircuit depth and resulting fidelity improvement; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Cut placement that accounts for post-mapping depth yields shallower worst-case subcircuits than qubit-count-only cutting methods.

**Limitation.** Adds coupling between the cutter and the mapper, increasing compile-time complexity; sampling overhead of cutting is unchanged.

**Relevance.** Compiler-stage cost model that couples partitioning with mapping — relevant to how a runtime should plan fragmented execution.

### TQE-214 — ZAP: Zoned Architecture and Performant Compiler for Field-Programmable Atom Array

- **DOI:** 10.1109/tqe.2026.3696707 · **Census year:** 2026 · **v7**, pp. 3103619-3103619 · **Online:** 2026-01-01
- **Lead author:** Chen Huang (+6 co-authors) · **arXiv:** 2411.14037
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing, architecture_control
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Compile-time cost of repeated global search over a dynamically reconfigurable architecture.

**Gate 2 — HPC/systems technique in the contribution.** Compiler-architecture codesign: zoned array plus a deterministic single-pass flow combining ASAP scheduling, look-ahead placement and conflict-aware routing.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Demonstrates the compile-time versus quality trade-off that heterogeneous back ends will force on the software stack.

**Research question.** Can a zoned neutral-atom architecture and a deterministic single-pass compiler be codesigned to control crosstalk and transport overhead without repeated global search?

**Quantum problem.** Field-programmable atom arrays are dynamically reconfigurable, so logical circuits must be mapped onto moving atoms subject to crosstalk and transport constraints.

**Classical / HPC problem.** Compile time versus solution quality: prior approaches rely on repeated global search; the contribution is a deterministic single-pass compilation flow with scheduling, placement and routing stages.

**Mechanism.** ZAP partitions the array into storage and entanglement zones and combines hardware-aware as-soon-as-possible separate scheduling, look-ahead placement and conflict-aware routing in one compilation pass.

**Computational bottleneck.** Compiler search cost (avoided by the single-pass design); atom transport time and crosstalk in the produced schedule.

**Evaluation platform.** Field-programmable atom array architecture model.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Compile time and circuit-quality metrics versus search-based neutral-atom compilers; the arXiv page could not be parsed, so exact figures are INSUFFICIENT_EVIDENCE (BASELINE_UNCLEAR).

**Major claim.** A zoned architecture plus a deterministic single-pass compiler avoids repeated global search while controlling crosstalk and transport overhead.

**Limitation.** Deterministic single-pass compilation trades optimality for speed; results are architecture-model based.

**Relevance.** Compiler-architecture codesign with explicit compile-cost motivation — one of the strongest compiler-systems papers in this venue.

### TQE-223 — DAG-Aware Gate Fusion for Efficient State-Vector Quantum-Circuit Simulation

- **DOI:** 10.1109/tqe.2026.3705783 · **Census year:** 2026 · **v7**, pp. 1-10 · **Online:** 2026-01-01
- **Lead author:** Shangshu Li (+2 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** HPC_FOR_Q · **Branch:** distributed_gpu_simulation
- **Deep-dive priority:** HIGH · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** State-vector memory traffic: every gate application traverses the full state array.

**Gate 2 — HPC/systems technique in the contribution.** Dependency-graph (DAG) aware gate fusion that reduces the number of full-array traversals.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** A kernel-level memory-bandwidth optimization for the most widely used classical quantum-simulation workload.

**Research question.** Can gate fusion for state-vector simulation be driven by circuit dependency structure rather than linear gate order or local heuristics?

**Quantum problem.** Exact state-vector simulation of quantum circuits for development and validation.

**Classical / HPC problem.** Memory-bandwidth-bound execution: every gate application traverses the full state vector, so fusing gates into larger operators reduces traversals; choosing which gates may legally fuse is a dependency-graph problem.

**Mechanism.** A directed-acyclic-graph-aware fusion method that builds fused operators directly from circuit dependencies, exposing fusion opportunities that linear-order heuristics miss.

**Computational bottleneck.** State-vector memory traffic (number of full-array traversals); fused-operator size versus reuse trade-off.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Simulation runtime improvement versus existing heuristic/linear-order fusion; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** DAG-aware fusion finds larger legal fused operators than linear-order heuristics and reduces state-vector traversal cost in exact simulation.

**Limitation.** Larger fused operators cost more to construct and apply densely; benefit is circuit-structure dependent.

**Relevance.** A memory-bandwidth optimization for the most common classical quantum-simulation kernel — core HPC_FOR_Q work.

### TQE-238 — Network-Based Quantum Computing: An Efficient Design Framework for Many-Small-Node Distributed Fault-Tolerant Quantum Computing

- **DOI:** 10.1109/tqe.2026.3722428 · **Census year:** 2026 · **v7**, pp. 3104632-3104632 · **Online:** 2026-01-01
- **Lead author:** Soshun Naito (+2 co-authors) · **arXiv:** 2601.09374
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** INCLUDED · **Scenario:** FUTURE_WORKLOAD, HPC_FOR_Q · **Branch:** multi_qpu_distributed_qc, architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Inter-node communication requirements and per-node logical-qubit capacity in a scale-out machine.

**Gate 2 — HPC/systems technique in the contribution.** A distributed-system design framework specifying how logical computation is decomposed across many small nodes.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Addresses the scale-out organization of quantum computers, the direct analogue of cluster design in HPC.

**Research question.** How should distributed fault-tolerant quantum computing be organized when each node holds only one or a few logical qubits?

**Quantum problem.** A logical qubit consumes many physical qubits, so a single node may hold very few logical qubits, forcing computation across many small nodes.

**Classical / HPC problem.** Distributed system design: partitioning logical computation across many small nodes, and the resulting inter-node communication and orchestration requirements.

**Mechanism.** Network-based quantum computing (NBQC), a design framework for realizing distributed fault-tolerant computation on many small nodes, specifying how logical operations are decomposed across the node network.

**Computational bottleneck.** Inter-node entanglement/communication requirements; per-node logical-qubit capacity.

**Evaluation platform.** Design-framework analysis.

**Scale.** Many small nodes each holding one or a few logical qubits.

**Performance metrics.** Resource and communication requirements of the proposed design; numeric values not recoverable from the truncated abstract.

**Major claim.** A design framework tailored to one-or-few-logical-qubit nodes makes many-small-node distributed fault-tolerant computing tractable, a regime prior distributed designs did not target.

**Limitation.** Framework-level; no implementation or runtime evaluation reported in the abstract.

**Relevance.** Architecture for scale-out quantum computing, the direct analogue of cluster design in HPC.

## 4. BORDERLINE records (37)

Recorded, not discarded. Each carries an explicit reason for and against inclusion alongside its gate justification;
a `WEAK:` marker on Gate 2 is the usual reason a record sits here rather than in section 3. These are the records a
reviewer should re-adjudicate before others if the corpus boundary moves.

### TQE-004 — Exploiting the Quantum Advantage for Satellite Image Processing: Review and Assessment

- **DOI:** 10.1109/tqe.2023.3338970 · **Census year:** 2024 · **v5**, pp. 1-9
- **Lead author:** Soronzonbold Otgonbaatar (+1 co-authors) · **arXiv:** 2308.09453
- **Article type:** REVIEW_SURVEY
- **Verdict:** BORDERLINE · **Scenario:** FUTURE_WORKLOAD, HPC_FOR_Q · **Branch:** benchmarking_performance_modeling, scientific_workflow_application
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Classical simulability, expressed via T-gate count, is used to decide HPC-versus-QPU placement.

**Gate 2 — HPC/systems technique in the contribution.** WEAK: resource counting through Clifford+T transpilation; no classical systems mechanism is built or measured.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Frames the HPC/QC division of work for one application domain, but at the level of resource estimates.

**Reason for inclusion:** Explicitly frames an HPC-versus-QPU partitioning decision and uses a classical-simulability criterion to make it.

**Reason against inclusion:** No classical systems mechanism is built or measured; the substance is an application review of QML for satellite imagery (false-positive class 5 territory).

**Research question.** What is the achievable division of work between HPC and quantum computing for Earth-observation and satellite image processing workloads?

**Quantum problem.** Applying parameterized quantum models to satellite imagery under NISQ constraints.

**Classical / HPC problem.** Uses T-gate counts after Clifford+T transpilation as a proxy for whether a model can be simulated on an HPC system, and frames the question as the optimal partition of work between HPC and QC.

**Mechanism.** Review plus assessment: transpiles candidate parameterized circuit models to Clifford+T and reads off resource requirements to decide HPC-simulability versus QPU deployment.

**Computational bottleneck.** Classical simulability threshold expressed through T-gate count.

**Evaluation platform.** Transpilation-based analysis; no measured HPC runs reported in the abstract.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** T-gate counts per model; numeric values not recoverable from the truncated abstract.

**Major claim.** T-gate counts of transpiled models can be used to decide whether a quantum model should run on an HPC simulator or a QPU.

**Limitation.** Assessment/review rather than a measured systems study; the HPC side is a simulability argument, not a measured workload.

**Relevance.** Explicitly addresses HPC/QC work division, which is the corpus's central question, but does so at the level of resource counting.

### TQE-006 — Quantum Vulnerability Analysis to Guide Robust Quantum Computing System Design

- **DOI:** 10.1109/tqe.2023.3343625 · **Census year:** 2024 · **v5**, pp. 1-11
- **Lead author:** Fang Qi (+6 co-authors) · **arXiv:** 2207.14446
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Prediction of program success rate as an input to system-design decisions.

**Gate 2 — HPC/systems technique in the contribution.** WEAK: reliability/performance modeling of device behaviour; no resource, scheduling or execution mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Supplies a predictive metric that could inform system design, without touching execution or resource usage.

**Reason for inclusion:** Performance modeling to guide system design is an explicit Gate-3 category; the paper targets system-level design decisions.

**Reason against inclusion:** The contribution is a noise-characterization metric; no computation cost, parallelism, scheduling or data-movement mechanism.

**Research question.** Can a systematic vulnerability analysis predict quantum program success rates better than the estimated success probability metric, and guide system design?

**Quantum problem.** Program outcomes deviate from noise-model predictions because circuit structure, state and device properties interact.

**Classical / HPC problem.** Performance/reliability modeling for a processor: building a predictive metric that guides architecture and system design choices.

**Mechanism.** Quantum vulnerability analysis: systematically perturbs program execution to attribute success-rate loss to specific structural and device factors, producing a predictive metric.

**Computational bottleneck.** Cost of the analysis campaign itself (simulation/characterization runs).

**Evaluation platform.** Quantum computers and/or simulators (not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Prediction accuracy versus the estimated success probability baseline; numeric values not recoverable from the truncated abstract.

**Major claim.** A structure-aware vulnerability metric predicts program success rate more accurately than ESP.

**Limitation.** Predictive modeling of device behaviour, not a systems mechanism; transferability across devices is unclear.

**Relevance.** Performance modeling for quantum systems design, adjacent to the benchmarking branch.

### TQE-020 — Testing and Debugging Quantum Circuits

- **DOI:** 10.1109/tqe.2024.3374879 · **Census year:** 2024 · **v5**, pp. 1-15 · **Online:** 2024-01-01
- **Lead author:** Sara Ayman Metwalli (+1 co-authors) · **arXiv:** 2311.18202
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** WEAK: no Gate-1 quantity is treated substantively (no cost, memory, latency or scaling).

**Gate 2 — HPC/systems technique in the contribution.** Software-stack tooling: a debugging process framework specialized by circuit-block class.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Marginal: developer tooling in the quantum software stack with no systems-resource consequence.

**Reason for inclusion:** Software-stack contribution; testing/debugging tooling is part of the classical side of the stack.

**Reason against inclusion:** No Gate-1 quantity is treated substantively (no cost, memory, latency, scaling).

**Research question.** What debugging procedures suit the different functional classes of quantum circuit blocks?

**Quantum problem.** Faults in quantum programs are hard to localize because state is not directly observable.

**Classical / HPC problem.** Software-stack tooling: a process framework for debugging, i.e. developer-facing infrastructure rather than a resource-cost mechanism.

**Mechanism.** Classifies circuit blocks as amplitude-permutation, phase-modulation or amplitude-redistribution and defines a debugging procedure per class.

**Computational bottleneck.** INSUFFICIENT_EVIDENCE

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** INSUFFICIENT_EVIDENCE

**Major claim.** Debugging strategies should be specialized to the functional class of the circuit block being tested.

**Limitation.** No cost, scalability or runtime analysis of the debugging procedures.

**Relevance.** Belongs to the quantum software stack, a listed sub-area, but without systems-resource content.

### TQE-030 — Variational Quantum Algorithms for the Allocation of Resources in a Cloud/Edge Architecture

- **DOI:** 10.1109/tqe.2024.3398410 · **Census year:** 2024 · **v5**, pp. 1-18 · **Online:** 2024-01-01
- **Lead author:** Carlo Mastroianni (+3 co-authors) · **arXiv:** 2401.14339
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** Q_FOR_HPC · **Branch:** qpu_scheduling_resource_mgmt
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Resource allocation and scheduling across sensors, edge/fog nodes, datacenters and quantum devices is the target problem.

**Gate 2 — HPC/systems technique in the contribution.** WEAK: QAOA versus VQE comparison on a QUBO encoding; no systems mechanism is contributed.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Evidence on whether quantum solvers could one day serve HPC resource management (Q_FOR_HPC).

**Reason for inclusion:** The workload is literally scheduling/resource allocation in a heterogeneous computing architecture, a Gate-1 and Gate-3 topic.

**Reason against inclusion:** The contribution is an optimizer comparison on a QUBO encoding (false-positive class E8); no systems mechanism is contributed.

**Research question.** Can variational quantum algorithms produce good assignments of computation to nodes in a heterogeneous cloud/edge architecture?

**Quantum problem.** Encoding an NP-hard assignment/scheduling problem for QAOA and VQE and comparing their success probabilities.

**Classical / HPC problem.** The target problem is genuine resource allocation and scheduling across sensors, edge/fog nodes, datacenters and quantum devices.

**Mechanism.** Formulates cloud/edge assignment as a QUBO and compares QAOA against a variational quantum eigensolver on success probability.

**Computational bottleneck.** Problem-size scaling of the QUBO encoding onto available qubits.

**Evaluation platform.** Simulation of QAOA/VQE (device details not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Success probability of the two algorithms; numeric values not recoverable from the truncated abstract.

**Major claim.** QAOA and VQE can express and solve small instances of the cloud/edge assignment problem, with a stated success-probability comparison.

**Limitation.** Instances are small; no comparison against production classical schedulers is reported in the abstract.

**Relevance.** Q_FOR_HPC on a scheduling workload; informative about whether quantum solvers could serve HPC resource management.

### TQE-032 — Trellis Decoding for Qudit Stabilizer Codes and Its Application to Qubit Topological Codes

- **DOI:** 10.1109/tqe.2024.3401857 · **Census year:** 2024 · **v5**, pp. 1-30 · **Online:** 2024-01-01
- **Lead author:** Eric Sabo (+2 co-authors) · **arXiv:** 2106.08251
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Decoding-graph size (memory) and an explicit one-time offline versus online cost split.

**Gate 2 — HPC/systems technique in the contribution.** Decoder algorithm with a precompute/runtime structure; no parallel or hardware implementation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Characterizes the memory-versus-latency structure of a general stabilizer decoder.

**Reason for inclusion:** Explicit precompute-versus-online cost split and graph-size (memory) analysis; decoder work is central to QEC classical processing.

**Reason against inclusion:** Per the QEC rule a decoder algorithm alone is BORDERLINE: no parallel implementation, no accelerator, no scheduling.

**Research question.** Can trellis decoding for stabilizer codes be made scalable and practical, including for qudit systems?

**Quantum problem.** Decoding arbitrary stabilizer codes, including topological qubit codes, in prime dimension.

**Classical / HPC problem.** Decoder scalability and memory: the method splits into a one-time offline computation that builds a compact decoding graph and an online decoding phase, an explicit precompute/runtime trade-off.

**Mechanism.** A canonical form for the trellis decoding graph from which structural properties (and hence size) can be computed, with an offline graph-construction phase and an online decode phase.

**Computational bottleneck.** Size of the trellis/decoding graph (memory) and the offline construction cost.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Decoding graph sizes and decoder performance; numeric values not recoverable from the truncated abstract.

**Major claim.** A canonical trellis form improves the scalability and practicality of trellis decoding and extends it to any prime-dimensional system.

**Limitation.** Trellis size still grows quickly with code size; no hardware implementation or latency measurement.

**Relevance.** Decoder algorithm with an explicit offline/online memory-versus-time structure.

### TQE-041 — Optimizing the Electrical Interface for Large-Scale Color-Center Quantum Processors

- **DOI:** 10.1109/tqe.2024.3416836 · **Census year:** 2024 · **v5**, pp. 1-17 · **Online:** 2024-01-01
- **Lead author:** Luc Enthoven (+2 co-authors) · **arXiv:** 2403.09526
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Per-qubit controller area and power, and electrical-interface bandwidth, as scalability limits.

**Gate 2 — HPC/systems technique in the contribution.** Unit-cell controller architecture; requirements analysis rather than a built or measured system.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Bounds how far the classical control interface can scale for one qubit technology.

**Reason for inclusion:** Scalability of the classical control interface is explicitly the subject; a unit-cell architecture is a systems-architecture contribution.

**Reason against inclusion:** Largely electronic circuit design for a specific qubit platform, adjacent to false-positive class 6 (control/readout electronics).

**Research question.** What electrical-interface architecture can control and read out a large-scale color-center quantum processor without limiting its scalability?

**Quantum problem.** Color-center qubits need optical and electrical control whose interface may bound system performance.

**Classical / HPC problem.** Controller architecture partitioned into repeated identical unit cells — a scalability/resource argument for the classical control plane.

**Mechanism.** Analyses the electrical-interface requirements and maps functions onto a scalable unit-cell electronic controller architecture.

**Computational bottleneck.** Per-qubit controller area/power; wiring and interface bandwidth.

**Evaluation platform.** Architecture analysis of the electronic controller.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Per-unit-cell resource and performance requirements; numeric values not recoverable from the truncated abstract.

**Major claim.** A unit-cell controller architecture meets the electrical-interface requirements of large color-center processors.

**Limitation.** Requirements analysis rather than a fabricated or measured system.

**Relevance.** Classical control-hardware architecture, a listed TQE sub-area, but close to the excluded cryo-electronics class.

### TQE-045 — Convolutional Neural Decoder for Surface Codes

- **DOI:** 10.1109/tqe.2024.3419773 · **Census year:** 2024 · **v5**, pp. 1-13 · **Online:** 2024-01-01
- **Lead author:** Hyunwoo Jung (+2 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Decoder accuracy and inference latency.

**Gate 2 — HPC/systems technique in the contribution.** ML decoder algorithm only; no FPGA/ASIC or parallel implementation to make the latency claim concrete.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** A candidate for accelerator deployment; would inform real-time decoding once implemented in hardware.

**Reason for inclusion:** Latency is stated as a target, and ML decoders are the main route to accelerator implementations.

**Reason against inclusion:** New decoder algorithm only, with no parallel or hardware implementation — BORDERLINE by the explicit QEC rule.

**Research question.** Can a convolutional neural network decode surface codes with better performance and lower latency than conventional decoders?

**Quantum problem.** Detecting and correcting errors in topological codes from syndrome data.

**Classical / HPC problem.** Decoder inference latency and accuracy — the classical processing that must keep up with syndrome generation.

**Mechanism.** A CNN decoder exploiting the locality of topological codes to map syndromes to corrections.

**Computational bottleneck.** Inference latency and model size; training data generation.

**Evaluation platform.** Software/ML evaluation (hardware deployment not indicated in the abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Decoding accuracy and latency versus conventional decoders; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** A CNN decoder improves surface-code decoding performance and latency relative to conventional algorithmic decoders.

**Limitation.** No hardware (FPGA/ASIC) implementation reported, so the latency claim is at the algorithm level; ML decoders need retraining per noise model and code distance.

**Relevance.** Decoder work with a stated latency motivation; would become INCLUDE with an accelerator implementation.

### TQE-049 — Learning a Quantum Computer's Capability

- **DOI:** 10.1109/tqe.2024.3430215 · **Census year:** 2024 · **v5**, pp. 1-26 · **Online:** 2024-01-01
- **Lead author:** Daniel Hothem (+3 co-authors) · **arXiv:** 2304.10650
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Classical simulation of the circuits is infeasible, so capability prediction must be built another way.

**Gate 2 — HPC/systems technique in the contribution.** ML performance modeling from an efficient circuit representation; no resource or execution mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Performance modeling that could inform which machines to build and use.

**Reason for inclusion:** Scalability against classical simulation cost is the stated driver, and the output informs procurement/usage decisions.

**Reason against inclusion:** The subject is device error behaviour; no resource, scheduling or execution mechanism is contributed.

**Research question.** Can a scalable model predict which circuits a quantum computer can run successfully, without classically simulating them?

**Quantum problem.** Predicting device capability across broad circuit classes.

**Classical / HPC problem.** Classical simulation of the circuits is infeasible, so the predictive model must be built from an efficient circuit representation and trained/evaluated at scale.

**Mechanism.** Encodes circuits in an efficient representation and trains convolutional neural networks to predict success, hardware-agnostically.

**Computational bottleneck.** Infeasibility of simulation-based prediction; training/inference cost of the capability model.

**Evaluation platform.** CNN models trained on circuit/device data.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Prediction accuracy of capability models; numeric values not recoverable from the truncated abstract.

**Major claim.** Capability models can be built from efficient circuit representations and scale past the point where classical simulation of the circuits is affordable.

**Limitation.** Predictive fidelity outside the training distribution is unverified; it models device behaviour, not system resources.

**Relevance.** Performance modeling explicitly motivated by classical simulation cost; input to decisions about which machines to build and use.

### TQE-068 — Hybrid Hamiltonian Simulation Approach for the Analysis of Quantum Error Correction Protocol Robustness

- **DOI:** 10.1109/tqe.2024.3486546 · **Census year:** 2024 · **v5**, pp. 1-11 · **Online:** 2024-01-01
- **Lead author:** Benjamin Gys (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling, architecture_control
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Simulation cost of analysing QEC protocol behaviour jointly with control-circuit behaviour.

**Gate 2 — HPC/systems technique in the contribution.** Hybrid simulation method; the cost saving is asserted rather than quantified.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Tooling for codesign of QEC protocols with classical CMOS control.

**Reason for inclusion:** Simulation-cost motivation plus explicit coupling to classical CMOS control design.

**Reason against inclusion:** Primarily a device/protocol robustness study; the systems content is a tooling remark rather than a measured result.

**Research question.** Can a hybrid Hamiltonian-based simulation approach make QEC-protocol robustness analysis tractable for small-scale architectures with CMOS control?

**Quantum problem.** Assessing how QEC protocols behave under realistic device and control imperfections.

**Classical / HPC problem.** Simulation tool efficiency: a hybrid simulation method is proposed because full simulation of protocol plus control is too costly as qubit numbers rise.

**Mechanism.** A hybrid Hamiltonian simulation approach that combines levels of description to evaluate QEC protocol robustness alongside CMOS control-circuit design.

**Computational bottleneck.** Cost of simulating protocol dynamics together with control-circuit behaviour.

**Evaluation platform.** Simulation study.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Simulation cost/accuracy trade-off; numeric values not recoverable from the truncated abstract.

**Major claim.** A hybrid simulation approach makes joint QEC-protocol and control-circuit robustness analysis affordable for small architectures.

**Limitation.** Small-scale architectures only; the classical cost saving is not quantified in the abstract.

**Relevance.** Simulation tooling for codesign of QEC with classical control.

### TQE-077 — RSFQ All-Digital Programmable Multitone Generator for Quantum Applications

- **DOI:** 10.1109/tqe.2024.3520805 · **Census year:** 2025 · **v6**, pp. 1-11 · **Online:** 2025-01-01
- **Lead author:** João Barbosa (+6 co-authors) · **arXiv:** 2411.08670
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Wiring count, interface overhead and power at cryogenic stages.

**Gate 2 — HPC/systems technique in the contribution.** Superconducting (RSFQ) circuit design; a device-level rather than computing-systems technique.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Speaks to control-plane integration overhead at the quantum-classical boundary.

**Reason for inclusion:** Explicit system-overhead and scalability framing for the classical control plane.

**Reason against inclusion:** Superconducting circuit design; closer to false-positive class 6 than to a computing-systems contribution.

**Research question.** Can RSFQ logic generate programmable multitone control signals on-chip so that control overhead scales better than room-temperature CMOS architectures?

**Quantum problem.** Control and readout signal generation for many qubits and sensor arrays.

**Classical / HPC problem.** System overhead and integration: moving signal generation on-chip reduces wiring and interface cost, a scalability argument for the control plane.

**Mechanism.** An RSFQ device generating multitone digital signals from complex pulse-train sequences using a circular shift register.

**Computational bottleneck.** Wiring/interface count and power at cryogenic stages.

**Evaluation platform.** RSFQ circuit design and characterization.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Tone count, frequency range and power; numeric values not recoverable from the truncated abstract.

**Major claim.** On-chip RSFQ multitone generation reduces total system overhead compared with room-temperature CMOS control architectures.

**Limitation.** Component-level demonstration; system-level scaling is argued rather than measured.

**Relevance.** Classical control hardware at the cryogenic interface, the same design space as the included C3-VQA paper but at circuit level.

### TQE-087 — Generating Shuttling Procedures for Constrained Silicon Quantum Dot Array

- **DOI:** 10.1109/tqe.2025.3542462 · **Census year:** 2025 · **v6**, pp. 1-38 · **Online:** 2025-01-01
- **Lead author:** Naoto Sato (+3 co-authors) · **arXiv:** 2401.14683
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** State-space size and search cost of generating valid operation procedures under shared-gate constraints.

**Gate 2 — HPC/systems technique in the contribution.** Formal-model-based routing/procedure automation; the classical search cost is not quantified.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows what compilation looks like under severe architectural constraints.

**Reason for inclusion:** Compilation/routing automation with a classical search-cost dimension, the same family as the included BeSnake paper.

**Reason against inclusion:** The systems content (search cost, scalability) is not quantified in the abstract; may be purely a formal-methods result.

**Research question.** How can valid shuttling procedures be generated automatically for a silicon quantum-dot array whose shared control gates heavily constrain qubit movement?

**Quantum problem.** Sharing control gates across rows/columns of a 2-D dot array couples the movements of many qubits.

**Classical / HPC problem.** Automated generation of operation sequences under architectural constraints — the routing/scheduling stage of compilation, with the classical search cost as the practical limit.

**Mechanism.** A formal model based on state-transition systems describing the array constraints, with an approach to derive shuttling procedures within that model.

**Computational bottleneck.** State-space size of the transition system; procedure-generation search cost.

**Evaluation platform.** Formal model and procedure generation (tooling details not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Generated procedure length / generation time; numeric values not recoverable from the truncated abstract.

**Major claim.** Shuttling procedures for a shared-gate silicon dot array can be generated automatically from a formal constraint model.

**Limitation.** State-transition models scale poorly with array size; no comparison against hand-designed procedures is reported in the abstract.

**Relevance.** Architecture-aware routing automation for a constrained qubit technology.

### TQE-095 — Emulation of Density Matrix Dynamics With Classical Analog Circuits

- **DOI:** 10.1109/tqe.2025.3552736 · **Census year:** 2025 · **v6**, pp. 1-16 · **Online:** 2025-01-01
- **Lead author:** Anthony J. Cressman (+1 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** distributed_gpu_simulation, architecture_control
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Cost of digital density-matrix simulation, which grows quadratically in Hilbert-space dimension.

**Gate 2 — HPC/systems technique in the contribution.** Analog-circuit accelerator substrate; no throughput, scaling or energy comparison against digital simulation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** An unconventional accelerator for a workload that otherwise consumes HPC cycles.

**Reason for inclusion:** Accelerator design for the quantum-simulation workload; Gate-1 'accelerator design' is present.

**Reason against inclusion:** No scaling, throughput or energy comparison against digital simulation is given, so the systems case is unproven.

**Research question.** Can classical analog CMOS circuits emulate open-quantum-system density-matrix dynamics, not just coherent state-vector dynamics?

**Quantum problem.** Modelling noisy (open) quantum systems, which requires density matrices rather than state vectors.

**Classical / HPC problem.** An alternative classical hardware substrate for quantum emulation: analog VLSI trades exactness for area/energy, an accelerator-design argument against digital simulation.

**Mechanism.** Extends analog-circuit quantum emulation from state-vector to density-matrix dynamics, mapping Lindblad-type evolution onto analog circuit elements.

**Computational bottleneck.** Cost of digital density-matrix simulation (quadratic in Hilbert-space dimension), which the analog substrate aims to avoid.

**Evaluation platform.** Analog VLSI circuit emulation (room temperature).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Emulation fidelity versus digital reference; numeric values not recoverable from the truncated abstract.

**Major claim.** Analog circuits can emulate density-matrix dynamics of noisy quantum systems, extending prior state-vector emulation results.

**Limitation.** Analog emulation has limited precision and unclear scaling to many qubits; no comparison against GPU simulators is reported.

**Relevance.** An unconventional accelerator for a workload that otherwise consumes HPC cycles.

### TQE-100 — Runtime–Coherence Tradeoffs for Hybrid Satisfiability Solvers

- **DOI:** 10.1109/tqe.2025.3563805 · **Census year:** 2025 · **v6**, pp. 1-22 · **Online:** 2025-01-01
- **Lead author:** Vahideh Eshaghian (+3 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** FUTURE_WORKLOAD, HPC_FOR_Q · **Branch:** hybrid_workflow
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Parallelizability and total runtime under a bounded per-segment coherence budget.

**Gate 2 — HPC/systems technique in the contribution.** Algorithmic decomposition into parallelizable subproblems; no runtime, scheduler or implementation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Indicates how quantum work can be chunked to fit the execution windows a scheduler could offer.

**Reason for inclusion:** Parallelism and runtime are treated substantively and tied to a hardware constraint.

**Reason against inclusion:** The result is an algorithm-complexity analysis; no runtime, scheduler or systems artifact.

**Research question.** How should a k-SAT search be divided into subproblems each solvable within a limited quantum coherence time, and what is the runtime-coherence trade-off?

**Quantum problem.** Search-based quantum speedups require coherence times that near-term devices do not have.

**Classical / HPC problem.** Parallel decomposition of a search workload: the paper asks how to split the task into parallelizable subproblems and quantifies the resulting runtime versus coherence-time trade-off.

**Mechanism.** Builds on Schoening's random-walk algorithm for k-SAT, partitioning the walk's search space into segments each executable within a bounded coherence window, with classical restarts between segments.

**Computational bottleneck.** Coherence time per subproblem versus total runtime; degree of achievable parallelism.

**Evaluation platform.** Analytical/numerical analysis.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Runtime scaling as a function of available coherence time; numeric values not recoverable from the truncated abstract.

**Major claim.** k-SAT search admits a decomposition whose runtime degrades gracefully as the per-segment coherence budget shrinks, restoring classical-style parallelizability.

**Limitation.** Theoretical analysis; no execution or scheduling implementation.

**Relevance.** Directly about parallelizability and runtime of hybrid execution, which is how quantum work will have to fit into a job scheduler.

### TQE-106 — Q-Gen: A Parameterized Quantum Circuit Generator

- **DOI:** 10.1109/tqe.2025.3572142 · **Census year:** 2025 · **v6**, pp. 1-16 · **Online:** 2025-01-01
- **Lead author:** Yikai Mao (+2 co-authors) · **arXiv:** 2407.18697
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN (A generator tool is described; repository was not verified.)
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** WEAK: no resource quantity is analysed in the paper itself.

**Gate 2 — HPC/systems technique in the contribution.** Dataset and benchmark-generation infrastructure for the classical stages of the workflow.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Supplies input infrastructure for compiler, simulator and performance studies.

**Reason for inclusion:** Benchmarking infrastructure is an explicitly relevant TQE sub-area, and the motivation is classical workflow automation.

**Reason against inclusion:** No Gate-1 resource quantity is analysed; the tool itself carries no performance claim.

**Research question.** Can a parameterized generator produce large, diverse, labelled circuit datasets for the classical stages of the quantum workflow?

**Quantum problem.** Circuits are the output of quantum algorithms and the input to every classical tool downstream.

**Classical / HPC problem.** Benchmark and dataset infrastructure for compilers, simulators and ML-on-circuits; the argument is that most of the workflow is classical and needs automation.

**Mechanism.** Q-gen, a high-level parameterized circuit generator covering 15 quantum algorithms, with customizable generation functions producing scalable circuit families.

**Computational bottleneck.** INSUFFICIENT_EVIDENCE

**Evaluation platform.** Software generator; dataset statistics reported.

**Scale.** 15 algorithm families, parameterized in qubit count.

**Performance metrics.** Dataset size/diversity statistics; numeric values not recoverable from the truncated abstract.

**Major claim.** A parameterized generator can supply scalable labelled circuit datasets for classical automation and optimization of the quantum workflow.

**Limitation.** A dataset/tool contribution; no performance result about any consuming system.

**Relevance.** Infrastructure for benchmarking compilers and simulators.

### TQE-107 — Reducing Quantum Error Correction Overhead With Versatile Flag-Sharing Syndrome Extraction Circuits

- **DOI:** 10.1109/tqe.2025.3572764 · **Census year:** 2025 · **v6**, pp. 1-24 · **Online:** 2025-01-01
- **Lead author:** Pei-Hao Liou (+1 co-authors) · **arXiv:** 2407.00607
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Lookup-table decoder memory and circuit area (depth times physical qubits).

**Gate 2 — HPC/systems technique in the contribution.** Parallelization is inside the quantum circuit; the classical decoder table is a secondary part of the contribution.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies decoder table cost for a syndrome-extraction scheme.

**Reason for inclusion:** The decoder (lookup-table) design and its memory cost are part of the contribution.

**Reason against inclusion:** Predominantly syndrome-extraction circuit design — false-positive class E10 (QEC circuit/protocol design).

**Research question.** Can flag qubits be shared across parallel syndrome-extraction circuits to reduce total circuit area while keeping decoding simple?

**Quantum problem.** Fault-tolerant syndrome extraction needs ancillas, flags, gates and measurements, all of which cost circuit area and introduce errors.

**Classical / HPC problem.** Classical decoding side: measurement outcomes across multiple extraction rounds are integrated into a lookup-table decoder, i.e. a memory-versus-latency decoder design choice.

**Mechanism.** Parallel flagged syndrome extraction with shared flag qubits, plus a lookup-table decoder built from multi-round measurement outcomes.

**Computational bottleneck.** Lookup-table size (memory) against decode latency; circuit area as depth times physical qubit count.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Circuit area, threshold and decoder table size; numeric values not recoverable from the truncated abstract.

**Major claim.** Sharing flag qubits across parallelized syndrome extraction reduces circuit area and improves the error threshold.

**Limitation.** Lookup-table decoding does not scale to large distances; the parallelism is in the quantum circuit, not classical processing.

**Relevance.** Touches the classical decoder through the lookup-table design, but the main contribution is a quantum circuit construction.

### TQE-108 — Memory-Optimized Cubic Splines for High-Fidelity Quantum Operations

- **DOI:** 10.1109/tqe.2025.3574463 · **Census year:** 2025 · **v6**, pp. 1-12 · **Online:** 2025-01-01
- **Lead author:** Jan Ole Ernst (+3 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Controller memory footprint per pulse against the required sampling rate, as control logic moves closer to the qubits.

**Gate 2 — HPC/systems technique in the contribution.** WEAK: a numerical interpolation (spline compression) scheme; no architecture, parallelism, latency or throughput result is established.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Concerns the memory budget of the real-time control layer, but without a systems-level evaluation.

**Reason for inclusion:** Controller memory is a genuine Gate-1 resource and the paper targets it explicitly, in the context of control logic moving closer to the qubits to cut feedback latency.

**Reason against inclusion:** Gate 2 is not met: the contribution is a numerical interpolation scheme for pulse parameters, with no architecture, parallelism, latency or throughput result to establish it as a systems technique. Demoted from INCLUDED during adversarial verification.

**Notes.** Demoted INCLUDED -> BORDERLINE during adversarial verification: Gate 1 (controller memory budget) holds, but Gate 2 is carried by a numerical compression technique with no systems-level evaluation.

**Research question.** How can time-resolved control pulses be represented so that high-fidelity operations fit in the limited memory of control electronics close to the qubits?

**Quantum problem.** Gate fidelity depends on finely resolved amplitude/phase/frequency trajectories.

**Classical / HPC problem.** Memory capacity and bandwidth of the control processor: as control logic moves closer to the qubits for latency reasons, pulse parameter storage becomes the binding resource.

**Mechanism.** Memory-optimized cubic spline interpolation of pulse parameters, so the controller stores few coefficients and reconstructs high-sample-rate waveforms on the fly.

**Computational bottleneck.** Controller memory footprint per pulse versus sampling rate; on-the-fly interpolation cost.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Memory reduction at fixed gate fidelity; exact figures not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Spline-compressed pulse representations preserve gate fidelity while substantially reducing control-electronics memory compared with storing sampled waveforms.

**Limitation.** Benefit depends on pulse smoothness; interpolation hardware cost is traded against memory saving.

**Relevance.** A concrete resource (memory) versus latency trade-off in the classical real-time layer of the stack.

### TQE-109 — Improved Belief Propagation Decoding Algorithms for Surface Codes

- **DOI:** 10.1109/tqe.2025.3577769 · **Census year:** 2025 · **v6**, pp. 1-16 · **Online:** 2025-01-01
- **Lead author:** Jiahan Chen (+3 co-authors) · **arXiv:** 2407.11523
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Decoder time complexity and iteration count to convergence.

**Gate 2 — HPC/systems technique in the contribution.** Decoder algorithm only (momentum and adaptive-gradient message updates); no parallel or hardware implementation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Accuracy at fixed computational cost is what determines whether real-time decoding is feasible.

**Reason for inclusion:** Explicit time-complexity framing and a decoder that is a candidate for parallel hardware.

**Reason against inclusion:** New decoder algorithm only — BORDERLINE by the explicit QEC rule.

**Research question.** Can optimization techniques borrowed from machine learning improve belief-propagation decoding accuracy for surface codes without postprocessing?

**Quantum problem.** BP decoding of degenerate quantum codes converges poorly without postprocessing.

**Classical / HPC problem.** Decoder time complexity: BP is attractive because it is nearly linear-time, and the paper aims to keep that while improving accuracy, i.e. accuracy at fixed computational cost.

**Mechanism.** Momentum-BP and AdaGrad-BP, which damp oscillations in message passing using momentum and adaptive step sizes over GF(4).

**Computational bottleneck.** Iteration count to convergence; per-iteration cost of message passing.

**Evaluation platform.** Numerical decoding simulations.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Logical error rate and iteration counts versus standard BP; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Momentum and adaptive-gradient message updates improve BP decoding accuracy for surface codes while retaining near-linear time complexity.

**Limitation.** No parallel or hardware implementation; latency is inferred from complexity, not measured.

**Relevance.** Decoder throughput/accuracy at fixed complexity is the quantity that determines whether real-time decoding is possible.

### TQE-119 — Fault-Tolerant Noise Guessing Decoding of Quantum Random Codes

- **DOI:** 10.1109/tqe.2025.3595778 · **Census year:** 2025 · **v6**, pp. 1-26 · **Online:** 2025-01-01
- **Lead author:** Diogo Cruz (+3 co-authors) · **arXiv:** 2407.01658
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Computational overhead of decoding, stated as the open issue the paper addresses.

**Gate 2 — HPC/systems technique in the contribution.** Decoder algorithm only; no parallelism, accelerator or scheduling contribution.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies decoding overhead when syndrome extraction is itself faulty.

**Reason for inclusion:** Computational overhead of decoding is explicitly the framing of the paper.

**Reason against inclusion:** Decoder algorithm only; no parallelism, accelerator or scheduling contribution.

**Research question.** Can noise-guessing decoding of quantum random linear codes be made fault tolerant at feasible computational overhead?

**Quantum problem.** Decoding quantum random linear codes when syndrome extraction itself is faulty.

**Classical / HPC problem.** Computational overhead of the decoder is stated as the open issue; guessing-based decoding trades decode attempts against accuracy.

**Mechanism.** A noise-guessing decoder extended to handle preparation, measurement and gate errors during syndrome extraction, accounting for error degeneracy.

**Computational bottleneck.** Number of guesses/decoding attempts; overhead growth with code length.

**Evaluation platform.** Numerical simulation.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Threshold error rate and decoding overhead; the threshold value is stated in the paper but was cut from the truncated abstract.

**Major claim.** Noise-guessing decoding remains viable under faulty syndrome extraction, with a stated threshold error rate.

**Limitation.** Guessing-based decoding cost grows steeply; no implementation on parallel hardware.

**Relevance.** Decoder computational overhead is the stated constraint, which is the systems-relevant quantity.

### TQE-140 — Toward Practical Application of the Quantum Carleman Lattice Boltzmann Method in Industrial CFD Simulations

- **DOI:** 10.1109/tqe.2025.3620130 · **Census year:** 2025 · **v6**, pp. 1-18 · **Online:** 2025-01-01
- **Lead author:** Francesco Turro (+2 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** Q_FOR_HPC, FUTURE_WORKLOAD · **Branch:** scientific_workflow_application
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** CFD is an HPC workload whose computational cost motivates the whole exercise.

**Gate 2 — HPC/systems technique in the contribution.** WEAK: quantum-algorithm feasibility assessment; no classical systems mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** A workload projection for Q_FOR_HPC on a flagship HPC application.

**Reason for inclusion:** Targets a core HPC application and reports resource requirements, informing future-workload projections.

**Reason against inclusion:** No classical systems mechanism; it is a quantum-algorithm feasibility assessment for a domain problem.

**Research question.** Is the Carleman-linearized quantum lattice Boltzmann method practical for industrial CFD benchmarks?

**Quantum problem.** Nonlinear LBM equations are linearized via Carleman expansion and solved with HHL, requiring deep circuits and good condition numbers.

**Classical / HPC problem.** CFD is a canonical HPC workload whose cost motivates the whole exercise; the paper assesses whether the quantum route could relieve it.

**Mechanism.** Hybrid quantum-classical LBM: Carleman linearization followed by HHL, evaluated numerically on three benchmark flows.

**Computational bottleneck.** Circuit depth and condition number of the linear systems; classical resources for the surrounding simulation.

**Evaluation platform.** Numerical assessment on three CFD benchmarks (simulated).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Accuracy versus classical LBM and resource requirements; numeric values not recoverable from the truncated abstract.

**Major claim.** A practical numerical assessment of quantum Carleman LBM on industrial benchmarks, reporting where the approach is and is not viable.

**Limitation.** Simulated rather than executed on hardware; HHL resource requirements remain far from practical.

**Relevance.** Q_FOR_HPC evidence on a flagship HPC workload; useful as a workload projection rather than a systems mechanism.

### TQE-144 — A Modular Quantum Network Architecture for Integrating Network Scheduling With Local Program Execution

- **DOI:** 10.1109/tqe.2025.3624658 · **Census year:** 2025 · **v7**, pp. 4100629-4100629 · **Online:** 2025-10-23
- **Lead author:** Thomas R. Beauchamp (+3 co-authors) · **arXiv:** 2503.12582
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** Q_IN_HPC, FUTURE_WORKLOAD · **Branch:** quantum_runtime_orchestration, multi_qpu_distributed_qc
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Scheduling latency against qubit lifetimes, and coordination between a network scheduler and a local program runtime.

**Gate 2 — HPC/systems technique in the contribution.** Architecture and interface definition (entanglement packet); no implementation or measured performance.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Structurally the same problem as coupling a job scheduler to a QPU runtime.

**Reason for inclusion:** Scheduling and execution-integration are the substance, and local program execution (computing) is explicitly in scope of the architecture.

**Reason against inclusion:** The setting is a quantum network delivering entanglement (false-positive class 4); the computing side is an interface, not a workload.

**Research question.** How can a network-level entanglement schedule be integrated with the execution of quantum programs running on the end nodes?

**Quantum problem.** Applications on end nodes need entanglement delivered when their program reaches the consuming instruction, within qubit lifetimes.

**Classical / HPC problem.** Scheduling and interface design between a network scheduler and a local program runtime; the entanglement packet is essentially a scheduling/QoS abstraction.

**Mechanism.** A modular, hardware-agnostic architecture defining an entanglement packet and the interfaces by which a network schedule is aligned with local program execution.

**Computational bottleneck.** Qubit lifetime versus scheduling latency; coordination between network and node schedulers.

**Evaluation platform.** Architecture specification.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** INSUFFICIENT_EVIDENCE

**Major claim.** Network scheduling and local quantum program execution can be integrated through a modular architecture with an entanglement-packet abstraction.

**Limitation.** Architecture definition without implementation or measured performance.

**Relevance.** The interface between a network scheduler and a program runtime is structurally the same problem as coupling a job scheduler to a QPU runtime.

### TQE-145 — Binary Tree Block Encoding of Classical Matrix

- **DOI:** 10.1109/tqe.2025.3624699 · **Census year:** 2025 · **v7**, pp. 1-18 · **Online:** 2025-10-23
- **Lead author:** Zexian Li (+3 co-authors) · **arXiv:** 2504.05624
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Compilation time and space are listed explicitly among the resources traded off.

**Gate 2 — HPC/systems technique in the contribution.** A circuit construction; the compilation-cost analysis is one axis among several rather than the mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Bears on classical data-loading cost, where data volume meets circuit construction in hybrid workloads.

**Reason for inclusion:** Compilation time and space are treated as primary resources, which is a Gate-1 quantity.

**Reason against inclusion:** The main result is a circuit construction with gate/qubit counts; the compilation-cost analysis may be secondary.

**Research question.** What is the best trade-off between circuit size, subnormalization, compilation time and space when block-encoding a classical matrix?

**Quantum problem.** Block encoding turns classical data into a matrix inside a quantum circuit, a prerequisite subroutine for many algorithms.

**Classical / HPC problem.** Compilation complexity in both time and space is listed explicitly as one of the resource dimensions, alongside circuit size and robustness — i.e. the classical cost of preparing the circuit.

**Mechanism.** Binary-tree block encoding (BITBL), a construction whose resource trade-offs across circuit size, subnormalization and compilation cost are analysed.

**Computational bottleneck.** Classical compilation time and memory to build the encoding circuit; circuit size.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Circuit size, subnormalization factor, compilation time and space; numeric values not recoverable from the truncated abstract.

**Major claim.** The binary-tree construction improves the joint trade-off among circuit size, subnormalization and compilation cost for block encoding.

**Limitation.** Classical data loading remains the bottleneck of the algorithms that consume block encodings.

**Relevance.** Data loading is where classical data volume meets quantum circuits — a data-movement question for hybrid workloads.

### TQE-147 — A Dynamic Testing Strategy With Incremental Learning Model for Quantum Programs

- **DOI:** 10.1109/tqe.2025.3626745 · **Census year:** 2025 · **v7**, pp. 1-27 · **Online:** 2025-10-31
- **Lead author:** Linzhi Huang (+4 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Execution budget: how many program runs are needed to reach a confidence level.

**Gate 2 — HPC/systems technique in the contribution.** ML-driven dynamic test selection in the software stack; no systems technique.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Concerns testing cost in the quantum software stack.

**Reason for inclusion:** Software-stack contribution with an explicit execution-cost trade-off.

**Reason against inclusion:** No HPC/systems technique; execution budget is the only Gate-1 quantity and it is treated statistically.

**Research question.** Can incremental learning drive a dynamic test-case selection strategy for quantum programs?

**Quantum problem.** Quantum programs are probabilistic and hard to observe, so classical testing techniques transfer poorly.

**Classical / HPC problem.** Test-execution cost: a dynamic strategy chooses which tests to run as evidence accumulates, which is a cost-versus-coverage trade-off in the software stack.

**Mechanism.** A dynamic testing strategy with an incremental learning model that updates its test selection from observed outcomes.

**Computational bottleneck.** Number of program executions (shots/test runs) required to reach a confidence level.

**Evaluation platform.** Quantum program benchmarks (details not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Fault-detection effectiveness versus number of executions; numeric values not recoverable from the truncated abstract.

**Major claim.** Incremental learning reduces the testing effort needed to detect faults in quantum programs relative to static testing strategies.

**Limitation.** Testing effectiveness depends on the fault models used; no runtime/system integration.

**Relevance.** Quantum software engineering, part of the software stack, with an execution-budget dimension.

### TQE-152 — Feynman Meets Turing: Computability Aspects of Exact Circuit Synthesis, Gate Efficiency, and the Spectral Gap Conjecture

- **DOI:** 10.1109/tqe.2025.3636049 · **Census year:** 2025 · **v7**, pp. 1-31 · **Online:** 2025-11-24
- **Lead author:** Yannik N. Boeck (+2 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Computability of the compilation task rather than a measured cost.

**Gate 2 — HPC/systems technique in the contribution.** Computable-analysis theory applied to exact synthesis and gate efficiency.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Sets outer bounds on what any quantum compiler can be asked to do.

**Reason for inclusion:** Concerns the compilation stage and its algorithmic limits, which bear on compiler design.

**Reason against inclusion:** Pure computability theory; no cost, scaling or implementation content (close to false-positive class 7).

**Research question.** Which exact circuit-synthesis and gate-efficiency questions are computable, and what does computable analysis say about the spectral gap conjecture?

**Quantum problem.** Exact synthesis of a unitary from a given gate family is fundamental to the circuit model.

**Classical / HPC problem.** Computability of the compilation task itself: whether a gate-agnostic synthesis algorithm can exist bounds what any compiler can do.

**Mechanism.** Recasts exact synthesis, gate efficiency and the spectral gap conjecture in the framework of computable analysis and derives computability results.

**Computational bottleneck.** Decidability/computability of synthesis rather than a measured cost.

**Evaluation platform.** Theoretical analysis.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** INSUFFICIENT_EVIDENCE

**Major claim.** Computable-analysis results delimit which exact-synthesis and gate-efficiency questions admit algorithmic solutions.

**Limitation.** No practical algorithm or implementation; results are existence/computability statements.

**Relevance.** Sets outer bounds on what a quantum compiler can be asked to do.

### TQE-154 — Low-Complexity Syndrome-Based Linear Programming Decoding of Quantum LDPC Codes

- **DOI:** 10.1109/tqe.2025.3640361 · **Census year:** 2025 · **v7**, pp. 1-19 · **Online:** 2025-12-04
- **Lead author:** Sana Javed (+6 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Decoder complexity and iteration budget, with early stopping controlling when the expensive stage runs.

**Gate 2 — HPC/systems technique in the contribution.** Decoder algorithm with a compute-budget control; no hardware or parallel implementation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** The early-stopping mechanism is a scheduling decision over an expensive classical stage.

**Reason for inclusion:** Explicit complexity/early-stopping mechanism (a compute-budget control) and decoder scheduling flavour.

**Reason against inclusion:** New decoder algorithm only, evaluated under an idealized noise model — BORDERLINE by the QEC rule.

**Research question.** Can a low-complexity syndrome-based linear-programming decoder reduce the error floor of min-sum decoding for quantum LDPC codes at acceptable cost?

**Quantum problem.** Quantum LDPC decoding suffers an error floor under iterative min-sum decoding.

**Classical / HPC problem.** Decoder complexity and early stopping: the LP stage runs only when a criterion triggers, avoiding a fixed maximum iteration count — a compute-budget mechanism.

**Mechanism.** A syndrome-based LP decoder usable standalone or as postprocessing after syndrome-based min-sum decoding, with an early-stopping criterion controlling when the expensive LP stage is invoked.

**Computational bottleneck.** Cost of the LP stage versus iterative min-sum; iteration budget.

**Evaluation platform.** Numerical decoding simulations under the code-capacity model.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Error-floor reduction and iteration savings versus flooded and layered SB-MS scheduling; numeric values not recoverable from the truncated abstract.

**Major claim.** LP postprocessing with early stopping substantially lowers the error floor of min-sum decoding while avoiding a fixed maximum iteration budget.

**Limitation.** Code-capacity model only; LP decoding is expensive and no hardware/latency evaluation is given.

**Relevance.** Decoder compute budget and scheduling of an expensive stage — the systems-relevant part of decoder design.

### TQE-163 — Multiplexed Bilayered Realization of Fault-Tolerant Quantum Computation Over Optically Networked Trapped-Ion Modules

- **DOI:** 10.1109/tqe.2025.3649617 · **Census year:** 2026 · **v7**, pp. 1-18 · **Online:** 2026-01-01
- **Lead author:** Nitish Kumar Chandra (+2 co-authors) · **arXiv:** 2411.08616
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** FUTURE_WORKLOAD, HPC_FOR_Q · **Branch:** multi_qpu_distributed_qc, architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Inter-module entanglement generation rate and per-module resource counts (modules, ions per module).

**Gate 2 — HPC/systems technique in the contribution.** WEAK for this corpus: the mechanism is photonic multiplexing and a bilayered module layout, a physical-layer technique rather than a classical systems technique.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Sizes the interconnect of a modular quantum computer, which is the multi-QPU analogue of node and network sizing.

**Reason for inclusion:** Modular and distributed quantum-computing architecture is an explicit INCLUDE shape, and the paper sizes inter-module resources for a computing objective (fault-tolerant MBQC) rather than a communication objective.

**Reason against inclusion:** The quantity actually optimized is the remote entanglement generation rate against the RHG lattice bond-failure threshold, achieved by photonic multiplexing. That is a quantum-networking physical-layer mechanism (false-positive class 4), not a classical computing-systems contribution: no classical cost, scheduling, runtime or software-stack element is analysed. Demoted from INCLUDED during adversarial verification.

**Notes.** Demoted INCLUDED -> BORDERLINE during adversarial verification: the optimized quantity is remote entanglement rate against a lattice bond-failure threshold, a quantum-networking physical-layer mechanism, so Gate 2 is not carried by a classical systems technique.

**Research question.** What module count, ion count per module and remote-entanglement rate are required for fault-tolerant measurement-based computation across optically networked trapped-ion modules?

**Quantum problem.** Fault-tolerant MBQC on a Raussendorf-Harrington-Goyal lattice built from many small modules whose inter-module links fail probabilistically.

**Classical / HPC problem.** Modular/distributed architecture sizing: relating interconnect rate, multiplexing degree and per-module resources to a system-level tolerance threshold — an architecture-level resource/throughput analysis.

**Mechanism.** A multiplexed bilayered module arrangement in which each module acts as a lattice site, with photonic links for remote entanglement and local Coulomb interactions for intra-module gates; multiplexing raises the remote entanglement rate above the bond-failure threshold.

**Computational bottleneck.** Remote entanglement generation rate versus lattice bond-failure tolerance; ions per module.

**Evaluation platform.** Architecture-level analysis with finite module and ion counts.

**Scale.** Finite number of modules and ions per module (exact figures not recoverable from the truncated abstract).

**Performance metrics.** Required entanglement rates and resource counts to stay above the bond-failure threshold; numeric values not recoverable from the truncated abstract.

**Major claim.** Multiplexing and a bilayered module layout can push remote entanglement rates past the RHG bond-failure tolerance with finite per-module resources.

**Limitation.** Idealized link and noise models; no execution-level or software-stack evaluation.

**Relevance.** Quantitative sizing of a modular quantum computer's interconnect — the multi-QPU analogue of node/network sizing in HPC.

### TQE-171 — Encrypted-State Quantum Compilation Scheme Based on Quantum Circuit Obfuscation for Quantum Cloud Platforms

- **DOI:** 10.1109/tqe.2026.3659096 · **Census year:** 2026 · **v7**, pp. 1-18 · **Online:** 2026-01-01
- **Lead author:** Chenyi Zhang (+3 co-authors) · **arXiv:** 2507.17589
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** Q_IN_HPC · **Branch:** compiler_mapping_routing, quantum_runtime_orchestration
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Compilation and execution overhead added by protecting a workload from the infrastructure running it.

**Gate 2 — HPC/systems technique in the contribution.** A security scheme for cloud compilation; the overhead trade-off is unquantified here.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** A multi-tenancy concern that arises if QPUs become shared centre resources.

**Reason for inclusion:** Cloud compilation service design with an overhead trade-off — a systems concern for shared QPU infrastructure.

**Reason against inclusion:** The contribution is a security scheme; the systems content (overhead) is secondary and unquantified here.

**Research question.** Can compilation be performed on a cloud platform without exposing the user's circuit structure and outputs?

**Quantum problem.** Quantum cloud platforms colocate compilers with hardware, so user circuits are visible to the provider.

**Classical / HPC problem.** Multi-tenant cloud service design: protecting a workload from the infrastructure that executes it, with compilation overhead as the cost to be bounded.

**Mechanism.** ECQCO applies quantum homomorphic encryption to conceal output states and an obfuscation mechanism to hide circuit structure during cloud compilation.

**Computational bottleneck.** Compilation and execution overhead added by encryption/obfuscation.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Security metrics and compilation/execution overhead; numeric values not recoverable from the truncated abstract.

**Major claim.** Circuit structure and outputs can be protected during cloud compilation with bounded overhead.

**Limitation.** Overhead of obfuscation directly competes with the fidelity budget on NISQ hardware.

**Relevance.** A multi-tenant quantum-cloud systems concern; relevant if QPUs become shared HPC-centre resources.

### TQE-172 — A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits

- **DOI:** 10.1109/tqe.2026.3659400 · **Census year:** 2026 · **v7**, pp. 1-52 · **Online:** 2026-01-01
- **Lead author:** Naheel Raza Rizvi (+6 co-authors) · **arXiv:** none listed
- **Article type:** REVIEW_SURVEY · **BIBLIOGRAPHY_HUB**
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Channel count, bandwidth and cryogenic integration limits of control and readout infrastructure.

**Gate 2 — HPC/systems technique in the contribution.** Survey synthesis of control/readout architectures; no new system or measurement.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Serves as a reference map of the classical control plane (tagged BIBLIOGRAPHY_HUB).

**Reason for inclusion:** Control systems and classical control hardware are an explicitly relevant TQE sub-area; as a survey it is a useful bibliography hub.

**Reason against inclusion:** Content is RF/microwave and cryogenic electronics engineering, adjacent to excluded class 6.

**Research question.** What are the control and readout architectures for superconducting qubits, and what are their requirements and scaling limits?

**Quantum problem.** Superconducting qubits need microwave pulse generation and readout signal analysis at increasing channel counts.

**Classical / HPC problem.** Surveys the classical RF/signal-processing infrastructure — generation, synthesis, readout analysis and cryogenic integration — and its scaling requirements.

**Mechanism.** Technical survey synthesizing device physics, circuit design, microwave engineering, signal processing and cryogenic integration into a control/readout architecture taxonomy.

**Computational bottleneck.** Channel count, bandwidth and cryogenic integration limits of control/readout hardware.

**Evaluation platform.** Literature survey.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Comparative requirements and parameters across architectures; numeric values not recoverable from the truncated abstract.

**Major claim.** A consolidated account of superconducting control and readout architectures, their key parameters and their scaling constraints.

**Limitation.** Survey; no new measurement or system.

**Relevance.** A reference map of the classical control plane, useful as an entry point into that literature.

### TQE-177 — Parallel Variational Quantum Algorithms With Gradient-Informed Restart to Speed Up Optimization in the Presence of Barren Plateaus

- **DOI:** 10.1109/tqe.2026.3663507 · **Census year:** 2026 · **v7**, pp. 1-17 · **Online:** 2026-01-01
- **Lead author:** Daniel Mastropietro (+3 co-authors) · **arXiv:** 2311.18090
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** hybrid_workflow
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Total circuit evaluations across parallel searches and the restart policy that governs them.

**Gate 2 — HPC/systems technique in the contribution.** A classical parallel-optimization strategy (Fleming-Viot particles with gradient-informed restart).

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Indicates how parallel VQA execution would consume shared QPU time.

**Reason for inclusion:** Parallel execution and restart policy are genuine execution-strategy content.

**Reason against inclusion:** The motivation is barren plateaus, which the criteria exclude; no scheduling or resource-management mechanism.

**Research question.** Does running many parallel variational searches with gradient-informed restarts reduce the time lost to flat optimization landscapes?

**Quantum problem.** Variational optimization stalls where gradients are small or noisy.

**Classical / HPC problem.** Parallel search with restart is a classical parallel-optimization strategy; the resource question is how many parallel particles are needed and what they cost in QPU time.

**Mechanism.** A Fleming-Viot inspired parallel scheme in which particles that reach low-gradient regions are stopped and restarted elsewhere in parameter space.

**Computational bottleneck.** Total circuit evaluations across parallel particles; restart policy cost.

**Evaluation platform.** Numerical experiments.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Optimization time/iterations versus sequential VQA; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Parallel particles with gradient-informed restart reduce time spent in flat regions compared with a single sequential variational run.

**Limitation.** Parallelism is in the classical optimizer loop; total quantum resource consumption may increase.

**Relevance.** Parallel execution of variational workloads bears on how VQA jobs would be scheduled on shared QPUs.

### TQE-182 — Parameter Analysis and Optimization of Layer Fidelity for Quantum Processor Benchmarking at Scale

- **DOI:** 10.1109/tqe.2026.3668098 · **Census year:** 2026 · **v7**, pp. 1-10 · **Online:** 2026-01-01
- **Lead author:** Maria Jose Lozano Palacio (+3 co-authors) · **arXiv:** 2510.16915
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Device time and measurement count required to characterize a large processor.

**Gate 2 — HPC/systems technique in the contribution.** Protocol-parameter optimization; the resource optimized is quantum device time, not a classical systems resource.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies the cost of characterizing processors at scale.

**Reason for inclusion:** Benchmarking infrastructure at processor scale with an explicit measurement-cost dimension.

**Reason against inclusion:** The resource optimized is quantum device time, not a classical systems resource; content is device characterization.

**Research question.** How should layer-fidelity benchmark parameters be chosen to characterize a large processor efficiently and reliably?

**Quantum problem.** Holistic device characterization at the scale of hundreds of qubits.

**Classical / HPC problem.** Measurement-campaign efficiency: qubit-chain selection and parameter choices determine how much device time the benchmark consumes at a given signal-to-noise ratio.

**Mechanism.** Extends the layer-fidelity protocol with a procedure for identifying optimal qubit chains and tuning benchmark parameters.

**Computational bottleneck.** Device time and measurement count for benchmarking at scale.

**Evaluation platform.** Large superconducting processors (device identity not recoverable from the truncated abstract).

**Scale.** Processor-scale (large qubit counts).

**Performance metrics.** Benchmark signal-to-noise and runtime versus the original protocol; numeric values not recoverable from the truncated abstract.

**Major claim.** Optimized chain selection and parameter settings make layer-fidelity benchmarking more informative per unit of device time.

**Limitation.** Refines an existing protocol; the resource analysed is device time rather than classical compute.

**Relevance.** Benchmarking at scale, a listed TQE sub-area, with measurement-cost content.

### TQE-186 — Rapid Autotuning of a SiGe Quantum Dot Into the Single-Electron Regime With Machine Learning and RF-Reflectometry FPGA-Based Measurements

- **DOI:** 10.1109/tqe.2026.3670353 · **Census year:** 2026 · **v7**, pp. 1-7 · **Online:** 2026-01-01
- **Lead author:** Marc-Antoine Roux (+20 co-authors) · **arXiv:** 2509.19537
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** architecture_control
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Acquisition time per stability diagram and the number of measurements needed to tune a device.

**Gate 2 — HPC/systems technique in the contribution.** Real-time FPGA measurement combined with ML autotuning to cut both per-measurement time and measurement count.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Calibration is a real-time classical workload that must scale with qubit count.

**Reason for inclusion:** Real-time FPGA processing plus measurement-count reduction is a throughput/latency contribution in the classical control plane.

**Reason against inclusion:** The subject matter is device tuning (false-positive class 6); no computing-systems abstraction is produced.

**Research question.** Can machine learning plus FPGA-based RF reflectometry cut the time needed to tune a quantum dot into the single-electron regime?

**Quantum problem.** Charge-state stability diagrams are slow to acquire, and the search space grows with qubit count.

**Classical / HPC problem.** Measurement throughput and real-time classical processing: the speedup comes from both faster FPGA-based acquisition and fewer measurements chosen by an ML autotuner.

**Mechanism.** Combines an autotuning algorithm with FPGA-based RF-reflectometry measurement to reduce both per-measurement time and the number of measurements.

**Computational bottleneck.** Acquisition time per stability diagram; number of measurements needed to locate the target charge state.

**Evaluation platform.** SiGe quantum dot device with FPGA-based RF reflectometry.

**Scale.** Single quantum dot.

**Performance metrics.** Reported speedup in tuning time; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Combining measurement speedup with measurement-count reduction gives a significant reduction in device tuning time compared with sampling-efficiency-only approaches.

**Limitation.** Demonstrated on a single dot; scaling to arrays is argued, not shown.

**Relevance.** Calibration automation is a real-time classical workload that will have to scale with qubit count.

### TQE-187 — Efficient Implementation of Randomized Quantum Algorithms With Dynamic Circuits

- **DOI:** 10.1109/tqe.2026.3671723 · **Census year:** 2026 · **v7**, pp. 1-13 · **Online:** 2026-01-01
- **Lead author:** Shu Kanno (+4 co-authors) · **arXiv:** 2503.17833
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** quantum_runtime_orchestration
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Per-circuit submission, compilation and queue overhead, and total wall-clock execution time.

**Gate 2 — HPC/systems technique in the contribution.** Circuit-level engineering using dynamic circuits; no runtime system or scheduler is built.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** An execution-model optimization aimed at job overhead rather than gate count.

**Reason for inclusion:** Wall-clock execution time and submission overhead are the optimized quantities — a genuine orchestration concern.

**Reason against inclusion:** No runtime system or scheduler is built; the mechanism is a circuit-level engineering technique.

**Research question.** Can dynamic circuits collapse many static circuit submissions into a single circuit and thereby cut the wall-clock cost of randomized algorithms?

**Quantum problem.** Randomized algorithms require sampling many distinct circuits, each of which is a separate job on a device.

**Classical / HPC problem.** Job submission and execution overhead: each distinct circuit costs setup/queueing time, so consolidating them into one dynamic circuit with many measurements is a throughput optimization.

**Mechanism.** Generates the randomizing probability distribution on the device using intermediate measurement and feedback, so one dynamic circuit realizes many static circuit instances.

**Computational bottleneck.** Per-circuit submission/compilation/queue overhead; mid-circuit measurement and feedback latency.

**Evaluation platform.** Real quantum hardware (device identity not recoverable from the truncated abstract).

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in total execution time for randomized algorithms; numeric values not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** Executing randomized algorithms as a single dynamic circuit reduces total execution time compared with submitting many static circuits.

**Limitation.** Depends on hardware support for mid-circuit measurement and feedback; benefit is tied to current submission overheads.

**Relevance.** An execution-model/orchestration optimization: it targets job overhead rather than gate count.

### TQE-189 — Beyond Asymptotic Scaling: Comparing Functional Quantum Linear Solvers

- **DOI:** 10.1109/tqe.2026.3674210 · **Census year:** 2026 · **v7**, pp. 1-26 · **Online:** 2026-01-01
- **Lead author:** Andreea-Iulia Lefterovici (+5 co-authors) · **arXiv:** 2503.21420
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** FUTURE_WORKLOAD, HPC_FOR_Q · **Branch:** benchmarking_performance_modeling
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Concrete resource requirements of quantum linear solvers at practical instance sizes.

**Gate 2 — HPC/systems technique in the contribution.** Empirical comparison under a common framework; no classical systems mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Projects which quantum kernels might eventually displace classical HPC solvers.

**Reason for inclusion:** Empirical performance modeling of a kernel central to HPC workloads, explicitly contrasting asymptotics with practice.

**Reason against inclusion:** Quantum-algorithm resource counting (false-positive class 7) with no classical systems mechanism.

**Research question.** Which quantum linear solver performs best on instances of practical size, as opposed to in asymptotic worst-case complexity?

**Quantum problem.** Quantum linear solvers underpin many algorithms but assume fault-tolerant hardware.

**Classical / HPC problem.** Empirical resource comparison: implements four solvers and measures their concrete resource requirements, a performance-modeling exercise for a future workload.

**Mechanism.** Implements four matrix-inversion-function quantum linear solvers under a common framework and compares their concrete resource usage on practical instances.

**Computational bottleneck.** Circuit resources (gate/qubit counts) at practical instance sizes; classical simulation cost of the comparison.

**Evaluation platform.** Simulation-based implementation and comparison.

**Scale.** Practical-size instances (dimensions not recoverable from the truncated abstract).

**Performance metrics.** Concrete resource counts per solver; numeric values not recoverable from the truncated abstract.

**Major claim.** Concrete-instance comparison ranks quantum linear solvers differently from their asymptotic complexity ordering.

**Limitation.** Fault-tolerant assumptions; no hardware execution and no classical HPC baseline comparison.

**Relevance.** Useful for projecting which quantum kernels could displace classical linear solvers in HPC workloads.

### TQE-203 — Quantum Communication Complexity of Regularized Linear Regression Protocols

- **DOI:** 10.1109/tqe.2026.3687237 · **Census year:** 2026 · **v7**, pp. 3103012-3103012 · **Online:** 2026-01-01
- **Lead author:** Sayaki Matsushita (+0 co-authors) · **arXiv:** 2508.16141
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** Q_FOR_HPC · **Branch:** multi_qpu_distributed_qc
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Communication cost of a distributed computation is the optimized quantity.

**Gate 2 — HPC/systems technique in the contribution.** Protocol communication-complexity analysis in the coordinator model; no implementation.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Gives communication bounds for distributed quantum-assisted linear algebra.

**Reason for inclusion:** Communication cost of distributed computation is treated as the central resource.

**Reason against inclusion:** Purely a communication-complexity result (false-positive class 7); no systems mechanism or measurement.

**Research question.** How much communication does distributed least-squares regression need in the quantum coordinator model, with and without L2 regularization?

**Quantum problem.** Distributed quantum protocols for a linear-algebra primitive under a coordinator model.

**Classical / HPC problem.** Communication cost of a distributed computation is the optimized quantity — the same currency as in classical distributed-computing complexity.

**Mechanism.** Improves and extends the distributed quantum least-squares protocol to ordinary and Tikhonov-regularized problems, with reduced communication.

**Computational bottleneck.** Quantum communication cost between the coordinator and the parties.

**Evaluation platform.** Theoretical protocol analysis.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in quantum communication cost relative to the prior distributed least-squares protocol; exact bounds not recoverable from the truncated abstract.

**Major claim.** The proposed protocols reduce the quantum communication cost of distributed least squares relative to the prior protocol, and extend it to regularized problems.

**Limitation.** Complexity-theoretic; no implementation, and the coordinator model abstracts away real network behaviour.

**Relevance.** Communication cost in distributed computation is a Gate-1 quantity; this is the quantum analogue of distributed-algorithm communication bounds.

### TQE-217 — Quantum Computing for Computational Sciences

- **DOI:** 10.1109/tqe.2026.3697204 · **Census year:** 2026 · **v7**, pp. 3103728-3103728 · **Online:** 2026-01-01
- **Lead author:** Saleh Almutairi (+6 co-authors) · **arXiv:** none listed
- **Article type:** REVIEW_SURVEY · **BIBLIOGRAPHY_HUB**
- **Verdict:** BORDERLINE · **Scenario:** FUTURE_WORKLOAD, Q_FOR_HPC · **Branch:** scientific_workflow_application, benchmarking_performance_modeling
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Resource requirements of fault-tolerant simulation against the classical methods it would displace.

**Gate 2 — HPC/systems technique in the contribution.** Survey and requirement analysis; no mechanism.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** A workload projection for the HPC application domains a quantum accelerator would serve (tagged BIBLIOGRAPHY_HUB).

**Reason for inclusion:** Future-workload projection for HPC application domains, with resource requirements as the organizing axis; useful as a bibliography hub.

**Reason against inclusion:** Application/algorithm survey with no classical systems mechanism (overlaps false-positive class 3).

**Research question.** What technical requirements must be met for quantum computing to deliver practical utility in chemistry, biochemistry and materials science?

**Quantum problem.** Translating asymptotic algorithmic speedups into usable results for computational-science workloads.

**Classical / HPC problem.** Assesses resource requirements of Hamiltonian-simulation frameworks against the classical methods they would displace — a workload-projection exercise for HPC application domains.

**Mechanism.** Survey of algorithms (QFT, phase estimation, linear solvers, VQE, QAOA) and near-optimal Hamiltonian simulation (qubitization, quantum signal processing) with an assessment of practical requirements.

**Computational bottleneck.** Resource requirements of fault-tolerant simulation versus the classical cost of the incumbent methods.

**Evaluation platform.** Literature survey and requirement analysis.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Resource-requirement estimates per application area; numeric values not recoverable from the truncated abstract.

**Major claim.** A consolidated assessment of what quantum computing must achieve before it is useful for computational-science workloads.

**Limitation.** Survey; estimates depend on the assumed hardware model.

**Relevance.** A workload-projection reference for the HPC application domains a quantum accelerator would serve.

### TQE-224 — Multilevel Gate Set Optimization of Quantum Circuits for Partial Differential Equations

- **DOI:** 10.1109/tqe.2026.3706630 · **Census year:** 2026 · **v7**, pp. 1-17 · **Online:** 2026-01-01
- **Lead author:** Tamiya Onodera (+3 co-authors) · **arXiv:** 2505.09320
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing, scientific_workflow_application
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** Two-qubit gate cost measured against the output of a production compiler.

**Gate 2 — HPC/systems technique in the contribution.** Multilevel gate-set compiler optimization.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Measures compiler effectiveness on a scientific-computing kernel, though the outcome is a gate-count result.

**Reason for inclusion:** Explicit comparison against a production compiler, and the workload is a scientific-computing kernel.

**Reason against inclusion:** The result is gate-count reduction, which the criteria place at BORDERLINE or EXCLUDE without systems implications.

**Research question.** Can multilevel gate-set optimization reduce the two-qubit gate cost of PDE Hamiltonian-simulation circuits below what an industrial compiler achieves?

**Quantum problem.** PDE Hamiltonians do not admit efficient Pauli expansions, so circuits are built from multicontrolled gates.

**Classical / HPC problem.** Compiler effectiveness: the baseline is an industry-grade compiler, and the contribution is optimization at multiple gate-set levels rather than a single pass.

**Mechanism.** Optimizes the circuit at several gate-set abstraction levels rather than leaving all work to the final compiler pass.

**Computational bottleneck.** CX gate count (quadratic in the relevant parameter after industrial compilation); optimization pass cost.

**Evaluation platform.** Circuit compilation with an industry-grade compiler as baseline.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in CX count relative to industry-grade compiler output; numeric values not recoverable from the truncated abstract.

**Major claim.** Multilevel gate-set optimization produces PDE simulation circuits with fewer two-qubit gates than an industry-grade compiler alone.

**Limitation.** Gate-count improvement without execution or compile-time results; PDE-specific.

**Relevance.** Compiler-stage optimization measured against a production compiler, on a workload drawn from scientific computing.

### TQE-230 — Topological Quantum Compilation Using Mixed-Integer Programming

- **DOI:** 10.1109/tqe.2026.3710775 · **Census year:** 2026 · **v7**, pp. 3104212-3104212 · **Online:** 2026-01-01
- **Lead author:** Pavel Rytir (+4 co-authors) · **arXiv:** 2511.09513
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** compiler_mapping_routing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS

**Gate 1 — classical systems problem.** MIP solver runtime and memory are the binding constraints on the compilation method.

**Gate 2 — HPC/systems technique in the contribution.** Compilation expressed as a classical combinatorial optimization workload solved by standard MIP solvers.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Shows classical solver cost becoming the limit on a compilation stage.

**Reason for inclusion:** Classical solver cost is the binding constraint on the compilation method — a genuine compilation-scalability question.

**Reason against inclusion:** Targets topological hardware that is not realized; no measured compile-time scaling reported in the abstract.

**Research question.** Can topological quantum compilation (braid-sequence synthesis) be expressed and solved as mixed-integer programming?

**Quantum problem.** Gates in topological quantum computing are realized by braid sequences that must be constructed explicitly.

**Classical / HPC problem.** Compilation as a classical combinatorial optimization workload solved by MIP; the practical limit is solver scalability.

**Mechanism.** Formulates a broad class of topological compilation problems as mixed-integer programs and solves them with standard MIP solvers.

**Computational bottleneck.** MIP solver runtime and memory as braid length and target precision grow.

**Evaluation platform.** Mixed-integer programming solvers.

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Solution quality (braid length/approximation error) and solver runtime; numeric values not recoverable from the truncated abstract.

**Major claim.** A general MIP formulation covers a broad class of topological compilation problems and produces braid sequences with optimality guarantees.

**Limitation.** MIP scalability limits problem size; results are for a hardware paradigm that does not yet exist in usable form.

**Relevance.** Compilation posed as a classical optimization workload with explicit solver-cost consequences.

### TQE-245 — Noise-model-free versus Bayes-optimal decoding of finite-energy GKP qubits

- **DOI:** 10.1109/tqe.2026.3730475 · **Census year:** 2026 · **EarlyAccess**, pp. 1-15 · **Online:** 2026-01-01
- **Lead author:** Hikaru Wakaura (+1 co-authors) · **arXiv:** none listed
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** BORDERLINE · **Scenario:** HPC_FOR_Q · **Branch:** qec_classical_processing
- **Deep-dive priority:** LOW · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Evidence flag:** NO_ABSTRACT
- **Abstract status:** NO_ABSTRACT

**Gate 1 — classical systems problem.** NOT EVIDENCED (NO_ABSTRACT): no classical cost, latency or memory quantity can be confirmed.

**Gate 2 — HPC/systems technique in the contribution.** NOT EVIDENCED: decoder comparison per the title; no mechanism recoverable.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Retained under the QEC decoder rule pending full-text retrieval; relevance unverified.

**Reason for inclusion:** Decoder algorithm comparison falls under the QEC decoder rule, which makes decoder-only work BORDERLINE rather than excluded.

**Reason against inclusion:** No abstract was retrieved, so no evidence of parallelism, hardware implementation or classical cost analysis exists.

**Research question.** How does noise-model-free decoding of finite-energy GKP qubits compare with Bayes-optimal decoding? (NO_ABSTRACT; question inferred from the title.)

**Quantum problem.** Decoding GKP-encoded qubits with finite energy, where the noise model may be unknown.

**Classical / HPC problem.** Decoder design under model uncertainty; the classical cost of the two decoding strategies is the natural systems question but is not evidenced here.

**Mechanism.** NO_ABSTRACT: mechanism not recoverable.

**Computational bottleneck.** INSUFFICIENT_EVIDENCE

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** INSUFFICIENT_EVIDENCE

**Major claim.** INSUFFICIENT_EVIDENCE — only the title is available.

**Limitation.** INSUFFICIENT_EVIDENCE

**Relevance.** Decoder comparison work; retained as BORDERLINE under the QEC decoder rule pending full-text retrieval.

## 5. False-positive log

### 5.1 Class legend

| Class | Definition |
|---|---|
| 1 | Post-quantum cryptography (lattice/SVP/ECDLP/Shor-for-crypto, PQC side channels) |
| 2 | Quantum-inspired classical methods (Ising machines, QUBO solvers run classically) |
| 3 | Classical quantum chemistry / many-body / field-theory simulation as the result |
| 4 | Quantum networking / QKD / quantum internet (routing, repeaters, key distribution, secret sharing) |
| 5 | Quantum machine learning applications (QNN/QGAN/QFL/quantum kernels on a domain task) |
| 6 | Quantum sensing / metrology / device & materials physics / cryo readout electronics |
| 7 | Quantum algorithms / complexity theory (oracles, walks, bounds, resource counts with no systems mechanism) |
| E8 | EXTENSION: quantum optimization applications (QAOA / annealing / Grover applied to a domain problem) |
| E9 | EXTENSION: VQA methodology & error mitigation (ansatz design, optimizer, expressibility, barren plateaus, ZNE/PEC/CDR) |
| E10 | EXTENSION: QEC code & protocol theory (new codes, thresholds, syndrome-extraction circuit design) |
| E11 | EXTENSION: quantum control / pulse & gate design / calibration / quantum feedback control theory |
| E12 | EXTENSION: quantum information theory (channel capacity, state discrimination, tomography statistics) |

Classes 1-7 are the canonical false-positive classes from CRITERIA.md. Classes E8-E12 are corpus-local extensions added because TQE's excluded population is dominated by topics the canonical seven do not name (quantum optimization applications, VQA/error-mitigation methodology, QEC code theory, quantum control, quantum information theory).

### 5.2 Excluded records by class

| Class | Label | Count | Share of exclusions |
|---|---|---:|---:|
| 4 | Quantum networking / QKD / quantum internet | 49 | 26.8% |
| 6 | Quantum sensing / metrology / device & materials physics / cryo readout electronics | 32 | 17.5% |
| E8 | EXTENSION: quantum optimization applications | 29 | 15.8% |
| 5 | Quantum machine learning applications | 21 | 11.5% |
| E9 | EXTENSION: VQA methodology & error mitigation | 16 | 8.7% |
| 7 | Quantum algorithms / complexity theory | 14 | 7.7% |
| E11 | EXTENSION: quantum control / pulse & gate design / calibration / quantum feedback control theory | 7 | 3.8% |
| E10 | EXTENSION: QEC code & protocol theory | 5 | 2.7% |
| E12 | EXTENSION: quantum information theory | 4 | 2.2% |
| 1 | Post-quantum cryptography | 4 | 2.2% |
| 3 | Classical quantum chemistry / many-body / field-theory simulation as the result | 1 | 0.5% |
| 2 | Quantum-inspired classical methods | 1 | 0.5% |
| | **Total** | **183** | **100%** |

### 5.3 Search-vocabulary terms that produced the most false positives

Counts are measured by case-insensitive regex over title plus the 700-character truncated abstract of all 246 records. 'matched' = records the term reaches; 'excluded' = of those, how many were excluded; 'precision' = retained share of matches (measured against the pre-verification verdicts, which differ from the final counts by three records).

| Term / vocabulary | Matched | Excluded | Retained | Precision | Why it misfires in TQE |
|---|---:|---:|---:|---:|---|
| "quantum" alone / journal-level harvesting | 246 | 183 | 63 | 25.6% | TQE's entire population is quantum, so any quantum-keyed harvest returns the whole journal. This is the dominant effect and it is structural, not lexical. |
| optimization / QUBO / annealing / QAOA / combinatorial | 74 | 56 | 18 | 24.3% | Largest single lexical driver. Matches quantum optimization applications to finance, logistics, imaging, power, telecom and manufacturing (class E8) plus VQA methodology (class E9). |
| distributed / multinode / node | 60 | 49 | 11 | 18.3% | Lowest precision of any systems-sounding term. In TQE 'distributed' and 'node' almost always mean entanglement distribution and network nodes (class 4), not distributed computation. |
| scalable / scalability / scaling | 62 | 32 | 30 | 48.4% | Used in TQE overwhelmingly to mean qubit-count scalability of a device or code, not system or software scalability. |
| machine learning / neural network / training | 41 | 32 | 9 | 22.0% | Matches QML application papers (class 5) and ansatz/architecture search (class E9), not ML-for-systems work. |
| simulation / simulator / emulation | 32 | 18 | 14 | 43.8% | Frequently means simulating a device, a network, a sensor or a physical model rather than scalable classical circuit simulation. |
| parallel / speedup / latency / throughput | 26 | 13 | 13 | 50.0% | Half the matches are algorithmic speedup claims or quantum-circuit-level parallelism rather than classical parallel execution. |
| scheduling / routing / resource allocation | 24 | 17 | 7 | 29.2% | Matches entanglement routing, repeater placement, QKD network planning and wavelength assignment (class 4) far more often than QPU scheduling. |
| readout / control electronics / FPGA / cryogenic | 16 | 7 | 9 | 56.2% | Acceptable precision overall, but the failures are the hardest kind to screen out at title level: cryo-CMOS, SFQ readout and device-electronics papers (class 6) are lexically indistinguishable from control-systems work. |
| decoder / decoding / syndrome | 14 | 5 | 9 | 64.3% | Good precision, but most retained matches are BORDERLINE decoder-algorithm papers rather than parallel or accelerated decoders. |
| benchmark / benchmarking | 12 | 5 | 7 | 58.3% | Splits between systems benchmarking (retained) and device characterization or QML-model benchmarking (excluded). |
| compiler / compilation / transpilation / mapping | 12 | 2 | 10 | 83.3% | The highest-precision term in this venue: nearly every match is genuine compilation work. |
| HPC / high-performance computing / cloud / serverless / supercomputing | 8 | 2 | 6 | 75.0% | Rare but high precision; these eight records are close to a minimal high-yield query for TQE. |

In TQE the false-positive problem is structural before it is lexical: every record in the venue is a quantum-computing record, so no quantum-side vocabulary discriminates at all. Among terms that do discriminate, the worst offenders by absolute volume are the optimization family (56 excluded matches) and the distributed/node family (49); the worst by precision is distributed/node at 18.3% retained, because 'distributed' and 'node' in TQE denote entanglement distribution and network nodes rather than distributed computation. 'Scalable' is near-useless here (48.4% precision but 62 matches) because it almost always means qubit-count scalability. The terms worth querying on are compiler/compilation/transpilation (83.3% precision), HPC/cloud/serverless (75.0%), decoder/syndrome (64.3%) and benchmark (58.3%), supplemented by literal phrases that regex cleanly: circuit cutting, state-vector simulation, decision diagram, multiprogramming, circuit packing, multi-QPU, gate fusion.

### 5.4 Excluded records, by class, with one-line reasons

#### Class 4 — Quantum networking / QKD / quantum internet (routing, repeaters, key distribution, secret sharing) (49 records)

| ID | Title | Reason |
|---|---|---|
| TQE-005 | A Linear Algebraic Framework for Dynamic Scheduling Over Memory-Equipped Quan... | Entanglement-swapping network scheduling; networking, not computing systems. |
| TQE-010 | Tools for the Analysis of Quantum Protocols Requiring State Generation Within... | Analysis tools for entangled-pair generation windows in networks. |
| TQE-012 | Rateless Protograph LDPC Codes for Quantum Key Distribution | LDPC information reconciliation for QKD. |
| TQE-014 | On the Bipartite Entanglement Capacity of Quantum Networks | Entanglement capacity of quantum networks. |
| TQE-026 | Probing Quantum Telecloning on Superconducting Quantum Processors | Telecloning demonstration; quantum communication protocol. |
| TQE-031 | Reliable Quantum Communications Based on Asymmetry in Distillation and Coding | Distillation/QEC trade-off for quantum links; communication protocol. |
| TQE-043 | Unital Qubit Queue-Channels: Classical Capacity and Product Decoding | Queue-channel classical capacity; quantum communication theory. |
| TQE-051 | Resource Placement for Rate and Fidelity Maximization in Quantum Networks | Repeater/memory placement planning in quantum networks. |
| TQE-061 | SPARQ: Efficient Entanglement Distribution and Routing in Space–Air–Ground Qu... | Entanglement routing in space-air-ground quantum networks. |
| TQE-064 | Quantum Switches for Gottesman–Kitaev–Preskill Qubit-Based All-Photonic Quant... | GKP-based quantum network switch. |
| TQE-071 | FPGA-Based Synchronization of Frequency-Domain Interferometer for QKD | FPGA synchronization for a QKD interferometer. |
| TQE-072 | TAQNet: Traffic-Aware Minimum-Cost Quantum Communication Network Planning | Minimum-cost QKD network planning. |
| TQE-076 | Convexification of the Quantum Network Utility Maximization Problem | Convexification of quantum network utility maximization. |
| TQE-079 | Quantum Two-Way Protocol Beyond Superdense Coding: Joint Transfer of Data and... | Two-way superdense coding protocol. |
| TQE-081 | Advance Sharing Procedures for the Ramp Quantum Secret Sharing Schemes With t... | Ramp quantum secret sharing procedures. |
| TQE-083 | Security and Fairness in Multiparty Quantum Secret Sharing Protocol | Multiparty quantum secret sharing security/fairness. |
| TQE-085 | Entanglement Routing in Quantum Networks: A Comprehensive Survey | Survey of entanglement routing in quantum networks. |
| TQE-088 | Qubit Rate Modulation-Based Time Synchronization Mechanism for Multinode Quan... | Time synchronization for multinode quantum networks. |
| TQE-094 | Optimized Distribution of Entanglement Graph States in Quantum Networks | Graph-state distribution in quantum networks. |
| TQE-099 | Quantum Direct-Sequence Spread-Spectrum CDMA Communication Systems: Mathemati... | Quantum spread-spectrum CDMA communication theory. |
| TQE-102 | Three-Party Controlled Authentication Semiquantum Key Agreement Protocol for ... | Semiquantum key agreement protocol. |
| TQE-103 | Quantum Wavelength-Division Multiplexing and Multiple-Access Communication Sy... | Quantum WDM/multiple-access network systems. |
| TQE-114 | Fidelity-Aware Multipath Routing for Multipartite State Distribution in Quant... | Fidelity-aware multipath routing in quantum networks. |
| TQE-117 | Generalized Quantum-Assisted Digital Signature | Quantum-assisted digital signature scheme. |
| TQE-118 | TCEP-Based Synchronization for Practical Communication Network | Entangled-photon time synchronization over fiber. |
| TQE-122 | High-Fidelity Artificial Quantum Thermal State Generation Using Encoded Coher... | Thermal-state resource generation for quantum steganography. |
| TQE-133 | Quantum Key Distribution Network and Quantum Secure Cloud Technologies for Ge... | QKD network and quantum secure cloud proof-of-concept for genome data. |
| TQE-141 | On the Capacity of Vector Linear Computation Over a Noiseless Quantum Multipl... | Capacity of a quantum multiple-access channel. |
| TQE-149 | Combined Physical- and Link-Layer Protocols for Quantum Networks | Physical/link-layer protocols for quantum repeater networks. |
| TQE-156 | On-Demand Resource Allocation for a Quantum Network Hub | Resource allocation at a quantum network (entanglement) hub. NO_ABSTRACT. |
| TQE-161 | Quantum Error Correction for Second-Generation Quantum Repeaters | QEC codes for second-generation quantum repeaters. |
| TQE-164 | Bridging All-Photonic and Memory-Based Quantum Repeaters | Interoperability of all-photonic and memory-based repeaters. |
| TQE-170 | Quantum Rotation Diversity in Displaced Squeezed Binary Phase-Shift Keying | Quantum rotation diversity for optical quantum communication. |
| TQE-176 | Realistic Quantum Network Simulation for Experimental BBM92 Key Distribution | Quantum network simulation for BBM92 QKD. |
| TQE-179 | Differential Phase Encoded Plug-and-Play Measurement-Device-Independent Quant... | Differential-phase-encoded MDI-QKD. |
| TQE-183 | Orthogonal Frequency-Division Multiplexing Continuous-Variable Terahertz QKD ... | OFDM continuous-variable terahertz QKD. |
| TQE-192 | InterQnet: A Heterogeneous Full-Stack Approach to Co-Designing Scalable Quant... | Project overview of a co-designed quantum network stack. |
| TQE-202 | Defending QKD Networks: Routing and Wavelength Assignment to Mitigate Physica... | Routing and wavelength assignment against QKD physical-layer attacks. |
| TQE-212 | Perfect Quantum Teleportation in Memory Amplitude-Damping Channels Based on P... | Teleportation protocols over memory amplitude-damping channels. |
| TQE-220 | Quantum Repeater Chains via Cavity–Magnon for Scalable Quantum Networks | Cavity-magnon quantum repeater chain architecture. |
| TQE-222 | Routing in Nonisotonic Quantum Networks | Pathfinding for nonisotonic quantum-repeater network utilities. |
| TQE-225 | Detection Error Probability Analysis Over Atmospheric Quantum Channels With P... | Error probability over atmospheric quantum optical channels. |
| TQE-231 | Automated Active-Visibility-Control Loop for Stabilized DPS-QKD Decoding Unde... | Active feedback stabilization of a DPS-QKD decoder. |
| TQE-233 | Quantum Communication Infrastructure Cost Optimization Using a Genetic Algorithm | ILP/genetic optimization of QKD infrastructure cost. |
| TQE-234 | Boosting Information Reconciliation for Decoy-State Quantum Key Distribution ... | Information reconciliation for satellite QKD downlinks. |
| TQE-239 | Entanglement Distribution and Teleportation in Assisted and Scalable Quantum ... | Entanglement distribution in passive optical access networks. |
| TQE-241 | Field Demonstration of a Passive Phase and Polarization Stabilization Archite... | Field demonstration of twin-field QKD stabilization. NO_ABSTRACT. |
| TQE-243 | Interconnecting Regional QKD Networks: Hybrid Key Delivery Across Quantum Dom... | Hybrid key delivery across interconnected QKD domains. |
| TQE-244 | RuleSet Generation Framework for Application Layer Integration in Quantum Int... | RuleSet generation for quantum internet application layer. NO_ABSTRACT. |

#### Class 6 — Quantum sensing / metrology / device & materials physics / cryo readout electronics (32 records)

| ID | Title | Reason |
|---|---|---|
| TQE-002 | Quantum Computation via Multiport Discretized Quantum Fourier Optical Processors | Photonic/optical processor physics; device-level scheme. |
| TQE-024 | Modeling and Experimental Validation of the Intrinsic SNR in Spin Qubit Gate-... | Spin-qubit RF readout SNR modelling; readout electronics physics. |
| TQE-042 | Superconducting Through-Substrate Vias on Sapphire Substrates for Quantum Cir... | Superconducting through-substrate via fabrication. |
| TQE-050 | Superconducting Nanostrip Photon-Number-Resolving Detector as an Unbiased Ran... | Superconducting nanostrip detector used as RNG; detector physics. |
| TQE-054 | Fault-Tolerant One-Way Noiseless Amplification for Microwave Bosonic Quantum ... | Microwave noiseless linear amplifier device proposal. |
| TQE-057 | Simulation of Charge Stability Diagrams for Automated Tuning Solutions (SimCATS) | Simulation of charge-stability diagrams for quantum-dot tuning; device data generation. |
| TQE-074 | Novel Trade-offs in 5 nm FinFET SRAM Arrays at Extremely Low Temperatures | 5 nm FinFET SRAM characterization at cryogenic temperature; device/circuit physics. |
| TQE-080 | Wavelet-Based Quantum Sensing of Geomagnetic Fluctuations With Multiple NV En... | NV-ensemble geomagnetic sensing. |
| TQE-093 | Observing the Poisson Distribution of a Coherent Microwave Field With a Param... | Josephson parametric photon detector measurement physics. |
| TQE-110 | Cryo-CMOS Bias-Voltage Generation and Demultiplexing at mK Temperatures for L... | Cryo-CMOS bias generation/demultiplexing; readout-control electronics. |
| TQE-111 | Control of a Josephson Digital Phase Detector via an SFQ-Based Flux Bias Driver | SFQ flux-bias driver for Josephson phase detector; readout electronics. |
| TQE-121 | Automated Charge Transition Detection in Quantum Dot Charge Stability Diagrams | ML edge detection in charge-stability diagrams; device tuning. |
| TQE-123 | Toward Axion Signal Extraction in Semiconductor Spin Qubits via Spectral Engi... | Axion signal extraction with spin qubits; sensing. |
| TQE-126 | Amplifying Two-Mode Squeezing in Nanomechanical Resonators | Two-mode squeezing in nanomechanical resonators. |
| TQE-135 | Quasiparticle Dynamics in Niobium Nitride Superconducting Microwave Resonator... | Quasiparticle dynamics in NbN resonators. |
| TQE-138 | Modeling and Evaluating Superconducting Ferroelectric SQUID Circuits | Ferroelectric SQUID logic cell modelling; superconducting digital device design. |
| TQE-151 | Transmon Qubit Modeling and Characterization for Dark Matter Search | Transmon prototype modelling for dark-matter detection. |
| TQE-162 | A Sparse-Event Simulation Engine to Model Coincidence-Based Ranging Architect... | Simulation engine for quantum lidar ranging. |
| TQE-178 | Explaining Robust Quantum Metrology by Counting Codewords | Robust quantum metrology with code-inspired probes. |
| TQE-181 | A Low Noise Signal Read-Out Circuit for Integrated Quantum Diamond Magnetometers | Low-noise readout circuit for a diamond magnetometer. |
| TQE-196 | Impact of High-Brightness Entangled Photon Pairs on CHSH Inequality Experiment | CHSH experiment modelling with bright photon-pair sources. |
| TQE-205 | Efficient Optical Coupling of Color Center Ensembles in Diamond | Optical coupling efficiency for NV ensembles. |
| TQE-208 | Satellite Microwave Detection via Cavity-Coupled Rydberg Atomic Receiver | Cavity-coupled Rydberg atomic receiver. |
| TQE-213 | Single-Hole Spin Qubit Optimization in SOI Quantum Dots via $\boldsymbol {k}\... | k.p simulation of hole spin qubits in SOI quantum dots. |
| TQE-215 | A Novel n + / i -Well Dot Ge 1− x Sn x -on-Si Single-Photon Avalanche Photodi... | GeSn single-photon avalanche photodiode design. |
| TQE-216 | Engineering Minimal-Complexity Clifford Circuits Controlled by Microwaves via... | Phonon-mediated Clifford gates in SiV centers; device-level gate construction. |
| TQE-219 | Impact of Interface Properties on Direct Tunneling in Al/ALD-Al 2 O 3 /Al Cap... | ALD Al2O3 barriers for Josephson junctions; fabrication. |
| TQE-228 | Resource-Efficient Emulation of Majorana Zero Mode Braiding on a Superconduct... | Superconducting trijunction emulation of Majorana braiding. |
| TQE-237 | Rydberg Atom Electric Field Sensors as Linear Time-Invariant Systems | Rydberg electric-field sensors modelled as LTI systems. |
| TQE-240 | Dissipative Feedback and Hybrid Lyapunov–Reinforcement Learning Control for N... | Lyapunov/RL control for NV-center magnetometry. |
| TQE-242 | Integrated Superconducting High-Q Seamless Cavity for Quantum Memory and Qubi... | Superconducting seamless cavity for memory/readout. NO_ABSTRACT. |
| TQE-246 | Effect of Nonidealities on Nonlocal Quantum Entanglement Quality as Measured ... | Nonidealities in CHSH violation measurements. NO_ABSTRACT. |

#### Class E8 — EXTENSION: quantum optimization applications (QAOA / annealing / Grover applied to a domain problem) (29 records)

| ID | Title | Reason |
|---|---|---|
| TQE-003 | Backtesting Quantum Computing Algorithms for Portfolio Optimization | Portfolio-optimization backtesting; quantum algorithm application. |
| TQE-019 | Quantum Fuzzy Inference Engine for Particle Accelerator Control | Quantum fuzzy inference applied to accelerator control. |
| TQE-021 | Postprocessing Variationally Scheduled Quantum Algorithm for Constrained Comb... | Variational schedule + postprocessing for constrained COPs. |
| TQE-025 | Multiobjective Optimization and Network Routing With Near-Term Quantum Computers | QAOA for multiobjective network routing; optimization application. |
| TQE-027 | A Comparative Study on Solving Optimization Problems With Exponentially Fewer... | Qubit-efficient VQE encoding for MaxCut; optimizer study. |
| TQE-035 | Incentivizing Demand-Side Response Through Discount Scheduling Using Hybrid Q... | Hybrid quantum optimization for demand-side discount scheduling. |
| TQE-039 | MIMO With 1-b Pre/Postcoding Resolution: A Quantum Annealing Approach | Quantum annealing for MIMO precoding. |
| TQE-046 | Approximate Solutions of Combinatorial Problems via Quantum Relaxations | Quantum relaxations for QUBO/MaxCut approximation. |
| TQE-047 | Energy Risk Analysis With Dynamic Amplitude Estimation and Piecewise Approxim... | Approximate compiling applied to energy-derivative amplitude estimation; circuit-depth result only. |
| TQE-053 | Noise Robustness of Quantum Relaxation for Combinatorial Optimization | Noise robustness of quantum-relaxation optimizer. |
| TQE-055 | Multidisk Clutch Optimization Using Quantum Annealing | Quantum annealing for clutch-manufacturing optimization. |
| TQE-056 | Solving Nonnative Combinatorial Optimization Problems Using Hybrid Quantum–Cl... | Hybrid algorithms for nonnative combinatorial optimization. |
| TQE-092 | Utilizing Quantum Annealing in Computed Tomography Image Reconstruction | QUBO/annealing CT image reconstruction. |
| TQE-096 | Two-Dimensional Beam Selection by Multiarmed Bandit Algorithm Based on a Quan... | Quantum-walk multiarmed bandit for beam selection. |
| TQE-125 | Compressed Space Quantum Approximate Optimization Algorithm for Constrained C... | Compressed-space QAOA for constrained optimization. |
| TQE-136 | Quantum Optimization Approaches in Medical Imaging: Advances in Quantum Algor... | QUBO-based medical tomographic reconstruction. |
| TQE-159 | Black-Box Optimization of the Storage Location Assignment Problem in Logistic... | Annealing-based storage-location assignment in logistics. |
| TQE-169 | Equivariant Quantum Approximate Optimization Algorithm | Symmetry-adapted QAOA mixer design. |
| TQE-173 | A Quantum Variational Approach to Phase-Only Pattern Synthesis | QAOA for antenna phase-only pattern synthesis. |
| TQE-175 | Quantum Annealing for Robust Principal Component Analysis | Quantum annealing for robust PCA. |
| TQE-191 | Advanced Quantum Annealing for the Biobjective Traveling Thief Problem: An $\... | Quantum annealing for the biobjective traveling thief problem. |
| TQE-194 | Quantum-Assisted Optimization and Security for Trustworthy AI-Driven Healthcare | QAOA plus security layer for healthcare AI; optimization application. |
| TQE-197 | Mitigating Precision Errors in Quantum Annealing via Coefficient Reduction of... | Coefficient reduction for annealer precision limits. |
| TQE-200 | Grover Adaptive Search-Based Hybrid Benders Decomposition for Mixed-Integer L... | Grover-based Benders decomposition for MILP. |
| TQE-201 | Quantum Compressed Sensing Tomographic Reconstruction Algorithm | QUBO compressed-sensing CT reconstruction. |
| TQE-204 | Quantum Subroutines in Branch-Price-and-Cut for Vehicle Routing | Quantum heuristic subroutine inside branch-price-and-cut for vehicle routing. |
| TQE-209 | Quantum Circuit-Based Adaptation for Credit Risk Analysis | Hardware-aware variational circuits for credit-risk distributions. |
| TQE-221 | Quantum-Based Resilient Routing in Networks: Minimizing Latency Under Dual-Li... | Quantum-based optimization for resilient telecom routing. |
| TQE-232 | Matrix Low-Dimensional Qubit Casting Based Quantum Electromagnetic Transient ... | Variational linear solver for power-system electromagnetic transient simulation. |

#### Class 5 — Quantum machine learning applications (QNN/QGAN/QFL/quantum kernels on a domain task) (21 records)

| ID | Title | Reason |
|---|---|---|
| TQE-001 | Quantum Conformal Prediction for Reliable Uncertainty Quantification in Quant... | QML uncertainty quantification; no classical systems contribution. |
| TQE-011 | Network Anomaly Detection Using Quantum Neural Networks on Noisy Quantum Comp... | QNN intrusion detection application. |
| TQE-015 | A Quantum-Classical Collaborative Training Architecture Based on Quantum Stat... | Quantum deep-learning training architecture; QML application. |
| TQE-017 | Understanding Logical-Shift Error Propagation in Quanvolutional Neural Networks | Fault-injection study of quanvolutional NN reliability; QML application. |
| TQE-018 | Application of Quantum Recurrent Neural Network in Low-Resource Language Text... | Quantum RNN text classification application. |
| TQE-040 | Hybrid Quantum Cycle Generative Adversarial Network for Small Molecule Genera... | Hybrid quantum GAN for molecule generation. |
| TQE-044 | On Quantum Natural Policy Gradients | Quantum natural policy gradients for PQC reinforcement learning. |
| TQE-058 | Quantum Circuit for Imputation of Missing Data | Variational circuit for data imputation. |
| TQE-063 | Local Binary and Multiclass SVMs Trained on a Quantum Annealer | SVM training on a quantum annealer; ML application. |
| TQE-066 | HyQ2: A Hybrid Quantum Neural Network for NextG Vulnerability Detection | Hybrid QNN for 5G vulnerability detection. |
| TQE-086 | Benchmarking Quantum Machine Learning Kernel Training for Classification Tasks | Benchmarking quantum kernel training for classification. |
| TQE-104 | Computable Model-Independent Bounds for Adversarial Quantum Machine Learning | Adversarial robustness bounds for QML. |
| TQE-129 | DT-QFL: Dual-Timeline Quantum Federated Learning With Time-Symmetric Updates,... | Quantum federated learning framework. |
| TQE-134 | Neural Architecture Search Algorithms for Quantum Autoencoders | Neural architecture search for quantum autoencoders. |
| TQE-153 | Relative Entropy-Based Training of Quantum Neural Networks | Relative-entropy cost function for QNN training. |
| TQE-157 | Dual-Discriminator Hybrid Quantum Generative Adversarial Networks for Improve... | Hybrid quantum GAN with dual discriminators. |
| TQE-160 | Integrated Encoding and Quantization to Enhance Quanvolutional Neural Networks | Encoding/quantization for quanvolutional networks. |
| TQE-190 | QATNet: A Lightweight Quantum–Classical Tabular Network for Low-Latency Intru... | Hybrid quantum-classical intrusion-detection model. |
| TQE-206 | QCHFT: Quantum Cross-Hybrid Fine-Tuning for LLMs | PQC adapters for LLM fine-tuning; QML application. |
| TQE-226 | Quantum Squeeze-and-Excitation Networks: Harnessing Quantum Noise for Robust ... | Quantum squeeze-and-excitation attention networks. |
| TQE-229 | Hybrid Quantum Capsule Network: Quantum Transformation Circuit as Vote Transf... | Hybrid quantum capsule network for image classification. |

#### Class E9 — EXTENSION: VQA methodology & error mitigation (ansatz design, optimizer, expressibility, barren plateaus, ZNE/PEC/CDR) (16 records)

| ID | Title | Reason |
|---|---|---|
| TQE-022 | Mitigating Barren Plateaus of Variational Quantum Eigensolvers | Ansatz design to mitigate barren plateaus; excluded by VQE rule. |
| TQE-037 | Distributionally Robust Variational Quantum Algorithms With Shifted Noise | Robust VQA parameter optimization under shifted noise. |
| TQE-052 | Improving Probabilistic Error Cancellation in the Presence of Nonstationary N... | Probabilistic error cancellation stability; error mitigation. |
| TQE-060 | Hierarchical Quantum Architecture Search for Variational Quantum Algorithms | Hierarchical quantum architecture (ansatz) search. |
| TQE-065 | Noise-Aware Quantum Amplitude Estimation | Noise model for amplitude estimation; algorithm-level noise handling. |
| TQE-069 | Expressiveness of Commutative Quantum Circuits: A Probabilistic Approach | Expressiveness of commutative parameterized circuits. |
| TQE-073 | Dissipative Variational Quantum Algorithms for Gibbs State Preparation | Dissipative variational algorithm for Gibbs-state preparation. |
| TQE-082 | Variational Quantum Algorithms for Differential Equations on a Noisy Quantum ... | Variational circuit learning for differential equations. |
| TQE-105 | Analysis of Parameterized Quantum Circuits: On the Connection Between Express... | Expressibility vs gate types in parameterized circuits. |
| TQE-166 | Feedback-Based Quantum Algorithm for Excited States Calculation | Feedback-based variational algorithm for excited states. |
| TQE-195 | Extension of Clifford Data Regression Methods for Quantum Error Mitigation | Clifford data regression variants; error mitigation. |
| TQE-199 | Robust Design Under Uncertainty in Quantum Error Mitigation | Uncertainty quantification for error-mitigated observables. |
| TQE-211 | Extrapolating Pauli Checks for Expectation Value Estimation on Noisy Quantum ... | Pauli check extrapolation; error mitigation. |
| TQE-218 | Emergent Bifurcations in Quantum Circuit Stability From Hidden Parameter Stat... | Statistical study of circuit-compression stability; parameter statistics. |
| TQE-227 | Variational Quantum Eigensolver: A Comparative Analysis of Classical and Quan... | VQE optimizer comparison; excluded explicitly by the VQE rule. |
| TQE-235 | Efficiently Architecting VQAs: Expressibility–Trainability–Resources Pareto-O... | Ansatz design-space exploration for VQAs. |

#### Class 7 — Quantum algorithms / complexity theory (oracles, walks, bounds, resource counts with no systems mechanism) (14 records)

| ID | Title | Reason |
|---|---|---|
| TQE-008 | Relation Between Quantum Advantage in Supervised Learning and Quantum Computa... | Learning-advantage vs computational-advantage theory. |
| TQE-016 | A Stable Hash Function Based on Parity-Dependent Quantum Walks With Memory (A... | Hash function from quantum walks. |
| TQE-029 | Accelerating Grover Adaptive Search: Qubit and Gate Count Reduction Strategie... | Grover adaptive search qubit/gate-count reduction. |
| TQE-033 | Harnessing the Power of Long-Range Entanglement for Clifford Circuit Synthesis | Clifford synthesis circuit-size bounds; gate-count theory. |
| TQE-059 | Quantum Speedup of the Dispersion and Codebook Design Problems | Grover adaptive search formulations for dispersion/codebook problems. |
| TQE-067 | Fixed-Point Grover Adaptive Search for Quadratic Binary Optimization Problems | Grover oracle construction for QUBO; gate-count analysis. |
| TQE-089 | Explicit Quantum Circuit for Simulating the Advection–Diffusion–Reaction Dyna... | Carleman-linearized ADR circuit; Pauli-term resource counting. |
| TQE-091 | Two-Step Quantum Search Algorithm for Solving Traveling Salesman Problems | Grover-type search for TSP; query-complexity construction. |
| TQE-097 | Mixed Grover: A Hybrid Version to Improve Grover's Algorithm for Unstructured... | Grover iteration/trial parameterization analysis. |
| TQE-116 | A Grover-Meets-Simon Approach to Match Vector Boolean Functions | Grover-meets-Simon algorithm for Boolean matching in EDA. |
| TQE-120 | Grover Adaptive Search With Spin Variables | Grover adaptive search with spin-variable dictionary. |
| TQE-165 | A Graphical Rule Book for Clifford Manipulations of Stabilizer States | Stabilizer/graph-state formalism review and extension; quantum information theory. |
| TQE-198 | Robust Quantum Walk Search on Complete Multipartite Graph With Multiple Marke... | Quantum walk search on multipartite graphs. |
| TQE-236 | Clifford Manipulations of Stabilizer States – Application to Linear Optical Q... | Clifford/stabilizer manipulation formalism for linear optics. NO_ABSTRACT. |

#### Class E11 — EXTENSION: quantum control / pulse & gate design / calibration / quantum feedback control theory (7 records)

| ID | Title | Reason |
|---|---|---|
| TQE-009 | State Preparation on Quantum Computers via Quantum Steering | State preparation via dissipative steering; circuit/control protocol. |
| TQE-112 | SU(4) Gate Design via Unitary Process Tomography: Its Application to Cross-Re... | Pulse-efficient SU(4) gate design and calibration. |
| TQE-124 | Realization and Calibration of Continuously Parameterized Two-Qubit Gates on ... | Calibration of parameterized two-qubit gates on a trapped-ion testbed. |
| TQE-128 | Fast State Stabilization Using Deep Reinforcement Learning for Measurement-Ba... | Deep RL for measurement-based quantum feedback control. |
| TQE-155 | Optimal Control-Assisted Rapid Quantum State Transfer on 1-D Spin Chain | Optimal-control state transfer on a spin chain. |
| TQE-158 | Robust $H_{\infty }$ Uncertainties-Tolerant Observer-Based Reference Quantum ... | Robust H-infinity quantum trajectory tracking control. |
| TQE-185 | Measurement-Informed Safe Reinforcement Learning for Quantum Battery Charging... | Safe RL control for quantum battery charging. |

#### Class E10 — EXTENSION: QEC code & protocol theory (new codes, thresholds, syndrome-extraction circuit design) (5 records)

| ID | Title | Reason |
|---|---|---|
| TQE-084 | Engineering Quantum Error Correction Codes Using Evolutionary Algorithms | Evolutionary search for stabilizer codes; code discovery. |
| TQE-148 | Erasure-Tolerance Scheme for the Surface Codes on Neutral Atom Quantum Computers | Erasure-tolerance atom-reloading scheme for surface codes. |
| TQE-184 | Encoder Circuit Optimization for Nonbinary Quantum Error Correction Codes in ... | Encoder circuit construction for qudit QEC codes; gate-count result. |
| TQE-188 | Synchronizable Hybrid Subsystem Codes | Synchronizable hybrid subsystem code constructions. |
| TQE-210 | Unified and Generalized Approach to Entanglement-Assisted Quantum Error Corre... | Unified entanglement-assisted QEC framework; code theory. |

#### Class E12 — EXTENSION: quantum information theory (channel capacity, state discrimination, tomography statistics) (4 records)

| ID | Title | Reason |
|---|---|---|
| TQE-028 | Variational Estimation of Optimal Signal States for Quantum Channels | Optimal signal-state estimation for quantum channels. |
| TQE-146 | Quantum Detection Over Quantum Channels With Uncertainty | Measurement design for quantum state discrimination. |
| TQE-168 | Optimal Allocation of Pauli Measurements for Low-Rank Quantum State Tomography | Pauli measurement allocation for state tomography; sample complexity. |
| TQE-174 | Information-Theoretic Analysis of Bayesian Quantum State Search | Bayesian quantum state search / classification. |

#### Class 1 — Post-quantum cryptography (lattice/SVP/ECDLP/Shor-for-crypto, PQC side channels) (4 records)

| ID | Title | Reason |
|---|---|---|
| TQE-070 | Grover's Oracle for the Shortest Vector Problem and Its Application in Hybrid... | Grover oracle for the shortest vector problem; post-quantum cryptanalysis. |
| TQE-113 | Quantum Resource Estimates for Computing Binary Elliptic Curve Discrete Logar... | Resource estimates for elliptic-curve discrete logs; cryptanalysis counting. |
| TQE-115 | Simulation of Shor Algorithm for Discrete Logarithm Problems With Comprehensi... | Shor DLP circuit simulation for cryptographic parameter pairs. |
| TQE-139 | Heuristic Time Complexity of NISQ Shortest-Vector-Problem Solvers | QAOA heuristics for the shortest vector problem; lattice cryptanalysis. |

#### Class 3 — Classical quantum chemistry / many-body / field-theory simulation as the result (1 records)

| ID | Title | Reason |
|---|---|---|
| TQE-023 | Simulating Quantum Field Theories on Gate-Based Quantum Computers | Quantum field theory simulation result on hardware. |

#### Class 2 — Quantum-inspired classical methods (Ising machines, QUBO solvers run classically) (1 records)

| ID | Title | Reason |
|---|---|---|
| TQE-180 | Accelerating the Max-Cut Problems via Distributed Ising Machine Solvers | Distributed Ising-machine Max-Cut solver; quantum-inspired hardware. |

## 6. Census-policy judgement for TQE

**Verdict: SELECTIVE_CENSUS.**

TQE is not a low-yield venue — 25 included plus 37 borderline records over three years is a real, sustained
stream, and it contains several papers that no general HPC venue would carry (FPGA distributed surface-code decoding,
an in-cryostat SFQ coprocessor, trapped-ion circuit packing for multi-tenant devices, decision-diagram simulation
across nodes, a hybrid serverless platform model). But 74.4% of the venue is out of scope, and
the out-of-scope share is stable year to year (78%, 69%, 77%), so a full census every year spends most of its effort
on records that will be excluded again. Selective tracking is the right trade.

### How far TQE should be tracked in future

Track these sub-areas in full, by topic rather than by section heading (TQE's article set is not organised into
headings that align with this corpus):

1. **Classical simulation of quantum circuits at scale** — state-vector, decision-diagram and tensor-network
   simulators, gate fusion, multinode/GPU parallelization, variable ordering. (TQE-013, TQE-167, TQE-223.)
2. **QEC classical processing** — parallel, FPGA/ASIC or scheduled decoders, syndrome bandwidth and compression,
   controller benchmarks for decode-dependent feed-forward. (TQE-062, TQE-130.) Decoder-algorithm-only papers stay
   BORDERLINE and need only a title-level pass.
3. **Compilation cost and scalability** — compiler inner-loop cost, compile-time versus quality, architecture-aware
   mapping/routing/scheduling, compiler benchmarking. (TQE-142, TQE-214, TQE-078, TQE-048, TQE-090.)
4. **Circuit cutting and distributed execution** — cut selection cost, reconstruction cost, fragment and shot
   orchestration, multi-QPU partitioning. (TQE-207, TQE-193, TQE-143; TQE-007 is the same shape but falls before
   the window.)
5. **Multi-QPU / modular quantum computing architecture** — collective operations, network-based FTQC, module
   sizing. (TQE-137, TQE-238; TQE-163 borderline.) Watch the boundary here: module-sizing papers whose optimized
   quantity is an entanglement rate belong to the quantum-networking class, not to this corpus.
6. **QPU resource management and runtime** — multiprogramming/packing, scheduling, serverless and cloud execution
   models, QoS. (TQE-150, TQE-101.)
7. **Classical control-plane systems work with a stated latency, memory, bandwidth or thermal budget** — FPGA
   control architectures, in-cryostat processing, ML readout firmware. (TQE-038, TQE-075, TQE-127; TQE-108
   borderline.) This is the sub-area with the worst signal-to-noise: it sits next to a large cryo-electronics and
   device-physics population that must be rejected on the same keywords, and a paper here earns inclusion only when
   a systems-level result — not just a memory or power motivation — is actually established.

Do **not** census these parts of TQE at all; they account for almost the entire excluded set and reliably fail the
gates: quantum networking, QKD, repeaters, entanglement routing and distribution (49 records); sensing, metrology,
device and materials physics, cryo readout electronics (32); quantum optimization and annealing applications (29);
QML applications (21); VQA methodology and error mitigation (16); quantum algorithms, complexity and code theory (23).

Practical cadence: screen TQE titles quarterly against the seven sub-areas above and read abstracts only for hits;
a full-population pass of this kind is worth repeating once every three years to recalibrate, not annually. The two
surveys flagged BIBLIOGRAPHY_HUB (TQE-172 on superconducting control and readout architectures, TQE-217 on quantum
computing for computational sciences) are worth keeping as entry points into the control-hardware and
application-projection literatures respectively.

### OPEN_QUESTIONs for this venue

- Q_IN_HPC is UNDERREPRESENTED_IN_THIS_CORPUS at TQE: only 5 scenario tags
  across 62 retained records, essentially TQE-101, TQE-150, TQE-171, TQE-193 and TQE-144. Work on QPUs inside
  HPC centres is evidently published elsewhere.
- GPU-based simulation is absent from the retained set: the simulation papers here are decision-diagram and
  state-vector work on CPUs and clusters. POSSIBLE_CROSSOVER with SC/IPDPS-style venues.
- TQE-143 needs full-text retrieval before it can be analysed; its verdict currently rests on the title alone.
- Early Access dates would change window placement for more records than TQE-007 if they were available; under
  YEAR_BASIS=ISSUE some 2024 records were first public in late 2023.

## 7. OUT_OF_WINDOW records (1)

Assessed and then found to fall outside the 2024-2026 census window. The assessment is retained for audit; these
records count toward no per-year total.

### TQE-007 — Optimal Partitioning of Quantum Circuits Using Gate Cuts and Wire Cuts

- **DOI:** 10.1109/tqe.2023.3347106 · **Census year:** 2024 · **v5**, pp. 1-10
- **Lead author:** Sebastian Brandhofer (+2 co-authors) · **arXiv:** 2308.09567
- **Article type:** ORIGINAL_RESEARCH
- **Verdict:** OUT_OF_WINDOW · **Scenario:** HPC_FOR_Q · **Branch:** circuit_cutting_reconstruction, compiler_mapping_routing
- **Deep-dive priority:** MEDIUM · **Conference extension:** UNKNOWN
- **Artifact:** UNKNOWN
- **Abstract status:** TRUNCATED_700_CHARS
- **Out-of-window reason:** First public availability 2023-12-26 (IEEE Early Access); volume 5 cover year 2024 was used in error

**Gate 1 — classical systems problem.** Sampling and classical postprocessing cost that grows exponentially with the number of cuts.

**Gate 2 — HPC/systems technique in the contribution.** Exact optimization over cut placements and cut realizations, i.e. a partitioning cost model for fragmented execution.

**Gate 3 — bearing on heterogeneous CPU/GPU/HPC to QPU computing.** Quantifies what the classical side pays when a circuit exceeds a single QPU. Assessment retained for audit; the record is outside the 2024-2026 window.

**Notes.** Moved out of the census window during adversarial verification. The gate assessment is retained for audit; the record does not count toward any 2024-2026 total.

**Research question.** Where should a quantum circuit be cut, and with which cut realization, so that the combined quantum plus classical postprocessing cost of partitioned execution is minimized?

**Quantum problem.** Limited qubit count, connectivity and fidelity force a large circuit to be split into smaller executable fragments.

**Classical / HPC problem.** Partitioning increases the total sampling/postprocessing work exponentially in the partitioning effort, so cut placement is a classical cost-optimization problem.

**Mechanism.** Formulates optimal selection of gate cuts and wire cuts as an exact optimization over cut locations and cut realizations, jointly accounting for the sampling overhead each cut adds.

**Computational bottleneck.** Exponential growth of sampling/reconstruction overhead with the number of cuts; search space of cut placements.

**Evaluation platform.** INSUFFICIENT_EVIDENCE

**Scale.** INSUFFICIENT_EVIDENCE

**Performance metrics.** Reduction in required sampling overhead versus heuristic cut selection; exact numbers not recoverable from the truncated abstract (BASELINE_UNCLEAR).

**Major claim.** An exact partitioning method that selects cut points and cut realizations jointly reduces the sampling overhead relative to prior partitioning heuristics.

**Limitation.** Exact optimization itself scales poorly with circuit size; overhead remains exponential in cut count.

**Relevance.** Circuit cutting is the main route to running oversized circuits on small QPUs, and its cost is borne by classical postprocessing — directly a CPU/GPU-side workload.


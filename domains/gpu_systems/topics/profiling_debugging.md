# Profiling, debugging, correctness, simulation and performance modelling (taxonomy N)

last_updated: 2026-09-19
last_checked: 2026-09-19
knowledge_as_of: 2026-09-18 (GPU corpus pass over SC/ICS/IPDPS/ISC/PPoPP/ASPLOS/ISCA/MICRO/HPCA/HPDC 2024–2026)

Coverage status: **GOOD, and unusually rich in verified non-citations.**
Five deep analyses (taxonomy `N`), all `CORE_GPU`. Verdict ledger:
`../corpus/_LEDGER_profiling_reliability.md` (shared with
`reliability_operations.md`, taxonomy `O`).

## 1. Problem landscape

The topic divides by what is being made visible. **Correctness tools** ask
whether a program's synchronisation is right — and the corpus holds a tool for
too *little* synchronisation and a tool for too *much*, which turn out to be
exact duals that do not cite each other. **Profilers** ask where a stall came
from, and split on a single engineering bet: instrument the ISA, or instrument
the source. **Simulators** ask how to make a GPU study affordable, and the
corpus's two papers reduce different costs and have never been composed.

Underneath all three sits a measurement hazard the reliability half of this
ledger establishes independently: **a software-stack change can move a GPU
counter by orders of magnitude** (see `reliability_operations.md` §7).

## 2. Key concepts

Data race vs over-synchronisation; the CUDA scope lattice (CTA / GPU / system)
and `__threadfence` variants; state-machine race detection with constant-width
metadata vs vector clocks; **NVBit (SASS-level binary instrumentation) vs Clang
source rewriting** as the two instrumentation routes; backward slicing over a
stall to its cause; per-vendor stall encodings (`s_waitcnt` on AMD, B1–B6
barrier bits on NVIDIA, SBID tokens on Intel); sampled simulation (which kernel
invocations to simulate) vs scale-model simulation (how large a machine to
simulate); MAPE as simulator fidelity.

## 3. Main mechanism families

**Family N1 — dynamic correctness checking.**
`../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md` (under-synchronisation)
and `../corpus/GPU-MICRO24-41--over-synchronization-in-gpu-programs.md`
(ScopeAdvice, over-synchronisation). Exact duals.

**Family N2 — stall attribution by backward slicing.**
`../corpus/GPU-SC26-41--leo-cross-vendor-gpu-stall-backward-slicing.md`.

**Family N3 — reduce how many kernel invocations you simulate.**
`../corpus/GPU-MICRO25-01--stem-root-sampled-gpu-simulation.md`.

**Family N4 — reduce how large a machine you simulate.**
`../corpus/GPU-HPCA24-41--gpu-scale-model-simulation.md`.

## 4. Representative papers

- **HiRace** (SC 2024) — **MEASURED**. Three separable reasons it beats
  IGUARD: **constant-width 64-bit metadata** (no access-record table, no
  eviction policy, no associative search); **one flat-array table lookup**
  instead of a vector-clock comparison loop; and **Clang source rewriting**, so
  the injected code is compiled and optimised *with* the kernel by `nvcc`
  `[paper]`. It rejects NVBit explicitly, citing its deprecation and its
  incompatibility "with NVIDIA architectures released since [IGUARD's]
  publication". Achieves **~3× average and 7.5× broad-evaluation slowdown**.
  Against `compute-sanitizer racecheck` the comparison is scope, not speed:
  racecheck found **92 of 346 injected races at every input size**, because it
  only inspects block-shared memory and **global-memory races are structurally
  invisible to it** `[paper]`.
- **ScopeAdvice / Over-Synchronization in GPU Programs** (MICRO 2024) —
  **MEASURED** on an **RTX 3090, CUDA 11.2**. Speedups after removing
  over-synchronisations, with the stall-cycle attribution that makes them
  causal rather than anecdotal `[paper]`: synthetic matrix multiply **54%**
  (fence stall cycles 4.4 → 0.13); synthetic stencil **50%** (2.8 → 0); and
  **cuML, a real library, 37%** (24.8 → 14.5). Instruments SASS through
  **NVBit** and measures that **NVBit alone contributes ~64% of a 29–522×
  slowdown** `[paper]`.
- **LEO** (SC 2026 attribution uncorroborated — see §8) — **MEASURED** on
  **GH200, MI300A and Intel PVC**, 21 workloads. Post-mortem, so **no runtime
  overhead of its own**; measurement overhead **~10% on AMD** at HPCToolkit's
  default sampling frequency and **~10% on Intel** at the shortest recommended
  100 µs period, while **NVIDIA overhead is not given as a percentage** —
  instead the authors flag that "NVIDIA's Activity API serializes kernel
  execution, potentially distorting measurement" `[paper]`. Analysis time
  **3–10 s per kernel on one CPU core**, but **NVIDIA tensor-core kernels with
  >8,000 edges took about 60 s** — dense tensor-core code is the scaling weak
  point. **Read the speedup carefully**: geometric means of **1.73× (GH200),
  1.74× (MI300A), 1.82× (PVC)** are reported, and the authors state that
  "speedup evaluation uses expert-designed optimizations informed by LEO
  analysis" `[paper]` — **the number measures a human-plus-tool loop, not the
  tool.**
- **Scale-Model Simulation** (HPCA 2024) — **SIMULATED** only; **no real GPU is
  used**, the target is a synthetic 128-SM configuration with 34 MB LLC and
  2.3 TB/s DRAM `[paper]`. Predicting a 128-SM target from 8-SM and 16-SM scale
  models, strong scaling: **4% average / 17% max error**, against **12% / 55%**
  for power-law regression and **17% / 68%** for linear regression `[paper]`.
  Its binding dependence is **per-SM architecture, not size** — a target with a
  different per-SM architecture requires new scale models, so the method
  extrapolates across *size within a generation* and **never across
  generations**.
- **STEM + ROOT** (MICRO 2025) — **SIM + MEAS**: profiling on **RTX 2080, H100,
  H200**, simulation in **MacSim** `[paper]`. Rodinia: **STEM 3.00× at 0.93%
  error** vs **Photon 2.84× at 2.71%**; CASIO: **STEM 109.60× at 0.36%**. The
  dependence is asymmetric and unusual: largely independent of the *simulated*
  architecture (DSE sweeps hold ~2% error) but dependent on the *profiled* one
  (**H100→H200 transfer costs 5.46% error**), because the clustering encodes
  the profiled silicon's microarchitecture.

## 5. Historical lineage

Verified from the papers' own citations
(`../corpus/_LEDGER_profiling_reliability.md` §5); wider chains in
`../synthesis/GPU_TOPIC_LINEAGES.md`.

- **GPA (GPU Performance Advisor) is the hub of the GPU performance-advisory
  literature**, confirmed from two independent citing papers. LEO names GPA as
  the work that "pioneered backward slicing for GPUs, but GPA supports only
  NVIDIA GPUs and cannot trace memory access dependencies through
  synchronization instructions such as AMD's `s_waitcnt`" `[paper, LEO]`;
  ScopeAdvice independently lists GPA among the instruction-level profiling
  tools it complements `[paper, ScopeAdvice]`. A 2024 synchronisation-scope
  tool and a 2026 cross-vendor stall slicer converge on the same ancestor.
- **The race-detection baseline set** — iGUARD (27–649× overhead), BARRACUDA
  (~3700×), ScoRD, `compute-sanitizer racecheck` — is cited by both HiRace and
  ScopeAdvice, with **mutually consistent characterisations of iGUARD**
  (27–649× vs ">30× average with outliers to ~1000×"), which strengthens both.
- **The sampling art** — Principal Kernel Analysis, TBPoint, Photon — is named
  by **both** simulation papers `[paper, both]`: a verified shared literature.
- **A stated cross-corpus link**: the ICS 2025 portability study
  (`../corpus/GPU-ICS25-145--taking-gpu-programming-models-to-task-performance-portability.md`)
  concludes "line-level stall attribution is a crucial capability missing from
  Omniperf" — and LEO builds exactly that. **ICS 2025 states the tooling gap;
  SC 2026 fills it.** This rests on the papers' own text.

## 6. Implementation families

`DYNAMIC_INSTRUMENTATION`, splitting by route: **NVBit/SASS** (ScopeAdvice) vs
**Clang source rewriting** (HiRace) vs **per-vendor ISA decoders plus
`nvdisasm`/`llvm-objdump`/GED** (LEO). `SIMULATOR`: Scale-Model Simulation
(Accel-Sim), STEM+ROOT (MacSim, profiled on real silicon). Note that
`../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md` — filed
under `gpu_core_execution.md` — is the corpus's other simulator-fidelity result
and reports **34.03% MAPE for the Accel-Sim baseline against a real RTX
A6000**; any simulation result in this topic should be read next to it.

## 7. Important disagreements / tensions

**T1 — a verified non-citation between exact duals.** HiRace (SC 2024) and
ScopeAdvice (MICRO 2024) "analyse the same programs over the same CUDA scope
lattice and cite the same baselines", and **neither cites the other**:
**HiRace is absent from ScopeAdvice's related-work list**, and HiRace's related
work does not mention over-synchronisation `[paper, both]`. The ledger calls
this "the clearest citation-level finding in this cluster".

**T2 — two quantified, opposite bets on instrumentation, and neither paper
cites the other.** ScopeAdvice measures that **NVBit alone contributes ~64% of
its 29–522× slowdown** `[paper]`; HiRace rejects NVBit for Clang source
rewriting on deprecation and architecture-compatibility grounds and reaches
**~3× average** `[paper]`. LEO takes the ISA route further still, buying
cross-vendor reach at the cost of permanent per-architecture maintenance.
**The 64% figure is direct quantitative support for HiRace's choice, and
neither paper knows it.**

**T3 — the simulation-cost literature partitions cleanly and the two halves
have never been composed.** STEM+ROOT reduces *how many kernel invocations* are
simulated (3× to 31,719× depending on kernel-call multiplicity); Scale-Model
Simulation reduces *how large a machine* is simulated (9.3×, and it is the only
method that works when **no model of the target exists at all**). Neither paper
mentions composing them, and nothing in either design forbids it.
**A second caution: STEM+ROOT's headline is bounded error, not speed** —
Photon is **1.54× faster on the CASIO suite at 9.85% error** against STEM's
**0.36%** `[paper]`, so the 31,719× figure is meaningless without its error
column.

**T4 — a tool's reported speedup may be a human's.** LEO's 1.73×/1.74×/1.82×
geomeans come from "expert-designed optimizations informed by LEO analysis"
`[paper]`. Recorded as stated, not converted into a claim about the tool.

**T5 — cross-vendor profiling is asymmetric by vendor policy, not by tool
design.** LEO can quote an overhead percentage for AMD and Intel but not for
NVIDIA, because NVIDIA's Activity API serialises kernel execution `[paper]`.
That asymmetry propagates into every cross-vendor profiling comparison in this
corpus.

## 8. Current limitations

**Access, and one specific rate-limit.** `dl.acm.org` → 403,
`ieeexplore.ieee.org` → 418, `dblp.org` robots-blocked — so several formally
open-access papers are `CLOSED_ACCESS` *as determined here*; that is an
access-path limitation, not a claim about licence
(`../synthesis/GPU_PENDING_FULLTEXT.md`). Specifically:
- **arXiv `2609.07912`** (the SC 2026 PyKokkos debugger, *pkdb*) **returned
  HTTP 429 on eight attempts** across `/abs/`, `/pdf/`, `/html/v1` and
  `/html/v2`, spread over the session with pauses, while other arXiv IDs
  fetched normally — so this is specific to that identifier. `PENDING_FULLTEXT`;
  **retry from a different network path.** Its mechanism was recovered from
  source only, and its SC 2026 attribution rests on `[README]` evidence
  ("Artifact for SC'26").
- **GCStack+GCScaler** (ISCA 2025) is `PUBLIC_ARTIFACT_ONLY`; its full stall
  taxonomy was recovered from source, **and the paper may not be
  deep-analysed** under the gate.
- **LEO's venue is unverified.** It was analysed as `GPU-SC26-41` on public
  full text, but **the census records `NOT_FOUND` in every official SC26 source
  and the arXiv record carries no venue comment**. It is treated here as a
  **preprint**; the SC 2026 attribution in the task assignment is
  uncorroborated. Any venue-level claim built on LEO must carry that caveat.
- **Existence unverified, do not carry forward as real papers**: *GPU Faults
  Across Cloud Providers* (SC 2026 seed, census `NOT_FOUND`) and *SigmaTrace*
  (SC 2026 seed, `NOT_FOUND`, not even a full title).

**Bounded by the corpus's own scope, not by access:** debugging proper is one
unread paper (*pkdb*). Nothing here supports a general statement about
interactive GPU debuggers.

**Nine rows carry `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`** for the pending
`../../ai_hpc_systems/` corpus, whose declared scope explicitly includes
"performance analysis" — among them TrioSim, AMALI, DeepContext and
*Forecasting GPU Performance for Deep Learning*. **Nothing about that corpus's
content may be asserted**, including venues, counts or coverage
(`../synthesis/GPU_EXISTING_CORPUS_OVERLAP.md`).

## 9. Research questions

`INFERENCE`, from §7, none falsified against the corpus:

1. Compose T3's two halves: sample kernels *and* shrink the machine. Neither
   paper forbids it and neither tries it.
2. Is HiRace sound against the consistency model formalised in
   `../corpus/GPU-ASPLOS24-142--towards-unified-analysis-gpu-consistency.md`?
   ScopeAdvice's advice to *weaken* a scope is only sound with respect to such
   a model, and that dependency is unexercised in this corpus.
3. What would an over-synchronisation detector cost on the Clang route
   (T2)? The two design bets have never been run on the same substrate.

## 10. Deeper lookup paths

`../corpus/_LEDGER_profiling_reliability.md` — §2 the six verdict-only
sub-theme tables, §4 the prior-corpus deduplication record, **§5 the seven
cross-paper findings**, §6 the watchlist and the existence-unverified list →
the five analyses above → the papers and their artifacts.
Cross-topic: `reliability_operations.md` (the `O` half of the same ledger, and
the counter-stability hazard), `gpu_core_execution.md` (simulator fidelity
against real silicon), `compiler_programming.md` (the ICS 2025 → LEO link and
the static half of GPU correctness).

# SOURCE_INVENTORY — `hpc_quantum`

**Generated:** 2026-09-07 (UTC) · **Method:** direct filesystem walk of the live Cowork workspace. Every number below was computed by `find`/`stat`/`grep` at staging time. **No count was copied from a previous session's report.**

---

## 1. Source workspace

| Field | Value |
|---|---|
| Source host | Anthropic Cowork cloud container (session `01PdeUA4U6NSdQBt7n9Ywicg`) |
| Primary source path | `/home/claude/quantum-hpc/` |
| Secondary source path | `/tmp/claude-0/-home-claude/e70d0282-821c-5eba-9007-2a27ddc0bcd8/scratchpad/` (session scratch — raw evidence extracts) |
| Git repository? | **NO.** `find /home/claude -maxdepth 4 -name .git -type d` returns nothing. The corpus is a plain file set. |
| Branch / HEAD / commit count | `N/A — NOT_GIT_MANAGED` |
| Working-tree status | `N/A — NOT_GIT_MANAGED` |
| Git bundle | **Not created.** Per instruction 6, no repository was fabricated for a non-repository source. |
| Total files staged | **39** |
| Total bytes staged | **1,088,129** |

### 1.1 Major directories in source

| Source directory | Files | Bytes | Nature |
|---|---|---|---|
| `/home/claude/quantum-hpc/` (root) | 5 | 468,424 | Primary research deliverables |
| `/home/claude/quantum-hpc/data/asplos/` | 5 | 257,203 | ASPLOS catalogs + per-branch deep-dives |
| `/home/claude/quantum-hpc/data/` | 1 | 9,947 | SC24 program table |
| scratchpad (loose files) | 23 | ~236 KB | Raw Crossref/program extracts, patch scripts, pre-verification backup |
| scratchpad `asplos/`, `sc25/` | 5 | ~57 KB | Author lists, volume lists, artifact spot-check extracts |

### 1.2 Material deliberately NOT staged — recorded, not copied

**Nine upstream third-party Git clones (~800 MB)** were made in the session scratch for artifact verification. They are public upstream code, not 김민식's research output, and are fully reproducible from the identities below. **Excluding them is a packaging decision, not a content decision; no research file was excluded.**

| Scratch dir | Upstream remote | HEAD |
|---|---|---|
| `parallax` | `https://github.com/positivetechnologylab/Parallax.git` | `2b52b52c2c81` |
| `cudaq` | `https://github.com/NVIDIA/cuda-quantum.git` | `f907bc6b7369` |
| `atlas` | `https://github.com/quantum-compiler/atlas.git` | `93f3d6550d9d` |
| `atlas-artifact` | `https://github.com/quantum-compiler/atlas-artifact.git` | `dd1b6863876a` |
| `quartz` | `https://github.com/quantum-compiler/quartz.git` | `c4abf876608b` |
| `qmlctn` | `https://github.com/PabloAndresCQ/qml-cutensornet.git` | `92119ea19b9c` |
| `qonductor` | `https://github.com/manosgior/Qonductor-SC25.git` | `5d1ac8a90cd5` |
| `qft` | `https://github.com/XiangyuG/qft_on_regular_architectures.git` | `5c01a0e51399` |
| `qdockbank` | `https://github.com/qiqi-xingyi/QDockBank_.git` | `d056c6dcfe04` |

Two directories in scratch, `qec/` and `papers/`, were **empty** and are recorded as such.

---

## 2. File classification — all 39 staged files

Classification is by document role as observed in the files themselves. A single file may serve two roles; it is listed under its dominant role and cross-noted.

| Role (instruction 8 category) | Count | Files |
|---|---|---|
| **Synthesis documents** | 2 | `QUANTUM_HPC_VENUE_MAP.md` (129,856 B — 21-venue landscape), `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md` (16,172 B — QEC/simulation/compilation lineages) |
| **Literature / paper-analysis files** | 5 | `SC_2024_2025_QUANTUM_HPC_CENSUS.md`, `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`, `data/asplos/qec_deepdive.md`, `data/asplos/arch_sim_deepdive.md`, `data/asplos/compilation_deepdive.md` |
| **Topic-level analyses** | *(embedded, no standalone file)* | Branch-level taxonomies live inside the two censuses (§6–§9) and the three deep-dives. `NOT_PRESENT_IN_SOURCE` as separate documents. |
| **Evidence / provenance documents** | 2 + 23 | `data/asplos/VOLUME_STRUCTURE.md`, `data/asplos/CORPUS.md`; plus 23 raw extracts under `working-evidence/` |
| **Research-gap / novelty documents** | *(embedded, no standalone file)* | Gap vocabulary is used **inside** the censuses and venue map — `VENUE_GAP` ×13, `POSSIBLE_CROSSOVER` ×8, `OPEN_QUESTION` ×7, `INSUFFICIENT_EVIDENCE` ×20. There is **no standalone gap/novelty file**. |
| **Implementation / code documents** | 0 | `NOT_PRESENT_IN_SOURCE` — the corpus analyses others' code but contains no implementation of its own. |
| **Data / catalog files** | 3 | `data/sc24_main.tsv` (SC24 program table), `data/asplos/CORPUS.md` (36-paper table), `working-evidence/asplos/vols.txt` |
| **Scripts** | 3 | `working-evidence/patch1.py`, `patch2.py`, `patch3.py` — the verification-correction patches applied to the ASPLOS census |
| **Context / handoff files** | 1 | `QUANTUM_HPC_RESEARCH_QUEUE.md` (21-venue queue, waves, per-venue census mechanics) |

---

## 3. Research coverage actually present — measured, not assumed

**What this corpus actually is:** a **conference-venue census and research-landscape map for Quantum-HPC *systems* research** (which venues accept what as an HPC contribution). It is **not** a VQE or quantum-chemistry literature review. The topic list in the staging brief is therefore mostly `NOT_PRESENT_IN_SOURCE` — which means *absent from this workspace*, never *absent from the literature*.

| Topic (as listed in the brief) | Status | Evidence found |
|---|---|---|
| VQE / variational algorithms | `PARTIAL_IN_SOURCE` | 37 occurrences across 5 files — as **census subject matter** (papers classified as variational: TreeVQA, Clapton, VarSaw, Red-QAOA, Elivagar) and as taxonomy branch names. No VQE-methods review. |
| ansatz | `PARTIAL_IN_SOURCE` | 6 occurrences — taxonomy entries and per-paper descriptions only. |
| UCC / UCCSD | `PARTIAL_IN_SOURCE` | 5 occurrences, 4 of them inside `arch_sim_deepdive.md` as one paper's **benchmark description** (H₂/LiH/BeH₂ under SPSA/COBYLA with UCCSD), 1 in the venue map (ICCD "MOSQ" line). Not a researched topic. |
| ADAPT-VQE | `PARTIAL_IN_SOURCE` | **Exactly 1 mention**, `arch_sim_deepdive.md:544`, listed as a competing technique inside one paper's related work. |
| measurement reduction | `PARTIAL_IN_SOURCE` | **Exactly 1 mention**, `arch_sim_deepdive.md:545`, same context. |
| quantum chemistry | `PRESENT_IN_SOURCE` **as an exclusion criterion** | Classical quantum chemistry / many-body / DFT / NNQS is the **dominant false-positive class** and is documented as such (SC census Appendix A.1, venue map §, research queue §). It is *excluded* from the corpus, not surveyed by it. |
| optimization (classical optimizer study) | `NOT_PRESENT_IN_SOURCE` | — |
| initialization / warm-start | `NOT_PRESENT_IN_SOURCE` | 0 occurrences. |
| barren plateaus / trainability | `NOT_PRESENT_IN_SOURCE` | 0 occurrences. |
| gradient estimation | `NOT_PRESENT_IN_SOURCE` | All "gradient" hits are **conjugate-gradient classical solvers** in program tables — unrelated. |
| noise / error mitigation | `PRESENT_IN_SOURCE` | 28 occurrences across 6 files — a named corpus branch (Clapton, VarSaw, QuFEM). |
| excited states | `NOT_PRESENT_IN_SOURCE` | 1 occurrence, and it is a **false-positive exclusion example** (a GW excited-state HPC paper excluded as classical chemistry). |
| hybrid classical-quantum cost | `PRESENT_IN_SOURCE` | Central to both censuses — SC's four acceptance pathways, the ASPLOS-vs-SC compilation-currency comparison. |
| HPC acceleration | `PRESENT_IN_SOURCE` | GPU 259 hits, MPI 466 hits across all 10 markdown files. |
| quantum simulation | `PRESENT_IN_SOURCE` | 305 hits; a named branch with a dedicated deep-dive (`arch_sim_deepdive.md`). |
| QEC decoding | `PRESENT_IN_SOURCE` *(not in the brief's list, but the densest branch)* | 229 hits; dedicated deep-dive + lineage document. |
| QPU scheduling / resource management | `PRESENT_IN_SOURCE` | 117 hits; RESCQ, Qonductor, AlphaSyndrome. |
| distributed quantum simulation | `PRESENT_IN_SOURCE` | Named branch (Atlas, Parallax, BQSim, COMPAS). |
| quantum workflow systems | `PARTIAL_IN_SOURCE` | Orchestration 42 hits, concentrated in the SC census (first main-track QPU orchestration paper). |
| benchmarking / performance | `PRESENT_IN_SOURCE` | Artifact/reproducibility matrix in both censuses (302 "artifact" hits). |
| classical cost of quantum algorithms | `PRESENT_IN_SOURCE` | The compilation-cost comparison is the sharpest single result in the ASPLOS census. |

---

## 4. Evidence-tag inventory — preserved exactly as found

Evidence grading vocabulary present in the corpus. **No tag was promoted during staging.**

| Tag | Occurrences |
|---|---|
| `[inference]` | 117 |
| `[paper]` | 86 |
| `[official-CFP]` | 77 |
| `[paper-preprint]` | 72 |
| `[official-program]` | 71 |
| `[proceedings]` | 70 |
| `[code]` | 45 |
| `[abstract]` | 25 |
| `[documentation]` | 21 |
| `[artifact]` | 8 |
| `[reconstruction]` | 2 |

Uncertainty markers also preserved verbatim: `STATUS_UNCLEAR` ×16, `TOTAL_COUNT_UNVERIFIED` ×10, `NOT_FOUND` ×114.

---

## 5. Complete staged file table

| # | Path (relative to `original/`) | Bytes | Source mtime (UTC) |
|---|---|---|---|
| 1 | `quantum-hpc/ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` | 95,223 | 2026-09-06 14:41 |
| 2 | `quantum-hpc/QUANTUM_HPC_ARCHITECTURE_LINEAGES.md` | 16,172 | 2026-09-06 14:40 |
| 3 | `quantum-hpc/QUANTUM_HPC_RESEARCH_QUEUE.md` | 27,409 | 2026-09-06 14:42 |
| 4 | `quantum-hpc/QUANTUM_HPC_VENUE_MAP.md` | 129,856 | 2026-09-06 14:42 |
| 5 | `quantum-hpc/SC_2024_2025_QUANTUM_HPC_CENSUS.md` | 199,764 | 2026-09-06 14:43 |
| 6 | `quantum-hpc/data/asplos/CORPUS.md` | 4,452 | 2026-09-06 14:41 |
| 7 | `quantum-hpc/data/asplos/VOLUME_STRUCTURE.md` | 2,551 | 2026-09-06 14:41 |
| 8 | `quantum-hpc/data/asplos/arch_sim_deepdive.md` | 99,222 | 2026-09-06 13:53 |
| 9 | `quantum-hpc/data/asplos/compilation_deepdive.md` | 83,946 | 2026-09-06 13:53 |
| 10 | `quantum-hpc/data/asplos/qec_deepdive.md` | 67,032 | 2026-09-06 13:28 |
| 11 | `quantum-hpc/data/sc24_main.tsv` | 9,947 | 2026-09-06 06:51 |
| 12 | `working-evidence/CENSUS.pre-verification.bak` | 82,935 | 2026-09-06 14:37 |
| 13 | `working-evidence/all.txt` | 53,444 | 2026-09-06 06:56 |
| 14 | `working-evidence/asplos/authors.txt` | 7,493 | 2026-09-06 13:26 |
| 15 | `working-evidence/asplos/found.txt` | 7,933 | 2026-09-06 12:42 |
| 16 | `working-evidence/asplos/vols.txt` | 370 | 2026-09-06 12:05 |
| 17 | `working-evidence/d2024.txt` | 4,064 | 2026-09-06 11:39 |
| 18 | `working-evidence/dump.txt` | 53,444 | 2026-09-06 06:56 |
| 19 | `working-evidence/e3759.txt` | 1,096 | 2026-09-06 06:58 |
| 20 | `working-evidence/expect.txt` | 296 | 2026-09-06 06:57 |
| 21 | `working-evidence/main.txt` | 23,760 | 2026-09-06 06:56 |
| 22 | `working-evidence/main_papers.txt` | 17,842 | 2026-09-06 06:56 |
| 23 | `working-evidence/p000.txt` | 2,958 | 2026-09-06 10:18 |
| 24 | `working-evidence/p025.txt` | 2,908 | 2026-09-06 10:23 |
| 25 | `working-evidence/paper_suffix.txt` | 1,152 | 2026-09-06 06:58 |
| 26 | `working-evidence/patch1.py` | 8,277 | 2026-09-06 14:38 |
| 27 | `working-evidence/patch2.py` | 5,710 | 2026-09-06 14:39 |
| 28 | `working-evidence/patch3.py` | 3,580 | 2026-09-06 14:39 |
| 29 | `working-evidence/prog.txt` | 13,301 | 2026-09-06 10:23 |
| 30 | `working-evidence/ptl.json` | 249 | 2026-09-06 07:11 |
| 31 | `working-evidence/rr.txt` | 296 | 2026-09-06 06:57 |
| 32 | `working-evidence/s3759.txt` | 1,064 | 2026-09-06 06:58 |
| 33 | `working-evidence/sc25/ptsbe.rst` | 11,087 | 2026-09-06 07:19 |
| 34 | `working-evidence/sc25/sample.h` | 30,380 | 2026-09-06 07:19 |
| 35 | `working-evidence/v1.txt` | 5,906 | 2026-09-06 10:14 |
| 36 | `working-evidence/v1_2025.txt` | 2,388 | 2026-09-06 11:38 |
| 37 | `working-evidence/v2.txt` | 7,796 | 2026-09-06 10:15 |
| 38 | `working-evidence/v2_2025.txt` | 733 | 2026-09-06 11:38 |
| 39 | `working-evidence/v2_2026.txt` | 2,093 | 2026-09-06 11:46 |

# SOURCE_MANIFEST — `hpc_quantum`

> **Staging only.** This directory is a preservation copy. Nothing here has been imported into the canonical repository, and no source content was rewritten. **Preserve first, interpret later.**

---

## 1. Identity

| Field | Value |
|---|---|
| **domain** | `hpc_quantum` |
| Source session | Anthropic Cowork cloud container, session `01PdeUA4U6NSdQBt7n9Ywicg` |
| Source absolute path (primary) | `/home/claude/quantum-hpc/` |
| Source absolute path (secondary) | `/tmp/claude-0/-home-claude/e70d0282-821c-5eba-9007-2a27ddc0bcd8/scratchpad/` |
| Export date | **2026-09-07** (UTC) |
| Git-managed source? | **No** — plain file set. No bundle created (instruction 6). |
| Source HEAD / commit count | `N/A — NOT_GIT_MANAGED` |
| Staged file count | **39** (11 corpus + 28 working-evidence) |
| Staged bytes | **1,088,129** |
| Archive filename | `source-archive/hpc-quantum-source-files.tar.gz` |
| Archive SHA-256 | `a27c8094411e43d35f5839bd2debf4cbb61fcb90f07f8e4153270d2556ca108e` |
| Bundle filename | `N/A — source is not a Git repository` |

**`VQE` is a topic inside this domain, not a top-level domain.** It is recorded here at the level it actually appears in the source — see §4.

---

## 2. What the source corpus is

Three sequential research phases, all present:

| Phase | Question asked | Deliverable in `original/quantum-hpc/` |
|---|---|---|
| 1 — Venue mapping | Which conferences publish Quantum-HPC **regular research papers** (2024–2026)? | `QUANTUM_HPC_VENUE_MAP.md`, `QUANTUM_HPC_RESEARCH_QUEUE.md` |
| 2 — SC census | What does SC accept as an **HPC contribution** in quantum work? | `SC_2024_2025_QUANTUM_HPC_CENSUS.md` |
| 3 — ASPLOS census | What succeeds as an ASPLOS regular paper, and how does that differ from SC? | `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`, `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`, `data/asplos/*` |

Scope discipline observed in the source and preserved unchanged: **main-conference regular/full research papers only** — workshops, posters, demos, tutorials, panels, invited talks, keynotes, industry-only material, extended abstracts and short papers are excluded, and the exclusions are documented in the files themselves.

---

## 3. Source status per staging-brief scope item

| Long-term scope item | Status |
|---|---|
| VQE / variational algorithms | `PARTIAL_IN_SOURCE` — as census subject matter and taxonomy branch, not as a methods review |
| quantum chemistry | `PRESENT_IN_SOURCE` **as an exclusion criterion** — classical quantum chemistry is the documented dominant false-positive class |
| hybrid quantum-classical workflows | `PRESENT_IN_SOURCE` |
| HPC-QPU integration | `PRESENT_IN_SOURCE` |
| QPU scheduling / resource management | `PRESENT_IN_SOURCE` |
| distributed quantum simulation | `PRESENT_IN_SOURCE` |
| GPU-accelerated quantum simulation | `PRESENT_IN_SOURCE` |
| quantum workflow systems | `PARTIAL_IN_SOURCE` |
| benchmarking / performance | `PRESENT_IN_SOURCE` |
| classical cost of quantum algorithms | `PRESENT_IN_SOURCE` |
| QEC decoding *(not in the brief list; densest branch in the source)* | `PRESENT_IN_SOURCE` |
| ansatz · UCC/UCCSD · ADAPT-VQE · measurement reduction | `PARTIAL_IN_SOURCE` — incidental mentions inside individual paper analyses (1–5 occurrences each) |
| optimization · initialization/warm-start · barren plateaus/trainability · gradient estimation · excited states | `NOT_PRESENT_IN_SOURCE` |

**`NOT_PRESENT_IN_SOURCE` means "not in this workspace." It does not mean "does not exist in the literature."**

---

## 4. Known incomplete areas — carried over verbatim from the source

These are the source's own unresolved items, **not new findings**:

1. **ASPLOS 2024 program total and session map** — `TOTAL_COUNT_UNVERIFIED`. The official program page truncates after Session 8C; five quantum papers have `STATUS_UNCLEAR` session placement.
2. **28th ASPLOS Volume 4 size** — never enumerated; a component of the 2024 program denominator.
3. **ASPLOS 2026 one-paper discrepancy** — 168 derived vs "167 unique papers" on the official page.
4. **Artifact badge status for all 36 ASPLOS papers** — `UNKNOWN`; ACM DL is the only publisher of that metadata and was unreachable.
5. **Two ASPLOS papers are abstract-only** — *A Fault-Tolerant Million Qubit-Scale Distributed Quantum Computer*, *ACQC*. Mechanisms not inferred.
6. **Two SC papers are closed-access** — LEXIQL, DQTetris. Entries are thin and labelled as such.
7. **2025/2026 ASPLOS volume denominators are single-source** — item-level records were retained only for the 2024 volumes.
8. **MICRO-59 program** — `PROGRAM_INCOMPLETE_AS_OF_2026-09-06`.
9. **ISCA / MICRO / HPCA counts in the venue map** were produced by the program-based method that the ASPLOS census later showed to undercount; the map flags them as unverified lower bounds.

---

## 5. Known external / pending material

| Item | Status |
|---|---|
| Nine upstream third-party Git clones used for artifact verification (~800 MB) | `EXTERNAL_WORKSPACE_PENDING` — **not copied.** Public upstream code, not this project's research output. Remotes + HEAD commits recorded in `SOURCE_INVENTORY.md` §1.2 so any of them is reproducible on demand. |
| `~/Documents/hpc-quantum-warmstart-paper` (user's own manuscript repo, present on the device) | `EXTERNAL_WORKSPACE_PENDING` — **deliberately not staged.** See §7. |
| `hpc-quantum-warmstart` (code repo) | `NOT_PRESENT_IN_SOURCE` — not found in this workspace or at the top level of `~/Documents`. |
| ACM DL / IEEE Xplore full texts | `EXTERNAL_WORKSPACE_PENDING` — blocked from the research environment throughout. |
| Planned but not yet run: ISC, ISCA, HPCA, MICRO, ICS censuses | `NOT_PRESENT_IN_SOURCE` — queued in `QUANTUM_HPC_RESEARCH_QUEUE.md`, not performed. |

---

## 6. Duplicate / overlap notes — flagged only, not resolved

Per instruction 14, **no deduplication was performed.** Observed overlaps, for the import step to adjudicate later:

- **Multiple summaries of the same paper.** Micro Blossom, Promatch, BQSim, RESCQ, QECC-Synth and others are described in *both* `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` (census entry + §13 deep-dive entry) *and* `data/asplos/qec_deepdive.md` / `arch_sim_deepdive.md` / `compilation_deepdive.md` (long-form analysis). `possible duplicate source` — the deep-dives are the fuller text; the census entries are the curated form.
- **QEC lineage content appears twice** — `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md` and `ASPLOS_…_CENSUS.md` §8 cover the same two-philosophy structure at different lengths. `possible duplicate source`.
- **ASPLOS volume structure appears three times** — `data/asplos/VOLUME_STRUCTURE.md`, census §2.3, and `QUANTUM_HPC_RESEARCH_QUEUE.md` §3. All three were updated together and agree.
- **`working-evidence/CENSUS.pre-verification.bak`** is the ASPLOS census **as drafted, before the verification corrections**. It is intentionally a near-duplicate of the final census and must **not** be treated as a competing version — it is the audit trail for Appendix A of the final document.
- **Corpus tables appear in two places** — `data/asplos/CORPUS.md` and census §§3–5.

---

## 7. Warm-start research project — kept separate, by instruction

`~/Documents/hpc-quantum-warmstart-paper` exists on the device and is **김민식's own active research project**, managed separately. It was **not** read into, copied into, or merged with this staging corpus.

Relationship recorded for completeness only: **no file in this staging corpus was derived from that repository**, and no cross-reference to it appears in the source files. The two are independent — this corpus is a **literature / research-landscape source**, that repository is an **active scientific project**.

---

## 8. Evidence grounding — preserved, never promoted

The source grades every claim. Tag counts as staged: `[inference]` 117, `[paper]` 86, `[official-CFP]` 77, `[paper-preprint]` 72, `[official-program]` 71, `[proceedings]` 70, `[code]` 45, `[abstract]` 25, `[documentation]` 21, `[artifact]` 8, `[reconstruction]` 2.

**No inference was upgraded to a confirmed fact. No preprint number was relabelled as a published result. No review-sourced claim was relabelled as an original-paper claim.** Uncertainty markers preserved verbatim: `STATUS_UNCLEAR` ×16, `TOTAL_COUNT_UNVERIFIED` ×10, `NOT_FOUND` ×114, `INSUFFICIENT_EVIDENCE` ×20.

## 9. Research gaps — preserved as found

`VENUE_GAP` ×13, `POSSIBLE_CROSSOVER` ×8, `OPEN_QUESTION` ×7. There is **no standalone gap or novelty file**; the vocabulary is used inline. Per instruction 13, **no gap was generated, closed, or falsified during staging**, including where the existing state may look wrong. The source's own rule — *VENUE GAP ≠ RESEARCH GAP* — is preserved as written.

---

## 10. Integrity verification

| Check | Result |
|---|---|
| Archive round-trip (`tar -xzf` → `diff -r` against `original/`) | **IDENTICAL** |
| Staged corpus vs live source (`diff -r /home/claude/quantum-hpc original/quantum-hpc`) | **IDENTICAL** |
| Staged working-evidence vs live scratch (`cmp` per file, 28 files) | **28 identical, 0 differing** |
| Source vs staged file count | **39 = 39** |
| SHA-256 manifest | `CHECKSUMS.sha256` — see §11 for the verification result |

---

## 11. Provenance and boundaries of this staging run

- Canonical repository `~/Documents/hpc-conference-research` was **read only** (existence + `git rev-parse`): HEAD `415c116`, branch `main`. **Not copied to, merged, edited, committed, catalogued, or otherwise modified.**
- The staging root `~/Documents/hpc-conference-research-import/` **already contained** a prior staging effort — `external/` (ASPLOS26, ICS26, IPDPS26, ISC26, …), `CHECKSUMS.sha256`, `SOURCE_EXPORT_MANIFEST.md`, 111 files. **That material was not touched.** `hpc_quantum/` was created as a **sibling** directory.
- No web search, no literature lookup, and no new analysis were performed during staging.

# Quantum-HPC Research Queue

**Phase 2 planning — order of regular-paper census by venue**
**Compiled 2026-09-06 (KST), from `QUANTUM_HPC_VENUE_MAP.md`**

---

## 0. What this document is

Phase 1 produced a venue map. Phase 2 is a **per-venue regular-paper census**: for each venue, enumerate every main-track regular paper 2024–2026 that meets the inclusion criteria, with full metadata, and classify it into the taxonomy. This document specifies **the order to do that in, and why**, plus the venue-specific mechanics needed to do it correctly.

**The order is not prestige-ordered.** It is ordered by expected yield per unit of effort toward the goal: *find SC-publishable Quantum-HPC research problems.* Three principles drive it:

1. **Target first.** SC defines what a publishable contribution looks like. Census it before anything else so every later venue can be read against that standard.
2. **Density second.** Venues with many relevant papers per year come before venues with one or two, regardless of reputation.
3. **Branch ownership third.** A venue that is the *only* home for a research branch (ISC for HPC-centre integration, OSDI for quantum OS, SIGMETRICS for performance characterization) outranks a higher-prestige venue whose output overlaps something already censused.

---

## 1. The queue

| Order | Venue | Years | Why this position | Expected yield | Status |
|---|---|---|---|---|---|
| **1** | **SC** | 2024, 2025 *(+2026 when public)* | The target venue. Everything downstream is judged against what SC accepts. Escalating scope: the SC26 topic area was renamed **"Post-Moore & Quantum Computing"**. | **11 — CENSUS COMPLETE 2026-09-06** (7 + 4, both verified by exhaustive volume enumeration) | **ACTIVE** · see `SC_2024_2025_QUANTUM_HPC_CENSUS.md` · SC26 `PROGRAM_INCOMPLETE_AS_OF_2026-09-06` |
| **2** | **ASPLOS** | 2024, 2025, 2026 | **✅ CENSUSED 2026-09-06** — `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md`. Largest quantum population in the survey; dedicated sessions all three years; 61% public-artifact rate, so deep-dive candidates come from here. | **36 (14/10/12)** — *the queue's 31 (9/10/12) was a program-based undercount* | **COMPLETE** |
| **3** | **ISC High Performance** | 2024, 2025, 2026 | Only venue with a dedicated Quantum Computing submission track, and the **sole main-track home** for HPC-centre QPU integration and operations. Proportionally densest. | 12 (5/3/4) | **ACTIVE** |
| **4** | **ISCA** | 2024, 2025, 2026 | Highest absolute session count (1→3→3). Its 2025 pivot from NISQ compilation to FT systems, decoder throughput and multi-QPU interconnect is exactly the direction of interest. | 34 (6/16/12) | **ACTIVE** |
| **5** | **ICS** | 2025, 2026 *(+2024 verify)* | **Fastest-rising HPC venue**: 0→2→5, with a session named "Quantum Computing" in 2026. Same community and overlapping PC with SC — a leading indicator. | 7 confirmed | **EMERGING → ACTIVE** |
| **6** | **IEEE QCE** — QSYS + QAPP tracks only | 2024, 2025 *(2026 deferred)* | Largest reservoir and **best early-warning sensor** — problems appear here 12–24 months before SC/ASPLOS. Census as a sensor, not a target. Requires the strictest workshop-exclusion discipline of any venue. | QSYS 46 (2024) + 51 (2025); expect ~20–30 in scope after filtering | **SCOPE_CONFIRMED + ACTIVE** · QCE26 per-track PDFs not yet posted |
| **7** | **SIGMETRICS** | 2025, 2026 | Owns the **performance modeling / characterization / variability** branch outright, with no HPC-venue competition. ScaleQsim is the most on-target single paper found anywhere. | 9 (4/5) | **ACTIVE** |
| **8** | **OSDI** | 2025, 2026 | Owns the **quantum OS / virtualization / QPU multi-tenancy** branch. Closest existing literature to operating a QPU as a shared HPC-centre resource. Small, high-value, fast to census. | 3 | **ACTIVE** |
| **9** | **HPCA** | 2025, 2026 *(skip 2024)* | Two dedicated sessions in each of 2025 and 2026; the 2026 decoder papers include the most transferable public artifact of the year. **2024 is a non-year — one paper, no session.** | 15 (7/8) | **ACTIVE from 2025** |
| **10** | **MICRO** | 2024, 2025 *(+2026 when public)* | The hardware end of the QEC-decoder thread, plus quantum control microarchitecture and cryogenic I/O. Complements ISCA/ASPLOS rather than duplicating them. | 11 (3/8) | **ACTIVE** · MICRO-59 `PROGRAM_INCOMPLETE_AS_OF_2026-09-06` |
| **11** | **CGO** | 2024, 2025, 2026 | Explicit quantum CFP scope, **two named "Quantum Computing" sessions in 2025**, and the strongest transfer of classical HPC compiler methodology (affine/polyhedral abstractions for qubit mapping; a JIT DSL from LBNL). | 8 (1/4/3) | **ACTIVE** |
| **12** | **CCGrid** | 2025 *(+2024, 2026 verify)* | The **HPC-QC middleware and workflow-orchestration** branch: Pilot-Quantum, FaaS hybrid workflow choreography, tensor-network simulation — three papers in one 2025 session. | 3 confirmed | **ACTIVE** · 2026 core yield fell to 0 |
| **13** | **ICPP** | 2024, 2025, 2026 | Dedicated CFP track with parallel-simulator and quantum-compilation scope. Modest yield (1–3/yr) but directly on-topic, and a realistic submission target. | 7 (1/3/3) | **SCOPE_CONFIRMED**, volume EMERGING |
| **14** | **IPDPS** | 2024, 2025, 2026 *(+2023 for AQUA lineage)* | Reliable 1–2 papers a year and the **only HPC venue with a QPU-multiplexing paper** (AQUA). Include 2023 here — it had a 3-paper quantum block, the local maximum. | 5 (2/1/2) | **WATCH → EMERGING** |
| **15** | **IISWC** | 2024, 2025 | Tiny volume, **highest signal-to-noise per paper in the survey**: an architecture-level performance model, a quantum resource orchestrator, and a QEC decoder benchmark suite. Fast to census, high value. | 3 | **EMERGING** |
| **16** | **HiPC** | 2024, 2025 *(+2026 in Dec)* | Main-track papers in consecutive years, and it just created a **dedicated Track 5 "Quantum Computing Systems and Applications"** whose scope names *"quantum HPC frameworks"*. Institutionalizing now. | 3 (2/1) | **ACTIVE** |
| **17** | **EuroSys** | 2026 | One paper, but exactly the right one: **elastic QEC decoder capacity planning**, with public code. A single-paper census that directly informs the decoder-as-HPC-workload thesis. | 1 | **EMERGING** |
| **18** | **OOPSLA** | 2025 *(+2024, 2026 selective)* | **qblaze** — a parallel sparse quantum simulator with strong multi-core scaling — is a genuine HPC simulation paper. Census the compilation/simulation subset only; skip the verification papers. | ~6 in scope of 15 | **ACTIVE (subset)** |
| **19** | **DAC** | 2024, 2025, 2026 | Densest **uncovered** venue. Filter hard: roughly half is device- or EDA-internal (readout electronics, cryo-CMOS). Keep distributed-QC co-design, FT compilation, decoder hardware. | ~15, ~half in scope | **ACTIVE** |
| **20** | **ICCAD** | 2024, 2025 | **QPU job scheduling**, hardware-aware circuit knitting, and microsecond-latency QEC decoders. Exclude the invited Special Sessions. | ~6 in scope | **ACTIVE** |
| **21** | **Euro-Par** | 2025, 2026 | Clean 0→1→2 rise across three *different* tracks — organic diffusion. Small but a genuine European-HPC signal. **Correct the record: there is no Euro-Par quantum track.** | 3 | **EMERGING** |

### Deferred — monitor, do not census yet

| Venue | Why deferred | Re-check trigger |
|---|---|---|
| **DATE** | Real named track ("D16 Design Automation for Quantum Computing") but yield overlaps DAC/ICCAD; skews to cryo-CMOS | After DAC + ICCAD are censused; pull the MQT Compiler Collection paper regardless |
| **HPEC** | HPC-native and culturally the closest fit, but lighter review (6 pp.); best used as a **people and community tracker**, not a literature base | Use continuously as an author-tracking source (PNNL NWQ-Sim, Lincoln Lab, NASA QuAIL) |
| **ICDCS** | The multi-QPU / quantum-cloud subset (3 papers) is in scope; the entanglement-routing bulk is a different community | If a multi-QPU interconnect branch is added to the taxonomy |
| **ICCD** | `Mera` and `MOSQ` are real simulation-acceleration papers; 2025 block skews to security. CFP unverified | If simulation acceleration becomes a focus branch |
| **PLDI** | 5/yr, but only **QVM** (2025) and **Cobble** (2026) are in scope | Pull those two papers directly; do not census the venue |
| **HPDC** | Main track empty three years running; the **QUASAR workshop** is dense and growing (3→4 papers) | After HPDC 2027 — or now, if the scope is ever widened to workshops |
| **IEEE Cluster** | 0 main-track, but CFP scope demonstrably opened in 2025 and quantum posters are appearing (SYCL QPU simulator, NetQMPI) | **Cluster 2026, 22–25 Sept 2026** — watch for a poster author converting to a full paper |
| **SOSP** | 0 across 185 papers, but identical CFP and overlapping PC with OSDI, which has taken three | SOSP 2027 |
| **PACT** | 1 paper in 2024, 0 in 2025. But its CFP scope is **non-monotonic**: absent in 2025, then **returning in 2026 as *"Quantum-HPC interfacing"*** — the most on-target wording PACT has ever used | **PACT 2026, 19–22 Oct 2026** — if the new sub-bullet converts into papers, PACT moves up the queue; a second empty year means LOW_PRIORITY |
| **ISPASS** | Scope confirmed, zero papers; IISWC's sibling and the natural home for quantum performance analysis | ISPASS 2026/2027 |
| **ACM SIGOPS ATC** | USENIX ATC's continuation under ACM sponsorship — same community and scope per the organizers; Hong Kong, Nov 2026 | **After notification, 18 Sept 2026** |
| **ACM Computing Frontiers, ASP-DAC** | Scope-confirmed, essentially empty | Annual scan only |

### Not queued
**PPoPP · CC (22/17/16 papers, zero quantum) · NSDI · USENIX ATC (now ACM SIGOPS ATC — watch only) · POPL** *(theory only — pull SimuQ 2024 and Amy & Lunderville 2025 directly if compiler analysis becomes a focus)* · ICPE · MASCOTS · PASC · eScience · HOTI · DSN · SoCC · Middleware · SPAA · ICPADS · HPCC · ICSE/FSE/ASE/ISSTA · ICRC · ISVLSI · QIP · TQC · APS March Meeting · QEC Conference · QTML · QCNC

---

## 2. Waves and what each answers

### Wave 1 — venues 1–4 · *"What does a publishable Quantum-HPC paper look like?"* — **SC ✅ · ASPLOS ✅ complete**
**SC → ASPLOS → ISC → ISCA.** These four span both poles: the HPC pole (SC, ISC) and the architecture pole (ASPLOS, ISCA). By the end of Wave 1 there should be a working sense of what each community counts as a contribution — and specifically, why SC accepts a GPU statevector partitioning paper while ASPLOS accepts an FPGA MWPM decoder, when both are "classical computation serving quantum".

**Deliverable:** `SC_2024_2025_QUANTUM_HPC_CENSUS.md` ✅ **(done 2026-09-06)** and `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` ✅ **(done 2026-09-06)** with `QUANTUM_HPC_ARCHITECTURE_LINEAGES.md`, then `CENSUS_ISC.md`, `CENSUS_ISCA.md`, plus a first pass at contribution-shape norms per community.

> **Wave-1 answer so far, from SC + ASPLOS.** The two poles differ most sharply on **compilation**: SC's three compilation papers are 3-of-3 arguments about *compile-time scalability* (the incumbent exact method's measured failure is the problem statement), while only 2 of ASPLOS's ten make that argument centrally — seven argue *output quality* or use a different cost model entirely. Artifact rates are statistically indistinguishable (ASPLOS 61%, SC 64%) despite ASPLOS running formal Artifact Evaluation and SC not requiring it, and in 36 ASPLOS papers **exactly one ships HDL**. **QEC decoding remains absent from every HPC venue in this map while being the densest ASPLOS branch** — `VENUE_GAP`, not a research gap.

> ⚠ **Method change forced by the ASPLOS census, applies to ISCA/MICRO/HPCA/ICS next.** Establish the **volume↔program-year mapping first**, sweep **volumes not programs**, keep **proceedings-year and program-year denominators separate in every sentence**, and mark any denominator you could not enumerate `TOTAL_COUNT_UNVERIFIED`. The ASPLOS draft failed this and needed a material correction (Appendix A of that census).

**Carried forward from the SC census — apply at every remaining venue.** Classify each paper by which of the **four acceptance pathways** it uses (HPC *is* the contribution / HPC enables a quantum claim / the HPC problem is compilation cost / the HPC content is the resource consumed), because SC turned out to have no single definition and "the venue accepted it" does not imply "it contains an HPC contribution." Apply the Quantum-problem / HPC-problem / venue-contribution split from the start — it is what exposed the two SC papers with no HPC content. Track real-QPU usage and strong/weak-scaling reporting as venue-level indicators (SC's answers were 1-of-11 and 3-of-11). And restore the context of every headline number before recording it: in the SC corpus most "N×" figures were circuit-quality ratios or self-comparisons, not speedups.

### Wave 2 — venues 5–8 · *"Where are the newest problems, and who owns the branches?"*
**ICS → QCE → SIGMETRICS → OSDI.** ICS is the growth edge. QCE is the sensor. SIGMETRICS and OSDI each own a branch that appears nowhere else. After Wave 2, the scheduling/resource-management and performance-characterization branches should be fully mapped.

**Deliverable:** branch-level literature maps for scheduling/resource management, quantum OS/virtualization, and performance modeling/characterization.

### Wave 3 — venues 9–14 · *"Complete the HPC community and the QEC-decoder thread"*
**HPCA → MICRO → CGO → CCGrid → ICPP → IPDPS.** HPCA and MICRO close out the decoder and control-microarchitecture literature; CGO closes the compiler literature; CCGrid, ICPP and IPDPS complete the HPC community.

**Deliverable:** a complete QEC-as-classical-workload literature map, and a complete HPC-venue census.

### Wave 4 — venues 15–21 · *"Secondary venues and the EDA pool"*
**IISWC → HiPC → EuroSys → OOPSLA → DAC → ICCAD → Euro-Par.** Diminishing returns, but IISWC and EuroSys are cheap and high-value, and the EDA pool is large enough that skipping it entirely would leave a real gap in the compilation literature.

---

## 3. Per-venue census mechanics

Venue-specific traps that will corrupt a census if not handled. **Read the entry before censusing the venue.**

| Venue | What to use as the authoritative main-track list | Traps |
|---|---|---|
| **SC** | ✅ **CENSUS COMPLETE.** Publisher volume identity. Main: `10.1109/SC41406.2024` (SC24), `10.1145/3712285` (SC25). | Proceedings pages are robots-disallowed. **Workshops are `10.1109/SCW63240.2024` and `10.1145/3731599`**; the SC-W volume repaginates from 1, so **use the DOI prefix, never the page number**. Exclude classical quantum-chemistry papers (SC25 **Gordon Bell block is pp. 1–136**, 11 papers — not pp. 1–59; SC24 100-million-atom Raman paper). **SC24 had three sessions, not two blocks** — and `.00078` (HPAC-ML) sits inside "Quantum and Approximate Computing II" with no quantum content, so **never census SC24 from session names.** SC25's Papers tags are "Post-Moore Computing" + "Quantum Computing"; "Quantum & Other Post Moore Computing Technologies" is the **Exhibitor Forum** taxonomy. |
| **ASPLOS** ✅ | **ACM volumes, swept in full. NOT the program session listing** — the 2024 program page truncates after Session 8C and undercounts by five papers. | **The deferral rule is the whole ballgame: a volume branded year N is presented at year N+1.** Verbatim, ASPLOS 2024 CFP: *"Accepted major revisions of the fall cycle will be published as ASPLOS'24 papers but will be presented in ASPLOS'25."* Full mapping — 29th: `3617232`(V1) `3620665`(V2) `3620666`(V3) presented 2024, `3622781`(V4) presented **2025**; 30th: `3669940`(V1) `3676641`(V2) presented 2025, `3676642`(V3) presented **2026**; 31st: `3760250`(V1) `3779212`(V2) presented 2026 — **there is no 31st V3**. Also feeding the 2024 program: 28th V4 `3623278`. Trap: `3818671.*` is the GPGPU workshop, not ASPLOS. ASPLOS 2025 was co-located with EuroSys; do not cross-attribute. |
| **ISC** | IEEE volumes `10.23919/ISC.<year>` (research papers). | ISC **workshops** are Springer LNCS (`High Performance Computing. ISC High Performance <year> International Workshops`) — excluded. Filter quantum-inspired annealing (2025 vector annealing; 2026 QUBO workflow paper is `Q_IN_HPC`-adjacent but not quantum hardware) and classical eigensolver work (2024 VASP paper). |
| **ISCA** | Official program session headings; DBLP proceedings TOC carries the same headings. | FTQCSA 2025 (Workshop on Fault-Tolerant Quantum Computer System Architecture) was co-located with ISCA 2025 — excluded. **SATIC (ISCA 2026, "Quantum 3" session) is an Ising-machine compiler, not quantum** — strict 2026 count is 11, not 12. |
| **ICS** | **Official program page** — ICS 2026's "Quantum Computing" session is the anchor. Cross-check ACM volumes `10.1145/3721145` (ICS'25), `10.1145/3797905` (ICS'26). | Workshops volume is `10.1145/3774895`. ICS 2026 "Parallel Quadratic Selected Inversion in Quantum Transport Simulation" is classical NEGF — the official program confirms it is *not* in the quantum session. SpinTune is quantum **sensing** — recommend exclusion. **Re-verify ICS 2024 by hand** (current finding is "none found", not a counted zero). |
| **IEEE QCE** | **The official per-track "Accepted Technical Papers" PDF** — nothing else. | (a) The most HPC-relevant-sounding titles are **WIHPQC workshop** papers (HPCQCMark, system-level quantum-accelerator integration, hybrid Quantum-HPC resource allocation, qubit health analytics) — all excluded. (b) Xplore mixes technical papers, workshop papers, poster abstracts and panel abstracts under one conference name. (c) **Page count does not discriminate** — QCE25 workshop papers ran 6–7 pp., overlapping the ≤7 pp. short-paper band; use the proceedings volume section heading. (d) Main-track pagination is continuous; workshop pagination restarts at 1 in Volume II. (e) **No per-track PDF exists for QCE26 yet** — defer. |
| **SIGMETRICS** | Official accepted-papers pages; papers appear in POMACS. | Runs Summer/Fall/Winter cycles — enumerate all three. Note SIGMETRICS/PERFORMANCE joint years have a larger proceedings TOC than the conference accepted-papers page. |
| **OSDI** | USENIX technical-sessions pages. | Small; the OSDI '26 quantum paper (qTPU) is easy to miss on a long program page — use site-restricted search as a second pass. |
| **HPCA** | Official program + **DBLP/IEEE for author lists**. | **"Best of CAL" is an invited re-presentation track, not main-track** — this is exactly the trap that inflates HPCA 2024 from 1 to 2. HPCA 2026 moved to the researchr platform and its **program-page author attributions are misaligned** — take authors from DBLP/IEEE. |
| **MICRO** | Official program; ACM volume `10.1145/3725843` (2025), IEEE Xplore (2024). | *SuperCore* (2024) and *SuperSFQ* (2025) are classical superconducting processors, not quantum. MICRO-59 program page is 404 as of 2026-09-06. |
| **CGO** | conference-publishing.com TOCs (they carry session names). | **Co-located with PPoPP, HPCA and CC in the same week** — verify every paper against CGO's own TOC. |
| **CCGrid** | Official program PDFs + IEEE volumes (`CCGrid59990.2024`, `CCGrid64434.2025`, `CCGrid68966.2026`). | The QUICK workshop is co-located — excluded. Filter **post-quantum cryptography** (2025 SPIFFE/SPIRE PQC; 2026 QRAP) — the dominant false positive here. The 2024 "Training Computer Scientists…" paper is a main-track education paper, out of taxonomy. |
| **ICPP** | ACM volumes `10.1145/3673038` (2024), `10.1145/3754598` (2025); **official schedule** for 2026 (proceedings not yet published). | Workshops are `10.1145/3677333` and `10.1145/3750720`. **Q-GEAR is registered under BOTH the main and workshop volume** — resolve against ACM DL before citing. ICPP 2026 has no quantum session; the three papers are scattered. |
| **IPDPS** | IEEE volumes `IPDPS57955.2024`, `IPDPS64566.2025`, `IPDPS65963.2026`. | Workshops are **IPDPSW** (`IPDPSW63119.2024` etc.) — the Union Find toric-code decoder paper is IPDPSW, not IPDPS. |
| **IISWC** | Official accepted-papers page / program PDF. | Two main-proceedings categories — **Regular (10 pp.) and Tool-and-benchmark (6–10 pp.)** — both main track; posters are separate. `decoder-bench` may formally be the latter. |
| **HiPC** | **IEEE proceedings volume, not the program page.** Main: `HiPC62374.2024`, `HiPC66333.2025`. | The advance programme lists **session names without paper titles** — programme inspection alone finds nothing. Workshops are **HiPCW** (`HIPCW63042.2024`, `HiPCW66559.2025`). Filter quantum-inspired (2025 QIEDP) and PQC (FALCON/RISC-V). |
| **EuroSys** | Official accepted-papers page + ACM volume. | Single paper; trivial. |
| **OOPSLA** | `/details/…OOPSLA/…` URLs on the SPLASH site. | **Track-page summarization truncates** — a first pass returned a false "zero" for 2024 and 2025. Use site-restricted search as a mandatory second pass. |
| **DAC / ICCAD / DATE** | Proceedings TOCs, filtered by category. | Excluded lesser categories: DAC **Late Breaking Results**; ICCAD **invited Special Sessions** (ICCAD 2024 SS8 was entirely quantum) and workshops; DATE **Extended Abstracts, Late Breaking Results, Multi-Partner Projects, PhD Forum**. Counting from a raw TOC will overstate every EDA venue substantially. **Also: `iccad-conf.com` is a different, unrelated control-engineering conference — the right site is `iccad.com`.** |
| **Euro-Par** | Springer **main-conference** LNCS volumes (`Euro-Par YYYY: Parallel Processing`) only. | Workshops are a separate LNCS volume (`… Parallel Processing Workshops` / Satellite Events). Filter classical quantum chemistry (2026 TAIN). |

---

## 4. Standing filter — apply at every venue

**Exclude by category:** workshop papers · posters · demos · extended abstracts · short papers where the venue treats them as a lesser category · tutorials · panels · keynotes · industry/vendor talks · doctoral symposia · competition results · invited re-presentation tracks (HPCA "Best of CAL") · journal-first presentation slots (PLDI `[TOPLAS]`).

**Exclude by topic — the three recurring false-positive classes:**
1. **Post-quantum cryptography** — the single most common false positive. Seen at CCGrid, PACT, HiPCW, ICCD.
2. **Classical quantum chemistry / many-body / quantum transport / neural-network quantum states** — classical HPC wearing a quantum-sounding title. Seen at SC (both years), ICPP, ICS, Euro-Par, HPDC.
3. **"Quantum-inspired" classical methods** — vector/Ising annealing, classical QUBO solvers. Seen at ISC, HiPC, ISCA.

**Also exclude:** pure device physics · fabrication/materials only · pure quantum information theory with no systems implication · chemistry-accuracy-only · new-ansatz-only · new-optimizer-only · pure QEC theory with no decoding/system/architecture implication · quantum **sensing** (distinct from quantum computing — e.g. ICS 2026 SpinTune).

**When uncertain, do not guess.** Record `BORDERLINE` with reasons for and against, or `STATUS_UNCLEAR` with exactly what could and could not be confirmed.

---

## 5. Per-paper record format for Phase 2

Recommended fields, so census files are comparable across venues:

```
- title:
  authors:              # first author + affiliation; full list optional
  venue:                # venue + year + track/session name if known
  pub_status:           # PUBLISHED_REGULAR_PAPER | ACCEPTED_FORTHCOMING | PREPRINT
                        # | PROGRAM_LISTED | STATUS_UNCLEAR
  evidence:             # [official-CFP] [official-program] [proceedings] [paper]
  doi:
  source_url:
  scenario:             # HPC_FOR_Q | Q_IN_HPC | Q_FOR_HPC | FUTURE_WORKLOAD
  taxonomy_branch:      # from Appendix A of the venue map
  one_line:             # what it does, in one sentence
  hpc_relevance:        # 1-5, with a reason
  artifact:             # PUBLIC_CODE | PUBLIC_ARTIFACT | PARTIAL
                        # | NO_PUBLIC_ARTIFACT_FOUND | UNKNOWN
  artifact_url:
  perf_claim_clarity:   # do they specify baseline / scale / precision / problem size /
                        # end-to-end boundary? HIGH | MEDIUM | LOW | N/A
  deep_dive_priority:   # 1-5
  notes:                # BORDERLINE reasoning, exclusions considered, caveats
```

**`deep_dive_priority` heuristic.** Rank up for: a public artifact (the paper-to-code chain can be closed); clearly specified performance claims; a contribution shape that maps onto an SC paper; a branch with few papers (higher marginal information). Rank down for: device-level contributions; unspecified baselines; a topic already well covered by three papers already in the queue.

---

## 6. Expected outputs of Phase 2

1. `CENSUS_<VENUE>.md` per venue, in queue order.
2. `QUANTUM_HPC_PAPER_INDEX.md` — every paper across all censuses, one row each, sortable by taxonomy branch, scenario tag, and deep-dive priority.
3. `QUANTUM_HPC_BRANCH_MAPS.md` — per-branch literature maps for the three densest branches: QEC as a classical workload, scheduling/resource management, and classical simulation at scale.
4. A revised `QUANTUM_HPC_VENUE_MAP.md` — the census will correct counts, resolve the `STATUS_UNCLEAR` items listed in Appendix C, and fill in the artifact column.

**Phase 3** (not planned here) is the per-paper deep dive: equations, algorithms, experiments, and code cross-verification, following the principles in Appendix B of the venue map.

---

## 7. Time-sensitive items

Four things happen soon after this survey date and should be picked up rather than missed:

| Date | Event | Action |
|---|---|---|
| **13–18 Sept 2026** | **IEEE QCE26**, Toronto — 372 technical papers in 9 tracks; program public, per-track PDFs not yet posted | Watch for the per-track "Accepted Technical Papers" PDFs; the QSYS session titles alone (Real-Time QEC Decoding, Distributed Quantum Systems, Scalable Quantum Circuit Simulation, Quantum Systems & Resource Management, Runtime Workflows & Compilation Reuse) are the field's forward signal for 2027 |
| **18 Sept 2026** | **ACM SIGOPS ATC 2026** notification (Hong Kong, Nov 2026) | First ACM-sponsored edition of the former USENIX ATC — check whether any quantum work landed |
| **22–25 Sept 2026** | **IEEE Cluster 2026**, Alexandria VA | Check whether a 2025 quantum poster author converted to a main-track paper |
| **Late Sept–Oct 2026** | **MICRO-59 program** publication (`microarch.org/micro59/program/` — currently 404) | Close the one program gap in this survey |
| **19–22 Oct 2026** | **PACT 2026**, Chicago | Its CFP added ***"Quantum-HPC interfacing"*** under middleware/runtime support — the most on-target CFP sub-bullet found in this survey. Check whether it produced papers |
| **Nov 2026** | **SC26**, 15–20 Nov | The accepted-papers list closes the largest gap in the map. Note: none of the 9 announced Best/Best-Student Paper finalists is quantum |
| **16–19 Dec 2026** | **HiPC 2026**, Bengaluru | First edition with the dedicated **Track 5 "Quantum Computing Systems and Applications"** — the clearest test of whether a new quantum track converts into papers |

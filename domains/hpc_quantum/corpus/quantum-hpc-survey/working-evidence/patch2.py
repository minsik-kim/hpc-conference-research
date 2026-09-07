p='ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md'
t=open(p,encoding='utf-8').read(); n=0
def rep(old,new,label):
    global t,n
    c=t.count(old); assert c==1, f"{label}: {c} occurrences"
    t=t.replace(old,new); n+=1; print("OK ",label)

# ---------- C2: provenance of the volume counts ----------
rep(
"""Every one of the ten relevant volumes was enumerated through the **Crossref REST API** with `cursor=*` deep paging. **A methodological warning worth recording: Crossref's `offset` paging proved unstable** — `offset=100` on the 2025-03-30 window re-served two items already returned at `offset=50`. Cursor paging is deterministic and was used throughout.

Completeness proofs achieved: per-volume item counts reconcile exactly with the established structure; DOI suffix ranges are contiguous and were verified (29V2 = `3640353–3640428`, 76 items with no gaps; 29V3 = `3651322–3651387` plus four keynote DOIs; 30V1 = `3707214–3707287` less two; 31V1 = `3762216–3762235`). All titles in every volume were swept against a ~50-term keyword set, not just "quantum".""",
"""**The instrument, stated exactly, because the denominators are only as good as it is.** ACM DL and IEEE Xplore are unreachable from this environment and `curl` egress is blocked, so no byte-exact API retrieval was possible. Volume contents were obtained from the **Crossref REST API** read through `WebFetch` — that is, a summarising read of the JSON response, not a raw download.

Three consequences that a reader must weigh:

1. **Crossref exposes no volume-level item count, and its `container-title` filter is silently ignored** — a query using it returns unrelated results with no error. No count in this census comes from that filter. Counts were built instead from **date-windowed `prefix:10.1145` queries with `cursor=*` deep paging, filtered client-side on the DOI stem** of each volume.
2. **`offset` paging is unstable** — `offset=100` on the 2025-03-30 window re-served two items already returned at `offset=50`. Cursor paging is deterministic and was used throughout.
3. **Item-level records were retained only for the 2024 volumes.** A retained extract of 170 DOIs with page ranges covers 29V2 (76), 29V3 (70) and 29V4 (24) and reconciles exactly. For 29V1 (28), 30V1 (72), 30V2 (88), 30V3 (19), 31V1 (20) and 31V2 (135) the retained extracts are **partial** (70 of 72 for 30V1, 87 of 88 for 30V2, 125 of 135 for 31V2), and those totals rest on the sweep's own reported item count rather than on an enumeration this census can re-display.

**Status of the denominators, therefore: 2024 = enumerated and reconciled; 2025 and 2026 = single-source and should be read as ±a few papers.** Corpus *membership* is on firmer ground than the denominators: every one of the 36 papers has its title and DOI corroborated by at least one non-Crossref source — arXiv, an author or group page, or an official program.

**A contiguity claim corrected in verification.** An earlier draft stated that 29V2 is `3640353–3640428`, "76 items with no gaps." The retained extract shows 76 items but **one gap at `3640398` and one out-of-range DOI, `3640665`** — the count is right, the contiguity claim was not. 29V3 is `3651322–3651387` (66 papers) plus four keynote DOIs `3655589–3655592` = 70 items. 29V4 is `3674167–3674190` less `3674187`, plus `3698899` = 24 items. 30V1 was reported as `3707214–3707287` less two; the retained extract covers only 67 of those, so that range is `[inference]` from the sweep rather than a displayed enumeration.

All titles in every volume were swept against a ~50-term keyword set, not just "quantum".""",
"C2 provenance")

# ---------- C1g: limitation 4 ----------
rep(
"""4. **The ASPLOS 2024 official program page truncates partway through Day 3** (after Session 8C). Session assignments for the five out-of-session quantum papers could not be recovered from it; their program year is inferred from their volume. The volume sweep, which does not depend on the program page, is what establishes their presence.""",
"""4. **The ASPLOS 2024 official program page is incomplete.** It lists sessions 1A, 1B … 8C and then stops; nothing after 8C appears, and the last entry is cut off mid-session. Both URL variants (`/main-program/` and `/main-program/index.html`) return the same truncated content. Consequently: (a) the retrievable portion holds roughly 140 papers, which is **not** the 2024 program total and must not be used as a denominator; (b) the session placement of five quantum papers is `STATUS_UNCLEAR` — they cannot be located on the page and cannot be shown absent from the program; (c) their *presence* in the 2024 program rests entirely on the volume sweep plus the deferral rule, which do not depend on the program page.""",
"C1g limitation 4")

# ---------- C3: GUOQ one hour ----------
rep(
"""**GUOQ is the cleanest inversion: it holds compile time fixed at one hour for every tool and asks who produces the best circuit inside it — compile time as experimental *control*, the precise opposite of SC's treatment of it as the dependent variable.**""",
"""**GUOQ is the cleanest inversion: its stated protocol is that "*unless otherwise indicated*, we allocated each tool 1 hour," and it asks who produces the best circuit inside that budget — compile time as experimental *control*, the precise opposite of SC's treatment of it as the dependent variable. The hedge is load-bearing and is recorded here rather than smoothed over: Quarl is an explicit exception, run on an A100 with 64 GB, so the budget is a default rather than a uniform constraint.** `[paper-preprint]`""",
"C3 GUOQ")

open(p,'w',encoding='utf-8').write(t); print(f"\n{n} edits applied")

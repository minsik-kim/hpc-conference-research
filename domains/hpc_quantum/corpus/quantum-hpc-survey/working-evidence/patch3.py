p='ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md'
t=open(p,encoding='utf-8').read(); n=0
def rep(old,new,label,count=1):
    global t,n
    c=t.count(old); assert c==count, f"{label}: {c} occurrences (expected {count})"
    t=t.replace(old,new); n+=1; print("OK ",label)

# ---------- C4: Micro Blossom O(d^3), not Theta ----------
rep("**keep the algorithm exact and spend Θ(d³) processing units**",
    "**keep the algorithm exact and spend O(d³) processing units** (the paper's own notation is O, not Θ)",
    "C4a governing idea")
rep("| Parallelism | filter stages; serial match residue | **Θ(d³) PUs**, one per vertex/edge | asynchronous, every k cycles |",
    "| Parallelism | filter stages; serial match residue | **O(d³) PUs**, one per vertex/edge | asynchronous, every k cycles |",
    "C4b table row")
rep("whose decoding graph is ~9× the vertices of d=13 (Θ(d³))",
    "whose decoding graph is ~9× the vertices of d=13 (vertex count grows cubically in d)",
    "C4c d=27 scaling")
rep("**Exactness has a superlinear worst case** — O(d⁹) even after Θ(d³)-way parallelisation.",
    "**Exactness has a superlinear worst case** — O(d⁹) even after O(d³)-way parallelisation.",
    "C4d worst case")
rep("**Mechanism to learn:** Θ(d³) processing units — one vPU per decoding-graph vertex, one ePU per edge",
    "**Mechanism to learn:** O(d³) processing units — one vPU per decoding-graph vertex, one ePU per edge",
    "C4e mechanism")

# ---------- C4f: the 8x comparison ----------
rep("""the 8× baseline excludes the baseline's own I/O, which the paper transparently notes;""",
    """the 8× is **not a like-for-like comparison** — Micro Blossom's own figure includes all CPU↔accelerator I/O while the baseline's latency excludes the baseline's own I/O, which the paper transparently notes (the asymmetry works against Micro Blossom, but it is still an asymmetry);""",
    "C4f 8x")

# ---------- C5: Promatch capacity provenance ----------
rep("""Governing idea: the main decoder has **fixed combinatorial capacity** (Hamming weight ≤ 10, 945 matchings), and progress in d comes from *shrinking the problem to fit*.""",
    """Governing idea: the main decoder has **fixed combinatorial capacity** — Hamming weight ≤ 10 and 945 matchings, which are **Astrea-G's capacity, inherited by Promatch rather than introduced by it** — and progress in d comes from *shrinking the problem to fit*.""",
    "C5a governing idea")
rep("""filter syndromes so the exact stage's fixed combinatorial capacity (Hamming weight ≤ 10, 945 matchings) suffices""",
    """filter syndromes so the exact stage's fixed combinatorial capacity (Hamming weight ≤ 10, 945 matchings — Astrea-G's, inherited) suffices""",
    "C5b mechanism")

# ---------- C5c: 960 ns as allotted budget ----------
rep("""**Evidence:** `RTL_SYNTHESIS` + `ANALYTIC_MODEL` — the 960 ns is a cycle count divided by an assumed 250 MHz, **not a measurement**.""",
    """**Evidence:** `RTL_SYNTHESIS` + `ANALYTIC_MODEL` — the 960 ns is a cycle count divided by an assumed 250 MHz, **not a measurement**, and it originates as a *budget allotted top-down* from the syndrome-cycle deadline rather than as an observed latency.""",
    "C5c 960 provenance")
rep("""| Provenance | cycle count × (1/250 MHz) | **measured on VMK180 board** |""",
    """| Provenance | cycle count × (1/250 MHz); a **top-down allotted budget**, not an observation | **measured on VMK180 board** |""",
    "C5d table provenance")

open(p,'w',encoding='utf-8').write(t); print(f"\n{n} edits applied")

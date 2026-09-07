import io,sys
p='ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md'
t=open(p,encoding='utf-8').read()
n=0
def rep(old,new,label):
    global t,n
    c=t.count(old)
    assert c==1, f"{label}: found {c} occurrences"
    t=t.replace(old,new); n+=1
    print(f"OK  {label}")

# ---------- C1a: 1.1 table ----------
rep(
"""**36 quantum-relevant main-track regular papers** were presented across the three conferences — substantially more than the 9/10/12 a session-name-based reading suggests.

| | ASPLOS 2024 | ASPLOS 2025 | ASPLOS 2026 |
|---|---|---|---|
| **Quantum papers presented** | **14** | **10** | **12** |
| Papers presented (program) | ~193 | 184 (derived) | 168 |
| **Share of program** | **~7.3%** | **~5.4%** | **~7.1%** |
| Quantum papers by *proceedings* year | 15 | 8 | 11 |
| Regular papers in proceedings | 194 | 176 | 152 |
| **Share of proceedings** | **7.7%** | **4.5%** | **7.2%** |
| Dedicated quantum sessions | 2 | 2 | 3 (one only half quantum) |
| **Quantum papers OUTSIDE quantum sessions** | **5 of 14** | 0 of 10 | 0 of 12 |
| Papers with public artifact | 12 of 14 (86%) | 5 of 10 (50%) | 7–8 of 12 (58–67%) |""",
"""**36 quantum-relevant main-track regular papers** were presented across the three conferences — substantially more than the 9/10/12 that a census built from the published programs finds.

**Two denominators, never mixed.** The **proceedings** denominator rests on a volume enumeration; the **program** denominator is *arithmetic derived from the volume structure plus the deferral rule*, not a count taken from a program page. Block C reports separately what the conferences' own published programs actually show, which for 2024 is less than the whole program (§2.5, limitation 4).

| | ASPLOS 2024 | ASPLOS 2025 | ASPLOS 2026 |
|---|---|---|---|
| **A — Proceedings year** *(bibliographic)* | | | |
| Quantum papers by proceedings year | 15 | 8 | 11 |
| Regular papers in proceedings | 194 | 176 | 152 |
| **Share of proceedings** | **7.7%** | **4.5%** | **7.2%** |
| **B — Program year** *(volume-derived, not counted from a program)* | | | |
| **Quantum papers presented** | **14** | **10** | **12** |
| Papers presented (volume-derived) | ~193 `TOTAL_COUNT_UNVERIFIED` | 184 (derived) | 168 |
| Share of program (derived) | ~7.3% | ~5.4% | ~7.1% |
| **C — What the published program shows** | | | |
| Dedicated quantum sessions | 2 | 2 | 3 (one only half quantum) |
| Quantum papers locatable in the program | 9 of 14 | 10 of 10 | 12 of 12 |
| Program page retrievable in full? | **No — truncates after Session 8C** | Yes | Yes |
| Session placement of the remaining 5 | `STATUS_UNCLEAR` | — | — |
| Papers with public artifact | 12 of 14 (86%) | 5 of 10 (50%) | 7–8 of 12 (58–67%) |

The 2024 program denominator is marked `TOTAL_COUNT_UNVERIFIED` because it is 170 enumerated papers (29th V1–V3) plus the 28th-Volume-4 cohort that fed the 2024 program, whose size was never enumerated in this census. The proceedings row is the series with the firmer basis.""",
"C1a 1.1 table")

# ---------- C1b: F2 ----------
rep(
"""**F2 — ASPLOS 2024's quantum population was undercounted by more than a third, because 5 of its 14 quantum papers sat outside the two quantum-named sessions.**
A census built from session names finds 9. A sweep of the proceedings finds 14. The five that hide are **One Gate Scheme to Rule Them All** (ISA design), **MorphQPV** (verification), **OnePerc** (photonic compilation), **Fermihedral** (fermion-to-qubit encoding) and **Exploiting the Regular Structure… with Permutable Operators** (compilation). `[proceedings]` **This is the single most important methodological lesson of this census: at ASPLOS, session names are not a reliable census instrument.**""",
"""**F2 — ASPLOS 2024's quantum population is 14, not the 9 a program-based census finds — a 36% undercount, from two separable causes.**
A census built from the published ASPLOS 2024 program finds **9**, all inside *Session 5D: Quantum Architecture* (5) and *Session 6D: Variational Quantum Computing* (4). A sweep of the volumes finds **14**. The five a program-based census misses are **One Gate Scheme to Rule Them All** (ISA design), **MorphQPV** (verification), **OnePerc** (photonic compilation), **Fermihedral** (fermion-to-qubit encoding) and **Exploiting the Regular Structure… with Permutable Operators** (compilation). `[proceedings]`

Two causes, and they must be kept apart:

1. **The official ASPLOS 2024 program page is incomplete.** It lists sessions 1A–8C and then stops mid-track; no session after 8C appears anywhere on it. `[official-program]` A substantial part of the program is therefore unretrievable, and **none of the five can be located on that page — but neither can they be shown to be absent from the program.** Their session placement is `STATUS_UNCLEAR`.
2. **Permutable Operators is a deferred paper** — 28th ASPLOS Volume 4, proceedings year 2023, presented in 2024 — so no sweep of the 2024-branded volumes would find it either.

**The methodological lesson stands, but it is about instruments rather than sessions: at ASPLOS neither session names nor the conference's own program page is a sufficient census instrument. Only a volume sweep combined with the deferral rule is.** An earlier draft of this census stated that the five "sat outside the two quantum-named sessions"; that was an inference the evidence does not carry, and it has been withdrawn (Appendix A, C1).""",
"C1b F2")

# ---------- C1c: F3 ----------
rep(
"""Corrected shares are **7.3% → 5.4% → 7.1%** by program year (7.7% → 4.5% → 7.2% by proceedings year). A prior reading reported""",
"""By proceedings year — the series with the firmer denominator — the shares are **7.7% → 4.5% → 7.2%**. By program year, on volume-derived denominators, they are **~7.3% → ~5.4% → ~7.1%**. Both series are flat with a 2025 dip; neither is a program-page count. A prior reading reported""",
"C1c F3")

# ---------- C1d: line 108 totals ----------
rep(
"""**Totals.** Proceedings year: 2024 = **194**, 2025 = **176**, 2026 = **152**. Program year: 2024 ≈ **193**, 2025 = **184** (derived, see limitations), 2026 = **168** (the official program page states "167 unique papers"; the one-paper discrepancy is unresolved).""",
"""**Totals.** Proceedings year: 2024 = **194**, 2025 = **176**, 2026 = **152**.

Program year is **derived from this table plus the deferral rule, not counted from any program page**: 2025 = **184** (30th V1+V2 = 160, plus 29th V4 = 24) and 2026 = **168** (30th V3 = 16, plus 31st V1+V2 = 152; the official 2026 program page states "167 unique papers" and the one-paper discrepancy is unresolved). **2024 = 170 enumerated (29th V1+V2+V3) plus the 28th-Volume-4 cohort, which this census never enumerated** — hence ≈ **193**, marked `TOTAL_COUNT_UNVERIFIED`. Every program-year share below inherits that status.""",
"C1d totals")

# ---------- C1e: §3 header ----------
rep(
"""**Sessions** `[official-program]`: *Session 5D: Quantum Architecture* (5 papers) and *Session 6D: Variational Quantum Computing* (4 papers). **Five further quantum papers were distributed across non-quantum sessions** and are recoverable only from the proceedings.""",
"""**Sessions** `[official-program]`: the retrievable part of the 2024 program (sessions 1A–8C; the page stops there) contains two quantum-named sessions — *Session 5D: Quantum Architecture* (5 papers) and *Session 6D: Variational Quantum Computing* (4 papers), 9 papers in total. **The five further quantum papers below are established by the volume sweep, not by the program page; where they were scheduled is `STATUS_UNCLEAR`** because the program page truncates before the end of the conference.""",
"C1e sec3 header")

# ---------- C1f: §6.1 ----------
rep(
"""14 → 10 → 12 papers; 7.3% → 5.4% → 7.1% of program. **The corrected numbers do not support a growth narrative.**""",
"""14 → 10 → 12 papers presented; ~7.3% → ~5.4% → ~7.1% on volume-derived program denominators, 7.7% → 4.5% → 7.2% by proceedings year. **On either denominator the corrected numbers do not support a growth narrative.**""",
"C1f sec6.1")

open(p,'w',encoding='utf-8').write(t)
print(f"\n{n} edits applied")

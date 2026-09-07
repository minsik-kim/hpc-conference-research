# ASPLOS volume structure — VERIFIED 2026-09-06 (foundational finding)

ASPLOS runs 3 submission cycles (Spring/Summer/Fall). The FALL cycle's accepted papers are
published in a volume branded year N but PRESENTED at conference year N+1.
Verbatim, ASPLOS 2024 CFP: "Accepted major revisions of the fall cycle will be published as
ASPLOS'24 papers but will be presented in ASPLOS'25."

| Conf year | Edition | Volumes (DOI stem) | Raw | Non-papers | REGULAR PAPERS |
|---|---|---|---|---|---|
| 2024 | 29th | 10.1145/3617232 (V1) | 28 | 0 | 28 |
| 2024 | 29th | 10.1145/3620665 (V2) | 76 | 0 | 76 |
| 2024 | 29th | 10.1145/3620666 (V3) | 70 | 4 | 66 |
| 2024 | 29th | 10.1145/3622781 (V4) | 24 | 0 | 24  <- PRESENTED AT ASPLOS 2025 |
| 2025 | 30th | 10.1145/3669940 (V1) | 72 | 0 | 72 |
| 2025 | 30th | 10.1145/3676641 (V2) | 88 | 0 | 88 |
| 2025 | 30th | 10.1145/3676642 (V3) | 19 | 3 | 16  <- PRESENTED AT ASPLOS 2026 |
| 2026 | 31st | 10.1145/3760250 (V1) | 20 | 0 | 20 |
| 2026 | 31st | 10.1145/3779212 (V2) | 135 | 3 | 132 |

TWO LEGITIMATE DENOMINATORS — they differ and must never be mixed:
(A) PROCEEDINGS year (bibliographic): 2024=194, 2025=176, 2026=152
(B) PROGRAM year (presented) — ALL DERIVED from this table + the deferral rule,
    none counted from a program page:
      2024 = 170 (29V1+V2+V3) + |28V4| NEVER ENUMERATED  => ~193 TOTAL_COUNT_UNVERIFIED
      2025 = 30th V1+V2 (160) + 29th V4 (24) = 184
      2026 = 30th V3 (16) + 31st V1+V2 (152) = 168  (page says "167 unique")

PROVENANCE OF THESE COUNTS (stated because it limits them):
  Crossref REST read through WebFetch; curl egress and ACM DL are blocked.
  Crossref exposes NO volume-level item count and its container-title filter is
  SILENTLY IGNORED — no count here comes from it. Counts = date-windowed
  prefix:10.1145 queries, cursor=* deep paging, filtered client-side on DOI stem.
  Item-level records RETAINED ONLY FOR 2024 (170 DOIs: 29V2=76, 29V3=70, 29V4=24).
  2025/2026 retained extracts are PARTIAL (30V1 70/72, 30V2 87/88, 31V2 125/135)
  => those totals are single-source, read as +/- a few papers.
  29V2 is NOT gap-free: 76 items, gap at 3640398, out-of-range 3640665.
  29V3 = 3651322-3651387 (66) + keynotes 3655589-3655592 (4) = 70.
  29V4 = 3674167-3674190 less 3674187, plus 3698899 = 24.

Prior-survey claim 193/177/152 -> 2024 REFUTED (194), 2025 REFUTED (176), 2026 CONFIRMED (152).
There is NO ASPLOS 2026 Volume 3: the 2026 CFP has only 2 cycles.
Trap: 10.1145/3818671.* = 18th GPGPU Workshop, shares 2026-03-22 pub date. NOT ASPLOS.

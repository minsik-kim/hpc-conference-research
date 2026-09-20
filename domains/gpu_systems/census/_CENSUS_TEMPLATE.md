# <VENUE> <YEAR> — GPU Census

census_status: `COMPLETE_CENSUS | PARTIAL_CENSUS | BLOCKED`
last_checked: <YYYY-MM-DD>
knowledge_as_of: <YYYY-MM-DD>

## 1. Population reconstruction (STEP A)

| Field | Value |
|---|---|
| official population count (main/regular research papers) | <N or UNKNOWN> |
| counted items excluded from population | <workshops / posters / tutorials / demos / BoF / keynotes / repro reports / GB finalists / industry / PhD forum / artifact-evaluation reports — with counts where known> |
| population source (primary) | <URL + source class> |
| population source (corroborating) | <URL + source class> |
| source class | `official-proceedings` \| `official-program` \| `publisher-proceedings` \| `bibliographic-index` \| `author-page` \| `search-engine` |
| enumeration completeness | `EXACT` \| `APPROXIMATE` \| `UNVERIFIED_TOTAL` |
| paper-type mixing notes | <how the venue labels types; how each was resolved> |

### 1.1 Population evidence notes

<How the count was obtained; any discrepancy between sources; anything left UNKNOWN.>

## 2. Broad GPU candidates (STEP B)

Screening was applied over the whole reconstructed population, not over the
seed list. Keyword hits were used only to order review, never to decide
relevance.

| # | Title (official) | Authors (first + et al.) | Session | DOI | Official URL | Public full text | Artifact/code | Screen reason |
|---|---|---|---|---|---|---|---|---|

## 3. Non-candidates with GPU keywords (screened out at STEP B)

| Title | Why not a GPU candidate |
|---|---|

## 4. Candidates found without GPU in the title

| Title | Where the GPU mechanism appears |
|---|---|

## 5. Seed-list reconciliation

| Seed entry (as given) | Resolution |
|---|---|

## 6. Unresolved / blocked items


# ID_NAMING_RULES

## Stable IDs

Once a source is assigned a stable ID (e.g. `SC24-13`, `ICS25-03`), that ID
is never changed and never reused for a different source, even if the
source is later reclassified, moved, or corrected.

## Current ID scheme

`<VENUE><YY>-<NN>` — e.g. `SC24-13` is the 13th cataloged source imported
from SC 2024. This scheme is preserved as-is for any corpus imported from
the pending external AI/HPC systems workspace; existing IDs from that
corpus must not be renumbered during import.

## Future: domain-prefixed IDs

A domain-prefixed ID scheme (e.g. `AIHPC-SC24-13`) may be introduced for
*new* sources added after this repository becomes multi-domain, to avoid
ambiguity once `hpc_systems_operations` and `hpc_quantum` acquire their own
corpora. This is a naming rule for future sources only:

- Do not retroactively rename existing IDs to fit a new scheme.
- If a domain prefix scheme is adopted, record the decision and its
  effective date in `GLOBAL_CHANGELOG.md`, and apply it only going forward.

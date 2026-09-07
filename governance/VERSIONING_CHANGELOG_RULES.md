# VERSIONING_CHANGELOG_RULES

Versioning in this repository is based on git history, not on filename
suffixes.

- Do not keep extending a document as `topic_v2.md`, `topic_v3.md`, etc.
  Edit the canonical file and let git history hold prior versions.
- If a historical snapshot is intentionally preserved as a separate file
  (e.g. because a decision explicitly needs to stay visible in its old
  form), the file must state that it is historical and name the current
  canonical file it was superseded by.

## Changelogs

Each domain keeps its own `CHANGELOG.md`. Repository-wide changes go in the
root `GLOBAL_CHANGELOG.md` instead. Example entry shape:

```
## 2026-11 — SC26 import

Added:
...

Changed:
...

Closed questions:
...

New questions:
...

Revalidated:
...
```

Where practical, topic and research-question documents record:

```
last_updated
last_checked
knowledge_as_of
```

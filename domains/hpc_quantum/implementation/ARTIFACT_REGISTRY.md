# ARTIFACT_REGISTRY — HPC & Quantum

**This domain's imported source project contains no implementation of its
own** — it analyzes other researchers' code and artifacts; it does not
ship any (`SOURCE_INVENTORY.md`'s classification: "Implementation /
code documents: 0 — `NOT_PRESENT_IN_SOURCE`"). This file exists to
preserve *provenance*, not to add implementation content.

## Third-party upstream repositories cloned during source verification (not imported)

The source project's authors cloned nine public upstream repositories
in a scratch workspace to spot-check artifact claims against paper claims
(~800 MB total). **These clones were not staged and are not copied into
this repository** — they are reproducible public code, not this project's
research output. Their identity is preserved here as provenance so any of
them can be re-cloned on demand.

| Repository (scratch dir name) | Remote | HEAD commit at verification time | Verifies claims for |
|---|---|---|---|
| `parallax` | `https://github.com/positivetechnologylab/Parallax.git` | `2b52b52c2c81` | PARALLAX (SC24) |
| `cudaq` | `https://github.com/NVIDIA/cuda-quantum.git` | `f907bc6b7369` | (dependency/reference during simulation-branch verification) |
| `atlas` | `https://github.com/quantum-compiler/atlas.git` | `93f3d6550d9d` | Atlas (SC24) |
| `atlas-artifact` | `https://github.com/quantum-compiler/atlas-artifact.git` | `dd1b6863876a` | Atlas (SC24) artifact evaluation |
| `quartz` | `https://github.com/quantum-compiler/quartz.git` | `c4abf876608b` | Atlas's Quartz submodule (hierarchical partitioning scheduler) |
| `qmlctn` | `https://github.com/PabloAndresCQ/qml-cutensornet.git` | `92119ea19b9c` | Matrix Product State Simulation paper (SC24) |
| `qonductor` | `https://github.com/manosgior/Qonductor-SC25.git` | `5d1ac8a90cd5` | Qonductor (SC25) |
| `qft` | `https://github.com/XiangyuG/qft_on_regular_architectures.git` | `5c01a0e51399` | QFT Kernels paper (SC24) |
| `qdockbank` | `https://github.com/qiqi-xingyi/QDockBank_.git` | `d056c6dcfe04` | QDockBank (SC25) |

## Artifact status recorded by the source (not this registry's own claim)

The two censuses' own artifact matrices (`SC_2024_2025_QUANTUM_HPC_CENSUS.md`
§9, `ASPLOS_2024_2026_QUANTUM_HPC_CENSUS.md` §12) are the authoritative
per-paper artifact status (`PUBLIC_CODE`, `PUBLIC_ARTIFACT`, `PARTIAL`,
`NO_PUBLIC_ARTIFACT_FOUND`, `UNKNOWN`) — this file does not restate or
re-derive that table. Notable finding preserved from source, not
re-verified here: across 36 ASPLOS papers, **exactly one** ships a hardware
description (Micro Blossom, Scala/SpinalHDL); Promatch claims an FPGA
synthesis result but publishes only C++/MPI.

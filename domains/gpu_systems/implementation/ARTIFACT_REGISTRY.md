# ARTIFACT_REGISTRY — gpu_systems

last_updated: 2026-09-19
last_checked: 2026-09-19

## What this records

Third-party source repositories that a deep analysis in this domain **checked out and read**, with the
commit the reading was pinned to. Per
[`governance/SOURCE_EVIDENCE_RULES.md`](../../../governance/SOURCE_EVIDENCE_RULES.md), an implementation
claim backed by one of these is `[code]` evidence, not `[inference]` from an architecture description.

Three cautions:

1. **A pinned commit is not the artifact the paper was evaluated with** unless the analysis says so. Several
   analyses record exactly this gap — for example the public `cupbop/CuPBoP` tree is the *baseline*
   framework and contains none of the paper's four optimisations, and the released RayFlex RTL exposes four
   opcodes with no B-tree opcode among them. Read the analysis, not just this table.
2. **This table was extracted mechanically** from the analyses' text, so a repository named near another
   repository's commit hash can be paired wrongly. Where the two disagree, **the analysis file is
   authoritative**, and it is the thing to cite.
3. Artifact-evaluation **badge** status is `UNKNOWN` throughout: badges are published in the ACM Digital
   Library, which was unreachable from the environment this corpus was built in.

## Registry

| Analysis | Repository | Pinned commit |
|---|---|---|
| [`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md) | `https://github.com/ucb-bar/virgo` | `dd03a7c87895a937ecbde30daf8aeddb583ec144` |
| [`GPU-ASPLOS25-01`](../corpus/GPU-ASPLOS25-01--virgo-cluster-level-matrix-unit.md) | `https://github.com/ucb-bar/virgo-kernels` | `dd03a7c87895a937ecbde30daf8aeddb583ec144` |
| [`GPU-ASPLOS25-81`](../corpus/GPU-ASPLOS25-81--lossless-floating-point-compression-cpus-gpus.md) | `https://github.com/burtscher/FPcompress` | `97f037249bd28682bfd83462ea1129e14df36d81` |
| [`GPU-ASPLOS26-01`](../corpus/GPU-ASPLOS26-01--mscclpp-gpu-communication-abstractions.md) | `https://github.com/microsoft/mscclpp` | `0d020627a1dc7328088bf6a95ff8c3dca48e3346` |
| [`GPU-ASPLOS26-141`](../corpus/GPU-ASPLOS26-141--tilus-tile-level-gpgpu-language-low-precision.md) | `https://github.com/NVIDIA/tilus` | `4597cd5ba3f24501ba411cefa61a76fd9d3ba2c8` |
| [`GPU-ASPLOS26-143`](../corpus/GPU-ASPLOS26-143--cheri-simt-capability-memory-protection-gpus.md) | `https://github.com/CTSRD-CHERI/SIMTight` | `6248c9b727d1f32280997492ecb0179d045eb674` |
| [`GPU-ASPLOS26-166`](../corpus/GPU-ASPLOS26-166--bullet-spatial-temporal-prefill-decode-sm-partitioning.md) | `https://github.com/zejia-lin/BulletServe` | `445afae2abc15d578d3107d37a9b57ebc49e5e46` |
| [`GPU-ICS25-01`](../corpus/GPU-ICS25-01--dream-device-driven-access-to-virtual-memory.md) | `https://github.com/nnurlan008/dream` | `8ed15b256f8ad88c88628c80cde06738349194e8` |
| [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md) | `https://github.com/szcompressor/cuSZp` | `16e164762fe67785f498a44bae7984058a7a6952` |
| [`GPU-ICS25-81`](../corpus/GPU-ICS25-81--aatrox-hierarchical-delta-gpu-lossy-compression.md) | `https://github.com/szcompressor/cuSZp` | `f581dcf329c907c320f4743a9c6e7ee2fb9c5494` |
| [`GPU-ICS26-106`](../corpus/GPU-ICS26-106--ocean-estimation-based-spgemm-hyperloglog.md) | `https://github.com/CornellHPC/Ocean-SpGEMM` | `cb093963f6e45d9deabf7848bc05a538af796315` |
| [`GPU-ICS26-81`](../corpus/GPU-ICS26-81--gpz-gpu-lossy-compressor-particle-data.md) | `https://github.com/szcompressor/cuSZp` | `16e164762fe67785f498a44bae7984058a7a6952` |
| [`GPU-IPDPS26-61`](../corpus/GPU-IPDPS26-61--microbenchmarking-nvidia-blackwell-b200.md) | `https://github.com/UD-CRPL/IPDPS_26_B200_Microbenchmark` | `91411b53aebaa4733477f22bde576b5182c669fc` |
| [`GPU-ISC26-182`](../corpus/GPU-ISC26-182--fine-grained-power-energy-attribution-amd-gpu-apu-exascale.md) | `https://github.com/hpc-ai-adv-dev/fastotf2` | `32b85fe8e62e68ecd1d913e82f66c514604fe564` |
| [`GPU-MICRO24-121`](../corpus/GPU-MICRO24-121--hsu-extending-rt-units-hierarchical-search.md) | `https://github.com/purdue-aalp/rayflex` | `de9d80c1e1a0a3a1d776f265bfe224b8eea0e183` |
| [`GPU-MICRO24-64`](../corpus/GPU-MICRO24-64--unleashing-cpu-potential-executing-gpu-programs.md) | `https://github.com/cupbop/CuPBoP` | `508bd62e928bea3b5f0633c8fa63b5f42f3b4da0` |
| [`GPU-MICRO25-61`](../corpus/GPU-MICRO25-61--dissecting-modeling-modern-gpu-cores.md) | `https://github.com/upc-arco/modern-gpu-simulator-micro-2025` | `117f9dca3f46b1d85d2a1ec9ddac6b89d49399b3` |
| [`GPU-PPoPP24-146`](../corpus/GPU-PPoPP24-146--gallatin-general-purpose-gpu-memory-manager.md) | `https://github.com/saltsystemslab/gallatin` | `f65a085414527c95c7197b724c90cb9740f105dc` |
| [`GPU-PPoPP25-128`](../corpus/GPU-PPoPP25-128--librts-spatial-indexing-library-ray-tracing.md) | `https://github.com/RTSpatial/RTSpatial` | `52509e8022abeab722f5a9a89d1917e8b481defe` |
| [`GPU-SC24-161`](../corpus/GPU-SC24-161--parvagpu-spatial-gpu-sharing-mig-mps-segments.md) | `https://github.com/MunQ-Lee/ParvaGPU_SC24` | `5f3de1e18582b4c81896a1c3eb0e2915238dfee6` |
| [`GPU-SC24-181`](../corpus/GPU-SC24-181--nvidia-built-in-power-sensor-energy-measurement.md) | `https://github.com/JimZeyuYang/GPU_Power_Benchmark` | `ab12c0606775e38872501de8a5cf57ca0e863fa1` |
| [`GPU-SC24-41`](../corpus/GPU-SC24-41--hirace-gpu-data-race-checking.md) | `https://github.com/JohnJacobsonIII/HiRace-Artifact-SC24` | `44a935f90acfe43c6178b2187ea84c9ab0c01450` |
| [`GPU-SC24-81`](../corpus/GPU-SC24-81--cusz-i-multi-level-interpolation-gpu-lossy-compression.md) | `https://github.com/JLiu-1/cusz-I` | `91e1bc546716f436a7781a96a3034696d1dc85b1` |
| [`GPU-SC25-81`](../corpus/GPU-SC25-81--agile-asynchronous-gpu-ssd-integration.md) | `https://github.com/arc-research-lab/AGILE` | `c644255b45f345fcd3c178159ab277ece2cb1d3d` |
| [`GPU-SC26-01`](../corpus/GPU-SC26-01--ozaki-ii-fp8-double-precision-gemm-emulation.md) | `https://github.com/RIKEN-RCCS/GEMMul8` | `e5db07fa0aa69435d1319d3e56b4c25e9a68d625` |

## Artifacts that exist but were not inspected

Recorded as `NOT_INSPECTED` in the analyses rather than described from the paper. The main ones are the
Cubie Zenodo artifact, `ucb-bar/virgo-kernels`, the GMLake repository, the TCCL Zenodo tarball (890.9 MB,
containing no paper PDF), the RTSpMSpM artifact (inspected for its OptiX primitive encoding but with no
reachable paper text), and the `zenodo.org` deposits referenced by several MICRO 2024/2025 papers.
No symbol, file name or behaviour is asserted anywhere in this domain from a repository that was not read.

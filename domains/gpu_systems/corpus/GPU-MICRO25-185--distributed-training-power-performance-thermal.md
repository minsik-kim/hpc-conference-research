# GPU-MICRO25-185 — Characterizing the Efficiency of Distributed Training: A Power, Performance, and Thermal Perspective

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (+ `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` caveat, see below)
primary_topic: `P — GPU power, energy, DVFS, thermal & energy attribution`
secondary_topics: `O — production/cluster telemetry; multi-GPU parallelism strategy`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER via arXiv HTML (arxiv.org/html/2509.10371v1) — authors/affiliation, abstract, motivation, the instrumentation description (NVML + modified Zeus; AMD-SMI extended via Zeus; Chakra profiler), the three cluster configurations, the model/parallelism matrix, the thermal-imbalance and throttling results, the microbatch/peak-power results, the LoRA and recomputation results, the stated limitations, and related work. NOT read line-by-line: every figure panel (Figs. 17 and 19 were read as described in text), and the Astra-Sim projection methodology.`

---

## PRIOR-CORPUS NOTE

No existing analysis in this repository. **`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING` (not imported)**; this paper's relatives on the LLM-serving power axis (DynamoLLM, TAPAS, POLCA) belong to that population, so **no claim is made here about what that corpus does or does not contain** — flag `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`. The paper itself is a *training* characterisation on named GPU hardware and is analysed on that basis.

## 12.1 Bibliographic facts

- Official title: *Characterizing the Efficiency of Distributed Training: A Power, Performance, and Thermal Perspective* [paper].
- Authors: **Seokjin Go, Joongun Park, Spandan More, Hanjiang Wu, Irene Wang, Aaron Jezghani, Tushar Krishna, Divya Mahajan** — all **Georgia Institute of Technology** [paper].
- Venue: **MICRO 2025**, Session 4A "Systems for AI (Training)". DOI `10.1145/3725843.3756111` (`census/MICRO_2025.md:40`).
- Publication type: `ARCHIVAL_MAIN_PAPER`; read as `PREPRINT` (arXiv `2509.10371v1`).
- Artifact: `NOT_FOUND_AFTER_SEARCH` in the text read. The measurement stack is built on **Zeus** (modified) and the **Chakra** profiler, both third-party.

## 12.2 Core question (one sentence)

When a parallelism strategy is chosen for LLM training, what does it do to the *physical* behaviour of the GPUs — peak power, temperature distribution across the chassis, and thermally induced clock throttling — and does the algorithmically optimal choice stay optimal once those effects are counted? [paper]

## 12.3 GPU/HPC problem translation

- **Scheduling / parallelism.** TP, PP, DP, EP, FSDP combinations and microbatch size are the independent variables.
- **Thermal and power.** The dependent variables are per-GPU temperature, clock frequency, throttling incidence and power draw — physical quantities, measured per device.
- **Communication.** Bandwidth underutilisation under certain TP+PP combinations is a named finding.

## 12.4 Why the problem exists (hardware root cause)

Three causes, all below the level at which ML-systems papers normally look [paper]:

1. **Air-cooled chassis airflow is front-to-back, so GPUs are not thermally equivalent.** Rear GPUs sit in the exhaust of the front ones and reach **up to 27 % higher temperature** than front GPUs in the HGX systems. On MI250 there is additionally a **5–10 °C skew *within* the GPU package** from airflow asymmetry. The physical slot a rank lands in becomes a performance variable.
2. **Throttling is the enforcement mechanism.** Rear GPUs show **reduced clock frequencies** under thermal constraint, which turns a chassis-position asymmetry into an execution-time straggler in a synchronous collective.
3. **Parallelism strategy changes the thermal load.** Deep pipeline parallelism raises **threadblock and warp counts** through asynchronous execution, elevating thermal load; tensor-parallel-heavy configurations maintain high occupancy but *fewer* threadblocks/warps and throttle less, at the cost of communication overhead. Compute–communication overlap **consistently raises peak temperature** because it stresses the memory and SM subsystems simultaneously rather than alternately.

## 12.5 Mathematical / performance model

NOT_IN_PAPER as a model paper — it is a characterisation. Beyond the test clusters, datacenter-scale behaviour is *projected* with **Astra-Sim**, explicitly not empirically validated at that scale (stated limitation). **Any Astra-Sim figure from this paper is a simulation result, not a measurement.**

## 12.6 Data layout and ownership

| Cluster | GPU | Count | Memory each | Nodes | Intra-node | Inter-node | TDP |
|---|---|---|---|---|---|---|---|
| HGX **H200** | NVIDIA H200 | 32 | 141 GB HBM3 | 4 | NVLink | 100 Gbps IB | 700 W |
| HGX **H100** | NVIDIA H100 | 64 | 80 GB HBM3 | 8 | NVLink | 100 Gbps IB | 700 W |
| **MI250** | AMD MI250 (4×2 GCDs per node) | 32 | 2×64 GB HBM2e | 4 | xGMI | 100 Gbps IB | 500 W |

All **air-cooled**, front-to-back airflow. Models: GPT-3 (175B, 30B), Llama-3 (70B, 30B), Mixtral (8×22B, 8×7B), FP16/BF16, global batch size 128. TP is confined within a node; PP spans nodes; DP takes the remainder. AMD runs are restricted to 30B models because of availability and lower memory capacity.

## 12.7 Pseudo code

Not an algorithm paper; no pseudo code is warranted. The experimental protocol is: warm up **10 iterations** (discarded, for temperature and activity to stabilise), then profile subsequent iterations with Chakra while Zeus samples NVML / AMD-SMI [paper].

## 12.8 Real implementation — the instrumentation chain

Stated explicitly because it is this paper's weakest link [paper]:

| Element | What the paper says |
|---|---|
| NVIDIA sensor | **NVML**, read through a **modified version of Zeus** |
| AMD sensor | **AMD-SMI**, extended via Zeus |
| Execution profiler | **Chakra**, PyTorch 2.6.0 |
| Metrics | core and memory temperature, per-component utilisation, PCIe bandwidth, GPU power draw, clock frequency |
| **Sampling rate** | **NOT STATED** — the paper does not disclose the NVML/AMD-SMI polling rate or the averaging treatment |
| Warm-up | first 10 iterations discarded |
| **External ground truth** | **NONE** — no PDU, wall meter or oscilloscope; the limitations section concedes this |

No `[code]` evidence: no artifact repository for the modified Zeus was located.

## 12.9 Kernel execution

Not resolved to kernels. The execution-level variable the paper actually tracks is **threadblock and warp count**, which it uses as the causal link from pipeline depth to thermal load [paper].

## 12.10 Memory traffic

Treated through PCIe bandwidth and the observation that certain **TP+PP combinations cause bandwidth underutilisation**. HBM traffic per se is not instrumented.

## 12.11 Findings (decomposed cause)

Each finding carries its hardware qualifier — all are air-cooled 32–64-GPU clusters:

1. **Thermal imbalance is positional and persistent.** Up to **27 % temperature differential between rear and front GPUs** (HGX H100/H200); **5–10 °C intra-package skew** on MI250. Rear GPUs show *no clear cooldown periods*.
2. **Throttling scales with pipeline depth.** PP16–32 configurations throttle more; TP-heavy configurations throttle less. Mechanism: asynchronous PP execution raises threadblock/warp counts.
3. **Microbatch size raises peak power whether or not it raises throughput.** Beyond the optimal point, execution becomes **bursty**, intermittently under-utilising compute while raising **peak power excursions**, which worsens throttling. This is the paper's cleanest actionable result: a tuning knob that looks free in a throughput-only view is not free physically.
4. **Compute–communication overlap consistently increases peak temperature** and throttling metrics.
5. **Activation recomputation cuts both ways** — it reduces throttling in deep-PP GPT3-175B by lowering pressure, but *increases* it in data-parallel Llama3-70B.
6. **LoRA fine-tuning lowers GPU power and temperature while achieving over 10× higher training efficiency** — the only configuration in the study that improves all three axes at once.
7. **Scale-up beats scale-out in communication-bound regimes** under careful tuning: fewer, higher-memory GPUs can win.
8. **An actual power failure during the study made GPUs run more than 4× slower**, producing severe stragglers — reported as an observed event, not an experiment.

## 12.12 Hardware generation dependence

Three SKUs across two vendors (H100, H200, MI250). The thermal results are **chassis-dependent as much as GPU-dependent**: they are properties of air-cooled HGX and 4-node MI250 systems with front-to-back airflow, and would not transfer unchanged to direct-liquid-cooled H100 or to MI300A nodes.

## 12.13 Limitations (authors' own, plus review)

1. **Scale:** 32–64 GPUs; anything larger is Astra-Sim projection, not measurement.
2. **AMD coverage is not matched** — smaller 30B models only, due to availability and memory capacity.
3. **No external ground truth** for thermal or power; manufacturer telemetry only.
4. **Sampling rates for NVML/AMD-SMI are not disclosed**; warm-up fixed at 10 iterations.
5. Findings are specific to 100 Gbps interconnects; 800 Gbps is projected, not tested.
6. Inference analysis is limited to a microbatch sweep.

**Review-side, and it is material here.** Limitation 4 is not a presentational gap. `GPU-SC24-181` establishes that on **H100** — two of this paper's three clusters — `nvidia-smi`/NVML's `power.draw.instant` observes **25 ms of every 100 ms** while `power.draw.average` applies a **1-second** average, and that a script written for an older part silently changes which of those it gets. This paper's headline power claim is about **peak power excursions from bursty execution**. A **1 s average would erase such excursions entirely**, and a 25 %-duty-cycle instant reading would capture them only by luck of phase. Without the field name and the polling rate, the *direction* of finding 3 is credible (bursty execution raises peak power) but its *magnitude* cannot be audited, and the possibility that true excursions are considerably larger than reported is live `[inference, grounded in GPU-SC24-181's measured W/T values for H100]`. Temperature readings are not subject to the same objection.

## 12.14 Relation to prior corpus

- **`GPU-ICS24-01` (Summit) — the most consequential connection in this cluster.** That paper established on 27,648 V100s that GPU memory double-bit errors correlate with short-term **power *swings*** (a ~33 W range over 15 minutes, p = 0.00056 after Šidák correction), **not** with temperature level. This paper independently shows that a purely *software* choice — microbatch size past its optimum, or deep pipeline parallelism — manufactures exactly that signal: bursty execution with peak power excursions, on every GPU in the job. Putting the two together yields a hypothesis this corpus can now state and neither paper states alone: **parallelism-strategy tuning may be a controllable input to GPU memory-reliability risk, via the power-swing pathway** `[inference, grounded in both papers' measured quantities — not asserted by either]`. Testing it needs DBE telemetry from a cluster whose parallelism configuration is known, which is precisely the data OLCF released for Summit.
- **Complementary to `GPU-ISC26-182`.** That paper supplies the instrument this one lacks: 1 ms power reconstructed by differentiating an energy counter, with a confidence window that says which samples may be attributed to a phase. Applying it to the microbatch-burstiness question would convert finding 3 from a direction into a magnitude.
- **`GPU-IPDPS26-41` / `GPU-IPDPS26-42`** (production GPU workloads and telemetry; elusive application performance) sit on the same production-characterisation axis, at cluster rather than chassis scale.
- **Related-work lineage from this paper's own citations:** DynamoLLM and TAPAS are named as power-aware *inference/serving* systems and explicitly distinguished from training, which the authors characterise as synchronous and tightly coupled; MegaScale, AxoNN and Pythia are named as prior LLM-training studies that examine software or aggregate metrics without system-level power/thermal characterisation.

---

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The findings are about **per-GPU thermal and clock behaviour inside a specific accelerator chassis** — rear-vs-front temperature differential in an air-cooled HGX, intra-package skew across an MI250's two GCDs, and thermally induced **GPU clock throttling** measured per device — and the causal chain runs through **threadblock and warp counts** driving SM thermal load. The measurements come from **NVML** and **AMD-SMI** per-GPU sensors. None of this is expressible for a CPU or a generic accelerator.

verdict: `CORE_GPU`

*(Measurement caveat carried forward: the NVML/AMD-SMI sampling rate and query field are undisclosed — see 12.13.)*

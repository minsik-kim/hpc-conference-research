# Classification brief — virtualization literature landscape 2024-2026

Purpose of the corpus: a reusable knowledge base so that reading ONE core virtualization
paper also gives you its technical background, the layer below and above it, alternative
mechanisms, trade-offs, and real cloud/HPC usage. This is NOT an exercise in pruning.
Broad preservation beats aggressive pruning. Accuracy beats completeness.

## The four layers

CORE — virtualization / isolation / virtual-resource abstraction IS the main contribution.
  VM/VMM/hypervisor, nested virtualization, vCPU, guest-host interface, VM memory
  virtualization, ballooning, live migration, VM introspection, SR-IOV, IOMMU, device
  passthrough, virtio/vSwitch, device virtualization, confidential VM, secure container
  architecture, unikernel, GPU virtualization, MIG/MPS abstraction, FPGA virtualization,
  accelerator virtualization, virtual firmware, any explicit resource virtualization.
  A paper stays CORE even if another corpus already analysed it.

SUPPORT — virtualization is not the headline, but knowing this paper lets you explain a
  CORE paper's architecture, design choice, or trade-off better. Decisive question:
  "does knowing this let me explain some CORE paper's design choice or trade-off better?"
  Typical: GPU interference, GPU preemption, spatial/temporal sharing, GPU fragmentation,
  checkpoint/restore, device migration, VM placement constrained by virtualization
  semantics, container networking mechanism, container image/runtime mechanism, serverless
  runtime isolation, memory/resource partitioning, CXL/device pooling, accelerator-sharing
  primitives.

CONTEXT — higher-level systems/application research that USES virtualized infrastructure.
  Keep it if it helps explain: why the abstraction is needed; what application-level
  problems multi-tenancy creates; how sharing/isolation affects SLOs; how real cloud/HPC
  infrastructure actually uses virtualization. Generic serverless scheduling, FaaS
  workflows, autoscaling, LLM serving, Kubernetes/microservice/GPU-cluster scheduling,
  cloud cost or carbon optimization normally land here.

DROP — conservative. Only: (1) no substantive relation to virtualization; (2) keyword false
  positive; (3) pure virtual-memory research with no link to machine/resource
  virtualization; (4) publication-criterion mismatch; (5) clear duplicate; (6) already
  deeply analysed elsewhere as CONTEXT with no added virtualization value; (7) generic
  application paper filling none of the three roles. Ambiguous -> CONTEXT.

## Known threshold traps (you will hit these)
- A paper that merely runs inside a VM or container is NOT a virtualization paper.
- GPU *sharing* is usually SUPPORT; it is CORE only when the contribution is the virtual
  GPU abstraction itself (a vGPU/MIG-like partition mechanism, GPU state virtualization,
  GPU checkpoint of virtualized state), not merely a scheduler over existing GPUs.
- Container *runtime/image* mechanism (image pull, layering, filesystem) is SUPPORT;
  container *isolation architecture* (microkernel/split-kernel/unikernel/sandbox boundary,
  syscall interposition as an isolation boundary) is CORE.
- Serverless: separate the mechanism that makes isolation cheap (snapshot/restore, memory
  reclamation, runtime isolation = CORE or SUPPORT) from a system that merely consumes
  serverless (CONTEXT).
- Disaggregation (CXL/far memory) is not virtualization by itself; it is CORE only when
  the paper builds a *virtual* resource abstraction over the disaggregated pool (e.g.
  elastic guest-physical memory), otherwise SUPPORT.
- Pure virtual memory / page-table work is DROP unless it touches nested translation,
  guest physical address space, or hypervisor-mediated memory.

## Publication criteria
Main corpus = main conference, regular/full, peer-reviewed, archival research paper.
Exclude workshop, poster, demo, short paper, extended abstract, tutorial, panel, doctoral
symposium, invited/industry-vendor presentation — but RECORD each exclusion with evidence.
OSDI-style "Operational Systems"/"Deployed Systems" tracks and clearly-labelled industry
tracks are archival and valuable: keep them as publication_type OPERATIONAL_REFERENCE or
INDUSTRY_TRACK, classified normally, but never counted in regular-research statistics.

## Taxonomy (one primary, secondaries as needed)
T1 CPU/machine virtualization (VM, VMM, hypervisor, nested, vCPU)
T2 Memory virtualization (guest memory, nested translation, ballooning, dedup, reclamation,
   tiered/disaggregated VM memory)
T3 I/O and device virtualization (IOMMU, SR-IOV, passthrough, virtio, vSwitch, NIC, NVMe,
   RDMA, SmartNIC, DPU)
T4 Migration/checkpoint/state (VM live migration, device-state migration, container
   migration, GPU checkpoint/restore)
T5 Container/lightweight isolation (namespace/cgroup, microkernel containers, unikernels,
   sandboxing, Wasm isolation)
T6 Accelerator virtualization (GPU virtualization, MIG, MPS, GPU multiplexing, FPGA
   virtualization, accelerator sharing)
T7 Confidential/security isolation (confidential VM, protected VM, trusted I/O, firmware
   virtualization, hypervisor correctness)
T8 Serverless/cloud abstraction (FaaS, cold start, serverless runtime, elastic execution)
T9 Resource management/multi-tenancy (placement, scheduling, interference, QoS,
   oversubscription, partitioning)
T10 Boundary/other (conceptually useful adjacent virtualization/isolation mechanisms)

## Read every paper as a mapping problem
Physical Resource -> Logical Resource Abstraction -> Workload. For each paper capture:
- Isolation: how is security/performance interference between tenants bounded?
- Multiplexing: how is one physical resource divided among consumers?
- Translation/Mediation: what extra path does the virtualization layer introduce?
  (e.g. GVA -> GPA -> HPA, or Guest -> VMM -> Device)
- State: where does virtualization state live, and how does it move on migration/checkpoint?
- Performance trade-off: record the structural shape, e.g. passthrough lowers software
  mediation cost but makes isolation, memory management and live migration harder.

## Reading priority (independent of layer)
P0 essential to learn the virtualization stack at all.
P1 important to understand one branch properly.
P2 supporting, consult when you go down that branch.
P3 landscape / operational context.
CORE is not automatically P0. A SUPPORT paper that explains a major architectural
trade-off can be P1.

## Evidence priority
1 published full paper / official proceedings version
2 author preprint or accepted manuscript
3 official conference program / abstract
4 artifact / code / documentation
5 existing corpus analysis
6 prior chat/session notes
Prohibited: final classification from title alone; copying prior CORE/BROAD/EDGE labels;
treating a prior corpus summary as having read the paper; forcing an ambiguous paper into a
layer from the abstract alone; "we analysed this before so it must be X".

## Depth expectation
CORE, SUPPORT, P0, P1 -> ideally abstract + introduction + architecture/design + relevant
implementation + evaluation setup + conclusions/limitations.
CONTEXT, P2, P3 -> abstract + introduction is acceptable when the role is clear.
Technically ambiguous -> read deeper before deciding.
Verify any number you record against the actual paper. Do not propagate numbers from
secondary summaries.

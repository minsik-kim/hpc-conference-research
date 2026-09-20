# GPU-SC24-82 — Hydrogen: Contention-Aware Hybrid Memory for Heterogeneous CPU-GPU Architectures

gpu_relevance: `RELATED_GPU` — **re-adjudicated from full text; the memory cluster's abstract-only `RELATED_GPU` is CONFIRMED, not overturned. See "Re-adjudication record" below.**
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `E HBM & data movement`
secondary_topics: `memory virtualization / hybrid-memory tiering (cross-cluster: _LEDGER_memory_virtualization.md)`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `Author-hosted PDF (people.iiis.tsinghua.edu.cn/~gaomy/pubs/hydrogen.sc24.pdf) read in two targeted passes: (1) title/authors/affiliations/abstract, introduction and motivation, hardware assumptions and memory organisation, and all four design components; (2) evaluation — simulator, modelled CPU/GPU/memory configuration, workloads, baselines, results, ablation, hardware overhead, related work. Author slide deck (people.iiis.tsinghua.edu.cn/~gaomy/pubs/slides/hydrogen.sc24.slides.pdf) located but NOT read.`

## 12.1 Bibliographic facts
- Title: *Hydrogen: Contention-Aware Hybrid Memory for Heterogeneous CPU-GPU Architectures* `[paper]`.
- Authors and affiliations `[paper]`: Yiwei Li, Mingyu Gao — Tsinghua University; Shanghai Qi Zhi Institute (Gao).
- Venue: **SC 2024**, DOI `10.1109/SC41406.2024.00017` `[census]`.
- Publication type: `ARCHIVAL_MAIN_PAPER`. The read source is an author-hosted copy of the paper — full-paper evidence, `[paper]`.
- Artifact: none named. `NOT_INSPECTED`.
- **`prior_corpus_check`**: `_LEDGER_memory_virtualization.md` records Hydrogen among the papers plausibly belonging to the `EXTERNAL_IMPORT_PENDING` ~80-paper AI/HPC corpus under `domains/ai_hpc_systems/`. **No claim of non-duplication is made.** `[repo-grep]`

## Re-adjudication record
`_LEDGER_memory_virtualization.md` line 58 records Hydrogen as `ABSTRACT_ONLY` / `RELATED_GPU`, with an explicit re-check instruction: "reclassify to `CORE_GPU` if the full text shows the mechanism keys on GPU-specific behaviour such as **warp-level migration triggers or GPU page-fault semantics**".

**Full text obtained and read. The verdict `RELATED_GPU` is CONFIRMED. It should not be reclassified.** The paper's own justification for treating the GPU differently is a *statistical* property, not a structural one: "GPUs, benefiting from thread-level parallelism, are more bandwidth-driven and can tolerate longer memory access latencies" `[paper]`. The token-based throttle "targets GPU-induced migration broadly without keying on warp-level triggers, GPU page faults, memory coalescing patterns, or TLB behavior" — it counts aggregate GPU-induced refills and dirty writebacks at the memory controller. The memory cluster's abstract-only reading ("substituting another bandwidth-hungry accelerator for the GPU would leave the design substantially intact") is exactly right, and the full text supplies the confirming evidence rather than contradicting it.

Two details the abstract could not have supplied, and which strengthen the `RELATED_GPU` call rather than weakening it:
1. **The GPU modelled is an integrated Intel Xe-LPG-class iGPU with 96 Execution Units**, not a discrete HBM-attached datacenter GPU. The "GPU" here shares a last-level cache with the CPU.
2. **HBM is the *fast tier of a two-tier main memory shared with the CPU*** (HBM2E 16 channels + DDR4-3200 4 channels), not a GPU's dedicated device memory. So even the HBM axis — this cluster's organising topic — is present in a form quite different from the discrete-GPU HBM the rest of the cluster studies.

Neither fact was available from the abstract; both are recorded here as the substantive addition this re-read makes.

## 12.2 Core question (one sentence)
When a CPU and a GPU share a hardware-managed HBM+DDR hybrid memory, they want opposite things from the fast tier — the CPU wants capacity, the GPU wants bandwidth — so can capacity and bandwidth be allocated *independently* rather than being coupled by the usual channel-partitioning? `[paper]`

## 12.3 GPU/HPC problem translation
- **Memory**: the whole paper. A two-tier main memory in **cache mode**, hardware-managed, behind a shared LLC.
- **Compute**: CPU cores and GPU EUs are the two contending clients; neither is modified.
- **Synchronization**: none.
- **Communication**: none (single node, integrated).
- **Scheduling**: an epoch-based online hill-climbing search over three allocation parameters is the control loop.

## 12.4 Why the problem exists
Root causes the paper names `[paper]`:
1. **Divergent preferences.** "CPUs and GPUs exhibit distinct preferences for the fast memory resources. **CPUs prefer larger fast memory capacity while GPUs require higher fast memory bandwidth.**" The stated reason for the GPU side is latency tolerance through thread-level parallelism.
2. **Conventional partitioning couples the two.** Partitioning fast memory by channel gives a client capacity and bandwidth in fixed proportion. There is no way to give the GPU many channels' bandwidth while giving the CPU most of the capacity.
3. **Migration into the fast tier consumes slow-tier bandwidth.** A GPU that aggressively pulls data into HBM burns DDR4 bandwidth on refills and dirty writebacks, degrading the CPU. This is the contention the token mechanism addresses.
4. **The hardware setting**: "heterogeneous processor like **Intel Xe-LPG** is connected to hybrid HBM and DDR memories", with **HBM2E as fast memory and DDR4 as slow memory**, in **cache mode** where "the fast memory is fully hardware managed" behind the shared LLC.

## 12.5 Mathematical / performance model
No closed-form model. The design is parameterised by three knobs searched online `[paper]`:
- **`cap`** — fast-memory capacity allocation ratio,
- **`bw`** — fast-memory bandwidth allocation ratio,
- **`tok`** — migration allowance (the token budget).

Token accounting is exact `[paper]`: a GPU-induced migration consumes **1 token for each refill, and 2 if there is also a dirty writeback**; when the counter reaches zero "further migrations for GPU accesses would be suppressed"; a periodic **"token faucet"** replenishes it adaptively.

Search: "an online, **epoch-based hill climbing algorithm**" over (`cap`, `bw`, `tok`), with a sampling epoch of **10M cycles**, optimising a **weighted IPC** objective until convergence `[paper]`.

## 12.6 Data layout and ownership
The key structural idea, and the paper's real contribution `[paper]`:
- The fast memory is a **set-associative hardware-managed cache**. Rather than mapping a partitioned dimension directly onto channels, Hydrogen uses "a novel **mapping scheme from ways/sets to channels**".
- **Ways associate with channels**, which is what gives **bandwidth isolation** — a client restricted to a subset of ways touches only a subset of channels.
- **CPU data additionally occupies ways from shared channels**, which is what gives it **extra capacity without extra dedicated bandwidth**. This is the decoupling: bandwidth comes from which channels you own, capacity comes from how many ways you occupy across both dedicated and shared channels.
- A **"fast memory swap"** relocates the hottest CPU data between the dedicated and shared channel hierarchies.
- **No GPU-internal ownership level appears anywhere.** There is no thread, warp, CTA, or SM in this design. The finest GPU-side granularity is "GPU accesses" as seen at the memory controller.

## 12.7 Pseudo code
Reconstructed `[reconstruction]`, using only the paper's parameter and mechanism names `[paper]`:
```
# ---- steady state, per fast-memory access ----
way = select_way(addr, client)          # ways -> channels mapping gives bandwidth isolation
                                        # CPU may also occupy ways on SHARED channels -> extra capacity
on miss:
    if client == GPU:
        cost = 1 + (1 if dirty_writeback else 0)     # 2 if a dirty writeback is also needed
        if token_counter < cost:  suppress the migration   # serve from slow memory instead
        else:                     token_counter -= cost;  migrate
    else:
        migrate                                      # CPU migrations are not throttled

periodically: token_faucet()            # adaptive replenishment of token_counter

# ---- control loop, every 10M-cycle sampling epoch ----
sample weighted_IPC for the current (cap, bw, tok)
hill_climb: perturb one of cap / bw / tok; keep the change if weighted_IPC improves
on (cap, bw) change:
    consistent hashing            -> minimise the set of blocks that must move
    lazy layout change            -> a misaligned block moves only when next accessed,
                                     off the critical path
```

## 12.8 Real implementation
**No artifact, no RTL, no real hardware.** The evaluation is entirely simulation in **zsim** `[paper]`. `NOT_INSPECTED`. No code symbol is asserted.
Hardware cost as reported `[paper]`: "**one extra `alloc` bit per way**", for **0.049% metadata storage overhead**, plus "only minor hardware changes" — registers and simple configuration logic.

## 12.9 Kernel execution
`NOT_APPLICABLE`. Hydrogen adds no kernel and changes nothing above the memory controller. **This is itself the evidence for the verdict**: the paper contains no kernel-, warp-, CTA- or SM-level mechanism at all.

## 12.10 Memory traffic
- **Two tiers**: fast **HBM2E, 16 channels at 1600 MHz**; slow **DDR4-3200, 4 channels at 1600 MHz** `[paper]`. The 16:4 channel ratio is the resource being partitioned.
- **Shared LLC**: 16-way, **16 MB**, 38-cycle latency `[paper]` — shared by CPU and GPU, which is only possible in an integrated part.
- **The traffic Hydrogen actually controls is *migration* traffic** between DDR4 and HBM2E, which is slow-tier bandwidth spent on refills and dirty writebacks. The token mechanism is a rate limiter on exactly this.
- **What the throughput is bounded by**: the paper does not frame the result as a bandwidth bound and reports no achieved-bandwidth or roofline figure. The implicit model is that **slow-tier (DDR4) bandwidth is the contended resource**, since that is what a migration consumes and what the token counter meters — but this is `[inference]` from the mechanism, not a paper claim. `NOT_ESTABLISHED`.

## 12.11 Why it is faster/slower (decomposed cause)
The ablation decomposes it cleanly, which is unusually good practice `[paper]`:
1. **Decoupled partitioning alone: 1.10×.** The ways/sets-to-channels mapping, giving the CPU capacity and the GPU bandwidth independently — this is the paper's novel structural idea and it is the largest single contributor.
2. **Token-based migration throttling: +4.4%.** Stopping the GPU from burning DDR4 bandwidth on aggressive migration.
3. **Hill-climbing online search: +8.6%.** Finding good (`cap`, `bw`, `tok`) per workload combination rather than fixing them.
4. **Reconfiguration made cheap** by consistent hashing plus lazy layout change, so the search can actually be run online without paying a bulk-relocation cost each time it moves.

Numbers with full qualifiers `[paper]`, all **simulated in zsim** on a modelled **8-core CPU (private L1 8-way 64 KB, L2 8-way 1 MB) + integrated GPU with 96 EUs (128 KB private L1 per 16 units), shared 16-way 16 MB LLC at 38 cycles, HBM2E 16 ch @1600 MHz + DDR4-3200 4 ch @1600 MHz**, over **12 randomly combined CPU+GPU workload pairs** drawn from **SPEC CPU2017 (5-billion-instruction traces, 2 copies each), Rodinia 3.1, and MLPerf Inference v3.0** (GPU kernel memory traces only):
- vs the non-partitioned baseline: **1.24× average, up to 1.48×**.
- vs **Profess**: **1.16× average, up to 1.31×** — this is the number the abstract and the census row carry.
- vs **HAShCache**: **1.47× average, up to 1.98×**.
- Other baseline: **WayPart** (simple way-partitioning without decoupling).
- Overhead: **0.049%** metadata storage (one `alloc` bit per way).

## 12.12 Hardware generation dependence
- The modelled system is an **integrated CPU+GPU with a shared LLC and a two-tier HBM2E/DDR4 main memory** — a configuration that matches the paper's cited exemplar, **Intel Xe-LPG**, and does **not** match any discrete NVIDIA or AMD datacenter GPU. On a discrete GPU, HBM is device-private, there is no shared LLC, and the CPU-GPU capacity/bandwidth contention Hydrogen resolves does not arise in this form.
- Consequently the design's relevance to the rest of this cluster is **structural analogy, not transfer**. The nearest real-world analogues are MI300A-class APUs and Grace-Hopper-class coherent superchips; the paper does not evaluate either, and this analysis makes no claim that the result carries to them.
- **No real GPU hardware is used at any point** `[paper]`.

## 12.13 Limitations
Recorded from this reading (the paper's own limitations discussion is not extensive in the read text):
1. **Entirely simulated in zsim**; no hardware, no RTL, no artifact.
2. **Only GPU kernel memory traces are simulated**, not GPU execution — so GPU-side effects that would change the access stream (occupancy, warp scheduling, coalescing, page faults) cannot appear in the result by construction. This is a methodological reason the design could not have keyed on GPU-specific semantics even if the authors had wanted it to, and it is directly relevant to the re-adjudication.
3. **Integrated-GPU setting only** (Intel Xe-LPG-class, 96 EUs); no discrete-GPU, APU or coherent-superchip configuration.
4. **12 workload combinations**, randomly composed — a small and arbitrary contention matrix.
5. The epoch-based hill climb is a local search over three coupled parameters with no convergence or stability guarantee reported — `UNKNOWN`.
6. Sensitivity to the 16:4 fast:slow channel ratio is not reported in the read text — `UNKNOWN`.

## 12.14 Relation to prior corpus
- **Re-adjudicates a row in `_LEDGER_memory_virtualization.md`** (line 58, and its summary line 81). That ledger's watchlist item is hereby resolved: the full text was obtained from the author's page, read, and the `RELATED_GPU` verdict is **confirmed**. The memory cluster should update its row to `PUBLIC_FULLTEXT` / `RELATED_GPU` (confirmed) and point at this file.
- **Prior art the paper compares against** `[paper]`: **HAShCache**, **Profess**, **WayPart**, and a non-partitioned baseline — all hybrid-memory / shared-cache partitioning designs. This is a memory-systems citation neighbourhood, not a GPU-architecture one, which is itself evidence for the verdict.
- **Within this cluster** it is the only paper on the HBM axis that treats HBM as a *tier* rather than as a bandwidth ceiling to be relieved by compression. `GPU-ISCA25-81` (Ecco) reduces the bytes that cross L2↔HBM; Hydrogen reallocates *who gets* HBM. They are complementary in principle and do not cite each other.
- **Adjacent, unread**: *Folded Banks* (ISCA 2025) proposes changing HBM's bank organisation itself; *TDMSim* (ISCA 2026) proposes a GPU DRAM cache with 2D materials. Both remain `UNRESOLVED` in the ledger for want of access. Hydrogen is the only one of the three whose full text was obtained.

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**YES — substantially the same.** This is the cluster's one clear YES and it is recorded with its evidence:
1. **The design's characterisation of the GPU is a statistical one**: "GPUs, benefiting from thread-level parallelism, are more bandwidth-driven and can tolerate longer memory access latencies" `[paper]`. Any bandwidth-hungry, latency-tolerant client — an NPU, a DSA, a streaming FPGA accelerator, a many-core throughput CPU — would motivate the identical design.
2. **No GPU structure appears in the mechanism.** The ways/sets-to-channels mapping, the consistent hashing, the lazy layout change and the hill-climbing search are memory-controller and cache-organisation techniques. There is no warp, CTA, SM, coalescer, page-fault path or TLB anywhere in the design.
3. **The token throttle counts memory-controller events** — refills and dirty writebacks — attributed to a client ID. Attribution is per-client, not per-warp or per-kernel.
4. **The methodology forecloses GPU-specificity**: only GPU *kernel memory traces* are simulated, so no GPU microarchitectural behaviour is in the model to key on.
5. **What is genuinely GPU-motivated**: the *asymmetry* of the policy — only the GPU's migrations are throttled, because the GPU is the party that migrates aggressively under bandwidth pressure. That is a real and correct observation about GPUs, but it is a behavioural premise the design consumes, not a hardware property the design depends on.

Under this cluster's strict counterfactual, a design that would be unchanged if the GPU were replaced by another bandwidth-hungry client is `RELATED_GPU`, and Hydrogen is squarely that. It remains genuinely useful to this corpus — it is the only full-text paper here on CPU-GPU HBM tiering — and it is correctly classified, not excluded.

verdict_basis: The mechanism is a hybrid-memory capacity/bandwidth partitioning and migration-throttling policy operating entirely at the memory controller and fast-memory cache organisation; the GPU enters only as a bandwidth-driven, latency-tolerant client identified at request granularity, and the evaluation simulates only GPU memory traces, so no GPU microarchitectural property is or could be load-bearing.

## What the throughput is bounded by
`NOT_ESTABLISHED`. The paper reports speedups (1.24× / 1.16× / 1.47× average against three baselines) and an ablation, but no achieved-bandwidth, occupancy or roofline figure. `[inference]` from the mechanism: the contended resource is **slow-tier DDR4 bandwidth**, since that is what a fast-tier migration consumes (1 token per refill, 2 with a dirty writeback) and what the token faucet meters — but the paper does not state this as a bound. All results are zsim simulation on a modelled integrated CPU+iGPU system; **no real GPU hardware is used**.

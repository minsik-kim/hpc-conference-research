<!-- Deep-analysis template for domains/gpu_systems/corpus/.
     Write one file per paper, named <stable-id>--<slug>.md.
     Stable IDs: GPU-<VENUE><YY>-<NN> (see governance/ID_NAMING_RULES.md;
     the GPU- prefix keeps these distinct from the pending AI/HPC import's
     SC24-13-style IDs and is never reused or renumbered).

     EVIDENCE TAGS are mandatory on every non-trivial claim:
       [paper] [artifact] [code] [author-presentation] [README]
       [official-web] [documentation] [reconstruction] [inference]
     A number without its hardware/workload/baseline qualifier is not a
     portable fact — restate the qualifiers each time the number is reused.
     Sections that the paper does not support are written as
     NOT_IN_PAPER / UNKNOWN, never filled by plausible completion. -->

# <stable-id> — <Official Title>

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS | EXISTING_CORPUS_DUPLICATE | GPU_DELTA_ANALYSIS | KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED`
primary_topic: `<A-Q letter + name>`
secondary_topics: `<...>`
last_checked: <YYYY-MM-DD>
knowledge_as_of: <YYYY-MM-DD>
read_depth: `<which sections of the full paper were actually read>`

## 12.1 Bibliographic facts
## 12.2 Core question (one sentence)
## 12.3 GPU/HPC problem translation (compute / memory / synchronization / communication / scheduling)
## 12.4 Why the problem exists (down to hardware root cause where the paper supports it)
## 12.5 Mathematical / performance model
## 12.6 Data layout and ownership (thread -> warp/wavefront -> block/workgroup -> SM/CU -> GPU -> node -> cluster)
## 12.7 Pseudo code (mark reconstructed names as [reconstruction])
## 12.8 Real implementation (pin commit if a repository exists; never invent symbols)
## 12.9 Kernel execution (kernel -> thread block -> warp -> instruction)
## 12.10 Memory traffic (register <-> shared/LDS <-> L1 <-> L2 <-> HBM; multi-GPU path if applicable)
## 12.11 Why it is faster/slower (decomposed cause, not a speedup number)
## 12.12 Hardware generation dependence
## 12.13 Limitations
## 12.14 Relation to prior corpus (precursor / follow-up / competing / complementary / existing duplicate)

## Counterfactual test record
> "If a generic accelerator or a CPU were used instead, would the core
> contribution be substantially the same?"

verdict_basis: <1-2 sentences naming the GPU-specific property the
contribution depends on>

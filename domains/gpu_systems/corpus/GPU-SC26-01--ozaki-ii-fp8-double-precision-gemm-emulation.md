# GPU-SC26-01 — Double-Precision Matrix Multiplication Emulation via Ozaki-II Scheme with FP8 Quantization

gpu_relevance: `CORE_GPU`
fulltext_state: `PUBLIC_FULLTEXT`
prior_corpus_check: `NO_EXISTING_ANALYSIS` (see §12.14 for the external-corpus caveat)
primary_topic: `F — Tensor/Matrix cores, numeric formats, precision emulation`
secondary_topics: `numerical linear algebra; INT8/FP8 matrix-engine throughput asymmetry; AMD CDNA matrix cores`
last_checked: 2026-09-18
knowledge_as_of: 2026-09-18
read_depth: `FULL_PAPER — §I incl. §I-A Background (hardware motivation), §II (Ozaki-II background), §III Proposed Method Using FP8_E4M3 incl. §III-F "Rationale for Choosing FP8 over FP16, BF16, and FP4", §IV performance model, §V numerical results (throughput, accuracy, working memory), §VI conclusion. Read via arXiv HTML for §I-IV and the arXiv PDF for §IV-VI (the HTML rendering truncated before §V). Plus [code] inspection of the GEMMul8 artifact at a pinned commit.`

## 12.1 Bibliographic facts

- Title: **Double-Precision Matrix Multiplication Emulation via Ozaki-II Scheme with FP8 Quantization** [paper]
- Authors: Yuki Uchino, Katsuhisa Ozaki, Toshiyuki Imamura [paper]. Affiliations are not stated in the rendered preprint text read — `NOT_IN_PAPER`. (The artifact lives under the `RIKEN-RCCS` GitHub organisation [README], which is consistent with a RIKEN R-CCS affiliation but is **not** a paper-level statement.)
- Preprint: arXiv:2603.10634v1, dated **11 March 2026** [paper]
- Venue: seeded as **SC 2026**. Census records `SC26_MEMBERSHIP_UNVERIFIED`; no SC 2026 program page or DOI confirming membership was reachable from this environment (`dl.acm.org` 403, `ieeexplore` 418). **Venue membership: `UNVERIFIED`.** Publication type as read: `PREPRINT`.
- Artifact: `https://github.com/RIKEN-RCCS/GEMMul8` — inspected. Pinned commit **`e5db07fa0aa69435d1319d3e56b4c25e9a68d625`** (`Wed Sep 16 21:08:04 2026 +0900`, "Fix: SYRK test compilation and test executable dependencies") [code]. **The inspected tree is six months newer than the preprint and has grown well beyond it** (see §12.8).

## 12.2 Core question (one sentence)

Given that new GPU generations are deliberately trading INT8 matrix throughput away in favour of FP8, can the Ozaki-II (Chinese-Remainder-Theorem, modular-integer) FP64-emulation scheme — which structurally wants *exact integer* products — be made to run on an **FP8** matrix engine at all, and at what cost in GEMM count and workspace?

## 12.3 GPU/HPC problem translation

- **Compute.** The paper's premise is a *ratio* problem, stated with hardware numbers: on **B300**, INT8 is quoted at **150 TOP/s** against **4500 TFLOP/s** FP8 [paper, Table I] — a 30× asymmetry. An emulation scheme that only speaks INT8 is therefore locked out of the fastest matrix path on that part. *Qualifier: vendor-specification throughputs as tabulated by the paper for B300, not measured.*
- **Memory.** Emulation is workspace-hungry: the scheme holds one low-precision matrix pair per modulus plus integer accumulators. The FP8 route roughly *doubles* the workspace relative to INT8 (§12.11), so HBM capacity becomes a first-order constraint, not an afterthought.
- **Synchronization / scheduling.** The `N` modular GEMMs are independent, so the work is a batch of GEMM launches plus scaling/reduction kernels; the paper's §IV performance model and the artifact's `batch_count` logic both reason about how many moduli fit in the available workspace at once [paper; code].
- **Communication.** Single-GPU. `NOT_IN_PAPER`.

## 12.4 Why the problem exists (hardware root cause)

Two root causes, both about the *number format*, not the bandwidth:

1. **FP8_E4M3 represents only a short run of integers exactly.** The paper states FP8_E4M3 "can only represent integers in range [−16, 16]", which caps the usable moduli at `{32, 31, 29, …, 7}` and hence caps the CRT product at `P/2 < 2^47` — "insufficient for even FP32 emulation" [paper]. Ozaki-II needs the low-precision product to be *error-free*; a 4-bit mantissa cannot carry an integer residue that a modulus of a few hundred requires.
   This is confirmed at the bit level in the artifact: `is_e4m3_hole_mag(x)` tests `(x & 0x11u) == 0x11u`, i.e. it rejects exactly those integer magnitudes that fall in E4M3's representational holes, and `valid_mag_pair` additionally enforces `MAX_ABS <= 32u` [code, `src/oz2/common/make_f8.hpp`, `src/oz2/common/fp8_limb_selection.hpp`].
2. **FP8 accumulates in FP32, INT8 in INT32.** The paper notes the accumulate types: "FP8_E4M3" MMA accumulating in FP32, "INT8 MMA units" accumulating in INT32 [paper]. FP32 accumulation is *not* exact for arbitrary integer sums, which is why the paper must bound `k ≤ 2^16` to keep the FP8 MMA rounding-free [paper]. INT32 accumulation has no such constraint at these magnitudes — hence the artifact's much larger `K_BLOCK_INT8 = 1 << 17` versus per-modulus FP8 k-blocking tables [code, `src/oz2/core/matmult.hpp`].
3. `[inference]` Structurally, FP8's four exponent bits are dead weight in a fixed-point/modular scheme. The paper states this as a limitation: FP8's exponent fields "remain underutilized in fixed-point operations, creating structural inefficiency compared to INT8 formulations" [paper, §VI].

## 12.5 Mathematical / performance model

**Ozaki-II as the paper states it** [paper]:
1. Convert FP64 `A, B` to integer matrices `A', B'` using scaling factors `μ`, `ν`.
2. For each of `N` pairwise-coprime moduli `{p_1 … p_N}`, compute `C'_ℓ := mod(A'_ℓ B'_ℓ, p_ℓ)` independently on the low-precision matrix engine.
3. Reconstruct by CRT: `C' ← mod( Σ_ℓ (q_ℓ P / p_ℓ) C'_ℓ , P )` with `P = Π_ℓ p_ℓ`.
4. Convert back to floating point.

**The FP8 adaptation — Karatsuba splitting** [paper, Eqs. 9–10]. Because a single FP8 operand cannot hold a residue mod a few-hundred modulus, each residue is split into two limbs, `A'_ℓ = s·A'^{(1)}_ℓ + A'^{(2)}_ℓ` (similarly for `B`), and the product reconstructed by the three-multiplication Karatsuba identity
`A'_ℓ B'_ℓ = s² C'^{(1)}_ℓ + C'^{(2)}_ℓ + s ( C'^{(3)}_ℓ − C'^{(1)}_ℓ − C'^{(2)}_ℓ )`.
So **3 FP8 GEMMs per modulus** in general, against **1 INT8 GEMM per modulus** [paper].

**Modulus budget.** For FP64 emulation the paper requires `P/2 > 2^{109} > 2^{53+53}`, satisfied at `N = 14` for the INT8 route; for the FP8 route it states `N ≥ 12` suffices for 53+ bits and reports **36 FP8 matrix multiplications** (= `3N` at `N = 12`) [paper].

**Code corroboration of the modulus design** [code, `src/oz2/common/table.hpp`]. The INT8 moduli are the descending sequence `256, 255, 253, 251, 247, 241, 239, 233, 229, 227, 223, 217, 211, 199, 197, 193, 191, 181, 179, 173` (indices 0–19). The FP8 moduli are **squares and near-squares of small integers**, with the source's own comments naming the base: `2401 // base-49`, `2209 // base-47`, `2025 // base-45`, `1849 // base-43`, `1681 // base-41`, `1369 // base-37`, `1024 // base-32`, `961 // base-31`, `841 // base-29`, interleaved with entries tagged `BASE49`, `BASE32_SUM`, `BASE32_DIFF`, `BASE33_SUM`. This is the Karatsuba structure made concrete: a modulus of the form `b²` lets the two FP8 limbs be digits in base `b` with `b ≤ 49` — and `src/oz2/common/fp8_limb_selection.hpp` carries `KaratsubaType::{BASE49, BASE32_SUM, BASE33_SUM}` with `base = base49 ? 48 : 32` and `MAX_ABS <= 32U`. **Note the code's `b` reaches 49, above the paper's `[−16,16]` exact-integer statement**, which the `is_e4m3_hole_mag` hole-avoidance logic is there to make safe: only the E4M3-representable magnitudes ≤ 32 with `(a & 0x11) != 0x11` are used [code]. `[inference]` this is a refinement of, not a contradiction of, the paper's argument.

**Accuracy model.** The paper grounds accuracy in truncation error during the matrix-scaling phase and in the modulus count; §III-F argues why FP8_E4M3 rather than FP16/BF16/FP4, on precision-under-FP32-accumulation grounds [paper]. A formal error theorem was not located in the text read — `NOT_IN_PAPER`.

## 12.6 Data layout and ownership

The paper is an algorithm-and-kernel-orchestration paper; the matrix products themselves are delegated to the vendor GEMM. Ownership as read:

- **thread**: performs the scaling / splitting / modular-reduction element work. The artifact's device helpers are per-element bit operations, e.g. `div_small_u32<D>` implemented as an inline PTX `mul.hi.u32` against a compile-time reciprocal, i.e. constant division without a divider [code, `make_f8.hpp`].
- **warp / block**: no warp-cooperative matrix layout is designed by this paper — the MMA fragment layout is cuBLAS/hipBLAS's business.
- **GPU-level workspace**: the dominant ownership question. The artifact selects, per call, how many moduli to process concurrently given the available workspace: `batch_count<NUM_MODULI>(arch, n, i, sizeC_Mid, sizeC_Hi, lwork_blas, worksizeC, …)`, with architecture special-cases `if (arch == 121) return 1u;` and `if (arch == 90 && n > 2048) return 1u;` [code, `src/oz2/core/matmult.hpp`]. `arch == 90` is SM90 = Hopper.
- **k-blocking ownership**: `configure_matprod_k_blocking<BACKEND, COMPLEX>` sets `K_BLOCK_INT8 = 1 << 17` for the INT8 backend (skipped entirely when the modulus is 256, since powers of two need no reduction) and per-modulus `k_block_first_fp8 / k_block_next_fp8` tables for FP8 [code]. This is the `k ≤ 2^16`-class constraint of the paper, realised as a per-modulus table.
- **node / cluster**: `NOT_IN_PAPER`.

## 12.7 Pseudo code

```
# [paper] Ozaki-II with an FP8 backend
mu, nu      = compute_scalings(A, B)                    # [paper] step 1
A_int,B_int = to_integer(A, mu), to_integer(B, nu)

for l in 0 .. N-1:                                      # N >= 12 for FP64  [paper]
    p   = moduli[l]                                     # e.g. 961 = 31^2   [code]
    Al  = mod(A_int, p);  Bl = mod(B_int, p)
    # Karatsuba split into two FP8-representable limbs
    A1,A2 = split_base_s(Al, s)                         # [paper] Eq. 9
    B1,B2 = split_base_s(Bl, s)
    C1 = fp8_gemm(A1, B1)                               # 3 FP8 GEMMs / modulus [paper]
    C2 = fp8_gemm(A2, B2)
    C3 = fp8_gemm(A1+A2, B1+B2)
    Cl = mod(s*s*C1 + C2 + s*(C3 - C1 - C2), p)         # [paper] Eq. 10
    accumulate_crt(C_acc, Cl, p)

C = from_integer(mod_crt(C_acc, P), mu, nu)             # [paper] steps 3-4
```

Backend-selection detail from the artifact: `constexpr auto CUDA_R_LOW = (BACKEND == Backend::INT8) ? CUDA_R_8I : CUDA_R_8F_E4M3;` appears at three call sites in `src/oz2/common/matmult.hpp` (lines 23, 123, 226) — the low-precision GEMM is a `cublasGemmEx`/`cublasLtMatmul`-family call parameterised by that type [code].

## 12.8 Real implementation

Repository `https://github.com/RIKEN-RCCS/GEMMul8`, pinned commit `e5db07fa0aa69435d1319d3e56b4c25e9a68d625` [code].

Verified symbols and facts (all `[code]`):
- `gemmul8::common::Backend::{INT8, FP8}` selects the emulation backend; moduli tables are template specialisations `moduli<Backend, IDX, COMPLEX>` in `src/oz2/common/table.hpp`, with separate real and complex modulus sets.
- FP8 path: `CUDA_R_8F_E4M3`, mapped under HIP to `HIP_R_8F_E4M3_FNUZ` on one ROCm branch and `HIP_R_8F_E4M3` on another (`src/oz2/common/self_hipify.hpp` lines 375, 382). **This is a concrete cross-vendor format hazard: AMD's FNUZ E4M3 variant has different NaN/zero encoding from NVIDIA's E4M3, and the library branches on it.** The paper's target list includes AMD MI300X/MI325X/MI350X/MI355X [paper].
- `cublasGemmEx` / `cublasGemmEx_64` and the `cublasLtMatmul` family are hipify-mapped to `hipblasGemmEx` / `hipblasGemmEx_v2` / `hipblasLtMatmul`, so the same emulation runs on CUDA and ROCm [code].
- E4M3 integer-hole handling: `is_e4m3_hole_mag`, `valid_mag_pair<MAX_ABS>`, `limb_selection<P, KaratsubaType, MAX_ABS>` with `representable(x) = a <= MAX_ABS && (a & 0x11U) != 0x11U` [code].
- Public API contract: `2 <= num_moduli <= 20` for FP64 output and `2 <= num_moduli <= 13` for FP32 output, with a `fastmode` boolean [code, `include/gemm.hpp`].
- `[code]` **Scope drift from the paper.** The inspected tree has extended Ozaki-II beyond GEMM to "symmetric, Hermitian, triangular, and triangular-solve routines" — `src/` contains `gemm, symm, hemm, syrk, syrkx, syr2k, herk, herkx, her2k, trmm, trsm, trtrmm` and a cuBLAS/hipBLAS **hook (interception) mode**, and the README claims "bit-wise reproducible results" [README]. None of that BLAS-3 extension or hook mode is in the preprint read. **Do not attribute it to the paper.**

## 12.9 Kernel execution

kernel → thread block → warp → instruction, per phase:
- **Scaling / splitting kernels**: elementwise, per-thread, integer-heavy; use inline PTX `mul.hi.u32` for constant division [code].
- **Modular GEMMs**: `N` (INT8) or `3N` (FP8) launches of the vendor low-precision GEMM. The matrix-unit instruction actually issued is whatever cuBLAS/hipBLAS selects for `CUDA_R_8I`/`CUDA_R_8F_E4M3` with FP32/INT32 compute type — this paper does **not** hand-write MMA. That is precisely the gap the sibling paper EmuGEMM (`GPU-SC26-02`) attacks.
- **CRT reconstruction**: elementwise integer reduction.

## 12.10 Memory traffic

- Every modular GEMM reads its operands from **global memory** and writes an accumulator back to global memory; with `N ≥ 12` moduli and 3 GEMMs each, the operands are re-read many times. The paper quantifies the consequence as workspace, not as traffic: at `m = n = k = 16384`, **INT8-based Ozaki-II (N=14) needs 27 GB** of workspace and **FP8-based Ozaki-II (N=12) needs 55 GB** [paper, §V]. *Qualifier: 16384³ FP64 GEMM, workspace only.* The paper attributes the ≈2× to storing multiple FP8 matrices per residue and to INT16 (not INT8) intermediates.
- Register ↔ shared ↔ L1/L2 detail: delegated to the vendor GEMM. `NOT_IN_PAPER`.
- Multi-GPU: `NOT_IN_PAPER`.

## 12.11 Why it is faster/slower (decomposed cause)

Causes, decomposed:
- **In FP8's favour**: access to the FP8 matrix pipe, which on the paper's tabulated B300 numbers is 30× the INT8 pipe (4500 TFLOP/s vs 150 TOP/s) [paper, Table I, vendor specs].
- **Against FP8, cause 1 — GEMM count**: 3 FP8 GEMMs per modulus versus 1 INT8 GEMM per modulus, i.e. a ~3× instruction-count penalty from the Karatsuba reconstruction [paper].
- **Against FP8, cause 2 — workspace**: ≈2× the working memory, which both costs traffic and limits how many moduli can be batched [paper, §V].
- **Against FP8, cause 3 — wasted exponent field**: FP8's 4 exponent bits carry no information in a fixed-point scheme, so the effective mantissa per byte is worse than INT8's [paper, §VI].
- **Against FP8, cause 4 — inexact accumulation**: FP32 accumulation forces the `k ≤ 2^16`-class blocking, adding reduction passes that INT32 accumulation does not need [paper; corroborated by the per-modulus FP8 k-block tables vs the single large `K_BLOCK_INT8` in `[code]`].

**Measured results, with hardware qualifiers** [paper, §V]:
- Platforms: NVIDIA **RTX 4090 Laptop** (Intel Core i9-14900HX host), NVIDIA **RTX 5080** (AMD Ryzen 9 7950X), **AMD Radeon RX 9070 XT** (Intel Core i7-7820X), NVIDIA **GH200** Grace Hopper Superchip, NVIDIA **GB10** Grace Blackwell Superchip, NVIDIA **B200 SXM** (Intel Xeon 6960P, SAKURAONE cluster). Matrix sizes `m=n=k` from 1024 to 16384. Baselines: native `cublasDgemm`, INT8-based Ozaki-II, FP8-based Ozaki-I, FP8-based Ozaki-II (proposed).
- **RTX 5080**: INT8-based Ozaki-II 4.8–15× over native DGEMM at `m=n=1024` and 7.4–24× at `m=n=8192`; FP8-based Ozaki-II 3.7–5.0× at `m=n=1024` and 4.3–9.4× at `m=n=8192`. INT8 beats FP8 by 1.3–3.1×.
- **B200, `m=n=k=16384`**: INT8-based Ozaki-II **137 TFLOP/s** (fast mode, 16 moduli) and **138 TFLOP/s** (accurate mode, 15 moduli); FP8-based Ozaki-II **61 TFLOP/s** (fast mode, 13 moduli) and **65 TFLOP/s** (accurate mode, 12 moduli).
- **Accuracy**: for normally distributed random entries, INT8-Ozaki-II at 15 moduli (fast) / 16 (accurate) and FP8-Ozaki-II at 13 (fast) / 12 (accurate) "achieve accuracy close to that of the cuBLAS Ozaki-I baseline with seven slices"; accurate mode beats fast mode throughout; FP8 shows a *smaller* accuracy spread between `k=1024` and `k=65536` than the INT8 variants [paper].
- The paper reports that its analytic §IV model closely matched measurement [paper].

**The paper's own bottom line is a negative-for-FP8 result**, quoted: "on platforms where INT8 MMA capacity is sufficient (e.g., INT8 throughput is at least about half of the FP8 throughput), the INT8-based approaches are preferable in terms of both throughput and working memory footprint" [paper, §VI]. FP8 is positioned as insurance for parts where INT8 has been cut.

## 12.12 Hardware generation dependence

This paper's *entire motivation* is generation-specific and must not be flattened:
- **Hopper (H200)**: has both INT8 and FP8 matrix paths; INT8 remains competitive.
- **Blackwell B200**: measured here; INT8-Ozaki-II is ~2.1× faster than FP8-Ozaki-II at 16384³ (137–138 vs 61–65 TFLOP/s).
- **Blackwell Ultra B300**: the pivot case — the paper's Table I quotes **150 TOP/s INT8 against 4500 TFLOP/s FP8** [vendor specs as tabulated]. B300 was **not** among the measured platforms; the B300 argument is specification-based, not measured. Do not report a measured B300 number.
- **Rubin**: discussed in the specification table only; **not measured** [paper].
- **GB10 / GB200-class Grace-Blackwell** and **GH200 Grace Hopper**: measured platforms.
- **AMD**: MI300X / MI325X / MI350X / MI355X are named as targets [paper]; the measured AMD part was a **Radeon RX 9070 XT** (RDNA-class consumer), **not** a CDNA3 MI300. Do not claim MI300X measurements from this paper. The artifact's `HIP_R_8F_E4M3_FNUZ` branch is the concrete CDNA-era FP8-variant handling [code].
- The `arch == 90` (SM90/Hopper) and `arch == 121` special-cases in the artifact's batching logic are evidence that workspace batching had to be tuned per generation [code].

## 12.13 Limitations

- **Stated**: FP8 is dominated by INT8 wherever INT8 throughput is ≳half of FP8 throughput [paper, §VI].
- **Stated**: FP8's exponent field is structurally wasted in a fixed-point scheme [paper, §VI].
- **Stated / structural**: `k ≤ 2^16` is assumed to keep the FP8 MMA rounding-free [paper]; larger `k` requires blocking.
- **Stated**: ≈2× workspace versus the INT8 route (55 GB vs 27 GB at 16384³) [paper, §V].
- `[inference]` 3 GEMMs per modulus means the FP8 route needs an FP8:INT8 throughput ratio better than ~3:1 merely to break even before workspace effects; the B200 measurement (2.1× *in INT8's favour*) is consistent with B200 not being such a part.
- B300 and Rubin claims rest on vendor specifications, not measurement. MI300-class CDNA3 parts were named but not measured.
- Behaviour on ill-conditioned or non-normally-distributed matrices beyond what §V reports: `NOT_IN_PAPER`.

## 12.14 Relation to prior corpus

- **Direct sibling / competitor**: `GPU-SC26-02` (EmuGEMM, arXiv 2606.25453) attacks the *other half* of the same problem — this paper chooses the number format and modulus set and then calls a vendor GEMM; EmuGEMM keeps the scheme and rewrites the GEMM as a fused Tensor Core kernel. Read together, they show the emulation field splitting into a *numerics* track and a *kernel-engineering* track. EmuGEMM explicitly cites "Ozaki et al." and "Uchino et al." — i.e. this paper's authors — as the prior implementations it optimises [that paper].
- **Precursors cited by this paper** [paper, §Related work]: the foundational Ozaki-I and Ozaki-II schemes (refs 20–22), INT8-based Ozaki implementations (refs 19, 25–26), FP16/FP8 emulation via Ozaki-I (refs 12–13), and OzIMMU. The CRT-in-matrix-arithmetic lineage is cited.
- **Cluster-adjacent watchlist item**: M3XU (SC 2024, "Achieving High-Precision and Complex Matrix Multiplication with Low-Precision MXUs") is the same problem class one venue-cycle earlier; no full text was retrieved.
- **Cross-cluster**: the PPoPP'26 MMU characterisation paper (`GPU-PPoPP26-02`) cites the Ozaki-scheme line and independently reports that **Blackwell B200's native FP64 matrix throughput regresses to ~30 TFLOP/s from H200's ~67 TFLOP/s** — which is the strongest available corroboration that FP64 emulation on low-precision matrix engines is becoming *necessary* rather than merely clever. That is that paper's measurement, not this one's.
- **External-corpus caveat**: precision-emulation GEMM work plausibly appears in the un-imported ~80-paper AI/HPC corpus (`domains/ai_hpc_systems/` is `EXTERNAL_IMPORT_PENDING`). For that reason no duplication claim is asserted; within *this* repository, hits for "2603.10634" are confined to `domains/gpu_systems/census/SC_2026.md`. `NO_EXISTING_ANALYSIS` in-repo; `KNOWN_EXTERNAL_CORPUS_NOT_IMPORTED` for the external question.

## Counterfactual test record

> "If a generic accelerator or a CPU were used instead, would the core contribution be substantially the same?"

**NO.**

verdict_basis: The paper exists *because of* a specific GPU matrix-engine property — the deliberate, generation-by-generation divergence between INT8 and FP8 MMA throughput on NVIDIA Blackwell-Ultra-class parts (150 TOP/s vs 4500 TFLOP/s on B300 per the paper's Table I) — and its technical content is entirely about the **FP8_E4M3 MMA operand and accumulator semantics**: which integers E4M3 can hold exactly (and which fall in its representational holes, `(a & 0x11) == 0x11` in the artifact), that the FP8 MMA accumulates in FP32 rather than INT32 and hence needs a `k ≤ 2^16` bound, and that these two facts together force a Karatsuba two-limb split costing 3 MMAs per modulus. On a CPU, FP64 is simply available and none of this arises; on a generic accelerator without an FP8 matrix pipe whose throughput dwarfs its integer pipe, the entire trade-off the paper evaluates disappears. Note the counterfactual is *format*-driven rather than *fragment-layout*-driven: the paper does not hand-write MMA fragments (its sibling EmuGEMM does), so its GPU-specificity is the numeric-format and accumulator contract of the matrix unit.

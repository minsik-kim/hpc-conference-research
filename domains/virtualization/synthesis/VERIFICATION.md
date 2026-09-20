# PAPER_CATALOG.csv 독립 검증 보고서 (12건 표본조사)

검증일: 2026-09-18. 대상: `/home/claude/virt/out/PAPER_CATALOG.csv` 410개 레코드 중 지정된 12건.
방법: 공식 프로그램/DOI 레지스트리(Crossref, Semantic Scholar) 조회, 저자 공개 PDF·GitHub artifact 원문 대조, ACM DL/IEEE Xplore/USENIX 프로그램 페이지 재확인. adversarial 관점에서 반증 시도.

## 요약 판정표

| id | 제목·venue·year 확인 | DOI 확인 | 저자 확인 | pubtype 확인 | 수치 확인 | evidence_depth 타당성 | 판정 |
|---|---|---|---|---|---|---|---|
| VIRT-EUROSYS25-03 (HyperAlloc) | OK (저자 호스팅 PDF로 확인, 단 PDF 자체는 익명화된 제출본) | OK (형식·리졸브 경로 타당, 직접 resolve는 프록시 차단으로 미실시) | 간접 확인 (PDF가 익명이라 SRA Hannover 페이지 출처에 의존 — 카탈로그도 이를 명시) | OK | 7건 중 6건 원문과 정확히 일치, **1건 불일치 발견**(아래 참조) | OK (익명 제출본이지만 실제 전체 본문·수치 확인됨) | **경미한 오류** |
| VIRT-OSDI26-01 (JANUS) | OK — USENIX 공식 presentation 페이지에서 제목·저자 20명 전원 정확히 일치 확인 | OK (USENIX가 OSDI 개별 논문에 DOI를 부여하지 않는다는 카탈로그 설명이 타당 — UNKNOWN 처리 적절) | OK (20명 전원 일치) | OK (main track) | UNVERIFIED (예산상 수치 대조 미실시) | OK (DESIGN_EVAL은 오히려 보수적) | **OK** |
| VIRT-OSDI26-06 (Nixie) | OK — 2026-09-21 USENIX 공식 presentation page로 제목·저자·venue·pages 확인 | OK (USENIX 논문은 DOI 없음) | OK | OK (main track) | 부분 확인 (초록 요약과 일치; 기존 full-text read 유지) | FULL 타당 | **OK — 이전 venue 미확인 해소** |
| VIRT-EUROSYS24-01 (HD-IOV) | OK | OK 개연성 (ACM DL 403, 직접 resolve 불가하나 같은 EuroSys'24 proceedings 접두사(3627703)를 S-NIC과 공유 — 정합적) | **불완전**: GitHub 저장소 자체에 전체 10명 저자가 나와 있음에도 카탈로그는 3명+"et al."만 기재 | OK | OK — "2.96x" 및 "2.9x" 수치가 GitHub README에 **원문 그대로** 확인됨 | OK (artifact 기반 DESIGN_EVAL 타당) | **경미한 오류** (저자 누락) |
| VIRT-EUROSYS24-04 (S-NIC) | OK | OK 개연성 (같은 이유로 403이나 형식 정합) | OK (4명 전원 저자 호스팅 PDF와 일치) | OK | OK — 6개 수치 전부 원문에서 **정확히 확인**됨 | OK (저자 호스팅 전문 확인, FULL 타당) | **OK** |
| VIRT-SOSP24-02 (VPRI) | OK (dblp SOSP'24 페이지, pp.541–557) | OK (UNKNOWN 처리 타당 — dblp에도 DOI 없음) | OK (12명 전원, "et al." 표기는 포맷상 특이하나 내용은 정확) | OK | OK — "최대 50% DRAM 낭비" 포함 6개 수치 전부 원문에서 **정확히 확인**됨 | OK | **OK** |
| VIRT-MICRO24-02 (Elastic Translations) | OK (MICRO'24 Session 1A, 정확한 시간·저자) | UNVERIFIED (IEEE/ACM에 DOI가 있을 수 있으나 미확인) | OK | OK | 일부 확인 (가상화 30%/150% 향상 수치 일치) | OK — **결정적 분류 근거(중첩/2단계 KVM 관리) 논문 원문에서 직접 확인됨**(아래 참조) | **OK** |
| VIRT-MICRO24-01 (vNPU/NeuISA) | OK (MICRO'24 Session 1A, "Best Paper Runner-up" 표기까지 정확히 일치) | UNVERIFIED | OK | OK | UNVERIFIED (예산상 arXiv 본문 수치 대조 미실시) | OK (선례 기록 및 주변 정황상 타당) | **OK** |
| VIRT-SOCC24-10 (Faascale) | OK | OK (Crossref로 제목·저자·venue 정확히 일치 확인) | OK | OK | N/A (quantitative_claims 필드 자체가 비어 있음 — 정직한 처리) | OK (GitHub 저장소 설명 문구까지 원문 대조 확인, DESIGN이 DESIGN_EVAL이 아닌 것도 타당) | **OK** |
| VIRT-SOSP25-01 (RDMA Live Migration) | OK | OK (Crossref로 제목·저자·venue·year 정확히 일치 확인) | OK (sigops 수락 목록과도 일치) | OK (main track으로 추정) | N/A (비어 있음, 정직) | OK (본문 접근 불가 상황을 정확히 자백 — 모범적 처리) | **OK** |
| VIRT-HPCA26-05 (DSAssassin) | OK (Semantic Scholar로 제목·저자·venue·year 확인) | OK | OK | UNVERIFIED (main track 추정) | **UNVERIFIED** — 본지 확인 시도 시 IEEE Xplore가 본 검증에서도 빈 페이지를 반환, 초록 원문 자체를 확보하지 못해 17.19 Kbps/85.7%/F1 수치들을 독립 대조 못함 | OK (paywall 상황이 본 검증에서도 재현됨 — 카탈로그 주장이 사실) | **UNVERIFIED** (수치·메커니즘 세부) |
| VIRT-CCGRID24-03 (Eswaran DS) | OK (Doctoral Symposium, pp.667–670 확인) | **오류**: 공유 DOI는 이 논문 것이 아님 | OK | OK (Doctoral Symposium 확인) | N/A (비어 있음) | OK | **중대한 오류** (DOI) |
| VIRT-CCGRID24-06 (HAPPIES) | OK (main track, pp.514–524 확인) | **오류**: 공유 DOI는 이 논문 것이 아님 | OK | OK | N/A (비어 있음, classification=CONTEXT라 적절) | OK | **중대한 오류** (DOI) |

---

## 발견된 문제 상세

### 1. [중대한 오류] CCGRID24-03 / CCGRID24-06 — 공유 DOI 10.1109/CCGrid59990.2024.00075는 **둘 다** 틀렸다

과제에서 이미 의심된 대로 두 레코드가 동일한 DOI(`10.1109/CCGrid59990.2024.00075`)를 갖고 있었다. Crossref에서 이 DOI를 직접 조회한 결과:

> DOI 10.1109/CCGrid59990.2024.00075 → **"Training Computer Scientists for the Challenges of Hybrid Quantum-Classical Computing"** (De Maio, Kanatbekova, Zilk, Friis, Guggemos, Brandic), CCGrid 2024

즉 이 DOI는 완전히 무관한 제3의 논문에 속한다. **두 레코드 모두 오답**이며, "둘 중 하나만 맞다"는 가정 자체가 틀렸다.

Crossref 서지 검색으로 정답 DOI를 복원했다:
- **VIRT-CCGRID24-03** (Eswaran/Yan/Gopalan, "Incorporating Memory Sharing-awareness in Multi-VM Live Migration", Doctoral Symposium, pp.667–670) → 올바른 DOI는 **`10.1109/CCGrid59990.2024.00084`**
- **VIRT-CCGRID24-06** (Huang et al., "HAPPIES: a History-Aware Efficient Cloud Resource Overcommitment System", main track, pp.514–524) → 올바른 DOI는 **`10.1109/CCGrid59990.2024.00064`**

(두 값 모두 Crossref의 서지매칭 검색 결과이며, IEEE Xplore 원본 TOC로 재대조하면 가장 확실하다. 다만 제목·저자가 완전히 일치하는 유일한 검색결과였으므로 신뢰도는 높다.) 저자·venue·pubtype(main track vs. doctoral symposium)은 두 레코드 모두 정확했다.

### 2. [경미한 오류] EUROSYS25-03 (HyperAlloc) — STREAM 수치 중 1건 불일치 가능성

카탈로그의 quantitative_claims: "STREAM 1st percentile … 70.1 GB/s (HyperAlloc) vs **31.9 GB/s (virtio-mem)** vs 30.9 GB/s (virtio-balloon)". 저자 호스팅 PDF를 원문 대조한 결과 70.1(HyperAlloc)과 30.9(virtio-balloon)는 정확히 일치했으나, virtio-mem 쪽 수치는 논문에서 **18.4 GB/s(virtio-mem+VFIO 조건)**로 나타나는 것이 확인되어 31.9라는 값을 원문에서 찾지 못했다. 두 가지 다른 실험 조건(VFIO 유무)이 혼동되었을 가능성이 있다. 나머지 6개 수치(reclaim throughput 344.8/34/0.95 GiB/s, 362x/10x speedup, 17% footprint, CPU 0.51%/0.15%, ~6% install overhead)는 모두 원문과 정확히 일치했다.

### 3. [경미한 오류] EUROSYS24-01 (HD-IOV) — 저자 명단 불완전

카탈로그는 저자를 "Zongpu Zhang; Jiangtao Chen; Banghao Ying; et al."로 축약했으나, 정작 카탈로그가 근거로 인용한 바로 그 GitHub artifact(Maphist0/hdiov-ae)의 인용 정보에 전체 10명(Zongpu Zhang, Jiangtao Chen, Banghao Ying, Yahui Cao, Lingyu Liu, Jian Li, Xin Zeng, Junyuan Wang, Weigang Li, Haibing Guan)이 명시되어 있다. 확보 가능했던 정보를 활용하지 않은 완성도 문제다. (참고: "2.96x device density"와 "2.9x faster initialization" 수치는 같은 README에서 **원문 그대로** 확인되어 정확했다.)

### 4. [해결] OSDI26-06 (Nixie) — OSDI 2026 공식 소속 확인

2026-09-21 최종 pass에서 USENIX 공식 page
`https://www.usenix.org/conference/osdi26/presentation/xu-yechen`을 확인했다. 제목,
저자 5명, OSDI 2026, pages 2085–2101이 모두 record와 일치한다. 이전 pass가 추정한
`/presentation/xu` slug가 틀렸던 것이 원인이며, venue/year 미확인 상태는 해소됐다.

### 5. [미확인] HPCA26-05 (DSAssassin) — 수치·메커니즘 디테일은 독립 확인 불가

DOI·저자·venue·year는 Semantic Scholar를 통해 정확히 일치 확인했다(Benfeng Chen, Kun Li, Shuwen Deng, Dongsheng Wang, Yun Chen — 카탈로그와 정확히 동일; 참고로 IEEE Xplore를 직접 재현 시도했을 때 한 소형 요약 모델이 "Ben Chen"/"Kunlin Li"로 오기했으나 이는 그 요약 과정의 오류였고 Semantic Scholar 원본 데이터로 교차 검증해 카탈로그 표기가 맞음을 확인함). 그러나 본문/초록 전문은 이번 검증에서도 IEEE Xplore가 빈 콘텐츠를 반환해 확보하지 못했다 — 카탈로그가 스스로 밝힌 "paywall/빈 렌더링" 상황이 그대로 재현됐다. 따라서 17.19 Kbps 공변 채널, 85.7% 웹사이트 지문 인식률, F1 92.0%/98.4% 키스트로크 추론 등 수치들과 "Scalable IOV 격리를 깬다"는 구체적 메커니즘 서술은 이번 검증으로 독립 확인하지 못했다(반증도 못했다). evidence_depth=ABSTRACT라는 자기 평가는 정직하고 타당하다.

### 6. [검증 통과 — 중요] MICRO24-02 (Elastic Translations) — 결정적 분류 근거는 실제로 논문에 있음

이 레코드가 CORE로 분류된 근거("KVM의 nested/stage-2 페이지 테이블을 직접 관리한다")를 저자 PDF 원문에서 직접 검색한 결과, 다음 문장들이 실제로 존재함을 확인했다:
- "The contiguous bit in the nested page tables is managed during nested faults by KVM."
- "ET allows the caching of coalesced 2D GVA to HPA translations in the TLB."
- "ET also supports virtualized execution under KVM, transparently managing the contiguous bit in the nested page tables."

즉 이 논문은 단순 TLB coalescing 논문이 아니라 실제로 KVM nested paging을 다루며, 가상화 실행에서 30% 평균/최대 150% 개선이라는 수치도 확인된다. **이번 배치에서 가장 리스크가 컸던 "결정적 분류 판단"은 검증을 통과했다.**

---

## 종합 평가

최종 재확인 기준 Nixie의 venue 미확인은 해소됐다. 남은 표본 이슈는 HyperAlloc 수치 1건,
HD-IOV 저자 축약, DSAssassin 세부 수치/메커니즘 미확인이다. CCGRID24-03/06 DOI 오류는
각각 올바른 값으로 복원됐고 raw batch에도 역반영됐다.

## 2026-09-21 최종 upload/retrieval reconciliation

- 최종 corpus record 410건과 `PAPER_CATALOG.csv` 410행은 ID 집합이 완전히 일치한다.
- batch/log paper record 397개 ID와 merged 410개 ID를 대조해, `_src: batch6c.yaml`을
  가리키지만 원 파일이 없던 CCGrid26 9건 + HPDC26 4건을 발견했다. 13건 모두 corpus에는
  이미 있었으므로 paper 누락은 아니며, 누락된 raw provenance layer를 `batches/batch6c.yaml`로
  복원했다.
- raw batch와 merged가 달랐던 DOI 정정 3건과 HyperAlloc `[VERIFY]` 경고를 raw batch에도
  동기화했다.
- `possible_omissions`에만 남은 EuroSys24/SOSP24 19개 제목은 원문을 읽지 못해 판정을
  확정하지 않은 `BORDERLINE/UNRESOLVED`다. 누락으로 숨기지 않고
  `batches/census24a_eurosys_osdi_sosp.yaml`에 제목·venue·year·탐색 근거가 보존돼 있다.
- 확정된 corpus 기준 의도적 배제는 DROP 48건이다. duplicate DOI/duplicate ID는 0건이며,
  ASPLOS 프로그램의 wrong-year/re-presentation 5건은 최종 corpus에서 제외된 상태다.

### 구조화 source 필드가 비어 있는 title-only record의 공식 program pointer

아래 record는 DOI/개별 URL/fullpaper가 `UNKNOWN`이지만, paper 자체를 확인한 공식 program
pointer를 이 표에 보존한다. PDF를 repository에 저장하지 않는 정책이므로 PDF 부재는 누락이 아니다.

| records | official source |
|---|---|
| `VIRT-HPCA25-04`, `-07`, `-08`, `-09` | https://hpca-conf.org/2025/main-program/ |
| `VIRT-MICRO25-07`, `-08`, `-09`, `-10` | https://microarch.org/micro58/program/index.php |
| `VIRT-HPCA26-01`, `-06`–`-11` | https://2026.hpca-conf.org/ |
| `VIRT-OSDI26-10` | https://www.usenix.org/conference/osdi26/presentation/srivatsan |
| `VIRT-OSDI26-14` | https://www.usenix.org/conference/osdi26/presentation/chai |
| `VIRT-OSDI26-06` (resolved venue flag) | https://www.usenix.org/conference/osdi26/presentation/xu-yechen |

이 표본을 근거로 판단하면, 이 코퍼스는 **부분적으로만 신뢰할 수 있다**. 긍정적인 면: 저자들이 스스로 "UNKNOWN", "ABSTRACT depth", "artifact-only evidence" 등을 매우 정직하게 표기하고 있고, 실제로 원문·GitHub artifact·공식 프로그램과 대조했을 때 제목·저자·핵심 수치의 정합률이 상당히 높았다(특히 S-NIC, VPRI, Faascale, SOSP25-01, 그리고 가장 중요하게는 MICRO24-02의 결정적 분류 판단까지 전부 검증 통과). 즉 "지어낸" 흔적은 거의 없었다.

부정적인 면: 크로스체크 없이 필드를 그대로 복사한 곳에서 명백한 사실 오류가 나왔다. 특히 CCGRID24-03/06의 DOI 오류는 심각하다 — 단순 오탈자가 아니라 **완전히 다른, 무관한 논문의 DOI가 두 개의 서로 다른 레코드에 중복 삽입**되어 있었고, 이는 자동 매칭/스크래핑 파이프라인이 검증 없이 잘못된 DOI를 채워 넣었을 가능성을 시사한다. 이런 유형의 오류가 검증 대상 12건 중 2건(전체 표본의 1/6)에서 나왔다는 것은, 나머지 398건에도 비슷한 DOI 오류가 산재할 가능성을 배제할 수 없다는 뜻이다. 결론적으로: **개별 레코드의 서술(메커니즘, 분류 근거, 정성적 내용)은 신뢰도가 높지만, DOI 같은 "기계적으로 채워 넣은" 식별자 필드는 별도의 전수 재검증 없이는 신뢰해서는 안 된다.** 이 코퍼스를 인용/링크 용도로 그대로 사용하기 전에 최소한 DOI 필드 전체에 대한 Crossref/DOI 리졸버 배치 검증을 권장한다.

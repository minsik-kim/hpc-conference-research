> ## ⚠️ 정정 고지 (2026-09-06 추가)
>
> **이 문서의 일부 주장은 `09_ADVERSARIAL_NOVELTY_AUDIT.md`의 반례 탐색으로 반박(FALSIFIED)되거나 약화되었다.**
> 이 문서를 인용·활용하기 전에 반드시 **`09` §13의 문서별 정정표**를 먼저 확인할 것. 특히:
> - `09` §0.1 — **인용 자체가 틀린 항목 3건** (SC25 Aurora 저자·소속, 504-GPU 논문의 수치, Gleaner의 수치). **절대 그대로 쓰지 말 것**
> - `09` §0.2 — "65.7%" 수치 해석 오류 → overall 40.0% vs 1.4%
> - `09` §2 — "센터 주도 SC 본트랙 논문 0편" 주장 **FALSIFIED** (반례 9편). SC의 State of the Practice는 **Technical Papers 트랙 내 토픽 영역**이며 별개 트랙이 아니다
> - `09` §4 — telemetry 비용 관련 헤드라인 가설 **not novel**. retention 해상도 축만 무조건 생존
> - `09` §5 — cross-layer RCA 주장 **FALSIFIED as stated** (Beacon, NSDI'19)
> - `09` §7 — safe remediation 비용모델 주장 **FALSIFIED** (HPDC'24)
> - `09` §9 — **KISTI 국내 선행연구 16편**이 이 문서군에서 누락되어 있었다
>
> **후속 문서:** `08`(보존 요구사항) · `09`(반례 감사) · `10`(최종 후보 순위) · `11`(첫 실험 설계) · `12`(미확보 자료 watchlist)

# 03. SC REGULAR PRECEDENTS — 운영 문제가 어떻게 일반화 가능한 systems research로 변환되었는가

**작성일:** 2026-09-06
**목적:** "실제 operational problem을 어떻게 SC Technical Paper 수준의 research question으로 바꾸었는가"에 답하는 논문만 골라 심층 분석한다. 단순 관련 논문은 `02_PAPER_CENSUS`에 있다.

**분석 틀 (각 precedent마다):**
**A** Operational starting point — 실제로 어떤 문제가 있었는가
**B** Why existing practice was insufficient — threshold/heuristic/dashboard/기존 ML이 왜 부족했는가
**C** Research abstraction — site-specific 문제를 어떤 일반 systems problem으로 추상화했는가
**D** Novel mechanism — 새 algorithm/system mechanism은 무엇인가
**E** Evaluation — 몇 개 시스템 / 몇 노드 / 얼마 기간 / production trace인가 / online deployment인가
**F** Generality — 다른 workload·system에 적용 가능함을 어떻게 입증했는가
**G** Why this could be an SC regular paper — 단순 engineering report와 무엇이 달랐는가

> ⚠️ **트랙 표기 경고.** SC 논문 페이지는 모든 트랙을 "Technical Papers Archive"로 표시하므로 Technical Paper와 State of the Practice를 구분할 수 없었다. 아래 모든 SC 항목은 `TRACK-UNKNOWN`이며, 내용에 근거한 추정만 병기한다. **"이 논문은 SC Technical Paper였다"고 인용문에 쓰지 말 것.**

---

# PART I — 최상위 precedent 9편 심층 분석

---

## P1. Live Forensics for HPC Systems: A Case Study on Distributed Storage Systems (Kaleidoscope) — SC20

**Jha, Cui, Banerjee, T. Xu, Enos, Showerman, Kalbarczyk, Iyer (UIUC / NCSA)** · SC20 본프로그램 · `TRACK-UNKNOWN` (내용상 Technical Paper 거의 확실) · ACM `10.5555/3433701.3433787`, NSF PAR `https://par.nsf.gov/servlets/purl/10293041`
**L5 · D4 · P4 · SC-REGULAR-PRECEDENT**

**A. Operational starting point.** Blue Waters의 distributed storage(Cray Sonexion: 6 MDS, 420 OSS, 17,280 HDD)에서 장애와 성능 저하가 계속 발생하는데, 어느 컴포넌트가 원인인지, 신뢰성 장애인지 단순 과부하인지 운영자가 판별할 수 없었다.

**B. Why existing practice was insufficient.** 기존 방식은 사후(post-hoc)·수동이었다. 스토리지 관리자가 로그를 grep하고 상관관계를 눈으로 찾았다. 문제 규모(2년간 843건의 실제 이슈)에서 이 방식은 확장되지 않았고, 무엇보다 **"장애"와 "과부하"를 구분하지 못했다** — 두 경우의 조치가 완전히 다른데도.

**C. Research abstraction.** 사이트 문제를 **"계층적 도메인 지식으로 구조화된 확률 모델 위에서, 관측된 telemetry로부터 (i) 결함 컴포넌트를 localize하고 (ii) 장애 모드를 분류하는 문제"**로 추상화했다. 즉 "우리 Lustre가 느리다"가 아니라 "계층적 시스템에서의 near-real-time localization + failure-mode classification"이다.

**D. Novel mechanism.** hierarchical domain-guided ML models — 스토리지 스택의 물리적/논리적 계층 구조를 모델 구조에 인코딩하고, PGM 기반 localization과 LOF 기반 diagnosis를 결합해 **1분 이내**에 결과를 낸다.

**E. Evaluation.** Blue Waters production telemetry **2년**, 라이브 운영 **3개월**, **843건의 운영자가 해결한 실제 이슈**를 ground truth로 사용. **component localization 99.3%, root-cause identification 95.8%, overhead <0.01%.** 실제 배포(D4).

**F. Generality.** 계층 구조를 도메인 지식으로 손수 구축하는 방식이 다른 서브시스템에도 이식 가능하다고 주장한다. **이것이 이 논문의 가장 약한 부분이다** — 다른 시스템/서브시스템으로의 이식은 실증되지 않았고, Cray/Lustre 세대에 특화되어 있다.

**G. Why SC regular.** reviewer가 요구하는 것을 전부 갖췄다: production 데이터, 실제 배포, 정량화된 운영 성과, 그리고 이식 가능하도록 일반적으로 기술된 방법. **특히 "843건의 operator-resolved ground truth"가 결정적이다.** 이 숫자가 SC에서 HPC RCA의 기준선을 세웠고, 2026년 현재까지 아무도 넘지 못했다.

> **KISTI 시사점:** A축(cross-layer RCA)에 진입하려면 이 기준선과 비교당한다. 알고리즘보다 **운영팀의 incident labeling 약속을 먼저 확보**해야 한다.

---

## P2. Prodigy: Toward Unsupervised Anomaly Detection in Production HPC Systems — SC23

**Aksar (BU/Sandia), Sencan (BU), Schwaller, Aaziz, Leung, Brandt (Sandia), Kulis, Egele, Coskun (BU)** · SC23 본프로그램 · `TRACK-UNKNOWN` (Technical Paper 거의 확실) · `10.1145/3581784.3607076`
**L3(+L5 설명) · D4 · P4 · SC-REGULAR-PRECEDENT**

**A. Operational starting point.** Sandia의 production 시스템(Eclipse 1,488 노드, Volta 52 노드)에서 성능 이상이 발생하지만, **labeled training data가 존재하지 않는다.** 운영자는 무엇이 anomaly인지 사후에만 안다.

**B. Why existing practice was insufficient.** 같은 그룹의 선행 연구가 정확히 이 벽에 부딪혔다: Tuncer et al.(TPDS 2019)은 supervised, Proctor(ISC'21)는 semi-supervised, E2EWatch(Euro-Par'21)는 supervised + Grafana 통합, ALBADross(Cluster'22)는 active learning으로 **labeling 비용을 28배 줄였지만 여전히 label이 필요했다.** 라벨 요구를 0으로 만드는 것이 남은 문제였다.

**C. Research abstraction.** **"label이 존재하지 않는 것이 제약이 아니라 문제 정의 자체인 환경에서의 anomaly detection"**으로 추상화했다. 이 프레이밍이 기여의 본체이며, 알고리즘(VAE)이 아니다.

**D. Novel mechanism.** TSFRESH feature 위의 VAE + CoMTE counterfactual explanation. 806개 metric을 156개로 축소(per-core metric은 noisy하다고 판단해 제거), 794개 TSFRESH feature를 Chi-square top-2000으로 선택. job-level·node-level 양쪽에서 예측 설명을 생성.

**E. Evaluation.** Eclipse 1,488 노드 + Volta 52 노드, 806→156 metric @1Hz, 모니터링 클러스터 약 10 TB/day. **offline F1 0.95, production 배포에서 88% detection accuracy.** LDMS+DSOS+Grafana+Django로 운영자 콘솔에 실제 연결(D4).

**F. Generality.** "healthy training set만 있으면 된다"는 요구가 이식성의 근거다. **그러나 cross-system validation은 없다** — 저자들 스스로 다른 문헌(AI4Sys'23 워크숍 3쪽 논문)에서 *같은 시스템의 노드 간에도* generic model F1 0.726 vs node-specific F1 0.898로 **0.17 F1의 일반화 격차**가 있다고 보고했다.

**G. Why SC regular.** offline 점수와 **production 배포 숫자를 함께** 보고했다는 점. SC reviewer는 2023년 이후 이것을 기대한다. 또한 anomaly가 대체로 synthetic injection으로 검증되었음을 숨기지 않았다.

> **KISTI 시사점:** 이 계열의 후속인 **SC25 NodeSentry**가 F1을 0.560 개선하며 같은 lane을 다시 채웠다. **node-level anomaly detector를 새로 제안하지 말 것.** 이 lane은 SC23과 SC25로 닫혔다.

---

## P3. Fine-grained Automated Failure Management for Extreme-Scale GPU Accelerated Systems — SC25

**Levitt, Barella, Zeltner, Musta, Cheney, Espinosa, Franza, Gerofi (Intel / Argonne)** · SC25 본프로그램 · `TRACK-UNKNOWN` (SotP 또는 Technical) · `10.1145/3712285.3759883`
**L7 · D5 · P3/P4 · SC-REGULAR-PRECEDENT — census 전체에서 유일한 진짜 L7/D5**

**A. Operational starting point.** Aurora(10,624 노드, 63,744 Intel Max GPU)에서 MTBF가 떨어지면서 **가용성을 지배하는 것이 MTBF가 아니라 MTTR**이 되었다. 수동 서비싱이 너무 느렸다.

**B. Why existing practice was insufficient.** 노드 health check는 규칙 기반으로 drain까지만 하고, 그 다음은 사람이 티켓을 열고 하드웨어 엔지니어가 처리한다(cf. ORNL Frontier `checknode`, CUG'23). 이 인간 루프가 MTTR의 병목이었다.

**C. Research abstraction.** **"장애 이력 통계로부터 실시간 수리 의사결정을 내리는 문제"** — 구체적으로 fine-grained multi-strike repair policy. "예측"이 아니라 "행동"으로 문제를 옮긴 것이 핵심이다.

**D. Novel mechanism.** 이벤트 이력을 위한 **centralized meta-database** + 다단계(multi-strike) 수리 정책 + 자동 복구 프레임워크. 학습 모델이 아니라 정책 공학이며, 저자들도 그렇게 제시한다.

**E. Evaluation.** Aurora production, 실제 배포(D5). **MTTR 최대 84배 감소** — 수동 서비싱 baseline 대비.

**F. Generality.** meta-database + multi-strike policy 설계는 재사용 가능하게 기술되었으나, 단일 사이트 결과다.

**G. Why SC regular.** **SC가 "탐지만 하는 시스템"이 아니라 "행동하는 시스템"을 받아준다는 유일한 증거.** 그리고 헤드라인 지표가 F1이 아니라 **운영 지표(MTTR)**다.

> **KISTI 시사점:** closed-loop remediation을 주장하려면 이 논문이 인용 기준점이다. 동시에 경고이기도 하다 — 84배는 *수동 baseline* 대비 값이며, 학습 정책이 규칙 정책을 이겼다는 증거가 아니다.

---

## P4. GPU Lifetimes on Titan (SC20) → Story of Two GPUs (SC25) — 한 계보로 읽을 것

**SC20:** Ostrouchov, Maxwell, Ashraf, Engelmann, Shankar, Rogers (ORNL) · `10.1109/SC41405.2020.00045`
**SC25:** S. Cui, Patke, Z. Chen, Ranjan, H. Nguyen, P. M. Cao, S. Jha, Bode, Bauer (UIUC/NCSA), Narayanaswami, Sow (IBM), Di Martino, Kalbarczyk, R. K. Iyer · `10.1145/3712285.3759821`
**둘 다 L3 · D2 · P4 · SC-REGULAR-PRECEDENT**

**A.** 센터가 수년치 GPU 오류 로그를 갖고 있지만, "GPU가 왜, 언제 죽는가"에 대한 과학적 답이 없다.

**B.** 대시보드의 기술통계(descriptive plot)로는 원인 구조를 말할 수 없다. 특히 "냉각 구조와 job 배치가 수명에 영향을 주는가" 같은 질문은 평균과 카운트로는 답이 안 된다.

**C.** **적절한 통계학의 문제로 추상화했다.** SC20은 survival analysis, SC25는 MTBE 분석 + 대규모 가용성 투영.

**D.** SC20: time-between-failures + survival analysis. SC25: 장애 모드 taxonomy + MTBE + 더 큰 규모로의 가용성 투영.

**E.** SC20: Titan **18,688 GPU, 약 6년, 10만 GPU-년** 이상의 수명 데이터. SC25: NCSA Delta/DeltaAI **1,056개 A100+H100, 2.5년, 1,170만 GPU-시간**의 오류 데이터.

**F.** SC20은 **데이터와 분석 코드를 공개**했다. SC25는 투영 모델로 일반화를 주장한다.

**G.** 두 논문 모두 **운영 데이터 자산에서 *과학적 결과*를 뽑았다.** SC20: GPU 수명이 냉각 구조상의 위치·job 배치와 상관된다. SC25: **H100 메모리 MTBE가 A100보다 3.2배 나쁘고**, 더 큰 규모에서는 **약 5% 노드 overprovisioning**이 필요하다. 기술통계가 아니라 결정에 쓰이는 수치다.

> **KISTI 시사점:** 수년치 GPU 오류 로그를 보유한 국가센터에게 **가장 직접적으로 모방 가능한 패턴**이다. 필요한 것은 새 알고리즘이 아니라 제대로 된 통계와 공개다.

---

## P5. Cost-Aware Prediction of Uncorrected DRAM Errors in the Field — SC20

**Boixaderas, Zivanovic, Moré, Bartolome, Vicente, Casas, Carpenter, Radojković, Ayguadé (BSC / UPC)** · SC20 · `TRACK-UNKNOWN` · 페이지 `sc20.supercomputing.org/.../pap241.html` (**DOI 미기재 — 인용 전 확인**)
**L4 · D2/D3 · P4 · SC-REGULAR-PRECEDENT**

**A.** MareNostrum 3에서 uncorrected DRAM error가 job을 죽인다. 사전 조치(page offlining, node draining)를 하려면 예측이 필요하다.

**B.** 기존 예측 연구는 **잘못된 목적함수를 최적화하고 있었다.** F1/precision/recall은 운영자가 신경 쓰는 값이 아니다 — 운영자는 잃은 node-hour를 신경 쓴다. 그리고 오탐(불필요한 drain)과 미탐(job 사망)의 비용이 완전히 비대칭이다.

**C.** **"운영 비용 함수 하의 예측 문제"**로 추상화했다. 모델 자체(random forest)는 평범하다. **평가 방법론이 기여다.**

**D.** random forest 분류기 + **비용-편익 평가 방법론**. 분류 지표를 node-hour 지표로 대체.

**E.** MareNostrum 3(3,056 노드) **2년치 error log**. **손실 계산시간 최대 57% 감소 ≈ 연 21,000 node-hour 절감.** 오픈소스 공개. 단, 절감은 로그에서 시뮬레이션한 값이지 운영에서 측정한 값이 아니다.

**F.** 비용 모델 프레이밍은 어떤 시스템·어떤 예측기에도 적용된다 — 그것이 일반화의 근거다. 하드웨어 자체는 한 기계·한 DRAM 세대.

**G.** **"우리 분류기가 좋다"를 "우리 운영이 싸졌다"로 바꿨다.** 이것이 engineering report와의 결정적 차이다.

**후속:** 같은 그룹이 **HPDC 2024**에서 *Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field*(`10.1145/3625549.3658686`)로 예측에서 **행동**으로 넘어갔다. MareNostrum 운영진(Moré, Bartolome, Vicente)이 공저자로 들어가 있고, 그것이 "in the field" 주장을 신뢰 가능하게 만든다.

> **KISTI 시사점:** 예측을 제안한다면 반드시 이 프레이밍을 채택할 것. 그리고 **운영팀을 공저자로 올릴 것** — BSC 사례가 그 효과를 보여준다.

---

## P6. A Taxonomy of Error Sources in HPC I/O Machine Learning Models — SC22

**Isakov, Currier, del Rosario, Kinsy (ASU); Madireddy, Balaprakash, Carns, Ross (ANL); Lockwood (LBNL)** · SC22 · `10.1109/SC41404.2022.00021`
**L3(meta) · D2 · P4 · SC-REGULAR-PRECEDENT — 가장 저평가된 precedent**

**A.** I/O throughput을 예측하는 ML 모델을 만들어 배포했는데 **실패한다.** 왜인지 모른다.

**B.** 기존 관행은 정확도가 떨어지면 모델을 바꾸는 것이었다. 실패의 *종류*를 구분하는 어휘가 없었다.

**C.** **"배포된 운영 ML 모델의 오차를 원인별로 귀속시키는 문제"**로 추상화했다. 즉 모델의 메타 수준을 연구 대상으로 삼았다.

**D.** 5가지 실패 모드 taxonomy — poor application modeling, poor system modeling, inadequate dataset coverage, I/O contention, I/O noise — 그리고 자기 모델의 오차를 각 모드에 귀속시키는 진단 도구.

**E.** 두 개의 주요 HPC 시스템, **수년치 로그**.

**F.** taxonomy는 구조적으로 일반화된다. 정성적이라는 것이 약점.

**G.** **negative results / epistemics 논문이 SC regular가 될 수 있음을 증명한다.** 새 알고리즘이 없다. 데이터와 정직함만 있다.

> **KISTI 시사점:** 이 분야에 새로 진입하는 그룹에게 **레버리지가 가장 높은 논문 형태**다. 한강에서 ML 모델을 돌려보고 왜 안 되는지를 체계적으로 쓰는 것만으로 SC regular 형태가 성립한다.

---

## P7. A Digital Twin Framework for Liquid-cooled Supercomputers as Demonstrated at Exascale (ExaDigiT) — SC24

**Brewer, Maiterth, V. Kumar, Wojda, Bouknight, Hines, W. Shin, Greenwood, Grant, Williams, F. Wang (ORNL)** · SC24 · `10.1109/SC41406.2024.00029`
**L4+L6 · D3/D4 · P4 · SC-REGULAR-PRECEDENT**

**A.** exascale 액냉 시스템에서 전력·냉각·스케줄링이 강하게 결합되어 있는데, "이 정책을 바꾸면 어떻게 되는가"를 production에서 실험할 수 없다.

**B.** 대시보드는 과거만 보여준다. 정책 변경의 counterfactual을 평가할 수단이 없었다 — 이는 모든 L6/L7 연구를 가로막는 메타 문제다.

**C.** **"결합된 물리-스케줄링 시스템의 검증된 시뮬레이션(digital twin)"** 문제로 추상화.

**D.** 세 모듈 결합: resource-allocator & power simulator + transient thermo-fluidic cooling model + AR visualization.

**E.** **Frontier(9,408 노드) + 중앙 에너지 플랜트, 6개월 telemetry를 replay하여 V&V.** 오픈소스, ORNL 운영에서 what-if 연구에 사용.

**F.** "실무자를 위한 lessons learned" 절을 명시적으로 두어 이식성을 주장한다.

**G.** **SC가 facility 계층과 IT 계층의 통합을 보상한다는 증거.** 건물을 소유한 센터가 대학 그룹 대비 구조적 우위를 갖는 축이다.

> **KISTI 시사점:** ExaDigiT는 물리를 풀었다. **정책 평가 방법론은 아무도 하지 않았다** — 이것이 `05`/`06`의 gap G10이다.

---

## P8. SIREN: Software Identification and Recognition in HPC Systems — SC25

**Jakobsche, Robertsén, Jones, Haus (HPE), Ciorba (Univ. of Basel)** · SC25 · `10.1145/3712285.3759873`
**L0–L2 · D3/D4 · P4 · SC-REGULAR-PRECEDENT — 숨은 카드**

**A.** ODA를 애플리케이션 단위로 하려면 어떤 애플리케이션이 돌았는지 알아야 하는데, **job 이름은 사용자가 아무렇게나 붙인 거짓말**이다.

**B.** 기존 관행(job name, module load 로그, 실행 파일 경로)은 신뢰할 수 없고, 이 부정확성이 **다른 사람들의 ODA 분석 결과를 조용히 무효화한다.**

**C.** **"프라이버시와 무결성을 보존하면서 실행 바이너리를 식별하는 문제"**로 추상화.

**D.** process-level metadata + environment + **실행 파일의 fuzzy hash**. 반복 실행을 인식하고 미지 바이너리를 유사도로 식별.

**E.** LUMI에서 opt-in 배포 캠페인.

**F.** opt-in coverage bias와 빌드 변형에 대한 fuzzy hash 민감도가 한계.

**G.** **telemetry 수집 인프라 자체가 SC regular 기여가 될 수 있음을 보여준다** — 단, 그것이 *다른 연구를 무효화하는 전제조건 문제*를 풀 때만.

---

## P9. MCBound (SC24) · Not All GPUs Are Created Equal (SC22) — "측정 → 행동" 2단 아크

**MCBound:** Antici, Bartolini, Kiziltan, Babaoglu (Univ. Bologna), Kodama (RIKEN) · SC24 · `10.1109/SC41406.2024.00062` · L4 · D3/D4 · P4
**Not All GPUs:** Sinha, Guliani, Jain, Tran, Sinclair (UW-Madison / AMD Research), Venkataraman · SC22 · 페이지 `pap186.html` (**DOI 미기재 — 확인 필요**) · L3 · D2 · P4

**MCBound.** Fugaku **220만 job run**에서 과거 telemetry로 스스로 label을 만들어(self-labeling), job이 실행되기 *전에* memory-bound인지 compute-bound인지 분류한다. F1-macro ≥ 0.89, Fugaku에 구현, 오버헤드 무시 가능. → **"과거 telemetry에서 자기 label을 유도한다"는 패턴을 이 census 최대 job 수 규모로 실행한 사례.**

**Not All GPUs.** Summit(ORNL) / Vortex(Sandia) / Longhorn(TACC) V100 + Corona(LLNL) MI60, **GPU의 90% 이상 샘플링, 10만 GPU-시간 이상** 수집. 명목상 동일한 GPU 간 **평균 32%, 최대 72%** 성능 편차. → 그리고 **SC24의 PAL**(`10.1109/SC41406.2024.00032`)이 이 측정 결과를 스케줄링 정책으로 전환했다.

**G(공통).** SC는 **측정 논문을 먼저 받아주고, 메커니즘 논문을 그 다음에 받아준다.** 이 아크는 census 전체에서 반복 확인된다:

| 측정 (year 1) | 메커니즘 (year 2) |
|---|---|
| SC22 Not All GPUs Are Created Equal | SC24 PAL (variability-aware scheduling) |
| SC20 GPU Lifetimes on Titan | SC25 Story of Two GPUs |
| SC21 Revealing Power/Energy/Thermal Dynamics (Summit) | SC24 ExaDigiT |
| IPDPS'20 Dragonfly variability (Bhatele) | IPDPS'26 Elusive GPU performance |

> **KISTI 시사점:** **1년차 characterization + 2년차 mechanism의 2편 계획이 이 venue의 실제 작동 방식과 일치한다.** 처음부터 메커니즘을 노리는 것보다 성공률이 높다.

---

# PART II — SC 밖의 최강 archival precedent (비교 기준)

SC만 보면 기준을 오판한다. 다음은 KISTI 제출물이 실제로 비교당할 논문들이다.

## Q1. Reinforcement Learning-based Adaptive Mitigation of Uncorrected DRAM Errors in the Field — HPDC 2024
Boixaderas 외 (BSC + MareNostrum 운영진) · `10.1145/3625549.3658686`, pp.240–252 · **L4→L7 · D3–D5 · P3/P4**
HPDC/IPDPS/Cluster 2020–2026 약 700건 중 **L7/D5에 도달한 사실상 유일한 논문.** 센터의 실제 결정(페이지를 offline 할 것인가, 노드를 drain 할 것인가)을 형식적 순차 의사결정 문제로 바꾸고, 그 센터의 필드 데이터로 학습하고, 운영 비용 함수로 평가했다.
> **"operational problem → generalizable research"의 최고 템플릿.**

## Q2. Correlation-wise Smoothing: Lightweight Knowledge Extraction for HPC Monitoring Data — IPDPS 2021
Netti, Tafani, Ott, Schulz (LRZ/TUM) · `10.1109/ipdps49936.2021.00010`, pp.2–12 · **L0/L1 · D2–D4 · P4**
가장 평범한 운영 불만("telemetry가 너무 많다")을 일반적이고 값싸고 평가 가능한 축소 방법으로 바꿨다. **이 다섯 venue를 통틀어 telemetry reduction 논문은 사실상 이것 하나이고, 5년간 후속이 없다.**

## Q3. ALBADross: Active Learning Based Anomaly Diagnosis for Production HPC Systems — IEEE Cluster 2022
Aksar 외 (BU + Sandia) · `10.1109/cluster51413.2022.00048`, pp.369–380 · **L3/L5 · D2–D3 · P4**
운영상의 장애물(label이 없고 전문가 시간이 비싸다)*이* 연구 기여다. **동일 F1에 label 28배 절감.** label 0에서 시작하는 센터에 이식성이 가장 높다.

## Q4. Aarohi: Making Real-Time Node Failure Prediction Feasible — IPDPS 2020
Das, Mueller, Rountree (NCSU + LLNL) · `10.1109/ipdps47924.2020.00115`, pp.1092–1101 · **L4 · D2–D3 · P4**
포화된 주제(failure prediction accuracy)를 **운영자만 알아차릴 제약**(추론이 lead time 안에 끝나야 한다)으로 재프레이밍했다. 운영 경험이 새 연구 축을 만드는 교과서적 사례.

## Q5. DCDB Wintermute — HPDC 2020
Netti, Müller, Guillen, Ott, Tafani, Ozer, Schulz (LRZ + TUM) · `10.1145/3369583.3392674`, pp.101–112 · **L0–L4 · D4/D5 · P3**
아카이벌 문헌에서 HPC ODA의 참조 아키텍처. LRZ에서 실제로 돌아간다. 단, **프레임워크이지 분석이 아니다** — cross-layer RCA 모델을 제공하지 않는다.

## Q6. AIIO — HPDC 2023 / IOAgent — IPDPS 2025
AIIO: Dong, Bez, Byna · `10.1145/3588195.3592986`, pp.155–167 · L5 · D2–D3 · P4
IOAgent: Egersdoerfer, Sareen, Bez, Byna, D. Xu, Dai · `10.1109/ipdps64566.2025.00036`, pp.322–334 · L5/L6 · D2–D3 · P4
센터가 이미 가진 telemetry(Darshan)만으로 per-job L5 진단을 만든 계보이며, **IOAgent는 "trustworthiness-aware LLM agent"라는 2025년 프런티어를 이 venue군에 처음 들여왔다.**

## Q7. Narya — OSDI 2020 (**F축의 최강 falsifier**)
Levy, Yao, Wu, Dang, Huang, Mu, Zhao, Ramani, Govindaraju, Li, Lin, Shafriri, Chintalapati (Microsoft Azure) · USENIX OSDI'20, pp.1155–1170 · **L4+L6+L7 · D5 · P4**
호스트 장애를 예측하고, **온라인 실험/bandit-RL로 완화 조치를 선택**하며, Azure에서 **15개월 운영, VM 중단 26% 감소.** closed-loop remediation을 제안하면 반드시 이것과 비교당한다.

## Q8. SuperBench — USENIX ATC 2024 Best Paper (**C·D축의 최강 falsifier**)
Xiong 외 (MSR + Microsoft) · arXiv 2402.06194; TOCS `10.1145/3767334` · **L2+L3+L6+L7 · D5**
gray failure를 능동 검증으로 잡고, **Selector가 검증 비용과 탐지 이득을 명시적으로 최적화**한다. **수십만 GPU, 2년 배포**, MTBI 최대 22.61배 개선. "telemetry 비용 대 품질" 프레이밍이 이미 존재한다는 가장 위험한 증거 — 단, **능동 벤치마크 스케줄링이지 수동 telemetry 수집이 아니다.**

## Q9. Perseus — FAST 2023 / IASO — ATC 2019 / Fail-Slow at Scale — FAST 2018 (**D축**)
Perseus: Lu 외 (SJTU/Alibaba/Xiamen), 24.8만 드라이브 10개월, fail-slow 304건 발견, p99.99 tail latency 48% 감소, **라벨링된 fail-slow 데이터셋 공개**.
IASO: Panda 외 (Nutanix), 3.9만 노드 1.5년+, peer 비교로 느린 노드를 "수 분 내" 격리.
Fail-Slow at Scale: Gunawi 외 (16개 기관, **LANL·ANL 포함**), 101건 인시던트 보고서로 fail-slow를 1급 장애 모드로 정의.
> **경고:** LANL/ANL이 이미 포함되어 있으므로 "HPC에서 fail-slow는 연구되지 않았다"고 쓸 수 없다. 또한 **"우리는 노드를 peer와 비교한다"는 기여가 될 수 없다.**

## Q10. RCACopilot — EuroSys 2024 / L4 — FSE 2025 (**G축**)
RCACopilot: Chen 외 (Microsoft + UIUC) · `10.1145/3627703.3629553` · 653건 인시던트, Micro-F1 0.766 / **Macro-F1 0.533**, 인시던트당 4.2초. **수집 컴포넌트는 30개 팀에서 4년 이상 운영.**
L4: Jiang 외 · `10.1145/3696630.3728531` · **428건의 실제 LLM 학습 장애**(평균 941 accelerator, 장애당 평균 16.92 GB 로그), **평균 진단 시간 34.7시간, 41.9%가 24시간 초과.** F1 0.873, faulty-node top-1 65.8%.
> **L4의 결정적 사실: 진단 경로에 LLM을 전혀 쓰지 않았다**(Drain + IsolationForest + DTW). 그럼에도 LLM 시대 log-AD baseline들(0.207–0.366)을 압도했다. 이것이 이 공간에서 가장 강력한 anti-LLM 논거다.

---

# PART III — 횡단 패턴: SC가 실제로 보상하는 것

## 3.1 반복 확인된 6가지 패턴

**① 운영 성과 지표로 평가하라.** MTTR 84배(SC25), 손실 node-hour 57%(SC20 BSC), 5% overprovisioning 필요(SC25), HPL 16.8→19.5 PF(ARCHER2), p99.99 48% 감소(Perseus). F1만 보고한 논문은 한 단계 아래로 읽힌다.

**② 측정 먼저, 메커니즘 나중.** §P9의 2단 아크 표 참조.

**③ production 데이터 + 실제 배포 주장을 함께 낼 것.** 2024년 이후 SC에서 "로그로 offline 돌렸다"의 기준선이 눈에 띄게 올라갔다.

**④ 방법론·부정 결과 논문이 통한다.** SC22 I/O ML error taxonomy가 증거.

**⑤ 소수 그룹이 이 공간을 점유하며, 매년 반복 등장한다.**

| 그룹 | 등장 |
|---|---|
| Devesh Tiwari (Northeastern) | SC20 Job Characteristics, SC21 I/O variability, SC23 carbon footprint, SC24 Fugaku incentives |
| Sandia monitoring (Brandt, Schwaller, Aaziz, Leung) | SC21, SC23 Prodigy, SC24 |
| ORNL ODA (W. Shin, F. Wang, Karimi, Zimmer, Atchley, A. Khan) | SC21 → SC24(×2) → **SC26 Best Paper nominee** |
| UIUC (R. K. Iyer) | SC20 Kaleidoscope → SC25 Story of Two GPUs |
| BU (Coskun) ↔ Sandia | ISC'21 Proctor → Euro-Par'21 E2EWatch → Cluster'22 ALBADross → SC'23 Prodigy |
| LRZ/TUM (Netti, Ott, Schulz) | HPDC'20 → IPDPS'21 → Cluster'21 conceptual framework |
| Bologna (Bartolini, Antici, Borghesi) ↔ CINECA & RIKEN | M100 ExaData, F-DATA, SC24 MCBound |

→ **작고 읽기 쉬운 커뮤니티다. cold submission보다 공저·데이터 협력이 훨씬 신뢰도 높은 경로다.**

**⑥ 연구 산출은 시스템 규모가 아니라 학술 파트너 유무와 상관된다.** Bologna↔CINECA, Bologna↔RIKEN, W&M↔ORNL, Basel/TUM↔LRZ, UMD(Bhatele)↔NERSC. 대학 그룹이 결합되지 않은 센터는 practice만 낸다. 그리고 **데이터를 공개한 센터가 곧 연구를 내는 센터**다(ORNL, LRZ, CINECA, RIKEN, NREL, LANL, ALCF vs CSCS, EPCC, JSC, LLNL, TACC, NERSC, CSC, Pawsey).

## 3.2 SC 본프로그램 연도별 규모 (A_SC_main.md, ±2편, 제목 기반 분류 포함)

| 연도 | 열거한 본프로그램 항목 | Core | Broad | Core 비중 |
|---|---|---|---|---|
| SC20 | ~105 | **8** | 14 | ~8% |
| SC21 | ~110 | **4** | 8 | ~4% |
| SC22 | ~92 | **4** | 7 | ~4% |
| SC23 | ~99 | **5** | 11 | ~5% |
| SC24 | ~114 | **10** | 17 | ~9% |
| SC25 | ~120 (reproducibility report ~20편 제외) | **12** | 18 | ~10% |
| SC26 | 미공개 | ≥1 확인 | UNKNOWN | — |

**2021–2023 평탄(연 4–5편) → 2024–2025 계단식 증가(연 10–12편).** 증가분은 거의 전부 (a) GPU/AI 클러스터 신뢰성, (b) power/cooling/carbon/water에서 왔다. **이 공간은 2년 만에 대략 두 배가 되었다.**

## 3.3 SC26 (PARTIAL / NOT YET PUBLISHED)

- 개최: 2026년 11월 15–20일, Chicago McCormick Place. 2026-09-06 현재 **미개최, proceedings 없음.**
- CFP 일정(검증됨, `sc26.supercomputing.org/program/papers/`): abstract 2026-04-01, paper 2026-04-08(연장 없음), AD appendix 2026-04-28(필수), notification 2026-07-01, camera-ready 2026-08-28.
- **State of the Practice 트랙 존속 확인.** 원문 범위: *"All aspects of the pragmatic practices of HPC, including operational IT infrastructure, services, facilities, large-scale application executions and benchmarks"*, 그리고 *"capture experiences and ongoing practice relating to modern computing centers or HPC-related software"*, *"do not need to cover novel research or developments."* → **한강/KISTI-6 운영 논문의 정확한 입구.**
- 확인된 in-scope SC26 논문 1건 (2026-08-13 Best Paper finalist 발표): **From Alert Fatigue to Root Cause: Causal Failure Cascade Discovery in HPC System** — Awais Khan, Christopher Zimmer, Anjus George, Ahmad Maroof Karimi, Feiyi Wang, Woong Shin (ORNL). **DOI 미발행, 초록 미확보.** 저자 구성이 SC21/SC24×2의 ORNL 운영 telemetry 그룹과 정확히 일치한다 — **ORNL ODA 라인이 마침내 Best-Paper-nominated RCA 논문을 냈다.**
- 전체 채택 목록은 fetch 불가(SC26 프로그램 사이트 401, ACM DL/IEEE Xplore 403) → `UNVERIFIED / UNAVAILABLE`.

> ⚠️ **이 한 건이 A축(cross-layer RCA)의 위험도를 크게 올린다.** SC26 논문이 공개되는 즉시 확보해서 읽어야 하며, 그 전에 A축 기반 제안서를 확정하지 말 것.

## 3.4 SC 본프로그램에 **없는** 것 (2020–2025, 실무에서는 흔한데)

| 부재 항목 | 상세 |
|---|---|
| **System log / syslog analytics** | log parsing, template mining, log-sequence anomaly detection 논문이 SC 본프로그램에 **사실상 0편**. SC 본프로그램은 구조화된 수치 telemetry(LDMS, Darshan, power counter, MCE/XID)만 쓴다. 연구판은 DSN/ISSRE/ICSE/FSE/ATC로 간다. → **넓게 열려 있지만, 부재 자체가 "SC reviewer는 log mining을 systems 기여로 보지 않는다"는 신호일 수 있다.** log 논문에는 systems 수준의 payoff(취한 행동, 아키텍처적 발견)를 반드시 붙여야 한다. |
| **production 상호연결망 혼잡 진단 (실계측 counter 기반)** | Slingshot이 도처에 있는데도 **2020–2025 SC 본프로그램에 운영 counter 기반 실운영 혼잡 field study가 없다.** 있는 것은 벤더 협업 characterization(SC20 Slingshot, SC24 GPU-to-GPU, SC24 Frontier network cost) 아니면 **시뮬레이션**(SC22 Dragonfly interference). |
| **facility 예지보전** | CDU, 펌프, 밸브, 칠러, 배전. ExaDigiT가 냉각 플랜트를 모델링하고 Titan GPU 연구가 냉각을 지목하지만, **facility telemetry로 facility 부품 고장을 예측한 논문은 0편.** |
| **telemetry sampling / reduction / retention** | 애플리케이션 측 tracing 유사물만 존재(SC21 Pilgrim, SC24 DFTracer, SC25 TraceFlow). **"시스템 telemetry를 얼마나 버려도 중요한 것을 계속 탐지할 수 있는가"는 SC 본프로그램에 없다.** |
| **self-healing / closed-loop remediation** | 6년간 D5 도달 1편(SC25 Aurora), 그것도 학습이 아니라 정책 공학. **학습 제어, RL-in-the-loop remediation 논문 0편. L5→L7 구간이 census 전체 최대의 구조적 공백.** |
| **HPC straggler / slow-node 탐지** | (ML 학습 프레임워크가 아니라 HPC 배치 시스템에서) telemetry 기반 slow-node 식별 논문 없음. SC24 GVARP가 가장 가깝고 애플리케이션 계측 기반. |
| **cross-site / multi-system 일반화** | **거의 모든 논문이 단일 사이트.** 예외 2편(SC22 Not All GPUs 4개 클러스터, SC24 GPU-to-GPU 3개 시스템)은 둘 다 benchmark 기반이지 telemetry 기반이 아니다. **operational model이 사이트 A에서 사이트 B로 이전됨을 보인 논문이 census에 0편.** |

> 이 마지막 항목이 **이 분야 최대 약점이자, 가장 명백한 P4급 연구 질문**이다.

# HANDOFF — virtualization domain

## 현재 상태

**1차 구축 완료.** 410건 검토, 362건 보존, topic 9 + synthesis 7 + census 3 작성 완료.
데이터는 `data/PAPER_CATALOG.csv`(410행), `data/PAPER_RELATIONS.csv`(330행),
`data/MERGED_CORPUS.yaml`에 있다.

## 작업 방식 (재개 시 그대로 따를 것)

1. 원 record는 `batches/*.yaml`. 각 파일은 `papers:` 리스트 + batch report 키를 갖는다.
2. record 스키마는 `evidence/RECORD_SCHEMA.md`, 분류 기준은 `evidence/CLASSIFICATION_BRIEF.md`.
3. record를 수정하면 `data/MERGED_CORPUS.yaml`과 두 CSV를 재생성해야 한다
   (batch 파일들을 merge하고 rescue 파일을 id 기준으로 덮어쓰는 순서).
4. **ID는 절대 재사용·변경하지 않는다.**

## 재개할 때 가장 먼저 할 일

`RESEARCH_STATUS.md` §5의 우선순위 목록을 그대로 따르면 된다. 요약:

1. **SC 2024 / SC 2025 전수 census** — 현재 최대 공백. SC24는 robots.txt 전면 차단,
   SC25는 총수(137)만 확보. 두 해 CORE=0은 신뢰 불가.
2. **초록 수준 CORE 25건 심화** — 목록은 `RESEARCH_STATUS.md` §3.1.
   `VIRT-SOSP25-01`을 최우선(mechanism 필드 전부 UNKNOWN, T3·T4 연결점).
3. **SoCC 2024 publication_type 22건 확정.**
4. **TITLE_ONLY 63건 재시도.**
5. **CCGrid24 중복 DOI 정정** (`VIRT-CCGRID24-03` / `-06`).
6. **batch 1~4 venue_populations backfill** (EuroSys25, SOSP25, ASPLOS25, Middleware25, CCGrid25).

## 접근 경로에 대해 알아낸 것 (다음 작업자에게 가장 유용한 정보)

이번 작업의 최대 병목은 문헌 접근이었다. 실제로 통한 경로와 막힌 경로:

**통한다:**
- **USENIX(ATC/OSDI)는 완전 open-access.** presentation 페이지 slug 패턴
  `usenix.org/conference/<venue>/presentation/<lastname>`, PDF는
  `usenix.org/system/files/<venue>-<lastname>.pdf`. proceedings contents PDF
  (`atc25_contents.pdf` 등)가 전수 열거에 가장 확실하다.
- **저자·연구실 개인 홈페이지 PDF.** ACM DL이 막혔을 때 가장 성공률이 높다.
- **GitHub artifact repo의 README.** `api.github.com/search/repositories`는 robots 차단이
  없다(github.com UI는 차단됨).
- **Crossref로 DOI 확보 → Semantic Scholar Graph API의 paper-by-DOI 엔드포인트.**
  검색 엔드포인트는 429가 잦지만 DOI 직접 조회는 통한다. 요청 간격을 두고 순차 호출할 것.
- **OpenAlex의 `abstract_inverted_index`** 로 초록 복원 가능.

**막힌다:**
- ACM DL — 거의 모든 경로에서 403. Gold OA/CC-BY 논문조차 봇 차단된다(BASK, RDMA migration).
- IEEE Xplore — paywall 또는 JS 게이트로 빈 응답.
- dblp — venue에 따라 robots 차단(OSDI·SC·ASPLOS·HPCA·MICRO가 자주 막히고
  EuroSys·SOSP·HPDC·CCGrid는 통했다).
- Google Scholar / Bing / DuckDuckGo — robots 차단.
- SC 공식 사이트 — robots.txt가 `/program/`·`/proceedings/` 전체 차단.

**운영상 주의:** WebSearch는 세션당 약 200회 예산이 있고, 소진되면 WebFetch만 남는다.
대규모 census를 돌릴 때는 keyword 검색보다 **공식 proceedings contents PDF 전수 열거**를
먼저 하는 편이 예산 효율이 훨씬 좋다.

## 이번 작업에서 조심해야 했던 함정 (반복 주의)

1. **접근 실패를 연구 동향으로 오독하지 말 것.** 1차 통과 직후 OSDI 2026 CORE=2,
   EuroSys 2024 CORE=0이었는데 둘 다 fetch 실패 artifact였다. rescue pass 후 각각 10, 3이 되었다.
   **연도별·venue별 수치가 이상하면 분류가 아니라 접근을 먼저 의심하라.**
2. **연도 오배정.** ASPLOS 공식 프로그램 페이지에 전년도 재발표 논문이 섞여 있다.
   DOI proceedings prefix로 교차 검증할 것 (ASPLOS26=3760250/3779212, ASPLOS25=3676642).
3. **제목으로 분류하지 말 것.** MICRO24 "Elastic Translations"는 pure virtual-memory 논문들과
   제목·session이 구분되지 않지만 실제로는 KVM nested page table을 다룬다.
4. **batch 간 record 생성 정책을 통일할 것.** 배제 논문에도 DROP record를 남길지 여부가
   batch마다 달라 venue별 비율 비교가 불가능해졌다. 다음 실행에서는 "배제도 전부 record"로 통일 권장.

## 공유 root 파일

이번 작업은 `domains/virtualization/` 안에서만 수행했고, `GLOBAL_CONTEXT.md`,
`MASTER_INDEX.md`, `README.md`, `catalog/papers.yaml` 등 공유 파일은 **수정하지 않았다.**
타 세션의 uncommitted 변경도 건드리지 않았다. 이 domain을 repository 전역 인덱스에 편입하려면
그 작업은 별도로 수행해야 한다.

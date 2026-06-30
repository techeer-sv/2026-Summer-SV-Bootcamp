# 부록 D. PR 템플릿 모음

> [02-03 컨벤션 합의 템플릿](../02-팀과-같이-쓰기/03-컨벤션-합의-템플릿.md) 에서 다룬 기본 PR 템플릿을, **목적별로 5종** 로 확장한 모음이에요.
> 그대로 복붙해서 `.github/PULL_REQUEST_TEMPLATE/` 폴더에 넣으시면 됩니다.
> 단일 템플릿만 쓴다면 `.github/PULL_REQUEST_TEMPLATE.md` 한 파일에 기본 5섹션만 넣어도 OK.

📎 GitHub 공식 — [Creating a PR template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)

---

## 0. 어디에 두나요

GitHub 이 인식하는 PR 템플릿 위치 (어느 곳이든 OK, 보통 `.github/` 권장):

| 위치 | 용도 |
| --- | --- |
| `pull_request_template.md` | 레포 루트 (가장 단순) |
| `docs/pull_request_template.md` | 문서 폴더에 모으고 싶을 때 |
| **`.github/pull_request_template.md`** ⭐ | 단일 템플릿 — 부트캠프 권장 |
| **`.github/PULL_REQUEST_TEMPLATE/`** ⭐ | 다중 템플릿 (이번 챕터에서 다룸) |

### 다중 템플릿 호출법 — URL 쿼리 파라미터

여러 템플릿을 두면 GitHub 이 **하나를 자동 선택하지 않습니다.** 대신 PR 생성 URL 에 `?template=파일명.md` 를 붙여서 원하는 템플릿을 호출해요.

```
https://github.com/<owner>/<repo>/compare/main...<branch>?template=bugfix.md
```

CONTRIBUTING.md 에 자주 쓰는 템플릿의 URL 을 적어두면 팀원이 한 번에 클릭할 수 있습니다.

> 💡 단일 템플릿(`.github/pull_request_template.md`) 은 PR 만들 때 자동으로 본문에 채워져요. 다중 템플릿은 URL 쿼리가 필요하기 때문에 부트캠프 4주라면 **기본 1개 + 자주 쓰는 1~2개** 정도가 적절.

---

## 1. 기본 — `feature.md` (또는 단일 템플릿)

가장 자주 쓰는 일반 기능/문서/리팩터 PR 용. 이 한 장이면 부트캠프 4주의 80% 가 커버됩니다.

````markdown
## 요약

<!-- 이 PR이 무엇을 하나요. 한두 줄로 -->

## 변경사항

- 항목 1
- 항목 2
- 항목 3

## 테스트

- [ ] 무엇을 / 어떻게 확인했나요
- [ ] 추가 케이스 (선택)

## 스크린샷 (UI 변경 시)

<!-- 이미지를 드래그&드롭하면 자동 업로드 -->

## 관련 이슈

Closes #
````

---

## 2. 버그픽스 — `bugfix.md`

버그를 고쳤다면, **재현·기대·실제·근본 원인** 4가지를 적어두면 리뷰가 빨라요.

````markdown
## 요약

<!-- 어떤 버그를 고쳤나요 -->

## 재현 절차 (수정 전)

1. ...
2. ...
3. ...

## 기대 동작

<!-- 정상적으로는 어떻게 되어야 하나 -->

## 실제 동작 (버그)

<!-- 무엇이 잘못됐나 -->

## 근본 원인

<!-- 왜 이런 일이 일어났나. 한 줄~한 문단 -->

## 변경사항

- 무엇을 어떻게 고쳤나

## 테스트

- [ ] 위 재현 절차로 버그가 더 이상 발생 안 함
- [ ] 회귀 가능성 있는 인접 기능 확인
- [ ] (가능하면) 회귀 테스트 추가

## 관련 이슈

Fixes #
````

---

## 3. 핫픽스 — `hotfix.md`

이미 배포된 운영 환경의 긴급 버그. **영향 범위**와 **롤백 계획**이 핵심.

````markdown
## 🚨 핫픽스 요약

<!-- 어떤 운영 이슈를 막기 위한 PR인가 -->

## 영향 범위

- **영향받는 사용자/기능:** 
- **영향 시간:** 발생부터 발견까지 (대략)
- **데이터 손실 여부:** 있음 / 없음 / 조사 중

## 변경사항 (최소한으로)

- <!-- 가능한 한 변경 범위를 좁게. 곁다리 정리는 후속 PR -->

## 테스트

- [ ] 로컬에서 재현이 사라지는 것 확인
- [ ] 스테이징/프리뷰 환경에서 재현이 사라지는 것 확인
- [ ] 인접 기능 회귀 점검

## 롤백 계획

<!-- 머지 후 문제 생기면 어떻게 되돌리나 -->
- 이 PR의 commit `<SHA>` 를 revert
- 또는 직전 태그 `vX.Y.Z` 로 재배포

## 후속 작업 (별도 이슈)

- [ ] 근본 원인 정리 / 재발 방지 (#)
- [ ] (필요 시) 사후 회고 노트

## 관련 이슈 / 알림

Fixes #
- Slack 알림: `#incidents` 채널 메시지 링크
````

> 💡 **부트캠프에서는 핫픽스 시나리오가 드물지만**, 운영 서비스를 다루는 팀이라면 한 번쯤 마주칠 수 있어요. 위 템플릿이 그 순간을 위한 안전망.

---

## 4. 리팩터링 — `refactor.md`

동작이 그대로여야 하는 PR. **"바뀐 게 없다는 증거"** 가 핵심.

````markdown
## 요약

<!-- 어디를 어떻게 정리했나요 -->

## 동기

<!-- 왜 이 리팩터가 필요했나. 어떤 문제를 풀고 싶었나 -->

## 변경사항

- 무엇을 어떻게 정리
- (선택) 새로운 구조의 다이어그램

## 동작 불변 증명 ⭐

- [ ] 외부 API/시그니처가 동일
- [ ] 기존 테스트가 그대로 통과
- [ ] (가능하면) before/after 동일 입력 → 동일 출력 비교
- [ ] (가능하면) DB 쿼리·HTTP 요청 수 동일

## 위험 / 트레이드오프

<!-- 새 구조의 장점·단점. 후속 작업이 필요한 부분 -->

## 관련 이슈

Refs #
````

---

## 5. 문서 전용 — `docs.md`

README, 주석, 가이드 문서만 변경하는 PR. 가벼운 양식.

````markdown
## 요약

<!-- 어떤 문서를 왜 바꿨나요 -->

## 변경사항

- 추가/수정/삭제 항목

## 미리보기

- [ ] GitHub 의 Markdown preview 로 렌더링 확인
- [ ] (외부 링크 추가했다면) 200 OK 확인

## 관련 이슈

Refs #
````

---

## 6. CONTRIBUTING.md 에 같이 적어둘 안내

다중 템플릿을 만들었다면 팀원이 어떤 걸 언제 쓰는지 알 수 있도록 한 줄로 안내:

````markdown
## PR 종류별 템플릿 빠른 링크

PR 만들 때 URL 끝에 `?template=...` 을 붙이거나, 아래 링크 사용.

| 상황 | 링크 |
| --- | --- |
| 일반 기능/문서 | `?template=feature.md` |
| 버그 수정 | `?template=bugfix.md` |
| 운영 긴급 | `?template=hotfix.md` |
| 리팩터링 | `?template=refactor.md` |
| 문서만 | `?template=docs.md` |

예: `https://github.com/<owner>/<repo>/compare/main...<branch>?template=bugfix.md`
````

---

## 7. PR URL 쿼리 — 더 많은 자동 채우기

PR 본문 외에도 URL 로 미리 채울 수 있는 항목들. 매크로 만들어두면 편합니다.

| 쿼리 | 채우는 것 | 예 |
| --- | --- | --- |
| `title=` | PR 제목 | `?title=feat: 로그인 폼 추가` |
| `body=` | PR 본문 | `?body=...` (URL 인코딩 필요) |
| `labels=` | 라벨 (쉼표 구분) | `?labels=feat,frontend` |
| `assignees=` | 담당자 (쉼표 구분) | `?assignees=leo,alice` |
| `reviewers=` | 리뷰어 (쉼표 구분) | `?reviewers=bob` |
| `template=` | 본문 템플릿 파일명 | `?template=bugfix.md` |
| `milestone=` | 마일스톤 번호 | `?milestone=1` |
| `projects=` | 프로젝트 | `?projects=org/<num>` |

여러 쿼리는 `&` 로 연결:

```
?template=bugfix.md&labels=fix,urgent&assignees=leo
```

> 💡 부트캠프에서 가장 자주 쓰는 조합은 `template` + `labels` 정도. 너무 많이 자동화하면 PR 생성 화면이 가려져 헷갈려요.

---

## 8. 좋은 PR 본문 vs 나쁜 PR 본문

### 좋은 예 ✅

````markdown
## 요약
로그인 폼의 빈 값 제출 시 alert이 뜨는 버그를 수정했습니다.

## 재현 절차
1. /login 접속
2. 이메일·비밀번호 비운 채 제출
3. → alert("이메일을 입력하세요") 가 두 번 뜸

## 근본 원인
폼 제출 핸들러가 React 리렌더링에 의해 두 번 호출되고 있었음.

## 변경사항
- onSubmit 에 e.preventDefault() 추가
- submitting 상태로 중복 호출 차단

## 테스트
- [x] 위 재현 절차로 alert 한 번만 뜸
- [x] 정상 입력 시 라우팅 동작 확인

Fixes #15
````

**좋은 이유:**
- 재현 절차가 명확
- 근본 원인을 한 줄
- 변경사항 ↔ 원인이 1:1로 매칭
- 테스트 체크박스 = 리뷰어가 따라할 수 있음
- `Fixes #15` 가 끝에

### 나쁜 예 ❌

````markdown
로그인 고쳤어요
````

**나쁜 이유:**
- 무엇을 / 왜 / 어떻게 모름
- 재현 절차 없음 → 리뷰어가 동작을 못 확인
- Issue 연결 안 됨

---

## 🩺 막힐 때

<details>
<summary><b>다중 템플릿을 만들었는데 PR 만들 때 자동 선택이 안 돼요</b></summary>

다중 템플릿은 <b>자동 선택이 안 되는 게 정상</b> 입니다. URL 끝에 <code>?template=파일명.md</code> 를 붙여야 호출돼요. 자세한 건 위 <b>0. 어디에 두나요</b> 박스.

</details>

<details>
<summary><b>본문에 한국어를 쓰면 깨져요</b></summary>

GitHub 본문은 UTF-8 이라 한국어 그대로 OK. 깨진다면 파일 저장 인코딩 확인 (VSCode 우하단 → UTF-8).

</details>

<details>
<summary><b>매번 본문을 다 채우기 귀찮아요</b></summary>

체크박스만이라도 정직하게 채우세요. 본문이 비어 있는 PR 보다는 "테스트: 확인 못 함" 이라도 솔직히 적힌 PR 이 훨씬 낫습니다 (리뷰어가 무엇을 확인해야 할지 알 수 있어요).

</details>

<details>
<summary><b>레포에 단일 템플릿(<code>pull_request_template.md</code>)과 다중 폴더가 같이 있어요</b></summary>

GitHub 동작이 헷갈릴 수 있어요. <b>둘 중 하나로 정리</b>하시는 게 안전. 부트캠프 4주에는 단일 1개 + 필요 시 다중 폴더로 옮기는 식이 깔끔합니다.

</details>

---

### 💡 한 줄 요약

단일 템플릿이면 `.github/pull_request_template.md` 한 파일. 다중이면 `.github/PULL_REQUEST_TEMPLATE/` 폴더 + URL 의 `?template=...` 으로 호출. 본문보다 **체크박스를 정직히 채우는 습관** 이 더 중요.

### 📚 더 깊이 보기

- GitHub 공식 — [Creating a PR template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- GitHub 공식 — [Using query parameters to create a PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request)
- [02-03 컨벤션 합의 템플릿](../02-팀과-같이-쓰기/03-컨벤션-합의-템플릿.md) — 본문 5섹션 원본
- [02-04 PR 리뷰 에티켓](../02-팀과-같이-쓰기/04-pr-리뷰-에티켓.md)
- 부록 — [B 커밋 컨벤션](./B-커밋-컨벤션-한-장.md), [E Issue 템플릿 모음](./E-Issue-템플릿-모음.md)

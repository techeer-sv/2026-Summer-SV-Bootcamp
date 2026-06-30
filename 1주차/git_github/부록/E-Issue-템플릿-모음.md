# 부록 E. Issue 템플릿 모음

> [01-03 Issue 만들기](../01-한사이클-혼자-돌려보기/03-issue-만들기.md) 의 3섹션 본문 템플릿을, **목적별 4종 + 신규 Issue Forms (YAML) 1예시** 로 확장했어요.
> `.github/ISSUE_TEMPLATE/` 폴더에 넣으면 GitHub 의 **New issue** 버튼을 눌렀을 때 종류 선택 화면이 나옵니다.

📎 GitHub 공식 — [About issue and PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)

---

## 0. 두 가지 방식 — Markdown vs Issue Forms (YAML)

GitHub은 Issue 템플릿을 두 가지 방식으로 지원해요.

| 방식 | 파일 확장자 | 특징 | 추천 |
| --- | --- | --- | --- |
| **클래식 Markdown** | `.md` | 일반 마크다운. 단순, 어떤 도구로도 편집 가능 | 부트캠프 4주에 충분 ⭐ |
| **Issue Forms** | `.yml` | 입력칸(input/textarea/dropdown/checkboxes) 으로 구조화 | 외부 기여자가 많을 때 / 정확한 입력 강제 필요 |

부트캠프에서는 **클래식 Markdown 4종 + (선택) Issue Forms 1예시** 정도면 충분합니다.

### 폴더 구조

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.md          ← 클래식
    ├── feature_request.md     ← 클래식
    ├── question.md            ← 클래식
    ├── discussion.md          ← 클래식
    ├── bug_report.yml         ← (선택) Issue Forms 예시
    └── config.yml             ← (선택) 종류 선택 화면 설정
```

> 💡 `.md` 와 `.yml` 이 같은 이름이면 GitHub 이 양쪽 다 보여줘서 헷갈려요. **하나로 통일**하세요 (`bug_report.md` 만 또는 `bug_report.yml` 만).

---

## 1. 버그 리포트 — `bug_report.md`

가장 자주 쓸 템플릿. frontmatter 의 `name`·`about`·`title`·`labels`·`assignees` 가 자동으로 채워져요.

````markdown
---
name: 🐛 Bug Report
about: 동작이 기대와 다른 부분을 신고합니다
title: "fix: "
labels: [fix]
assignees: ''
---

## 무엇이 잘못됐나요

<!-- 한 줄로 명확히 -->

## 재현 절차

1. 
2. 
3. 

## 기대 동작

<!-- 정상적으로는 어떻게 되어야 하나 -->

## 실제 동작

<!-- 무엇이 잘못 나오나. 에러 메시지를 텍스트로 -->

```
(에러 메시지 / 콘솔 로그가 있다면 여기에)
```

## 환경

- OS: (macOS 14.5 / Windows 11 등)
- 브라우저: (Chrome 130 등)
- 앱 버전 / 커밋 SHA:

## 스크린샷 (선택)

<!-- 드래그&드롭으로 첨부 -->

## 참고

- 관련 이슈/PR: #
- 처음 발생 시점:
````

> 💡 `title: "fix: "` 처럼 prefix를 미리 박아두면 컨벤션 잊는 사고가 줄어요.

---

## 2. 기능 요청 — `feature_request.md`

````markdown
---
name: ✨ Feature Request
about: 새 기능을 제안합니다
title: "feat: "
labels: [feat]
assignees: ''
---

## 어떤 기능인가요

<!-- 한 줄 설명 -->

## 왜 필요한가요 (사용자 가치)

<!-- 어떤 문제를 풀어주나. 누구한테 도움 되나 -->

## 제안하는 동작

- [ ] 사용자가 X 를 누르면
- [ ] Y 가 표시되고
- [ ] Z 로 이동한다

## 대안 / 이미 고려한 방법

<!-- "이렇게도 가능하지만 이 안이 더 좋다" -->

## 참고

- 비슷한 사례 (다른 서비스): 
- 관련 이슈: #
````

---

## 3. 질문 — `question.md`

````markdown
---
name: ❓ Question
about: 코드/기능/협업 관련 질문
title: "question: "
labels: [question]
assignees: ''
---

## 무엇이 궁금한가요

<!-- 한 줄로 -->

## 이미 시도한 것

<!-- 어디까지 찾아봤나 / 어떤 키워드로 검색했나 -->

## 참고 자료

<!-- 관련 링크 -->
````

> 💡 부트캠프에서는 질문도 이슈로 남겨두면 같은 의문이 생긴 다른 팀원이 검색할 수 있어요. Slack 보다 Issue 가 검색성·기록성 좋음.

---

## 4. 논의 / 의사결정 — `discussion.md`

작은 의사결정·기술 선택·아키텍처 토론을 남길 때.

````markdown
---
name: 💬 Discussion
about: 팀 의사결정·기술 선택·토론
title: "discussion: "
labels: [discussion]
assignees: ''
---

## 무엇을 결정해야 하나요

<!-- 한 줄로 -->

## 배경 / 맥락

<!-- 왜 이 결정이 필요한가 -->

## 옵션

### 옵션 A. ___
- 장점:
- 단점:

### 옵션 B. ___
- 장점:
- 단점:

### 옵션 C. (선택)

## 결정 / 다음 단계

<!-- 토론 후 채워주세요 -->

- [ ] 결정자:
- [ ] 결정 일자:
- [ ] 후속 작업 (Issue/PR 링크):
````

> 💡 부트캠프 4주 동안 큰 의사결정 (DB 선택, 인증 방식, 배포 호스팅 등) 마다 이 템플릿으로 Issue 만들면, 회고할 때 "왜 그렇게 정했지?" 가 살아 있어요.

---

## 5. (선택) Issue Forms 예시 — `bug_report.yml`

입력칸을 강제하고 싶을 때. 외부 기여자가 많은 오픈소스에서 표준이고, 부트캠프에서는 옵션입니다.

```yaml
name: 🐛 Bug Report
description: 동작이 기대와 다른 부분을 신고합니다
title: "fix: "
labels: [fix]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## 버그를 신고해 주셔서 감사합니다 🙏
        아래 항목을 가능한 한 정확히 채워주세요. 멘토·팀원이 빠르게 도와드릴 수 있어요.

  - type: textarea
    id: what-happened
    attributes:
      label: 무엇이 잘못됐나요
      description: 한 줄로 명확히
      placeholder: 예) 로그인 폼 제출 시 alert 가 두 번 뜸
    validations:
      required: true

  - type: textarea
    id: reproduce
    attributes:
      label: 재현 절차
      description: 어떻게 하면 이 버그가 다시 나오나요
      placeholder: |
        1. /login 접속
        2. 이메일·비밀번호 비운 채 제출
        3. alert이 두 번 뜸
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: 기대 동작
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: 실제 동작 (에러 메시지가 있다면 텍스트로)
    validations:
      required: true

  - type: dropdown
    id: severity
    attributes:
      label: 심각도
      options:
        - 낮음 (불편)
        - 중간 (기능 일부 불가)
        - 높음 (기능 전체 불가)
        - 운영 긴급 (서비스 중단)
    validations:
      required: true

  - type: input
    id: env-os
    attributes:
      label: OS
      placeholder: 예) macOS 14.5, Windows 11
    validations:
      required: true

  - type: input
    id: env-browser
    attributes:
      label: 브라우저 (또는 환경)
      placeholder: 예) Chrome 130, Safari 17
    validations:
      required: false

  - type: checkboxes
    id: confirmations
    attributes:
      label: 확인
      options:
        - label: 기존 Issue 에서 같은 버그가 없는지 검색했다
          required: true
        - label: 최신 main 브랜치에서도 재현된다
          required: false
```

### 주요 필드 타입

| 타입 | 무엇 |
| --- | --- |
| `markdown` | 안내문 표시 (입력 X) |
| `input` | 한 줄 입력 |
| `textarea` | 여러 줄 입력 |
| `dropdown` | 선택 목록 |
| `checkboxes` | 체크박스 (필수 동의 등) |

`validations.required: true` 로 필수 입력을 강제할 수 있어요.

---

## 6. 종류 선택 화면 설정 — `config.yml`

`.github/ISSUE_TEMPLATE/config.yml` 을 추가하면 New issue 화면을 커스텀할 수 있어요.

```yaml
blank_issues_enabled: false       # "빈 Issue 만들기" 옵션 끄기 (템플릿 사용 강제)

contact_links:
  - name: 💬 팀 Slack 채널
    url: https://your-team.slack.com/archives/CXXXXXXX
    about: 가벼운 질문/잡담은 Slack 으로

  - name: 📚 핸즈온 실습 자료
    url: https://github.com/<owner>/<repo>/tree/main/practice
    about: Git/GitHub 사용법 가이드 (이 자료)
```

이렇게 두면 New issue 화면에 위 두 링크가 함께 보여서, **이슈 아닌 것은 다른 곳으로 라우팅**할 수 있어요.

---

## 7. 좋은 Issue vs 나쁜 Issue

### 좋은 예 ✅

````markdown
## 무엇이 잘못됐나요
로그인 폼 제출 시 alert이 두 번 뜨고, 두 번째 alert 후 라우팅이 안 됩니다.

## 재현 절차
1. /login 접속
2. 이메일·비밀번호 빈 값으로 제출
3. alert("이메일을 입력하세요") 가 두 번 뜸
4. 두 번째 OK 누르면 라우팅 멈춤

## 기대 동작
alert 1회 표시 후 폼 유지

## 실제 동작
alert 2회 + 라우팅 차단

## 환경
- macOS 14.5, Chrome 130
- 커밋: a1b2c3d
````

### 나쁜 예 ❌

````markdown
로그인 안 됨
````

**차이:** 좋은 예는 멘토·팀원이 자기 컴퓨터에서 그대로 재현할 수 있고, 나쁜 예는 답변 전에 6번 더 질문을 해야 합니다.

---

## 8. 라벨 자동 부여 — frontmatter `labels`

`.md` 템플릿의 frontmatter `labels` 또는 `.yml` 의 `labels` 에 적은 값이 Issue 생성 시 **자동으로 부착**됩니다. 단, 그 라벨이 **레포에 이미 존재해야** 동작해요.

부트캠프 권장 기본 라벨 4종 (02-03 컨벤션 합의의 권장값):

| 라벨 | 색 | 의미 |
| --- | --- | --- |
| `feat` | `#a2eeef` | 새 기능 |
| `fix` | `#d73a4a` | 버그 |
| `docs` | `#0075ca` | 문서 |
| `discussion` | `#d4c5f9` | 논의 필요 |

레포 **Issues 탭 → Labels → New label** 에서 추가.

---

## 🩺 막힐 때

<details>
<summary><b>New issue 버튼을 눌렀는데 종류 선택 화면이 안 나와요</b></summary>

<code>.github/ISSUE_TEMPLATE/</code> 안에 템플릿 파일이 1개 이하면 종류 선택 없이 바로 본문 화면으로 갑니다. 2개 이상부터 선택 화면이 떠요.

</details>

<details>
<summary><b>frontmatter 의 <code>labels</code> 가 자동으로 안 붙어요</b></summary>

해당 라벨이 레포에 미리 존재해야 동작합니다. <b>Issues 탭 → Labels</b> 에서 라벨을 먼저 만드세요.

</details>

<details>
<summary><b><code>config.yml</code> 에 <code>blank_issues_enabled: false</code> 를 했더니 옵션이 안 보여요</b></summary>

정상입니다. 빈 Issue 만들기 옵션을 끈 거예요. 멘토/Admin 이 필요할 때 임시로 <code>true</code> 로 바꿀 수 있어요.

</details>

<details>
<summary><b>Markdown 템플릿과 YAML 폼이 동시에 있으면?</b></summary>

GitHub 이 둘 다 보여줘서 종류 선택 화면이 복잡해져요. <b>같은 목적의 템플릿은 하나로 통일</b>하세요. 부트캠프 4주에는 Markdown 4종이면 충분.

</details>

---

### 💡 한 줄 요약

`.github/ISSUE_TEMPLATE/` 폴더에 `.md` 파일 1~4개 + (선택) `config.yml` 한 장. frontmatter 의 `labels`·`title` prefix 가 자동 채움. 외부 기여자가 많아지면 그때 Issue Forms YAML.

### 📚 더 깊이 보기

- GitHub 공식 — [About issue and PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- GitHub 공식 — [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- GitHub 공식 — [Configuring the template chooser](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#configuring-the-template-chooser)
- [01-03 Issue 만들기](../01-한사이클-혼자-돌려보기/03-issue-만들기.md) — 본문 3섹션 원본
- [02-03 컨벤션 합의 템플릿](../02-팀과-같이-쓰기/03-컨벤션-합의-템플릿.md)
- 부록 — [D PR 템플릿 모음](./D-PR-템플릿-모음.md), [F README 작성법](./F-README-작성법.md)

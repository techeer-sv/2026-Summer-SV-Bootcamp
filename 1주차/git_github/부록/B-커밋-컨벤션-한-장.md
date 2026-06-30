# 부록 B. 커밋 컨벤션 한 장

[Conventional Commits 공식 (한국어)](https://www.conventionalcommits.org/ko/v1.0.0/) 기반. 부트캠프 4주에 딱 필요한 만큼.

---

## 형식

```
<type>: <한 줄 요약>

[필요하면 본문 — 무엇을 / 왜]

[꼬리: Closes #N, Refs #M 등]
```

- 첫 줄 요약은 **50자 이내**, 마침표 ❌
- 요약 ↔ 본문 사이에 **빈 줄 1개**
- 본문은 한 줄 72자 이내가 읽기 좋음 (선택)
- 한국어 / 영어 모두 OK — 팀 안에서 통일

---

## Type 7종

| Type | 의미 | 예시 |
| --- | --- | --- |
| **feat** | 새 기능 추가 | `feat: 로그인 폼 추가` |
| **fix** | 버그 수정 | `fix: 비밀번호 빈 값 제출 시 alert` |
| **docs** | 문서만 (README, 주석) | `docs: README에 환경 변수 설정 추가` |
| **style** | 동작 변화 없는 포맷 (공백, 세미콜론, 정렬) | `style: ESLint --fix 자동 정렬` |
| **refactor** | 동작 그대로, 구조 개선 | `refactor: AuthService를 클래스로 분리` |
| **test** | 테스트 추가/수정 | `test: 로그인 폼 유효성 케이스 추가` |
| **chore** | 빌드·설정·의존성 (package.json, .github/) | `chore: ESLint 규칙에 no-console 추가` |

> 💡 더 세분화하고 싶다면 `perf` (성능), `ci` (CI 설정), `build` (빌드 시스템) 도 있어요. 부트캠프에선 위 7개로 충분.

---

## 좋은 예 vs 나쁜 예

| ✅ 좋은 예 | ❌ 나쁜 예 |
| --- | --- |
| `feat: 로그인 폼 추가` | `update` |
| `fix: 비밀번호 빈 값 제출 시 alert` | `버그 수정` |
| `docs: README에 환경 변수 설정 추가` | `readme` |
| `refactor: AuthService를 클래스로 분리` | `리팩토링` |
| `chore: ESLint 규칙에 no-console 추가` | `ㅋㅋ` |
| `test: 로그인 폼 유효성 케이스 추가` | `테스트` |

### 좋은 예의 공통점

- **type** 으로 한눈에 성격 파악
- **무엇을** 했는지 명사로
- 50자 이내, 마침표 없음

### 나쁜 예의 공통점

- type 없음
- "수정", "변경" 같이 동작이 추상적
- 코드 리뷰어가 메시지만 보고는 무슨 일이 일어났는지 모름

---

## 본문이 필요할 때

복잡한 변경은 짧은 본문으로 **무엇을 / 왜** 를 설명.

```
feat: 로그인 폼 추가

- 이메일·비밀번호 필드
- 빈 값 제출 시 인라인 에러
- 제출 후 /dashboard 로 라우팅

Closes #3
```

본문 작성하려면 `git commit` 만 입력 (`-m` 없이). 에디터가 열려요.

---

## 꼬리 — 이슈와 연결

본문 마지막 빈 줄 뒤에 키워드 + 이슈 번호.

| 키워드 | 효과 |
| --- | --- |
| `Closes #1` / `Close #1` | PR 머지 시 Issue 자동 닫힘 |
| `Fixes #1` / `Fix #1` | 동일 |
| `Resolves #1` / `Resolve #1` | 동일 |
| `Refs #1` | 참조만 (자동 닫기는 안 함) |

> 💡 자동 닫기는 **PR 본문** 에 적어두는 게 더 확실합니다. 커밋 메시지의 키워드는 squash merge 시점에 누락될 수 있어요.

---

## 한 커밋의 크기

원칙: **한 커밋 = 한 논리적 변경**.

| ✅ | ❌ |
| --- | --- |
| `feat: 로그인 폼 마크업` + `feat: 로그인 폼 검증 로직` + `style: 로그인 폼 정렬` (3개 커밋) | `feat: 로그인` (마크업 + 검증 + 스타일 + 라우팅 한 번에) |

**작은 커밋의 장점:**
- 리뷰어가 한 번에 봐야 할 변경이 적음
- 문제 생기면 어느 커밋이 원인인지 빠르게 식별
- 일부만 revert 가능

**현실 팁:** 가지 안에서는 작게 자주 커밋, main에 머지할 땐 **Squash로 한 줄로 합치기**. 이 자료 권장 동선.

---

## 커밋 메시지를 잘 쓰는 습관

1. **VSCode를 에디터로** — 본문이 필요할 때 편하게:
   ```bash
   $ git config --global core.editor "code --wait"
   ```
2. **컨벤션을 IDE 플러그인이 검사하게** — VSCode "Conventional Commits" 확장
3. **PR 제목도 같은 형식** — Squash 머지하면 PR 제목이 main의 한 줄 커밋이 됨

---

## (참고) BREAKING CHANGE — 부트캠프에선 거의 안 씀

대규모 변경으로 호환성이 깨질 때.

```
feat!: 인증 토큰을 JWT에서 OAuth로 전환

BREAKING CHANGE: 기존 /auth/token 엔드포인트 제거
```

부트캠프 4주에는 거의 안 쓰입니다. 오픈소스에 기여할 때 만나게 될 거예요.

---

### 💡 한 줄 요약

`<type>: <요약>` 형식, type 7종, 50자 이내, 마침표 없음. 한 커밋 = 한 논리적 변경.

### 📚 더 깊이 보기

- [Conventional Commits 1.0.0 (한국어)](https://www.conventionalcommits.org/ko/v1.0.0/)
- [Karma Commit Message Guide](http://karma-runner.github.io/6.4/dev/git-commit-msg.html) (영문)
- [How to Write a Git Commit Message — Chris Beams](https://cbea.ms/git-commit/) (영문, 클래식)
- VSCode 확장 — [Conventional Commits](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits)

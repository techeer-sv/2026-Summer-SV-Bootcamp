# 03-01. FAQ — 자주 만나는 5가지

> 📎 세션 슬라이드 23~26 (RISK 1~3)
>
> 부트캠프 4주에 가장 자주 마주칠 5가지를 정리했어요. 각 항목은 **증상 → 원인 → 처방 → 예방** 4단으로 구성돼 있습니다.

---

## 🚨 1. `! [rejected] ... fetch first`

### 증상

`git push` 했더니 거부.

```
 ! [rejected]        feat/login -> feat/login (fetch first)
error: failed to push some refs to 'https://github.com/...'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
```

### 원인

원격 (`origin`) 의 같은 브랜치에 **내 로컬보다 새로운 커밋**이 있어요. 보통:

- 다른 팀원이 같은 브랜치에 push했거나
- 내가 GitHub 웹에서 직접 파일을 수정했거나
- 직전에 PR 페이지에서 GitHub 자동 커밋 (예: Suggestion 적용) 이 추가됐거나

### 처방

```bash
$ git pull --rebase
# 원격의 변경을 가져오면서 내 커밋들을 그 위로 다시 쌓기

$ git push
# 다시 시도
```

**또는** `--rebase` 없이 일반 pull:

```bash
$ git pull
$ git push
```

차이:
- `git pull` (= fetch + merge) — main에 머지 커밋 한 줄이 추가됨
- `git pull --rebase` — 머지 커밋 없이 일직선 히스토리

부트캠프에선 어느 쪽이든 OK. 더 깔끔한 건 `--rebase`.

> ⚠️ **충돌이 같이 발생하면?** [02-05 Conflict 해결](../02-팀과-같이-쓰기/05-conflict-해결.md) 으로.

### 예방

- 작업 시작 전 항상 `git pull`
- 같은 브랜치에 두 명이 동시에 작업하지 않기
- GitHub 웹에서 직접 파일 수정은 가벼운 README 정도만

---

## 🚨 2. `.env` 를 실수로 push 했어요

### 증상

가장 무서운 사고. API 키, DB 비밀번호 같은 비밀이 들어 있는 `.env` 파일을 commit·push 한 상황. push된 직후 봇이 **1분 안에 스캔**해서 키를 빼갑니다.

### 처방 — 순서가 중요해요

#### 🥇 1순위. **그 비밀들을 즉시 모두 재발급/리볼브**

| 비밀 종류 | 어디서 재발급 |
| --- | --- |
| **OpenAI / Anthropic 같은 LLM API 키** | 각 서비스 콘솔에서 즉시 revoke + 새 키 발급 |
| **GitHub PAT** | [github.com/settings/tokens](https://github.com/settings/tokens) |
| **AWS Access Key** | IAM 콘솔에서 Deactivate + 새 키 |
| **DB 비밀번호** | DBA 또는 DB 관리 콘솔 |
| **OAuth Client Secret** | 발급해준 서비스 (Google, Kakao 등) |

**이 단계가 무조건 1순위입니다.** 히스토리에서 지우는 건 그다음.

#### 🥈 2순위. 히스토리에서 제거

푸시된 파일을 히스토리에서 통째로 삭제. **혼자 작업하는 레포가 아니면 팀원과 동기화 후 진행하세요** (히스토리가 바뀌면 다른 사람의 로컬과 충돌).

```bash
# git-filter-repo 설치 (한 번만)
# macOS:  brew install git-filter-repo
# Windows: pip install git-filter-repo

# 레포 폴더에서
$ git filter-repo --path .env --invert-paths --force
$ git push --force origin main
```

> ⚠️ 이 작업은 **이 자료의 권장 동선에서 벗어난 위험 명령**입니다. 가능하면 **멘토와 함께** 진행하세요. 잘못하면 팀 작업물을 날릴 수 있어요.

#### 🥉 3순위. 예방 조치

```bash
# .gitignore에 .env가 정말 들어 있는지 확인
$ cat .gitignore | grep .env
.env
.env.local
.env.*.local
```

없으면 추가하고 commit·push.

### 예방

- 첫 commit 전부터 `.env` 가 `.gitignore` 에 있는지 무조건 확인 ([01-02](../01-한사이클-혼자-돌려보기/02-gitignore-와-env.md))
- `.env.example` 파일은 추적하되 (어떤 변수가 필요한지 문서화), 실제 값이 들어간 `.env` 는 절대 추적 안 함
- GitHub의 **Secret scanning** (Public 레포는 자동 활성화) 알림을 받으면 즉시 대응

---

## 🚨 3. 잘못된 브랜치에 커밋했어요

### 증상

main에서 작업하다 깜빡, 또는 다른 feature 브랜치에 잘못 커밋한 상황.

```bash
$ git log --oneline
4f2c1ab (HEAD -> main) feat: 로그인 폼 (오늘 작업)
a1b2c3d Initial commit
```

main 에 작업을 해버린 케이스 (보호 룰 켜기 전 상태). 또는 `feat/#1` 브랜치에 있어야 할 작업을 `feat/#2` 에 한 상황.

### 처방 — 안전한 길

#### 케이스 A. **아직 push 안 한** 잘못된 커밋

```bash
# 1. 현재 브랜치의 마지막 커밋을 풀어내기 (변경은 유지)
$ git reset --soft HEAD~1

# 2. 변경사항을 임시 보관
$ git stash

# 3. 올바른 브랜치로 이동 (없으면 만들기)
$ git switch -c feat/#1-login-form    # 또는 git switch <기존-브랜치>

# 4. 변경 다시 꺼내기
$ git stash pop

# 5. add + commit
$ git add .
$ git commit -m "feat: 로그인 폼"
```

#### 케이스 B. **이미 push한** 잘못된 커밋

main 에 직접 push해버린 경우 — 보호 룰이 안 켜져 있던 상태일 거예요. 안전한 길은:

1. **PR을 사후 복원하지 마세요.** 이미 박힌 main 커밋은 그대로 두고
2. 그 커밋을 `git revert` 로 안전하게 되돌리는 새 커밋을 추가 ([02 안전한 되돌리기](./02-안전한-되돌리기.md))
3. 그다음 올바른 브랜치에서 다시 작업 + PR

> ⚠️ `git push --force` 로 main 의 잘못된 커밋을 지우려 하지 마세요. 팀원 작업을 날립니다. revert가 정답.

### 예방

- 작업 시작 시 항상 `git branch` 로 현재 브랜치 확인 (또는 VSCode 좌측 하단 상태바)
- main 보호 룰 켜기 ([02-02](../02-팀과-같이-쓰기/02-보호-룰-3개.md))

---

## 🚨 4. push 401 / 403 — 인증 에러

### 증상

```
remote: Permission to user/repo.git denied to your-username.
fatal: unable to access 'https://github.com/...': The requested URL returned error: 403
```

또는:

```
remote: Support for password authentication was removed on August 13, 2021.
```

### 원인

| 메시지 | 원인 |
| --- | --- |
| `Permission ... denied` | 레포 권한 부족 (collaborator 아님 / read only) |
| `password authentication was removed` | 비밀번호로 인증 시도 — GitHub은 2021년부터 PAT 또는 OAuth 만 허용 |
| `Authentication failed` | PAT 만료 / 잘못된 토큰 |

### 처방

#### 권한 부족이면

팀장에게 collaborator 추가 + **Write** 권한 요청.

#### PAT 만료/없음이면

[00-04 인증](../00-환경세팅/04-인증.md) 의 PAT 발급 단계로. 만들고 다시 push 시도하면 비밀번호 칸에 PAT 붙여넣기 안내가 떠요.

#### 이전 자격증명이 캐시에 끼어 있으면

**macOS:** Keychain Access 앱 → `github.com` 검색 → 항목 삭제 → 다시 push

**Windows:** 제어판 → 사용자 계정 → 자격 증명 관리자 → Windows 자격 증명 → `git:https://github.com` 항목 제거

### 예방

- PAT 만료일을 캘린더에 표시
- 부트캠프 시작할 때 한 번에 인증 셋업 완료 ([00-04](../00-환경세팅/04-인증.md))

---

## 🚨 5. 머지된 내 브랜치 처리

### 증상

PR이 squash 머지됐어요. GitHub UI에서는 가지가 자동 삭제됐는데, **내 컴퓨터에는 아직 남아 있는 상태**. `git branch` 했을 때:

```bash
$ git branch
* feat/#1-login    ← 이미 머지됐는데 로컬에 남아 있음
  feat/#2-signup
  main
```

### 처방

```bash
# 1. main으로 이동 + 최신 받기
$ git switch main
$ git pull

# 2. 머지된 로컬 브랜치 삭제
$ git branch -d feat/#1-login
Deleted branch feat/#1-login (was 4f2c1ab).

# 3. 원격에서 사라진 브랜치 참조도 정리
$ git fetch --prune
```

### 일괄 청소 (오래된 브랜치 여러 개)

```bash
# 머지된 브랜치만 한 번에 (main, develop 제외)
$ git branch --merged | grep -vE '(^\*|main|develop)' | xargs -n 1 git branch -d
```

### 예방

- GitHub 레포 설정 → **Automatically delete head branches** 켜기 (원격은 자동 정리)
- 머지 직후 로컬도 같이 정리하는 습관

---

## 한 발자국 더 — 그 외 자주 보는 메시지들

| 메시지 | 원인 / 가는 곳 |
| --- | --- |
| `fatal: not a git repository` | Git 저장소가 아닌 폴더에서 git 명령 실행. `git init` 또는 올바른 폴더로 이동 |
| `nothing to commit, working tree clean` | 변경사항 없음 (에러 아님) |
| `Your branch is behind 'origin/main' by N commits` | 원격이 앞서 있음. `git pull` |
| `Your branch is ahead of 'origin/main' by N commits` | 로컬이 앞서 있음. `git push` 안 한 상태 |
| `error: Your local changes ... would be overwritten by merge` | 작업 중인 변경이 merge에 의해 덮어써질 위험. 먼저 commit 또는 stash |
| `fatal: refusing to merge unrelated histories` | 서로 다른 Git 히스토리를 합치려는 시도 (보통 init 한 두 폴더). `--allow-unrelated-histories` 옵션 — 단 의도 확인 필수 |

위 메시지들을 한 줄짜리 표가 아닌 **4단(메시지/원인/처방/예방)** 으로 풀어 쓴 [**03-05 에러 메시지 사전**](./05-에러-메시지-사전.md) 도 함께 두었어요. 메시지가 길거나 처음 보는 형태면 그쪽으로.

[**다음: 02 안전한 되돌리기 →**](./02-안전한-되돌리기.md)

---

### 💡 한 줄 요약

자주 막히는 5가지: **rejected push → pull, .env 푸시 → 키 재발급 1순위, 잘못된 브랜치 → reset --soft + stash, 401 → PAT, 머지 후 정리 → branch -d**.

### 📚 더 깊이 보기

- [02 안전한 되돌리기](./02-안전한-되돌리기.md) — revert / stash
- GitHub 공식 — [About authentication to GitHub](https://docs.github.com/en/authentication)
- GitHub 공식 — [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- 위키독스 — *3.2.3 충돌 해결 방법*, *4.3 기존 커밋의 이메일 변경* (filter-repo 사용법)
- Pro Git — *§7.7 Reset 명확히 알고 가기*

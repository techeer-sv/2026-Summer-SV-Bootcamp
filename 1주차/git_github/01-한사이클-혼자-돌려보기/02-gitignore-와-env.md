# 01-02. .gitignore와 .env

📎 세션 슬라이드 12 (.gitignore)

> ⚠️ **이 챕터를 건너뛰지 마세요.** 부트캠프 4주에서 가장 자주 일어나는 사고가 **`.env` 파일에 든 API 키를 GitHub에 푸시해버리는 것**입니다. 한 번 push되면 `git log`에 영원히 남아서 키를 즉시 재발급해야 해요.

---

## 1. `.gitignore` 란

Git에게 **"이 파일들은 절대 추적하지 마"** 라고 알려주는 파일입니다. 프로젝트 루트에 `.gitignore` 라는 이름으로 두고, 안에 무시할 패턴을 한 줄에 하나씩 적어요.

```gitignore
# 주석은 # 으로

# 환경 변수 파일 — 비밀 키가 들어 있어 절대 올리면 안 됨
.env
.env.local
.env.*.local

# 의존성 폴더 — 용량 크고, package.json만 있으면 재설치 가능
node_modules/

# 빌드 결과물
dist/
build/

# OS가 자동으로 만드는 파일
.DS_Store           # macOS
Thumbs.db           # Windows

# 에디터 설정
.vscode/
.idea/
```

`.gitignore` 자체는 Git이 추적해야 해요. 팀원 모두가 같은 무시 규칙을 공유해야 하니까요.

---

## 2. 이번 실습 레포의 `.gitignore` 확인

01-01에서 GitHub 레포 만들 때 언어 템플릿을 골라뒀다면 이미 적절한 `.gitignore` 가 있을 거예요. 확인:

```bash
$ cat .gitignore
# Logs
logs
*.log
npm-debug.log*
...
```

내용이 어느 정도 있으면 OK. 비어 있거나 부족하면 [**gitignore.io**](https://www.toptal.com/developers/gitignore) 에서 본인 환경을 선택 (예: `Node`, `macOS`, `VisualStudioCode`) 후 생성된 내용을 복사해서 채워넣으세요.

> 💡 **gitignore.io** 는 OS · 에디터 · 언어를 조합해 최적의 `.gitignore` 를 만들어주는 무료 서비스예요. 부트캠프 프로젝트 시작할 때마다 한 번씩 이용하시면 좋습니다.

---

## 3. 실습 — `.env` 가 정말 안 올라가는지 확인

가장 자주 일어나는 사고를 시뮬레이션해봅시다.

### 단계 1. 가짜 `.env` 만들기

```bash
$ echo 'OPENAI_API_KEY=sk-fake-1234-DO-NOT-USE' > .env
$ cat .env
OPENAI_API_KEY=sk-fake-1234-DO-NOT-USE
```

이 키는 가짜지만, 진짜 키였다면 GitHub에 올라간 순간 봇이 1분 안에 스캔해서 빼가요.

### 단계 2. `git status` 로 확인

```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`.env` 파일이 **안 보이면** `.gitignore` 가 잘 동작하는 거예요. Git이 이 파일의 존재 자체를 무시하고 있는 상태.

### 단계 3. 만약 `.env` 가 status 에 나타나면

`.gitignore` 에 `.env` 가 없거나 오타가 났을 수 있어요. 다음을 실행:

```bash
$ echo ".env" >> .gitignore
$ git status
```

이제는 안 보일 거예요. **추적 안 되는 게 정상.**

### 단계 4. 일부러 강제로 add 해보기

```bash
$ git add .env
The following paths are ignored by one of your .gitignore files:
.env
hint: Use -f if you really want to add them.
```

Git이 **막아줍니다.** 이게 `.gitignore` 의 진가예요.

### 단계 5. 정리

```bash
$ rm .env
```

실습 끝났으니 가짜 `.env` 는 지웁니다.

---

## 4. ⚠️ 함정 — 이미 추적 중인 파일은 `.gitignore` 가 못 막아요

`.gitignore` 는 **추적 시작 전인 파일**에만 효과가 있어요.
이미 commit된 파일은 `.gitignore` 에 추가해도 계속 추적됩니다.

### 시뮬레이션

```bash
# 1. .gitignore에 secrets.txt 가 없는 상태에서 추가·커밋
$ echo "secret" > secrets.txt
$ git add secrets.txt
$ git commit -m "test: track secrets"

# 2. 뒤늦게 .gitignore에 추가
$ echo "secrets.txt" >> .gitignore

# 3. 파일 수정
$ echo "new secret" >> secrets.txt

# 4. status 확인
$ git status
modified:   secrets.txt    # ← .gitignore 에 추가했는데도 잡힘!
```

### 해결법: 추적에서 강제로 빼기

```bash
$ git rm --cached secrets.txt
rm 'secrets.txt'

$ git status
deleted:    secrets.txt
        (.gitignore에 등록되어 더 이상 안 보임)
```

`--cached` 는 **로컬 파일은 그대로 두고 Git 추적에서만 빼라**는 옵션. 실수로 추적한 비밀 파일을 빼낼 때 자주 씁니다.

이 변경을 commit하면 이제부터 정상.

```bash
$ git commit -m "chore: stop tracking secrets.txt"
```

> ⚠️ **주의 — 이미 push까지 됐다면 단순 untrack로 부족합니다.** 히스토리에 그 파일이 여전히 남아 있어요. 그 경우는 [3-01 FAQ #2 — .env 실수 push](../03-자주-막히는-순간/01-faq.md) 참고. **이미 push된 비밀 키는 그 즉시 재발급이 1순위.**

---

## 5. 자주 쓰는 `.gitignore` 패턴 치트시트

```gitignore
# 와일드카드 — 확장자로 매칭
*.log              # 모든 .log 파일
*.tmp

# 디렉토리 — 끝에 슬래시
node_modules/
__pycache__/
.venv/

# 특정 경로
/build/            # 루트의 build만 (하위 build/는 무시 안 함)
build/             # 어디든 build 폴더

# 부정 — 일부만 추적
*.log              # 모든 로그 무시
!important.log     # 단 important.log는 추적
```

---

## 🩺 막힐 때

<details>
<summary><b><code>.gitignore</code> 에 .env를 추가했는데 여전히 status에 보여요</b></summary>

대부분 위 <b>4번 — 이미 추적 중인 파일</b> 케이스. <code>git rm --cached &lt;파일&gt;</code> 으로 추적에서 빼주세요.

</details>

<details>
<summary><b>Git이 <code>.env.example</code> 같은 파일은 추적해야 하는데, 패턴 때문에 같이 무시돼요</b></summary>

부정 패턴을 쓰면 됩니다:

```gitignore
.env*
!.env.example
```

</details>

<details>
<summary><b>이미 <code>.env</code> 를 GitHub에 push해버렸어요</b></summary>

**1순위: 그 키들을 모두 즉시 재발급/리볼브**하세요. OpenAI 키, DB 비밀번호 등 모두. 봇이 1분 안에 스캔해갑니다.

그다음 히스토리 정리는 <a href="../03-자주-막히는-순간/01-faq.md">FAQ #2</a> 참고. 단, **재발급이 먼저** 입니다.

</details>

---

## ✅ 체크포인트

- [ ] 레포 루트에 `.gitignore` 가 있음
- [ ] `.env` 가 `.gitignore` 에 포함됨
- [ ] 가짜 `.env` 를 만들었을 때 `git status` 에 안 나타남
- [ ] `.gitignore` 의 의미와 한계 (이미 추적 중인 건 못 막는다는 점) 이해

[**다음: 03 Issue 만들기 →**](./03-issue-만들기.md)

---

### 💡 한 줄 요약

`.gitignore` 에 `.env`·`node_modules/`·OS 파일은 무조건 포함. 이미 추적 중인 파일은 `git rm --cached`. **실수로 키 push했으면 키 재발급이 1순위.**

### 📚 더 깊이 보기

- GitHub 공식 — [Ignoring files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)
- [gitignore.io](https://www.toptal.com/developers/gitignore) — 환경별 .gitignore 자동 생성
- [github.com/github/gitignore](https://github.com/github/gitignore) — 언어별 공식 템플릿 모음
- 위키독스 — *2.01 .gitignore 파일 관리* (가장 친절하고 자세함)
- Pro Git — *§2.2 수정하고 저장소에 저장하기* (`.gitignore` 절)

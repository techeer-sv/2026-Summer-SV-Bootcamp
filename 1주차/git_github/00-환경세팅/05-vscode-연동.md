# 00-05. VSCode 연동

📎 세션 슬라이드 12, 13, 23 (.gitignore · Commit · Conflict 해결)

이 챕터에서는 VSCode를 Git과 GitHub의 손잡이로 만들어요. 터미널과 GUI를 자유롭게 오갈 수 있는 상태가 목표입니다.

> 💡 **이 자료는 CLI를 메인으로 가지만**, 시각화가 필요한 두 장면 — 스테이징 / 충돌 해결 — 에서는 VSCode가 압도적으로 편해요.

---

## 1. VSCode 설치 (이미 있으면 건너뛰기)

[**code.visualstudio.com**](https://code.visualstudio.com/) 에서 OS에 맞는 인스톨러 다운로드.

**Windows 인스톨러:** 마법사 도중 **"Add to PATH"** 와 **"Open with Code"** 옵션을 체크해두시면 터미널에서 `code .` 명령으로 폴더를 열 수 있어 편해요.

**macOS:** 다운받은 `.zip` 압축 풀어서 `/Applications` 폴더에 드래그.

### 터미널에서 `code` 명령 활성화 (macOS)

VSCode를 열어 명령 팔레트 (`Cmd+Shift+P`) → `Shell Command: Install 'code' command in PATH` 실행.

이제 터미널에서:

```bash
$ code .
# 현재 디렉토리를 VSCode로 열기
```

---

## 2. Git 자동 인식 확인

VSCode는 시스템에 깔린 Git을 자동으로 찾습니다. 확인 방법:

1. VSCode 실행
2. 좌측 사이드바의 **Source Control** 아이콘 (가지 모양 ⤴) 클릭
3. 아래 메시지 중 하나가 보이면 Git 인식 완료:
   - "Open Folder" / "Clone Repository" / "Initialize Repository"

만약 "**Git not found. Install it...**" 경고가 뜨면 [🩺 막힐 때](#-막힐-때) 박스로.

---

## 3. CLI ↔ Source Control 패널 매핑

같은 동작이 양쪽에서 어떻게 보이는지 정리해뒀어요. **CLI를 모를 때 GUI로 한 번 해보고, GUI에서 무슨 일이 일어나는지 CLI로 다시 확인**하는 식으로 익히면 빨라요.

| CLI 명령 | VSCode Source Control 패널 |
| --- | --- |
| `git status` | 패널 자체가 곧 status. 변경된 파일들이 그룹별로 표시됨 |
| `git diff <파일>` | 파일 이름 클릭하면 좌측에 원본, 우측에 변경본의 diff 뷰가 열림 |
| `git add <파일>` | 파일 옆 **`+`** 버튼 클릭 → "Staged Changes" 그룹으로 이동 |
| `git add .` | "Changes" 옆 **`+`** 버튼 클릭 |
| `git reset HEAD <파일>` (unstage) | "Staged Changes"의 파일 옆 **`-`** 버튼 |
| `git commit -m "메시지"` | 상단 메시지 입력칸에 입력 후 ✓ (Commit) 버튼 |
| `git push` | 패널 상단 `…` 메뉴 → Push, 또는 좌측 하단 상태바의 동그라미·화살표 아이콘 |
| `git pull` | 같은 곳의 Pull |
| `git checkout <브랜치>` | 좌측 하단 상태바의 현재 브랜치 이름 클릭 → 목록에서 선택 |
| `git branch <새브랜치>` | 좌측 하단 브랜치 클릭 → "Create new branch..." |

> 💡 **단축키 정리표**가 필요하시면 명령 팔레트(`Cmd/Ctrl+Shift+P`)에서 `Git:` 으로 검색하면 모든 Git 명령이 나옵니다.

---

## 4. 추천 확장 (선택)

부트캠프 4주 동안 도움이 될 확장 두 개. 둘 다 무료.

### GitLens — 누가 언제 이 줄을 고쳤는지

[VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) 또는 확장 탭에서 "GitLens" 검색 → Install.

설치 후 코드 어느 줄에 커서를 두면 줄 끝에 회색 글씨로 **"You, 3 days ago · feat: add login form"** 같은 정보가 떠요. 팀원 누가 어떤 줄을 언제 고쳤는지 확인할 때 유용.

### GitHub Pull Requests — VSCode에서 PR 리뷰

[VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) → Install.

설치 후 좌측 사이드바에 PR 아이콘이 생겨요. 팀원의 PR을 VSCode 안에서 직접 체크아웃·리뷰·머지할 수 있어요. PR 리뷰 챕터(Part 2-04)에서 한 번 더 다룹니다.

---

## 🩺 막힐 때

<details>
<summary><b>VSCode가 "Git not found" 라고 떠요</b></summary>

VSCode가 PATH에서 Git을 못 찾는 상황. 먼저 터미널에서 <code>git --version</code> 이 동작하는지 확인하시고:

- 동작한다면 → VSCode를 완전히 종료 후 재실행 (Mac은 <code>Cmd+Q</code>, Windows는 작업 표시줄 X)
- 동작 안 한다면 → <a href="./02-git-설치.md">02 Git 설치</a> 로 돌아가 PATH 문제 해결

</details>

<details>
<summary><b>VSCode에서 한글 파일명이 깨져 보여요 (macOS)</b></summary>

macOS는 NFD, Linux/Windows는 NFC로 한글을 저장해 충돌이 종종 생겨요. 글로벌 설정 한 줄:

```bash
$ git config --global core.precomposeunicode true
```

</details>

<details>
<summary><b>"code ." 명령이 안 잡혀요 (macOS)</b></summary>

위 1번의 <b>"Shell Command: Install 'code' command in PATH"</b> 를 다시 실행. 그래도 안 되면 새 터미널 창을 열어보세요.

</details>

<details>
<summary><b>Source Control 패널에 내 변경이 안 보여요</b></summary>

폴더가 Git 저장소가 아닌 상태입니다. 패널의 "Initialize Repository" 버튼 또는 터미널에서 <code>git init</code> 실행. (Part 1-01에서 자세히)

</details>

---

## ✅ 체크포인트

- [ ] VSCode가 시스템에 설치됨
- [ ] VSCode의 Source Control 패널을 열 수 있음
- [ ] (선택) `code .` 명령이 터미널에서 동작
- [ ] (선택) GitLens / GitHub Pull Requests 확장 설치

다 체크되면 [**다음: 06 체크리스트 →**](./06-체크리스트.md)

---

### 💡 한 줄 요약

VSCode의 Source Control 패널이 곧 CLI 명령들의 GUI 버전. 스테이징·충돌 해결만큼은 GUI가 더 편하니 둘 다 손에 익히세요.

### 📚 더 깊이 보기

- VSCode 공식 — [Source Control in VS Code](https://code.visualstudio.com/docs/sourcecontrol/overview)
- VSCode 공식 — [Working with GitHub](https://code.visualstudio.com/docs/sourcecontrol/github)
- GitLens — [gitlens.amod.io](https://www.gitkraken.com/gitlens)
- 위키독스 — *4장 Git 고급 명령* (VSCode를 활용한 conflict 해결 등)

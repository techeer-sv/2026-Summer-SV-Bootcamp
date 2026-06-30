# 00-02. Git 설치

이 챕터를 끝내면 어느 터미널에서든 아래 명령이 나옵니다.

```bash
$ git --version
git version 2.45.0   # 숫자는 조금 달라도 OK
```

여러분 OS에 맞춰 **한쪽만** 따라하시면 됩니다.

- [macOS는 여기로 →](#macos)
- [Windows는 여기로 →](#windows)
- 둘 다 끝나면 [공통: 사용자 정보 설정](#공통-사용자-정보-설정-처음-한-번만) 으로

---

## macOS

### 자기 맥이 어떤 칩인지 먼저 확인

```bash
$ uname -m
arm64       # → Apple Silicon (M1/M2/M3/M4)
x86_64      # → Intel
```

칩 종류에 따라 Homebrew 설치 경로가 살짝 달라요. 명령어 자체는 같습니다.

### 옵션 A. Homebrew로 설치 (권장)

**Homebrew가 이미 깔려 있는지 확인:**

```bash
$ brew --version
Homebrew 4.x.x   # 이런 출력이 나오면 깔려 있는 거예요
```

이미 깔려 있으면 **B 단계로** 바로 점프하세요.

**Homebrew가 없으면:** 공식 사이트 [brew.sh](https://brew.sh) 의 한 줄짜리 설치 명령을 그대로 복사해 실행합니다.

```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치가 끝나면 화면 끝에 **"Next steps"** 라며 두 줄짜리 명령이 나옵니다. 그 두 줄을 그대로 복사해서 실행하셔야 PATH에 `brew`가 등록돼요. (Apple Silicon은 `/opt/homebrew`, Intel은 `/usr/local` 경로를 씁니다.)

**그다음 Git 설치:**

```bash
$ brew install git
```

`==> Pouring git--2.x.x.arm64_sonoma.bottle.tar.gz` 같은 진행 표시가 지나가고 `🍺` 가 보이면 끝.

### 옵션 B. Xcode Command Line Tools (Homebrew 없이 가볍게)

Homebrew를 안 쓰고 가고 싶으면 이 한 줄이면 됩니다.

```bash
$ xcode-select --install
```

회색 팝업이 뜨면 **"설치"** 클릭 → 약관 동의 → 다운로드 (몇 분 걸려요).

설치가 끝나면 바로 `git --version` 이 동작합니다.

### macOS — 옵션 비교

| 옵션 | 좋은 점 | 아쉬운 점 |
| --- | --- | --- |
| **A. Homebrew** | Git 최신 버전 / 나중에 `brew upgrade git` 한 줄로 업데이트 | Homebrew 자체 설치가 한 단계 더 필요 |
| **B. Xcode CLT** | 클릭 한 번이면 끝, 별도 설치 도구 불필요 | Git 버전이 약간 옛날 / 업데이트 = Xcode CLT 통째로 재설치 |

> 💡 부트캠프 4주에는 어느 쪽이든 충분해요. Homebrew를 향후에도 쓸 생각이면 A, 한 번만 깔고 잊고 싶으면 B.

### macOS — 🩺 막힐 때

<details>
<summary><b>"xcrun: error: invalid active developer path" 가 떠요</b></summary>

Xcode CLT 경로가 깨진 상태입니다. 다시 설치하세요.

```bash
$ xcode-select --install
```

</details>

<details>
<summary><b>brew install 도중 "Permission denied" 가 나와요</b></summary>

`/usr/local` 또는 `/opt/homebrew` 권한 문제입니다. **절대로 `sudo`를 붙이지 마세요.** Homebrew는 sudo 없이 동작해야 정상입니다. 아래 진단 명령을 먼저 돌려보세요.

```bash
$ brew doctor
```

진단 결과의 안내를 따르거나, 결과 전체를 멘토에게 공유해주세요.

</details>

<details>
<summary><b>회사망/학교 와이파이에서 curl이 안 돼요</b></summary>

프록시 뒤에 있을 가능성이 큽니다. 핫스팟으로 잠깐 전환하시거나, 네트워크 담당자에게 프록시 주소를 받아 `~/.zshrc` 에 아래 두 줄을 추가하세요.

```bash
export HTTP_PROXY=http://proxy.회사.com:포트
export HTTPS_PROXY=http://proxy.회사.com:포트
```

`source ~/.zshrc` 후 다시 시도.

</details>

<details>
<summary><b>"command not found: git" 인데 brew install 은 성공했어요</b></summary>

PATH에 brew 경로가 안 들어간 상태예요. 아래를 실행하고 새 터미널을 띄우세요.

```bash
# Apple Silicon
$ echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
$ eval "$(/opt/homebrew/bin/brew shellenv)"

# Intel Mac
$ echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
$ eval "$(/usr/local/bin/brew shellenv)"
```

</details>

이제 [**공통 설정 →**](#공통-사용자-정보-설정-처음-한-번만) 으로 점프하세요.

---

## Windows

[**git-scm.com/download/win**](https://git-scm.com/download/win) 에 접속하면 자동으로 인스톨러 다운로드가 시작됩니다.

받은 `.exe` 파일을 더블클릭하고 마법사를 따라가세요. 옵션이 많아 보이지만 **권장값으로만 따라가면 됩니다.**

### Git for Windows 인스톨러 권장 옵션

순서대로 나오는 각 화면의 권장값입니다. 다른 옵션은 건드리지 마세요.

| # | 화면 | 권장 |
| --- | --- | --- |
| 1 | License | 그대로 Next |
| 2 | Install Location | 그대로 Next |
| 3 | Select Components | 그대로 Next (기본 체크박스만 유지) |
| 4 | Start Menu Folder | 그대로 Next |
| 5 | **Choosing the default editor** | **Visual Studio Code** 선택 (VSCode 설치되어 있을 때) |
| 6 | **Adjusting the name of the initial branch** | **Override the default branch name for new repositories → `main`** |
| 7 | Adjusting your PATH environment | 그대로 (`Git from the command line and also from 3rd-party software`) |
| 8 | Choosing the SSH executable | 그대로 (`Use bundled OpenSSH`) |
| 9 | HTTPS transport backend | 그대로 (`Use the OpenSSL library`) |
| 10 | **Configuring the line ending conversions** | **Checkout Windows-style, commit Unix-style line endings** (기본값) |
| 11 | Configuring the terminal emulator | 그대로 (`Use MinTTY`) |
| 12 | Choose the default behavior of `git pull` | 그대로 (`Default (fast-forward or merge)`) |
| 13 | Choose a credential helper | **`Git Credential Manager`** (기본값) — 인증 자동화에 꼭 필요 |
| 14 | Extra options | 그대로 (`Enable file system caching`) |
| 15 | Experimental options | **체크 안 함** (기본값) |

마지막 **Install** 클릭, 끝나면 **Finish**.

### Git Bash 띄우기

시작 메뉴에서 **"Git Bash"** 를 검색해서 띄우세요. 검은 화면 터미널이 떠요. **앞으로 이 자료의 모든 명령어는 이 Git Bash 안에서 칩니다.** PowerShell/CMD가 아니에요.

> 💡 PowerShell·CMD에서도 `git` 명령어는 동작합니다. 단, 이 자료의 셸 명령(`ls`, `touch`, `cat` 등)은 Git Bash 기준으로 적혀 있어서 다른 셸에서는 일부 안 먹어요. 헷갈리지 않게 **Git Bash 하나로 통일**하시는 게 좋아요.

### Windows — 🩺 막힐 때

<details>
<summary><b>인스톨러 도중 "이 앱이 디바이스를 변경하도록 허용하시겠습니까?" 가 떠요</b></summary>

정상입니다. **예** 를 누르세요. 관리자 권한이 없는 회사 노트북이면 IT 부서에 설치 요청을 하셔야 합니다.

</details>

<details>
<summary><b>한글이 깨져 보여요 (예: <code>aŔaˇ\</code>)</b></summary>

Locale 설정 문제예요. Git Bash에서 아래를 실행하세요.

```bash
$ echo 'export LANG="ko_KR.UTF-8"' >> ~/.bashrc
$ echo 'export LC_ALL="ko_KR.UTF-8"' >> ~/.bashrc
$ source ~/.bashrc
```

새 Git Bash 창을 띄우면 정상으로 보입니다.

</details>

<details>
<summary><b>회사망에서 인스톨러 다운로드가 안 돼요</b></summary>

방화벽 또는 프록시 뒤일 가능성. 핫스팟으로 잠깐 받아오거나, IT 부서에 Git for Windows 설치 요청.

</details>

<details>
<summary><b>설치는 됐는데 PowerShell에서 <code>git</code>이 안 잡혀요</b></summary>

7번 옵션을 잘못 선택한 경우입니다. 인스톨러를 다시 실행해서 **"Git from the command line and also from 3rd-party software"** 로 다시 설정 후 새 PowerShell 창을 띄우세요.

</details>

<details>
<summary><b>VSCode가 안 깔려 있는데 5번 옵션에 어떻게 해야 하나요</b></summary>

지금은 **Use Vim** 그대로 두고 진행하셔도 됩니다. VSCode 설치 후 나중에 아래 한 줄로 바꾸시면 돼요.

```bash
$ git config --global core.editor "code --wait"
```

</details>

이제 [**공통 설정 →**](#공통-사용자-정보-설정-처음-한-번만) 으로.

---

## 공통: 사용자 정보 설정 (처음 한 번만)

OS 상관없이 같습니다. 터미널 (macOS는 Terminal/iTerm, Windows는 Git Bash)에서 아래 세 줄을 한 번 실행하세요.

```bash
$ git config --global user.name "본인 이름"
$ git config --global user.email "본인이메일@example.com"
$ git config --global init.defaultBranch main
```

| 설정 | 무엇인가요 |
| --- | --- |
| `user.name` | 커밋에 표시될 이름. 본명·닉네임 자유 (팀 안에서 누군지 알아볼 수 있는 이름 권장) |
| `user.email` | 커밋에 표시될 이메일. **GitHub 가입에 쓸 이메일과 일치시키세요.** 안 그러면 잔디(GitHub 활동 그래프)에 안 찍혀요 |
| `init.defaultBranch=main` | 새 레포의 기본 브랜치를 `main`으로 (옛날 기본값은 `master` 였어요) |

### 잘 들어갔는지 확인

```bash
$ git config --global --list
user.name=...
user.email=...
init.defaultbranch=main
```

세 줄 다 보이면 완료입니다.

---

## ✅ 체크포인트

- [ ] 터미널에서 `git --version` 이 버전 숫자를 출력
- [ ] `git config --global user.name` 이 내 이름 출력
- [ ] `git config --global user.email` 이 **GitHub 가입에 쓸** 이메일 출력
- [ ] `git config --global init.defaultBranch` 가 `main` 출력
- [ ] (Windows) Git Bash가 시작 메뉴에 있음

다 체크되면 [**다음: 03 GitHub 가입 →**](./03-github-가입.md)

---

### 💡 한 줄 요약

OS에 맞춰 Git을 설치하고 `user.name` · `user.email` · `init.defaultBranch=main` 세 줄을 한 번 실행하면 끝. 막히면 챕터 안 **🩺 막힐 때** 박스부터.

### 📚 더 깊이 보기

- 위키독스 — *1.2 git 설치*, *1.3 Git Bash*, *1.4 Git 사용자 정보 설정*, *1.3.1 Git Bash 한글 출력*
- Pro Git — *§1.5 Git 설치*, *§1.6 Git 최초 설정* → [git-scm.com/book/ko/v2](https://git-scm.com/book/ko/v2)
- Git 공식 다운로드 → [git-scm.com/downloads](https://git-scm.com/downloads)
- Homebrew 공식 → [brew.sh](https://brew.sh)


# 00-03. GitHub 가입

📎 세션 슬라이드 05~06

이 챕터를 끝내면 GitHub 계정이 만들어지고, 2단계 인증(2FA)까지 설정되어 안전하게 로그인할 수 있는 상태가 됩니다.

> 💡 **이미 GitHub 계정이 있는 분도 이 챕터는 한 번 훑어보세요.** 잔디 인식을 위한 이메일 일치 확인 / 2FA 미설정 시 한 달 안에 계정 잠금 위험 같은 중요한 점이 있어요.

---

## 1. 가입

[**github.com**](https://github.com) 에 접속해 우상단 **Sign up** 클릭.

순서대로 다음을 입력합니다.

| 입력 | 권장 |
| --- | --- |
| **Email** | **00-02에서 `git config --global user.email` 에 넣은 이메일과 동일하게** 입력 (잔디 인식의 핵심) |
| **Password** | 15자 이상 (또는 8자 이상에 숫자·소문자 포함) — GitHub 권장 |
| **Username** | 영문 소문자·숫자·하이픈. 한 번 정하면 바꾸기 번거롭습니다 |

### Username 정할 때

이 이름이 곧 여러분의 GitHub URL이 됩니다 → `github.com/내-username`. 4주 동안 팀원·멘토가 계속 부를 이름이에요.

- ✅ `leo-dev`, `jeong-dlwjd`, `kim-frontend` — 본인 식별이 쉬움
- ❌ `xX_destroyer_Xx`, `cool-guy-2026` — 협업·이력서·SNS에서 곤란해질 수 있음

> 💡 username은 나중에 바꿀 수 있긴 하지만, 이미 만든 PR/이슈 URL 일부가 바뀌어서 팀에 혼란을 줄 수 있어요. **처음에 잘 정해두는 것이 베스트.**

### 이메일 인증

가입 직후 GitHub이 보낸 메일의 인증 링크를 클릭하시면 됩니다.
**인증 메일이 안 오면:** 스팸함 확인 → 그래도 없으면 GitHub에서 **Resend verification email** 클릭.

---

## 2. 2단계 인증 (2FA) 설정 — **필수**

GitHub은 2023년 9월부터 모든 사용자에게 **2FA를 의무화**하고 있어요. 안 켜두면 며칠~몇 주 안에 계정이 일시 잠겨요.
가입 직후 바로 설정하시는 게 가장 깔끔합니다.

[**github.com/settings/security**](https://github.com/settings/security) 또는 우상단 프로필 → **Settings** → 좌측 **Password and authentication** → **Two-factor authentication** → **Enable two-factor authentication**.

### 인증 방식 — 인증 앱 권장

| 방식 | 추천도 |
| --- | --- |
| **Authenticator app** (인증 앱) | ⭐⭐⭐ 권장. 휴대폰 없이도 PC 앱으로 받을 수 있음 |
| Passkeys (생체 인증) | ⭐⭐ 새 폰·노트북에서 다시 등록해야 해서 번거로움 |
| SMS | ⭐ 비추 (GitHub도 비권장). 보안 약함 + 해외 번호 문제 |

인증 앱 추천 (셋 중 하나, 다 무료):

- [**1Password**](https://1password.com) — 비밀번호도 같이 관리하고 싶다면
- [**Authy**](https://authy.com) — 인증 코드 전용
- **Google Authenticator** — 가장 간단, 다만 기기 변경이 번거로움

### 설정 단계

1. 인증 앱을 휴대폰(또는 PC)에 설치
2. GitHub 화면의 **QR 코드**를 앱으로 스캔
3. 앱에 6자리 코드가 뜨면 GitHub에 입력
4. **백업 코드(Recovery Codes) 16개** 가 화면에 표시 → **반드시 다운로드하거나 캡처해서 안전한 곳에 보관**

> ⚠️ **백업 코드는 휴대폰 분실 시의 유일한 구명줄입니다.** 백업 코드 없이 폰을 잃으면 계정 복구가 며칠~몇 주 걸리고 실패하기도 해요. PDF로 다운받아 이메일 자기 자신에게 보내두거나, 1Password 같은 보안 저장소에 저장하세요.

---

## 3. 프로필 설정 (선택이지만 권장)

[**github.com/settings/profile**](https://github.com/settings/profile)

| 항목 | 권장 |
| --- | --- |
| **Name** | 한글 또는 영문 본명 — 팀원이 PR 리뷰에서 누군지 알아볼 수 있게 |
| **Profile picture** | 얼굴 사진 또는 식별 가능한 아바타 — 회색 기본 아바타는 협업에서 누가 누군지 헷갈려요 |
| **Bio** | 짧게 "테코 부트캠프 2026 프론트엔드" 같은 한 줄 |

---

## 4. 잔디 인식 확인 — **중요**

여기가 자주 놓치는 부분이에요. **두 이메일이 같아야** GitHub 활동 그래프(잔디)에 커밋이 찍힙니다.

```bash
# 1. 로컬 Git 설정 확인
$ git config --global user.email
your-email@example.com

# 2. GitHub의 등록 이메일 확인
#    github.com/settings/emails 페이지에서 Primary email 확인
```

두 값이 **글자 그대로 일치**해야 합니다. 대소문자·도트(.) 차이도 다른 이메일로 취급될 수 있어요.

### 만약 다르다면

**옵션 A. 로컬 설정을 GitHub에 맞춰 바꾸기 (가장 쉬움)**

```bash
$ git config --global user.email "github에-등록된-이메일@example.com"
```

**옵션 B. GitHub에 로컬 이메일을 추가 등록하기**

[**github.com/settings/emails**](https://github.com/settings/emails) → **Add email address** → 추가한 메일 인증 → Primary 로 지정 (선택).

---

## 5. (선택) Student Pack 신청

학생이라면 GitHub이 무료로 제공하는 [**Student Developer Pack**](https://education.github.com/pack) 을 받을 수 있어요. GitHub Copilot 무료 사용, JetBrains IDE 무료, Notion 학생 플랜 등이 포함됩니다. 학교 이메일이 있다면 신청해두시면 4주 프로젝트 내내 도움이 됩니다.

---

## 🩺 막힐 때

<details>
<summary><b>인증 메일이 30분이 지나도 안 와요</b></summary>

1. 스팸함 / 프로모션 탭 확인
2. GitHub 가입 페이지에서 <b>Resend verification email</b>
3. 그래도 안 오면 다른 이메일 주소로 가입 시도 (학교 메일 ↔ 개인 메일 등)

</details>

<details>
<summary><b>원하는 username이 이미 사용 중이에요</b></summary>

뒤에 자기 식별 가능한 숫자/단어 붙이기 추천 (예: <code>jeong-dlwjd</code>, <code>kim-fe-26</code>). 회사명·국적·생년월일은 비추.

</details>

<details>
<summary><b>2FA 인증 앱을 깐 폰을 분실/초기화 했어요</b></summary>

1. <b>백업 코드(Recovery Codes)</b> 가 있으면 그걸로 로그인 후 새 인증 앱 등록
2. 백업 코드도 없으면 GitHub Account Recovery 절차 진행 → <a href="https://support.github.com/contact">support.github.com/contact</a>. 며칠~몇 주 걸릴 수 있어요

</details>

<details>
<summary><b>GitHub에서 계정 잠금 메일이 왔어요 (2FA 미설정)</b></summary>

GitHub의 2FA 의무화에 따른 자동 잠금이에요. 메일의 안내 링크 또는 위 2. 단계 그대로 2FA 설정하시면 잠금이 풀립니다.

</details>

<details>
<summary><b>회사망에서 github.com이 차단돼요</b></summary>

핫스팟으로 잠시 전환해서 가입하시거나, IT 부서에 github.com 허용 요청. 4주 프로젝트 내내 github.com 접속이 필요하니 미리 풀어두시는 게 좋습니다.

</details>

---

## ✅ 체크포인트

- [ ] [github.com](https://github.com) 에 로그인 가능
- [ ] 이메일 인증 완료 (가입 메일 ↔ 클릭)
- [ ] **2FA 활성화 완료**
- [ ] **백업 코드 안전한 곳에 저장**
- [ ] `git config --global user.email` 의 값이 GitHub 등록 이메일과 일치
- [ ] (선택) 프로필 이름·사진 설정

다 체크되면 [**다음: 04 인증 →**](./04-인증.md)

---

### 💡 한 줄 요약

GitHub 가입 → 2FA 필수 + 백업 코드 저장 → `git config user.email` 과 GitHub 등록 이메일 일치 확인.

### 📚 더 깊이 보기

- GitHub 공식 — [Securing your account with 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa)
- GitHub 공식 — [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)
- 위키독스 — *5.1 GitHub 소개*, *5.1.2 GitHub 시작*
- Pro Git — *§6.1 계정 만들고 설정하기* → [git-scm.com/book/ko/v2](https://git-scm.com/book/ko/v2)

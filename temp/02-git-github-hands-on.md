# 2. Git, GitHub, & 프로젝트 구조 — 핸즈온 실습

## 초급: 나만의 첫 저장소 만들고 변경 이력 관리하기

**목표**: 로컬 저장소를 만들고, 변경 사항을 기록·확인·되돌리고, GitHub에 push/pull까지 한 사이클을 직접 경험한다.

**진행 순서**
1. 새 프로젝트 폴더를 만들고 `git init`으로 저장소 초기화
2. `README.md`, `.gitignore` 작성 후 `git add` → `git commit`
3. 파일을 수정한 뒤 `git status`, `git diff`로 무엇이 바뀌었는지 확인
4. `git log`로 지금까지의 커밋 히스토리 확인
5. 일부러 파일을 망가뜨린 뒤 `git restore`로 마지막 커밋 상태로 되돌리기
6. 커밋을 하나 더 쌓고, `git revert`로 특정 커밋의 변경을 취소하는 새 커밋 만들기
7. GitHub에서 새 repository 생성 → `git remote add origin <url>` → `git push`
8. 다른 폴더에 `git clone`으로 받아서 수정 후 `git pull`로 동기화

**결과물**
- 커밋이 5개 이상 쌓인 GitHub repository (README, .gitignore 포함)
- `git log`, `git diff`, `git restore`, `git revert`를 각각 1번 이상 사용한 캡처/메모

---

## 고급: 팀 협업 시뮬레이션 — 브랜치, 충돌, PR

**목표**: 브랜치 분리 작업, merge conflict 해결, PR 리뷰 및 merge 전략까지 실제 협업 흐름을 체험한다.

**준비물**: 2인 1조 (혼자 진행한다면 두 개의 로컬 클론으로 역할을 나눠서 진행)

**진행 순서**
1. main 브랜치에서 `feature/header`, `feature/footer` 두 브랜치 생성
2. 같은 파일의 같은 영역을 각자 브랜치에서 수정 후 커밋
3. `feature/header`를 GitHub에 push → PR 생성 → (짝과) 코드 리뷰 → approve → merge
4. `feature/footer`를 main에 merge 시도 → **merge conflict** 발생시키기
5. 충돌 마커(`<<<<<<<`, `=======`, `>>>>>>>`)를 직접 열어 수동으로 해결 후 merge commit 완료
6. 동일한 변경을 merge commit / squash merge / rebase 세 방식으로 각각 시도해보고 `git log --graph`로 히스토리 모양 비교
7. main, develop, feature 브랜치 구조를 다이어그램으로 그려보고 자신들의 브랜치를 매핑

**결과물**
- 머지 완료된 PR 2개 이상
- merge conflict를 해결한 커밋 1개
- merge / squash / rebase 결과 비교 메모 (git log 그래프 캡처 포함)

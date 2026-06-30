# 영화 게시판 백엔드 핸즈온 (Django REST API)

회원가입/로그인 + 영화 글(Movie, **포스터 이미지 포함**)/댓글(Comment) 을 **Django** 하나로 만드는 실습.
게시판 **목록은 이미지+제목**, **상세는 제목·사진·글·댓글 전부** 를 내려주는 미니멀 REST API.

> 📘 **진행 흐름·이유·개념 설명은 전부 [실습가이드.md](실습가이드.md) 를 보세요.**
> 이 README는 **"어떻게 실행하나"** 만 다룹니다.

---

## 1. 실행 방법 (MySQL 도커)

```bash
cd django-board-handson
python -m venv venv
source venv/bin/activate          # 윈도우: venv\Scripts\activate
pip install -r requirements.txt   # Django·DRF·Pillow·mysqlclient

docker compose up -d              # MySQL 컨테이너 띄우기 (포트 3306)
python manage.py migrate          # 테이블 생성
python manage.py runserver        # http://127.0.0.1:8000/swagger
```
> ⚠️ **로컬에 이미 MySQL이 3306을 쓰고 있으면** 도커가 아니라 그쪽으로 붙어 `Access denied` 가 나요.
> 그땐 로컬 MySQL을 잠깐 끄세요: `brew services stop mysql` (끝나면 `brew services start mysql`).
>
> mac에서 `mysqlclient` 설치가 실패하면: `brew install mysql-client pkg-config` 후 다시 `pip install`.

---

## 2. 테스트 (3가지 방법)

| 방법 | 어떻게 |
|---|---|
| **Swagger** | http://127.0.0.1:8000/swagger → API 클릭 → **Try it out** → 값 입력(포스터는 **파일 선택**) → **Execute** |
| **.http** | `docs/http/board.http` 열고 각 요청의 **Send Request** 클릭 (3번이 이미지 업로드) |
| **curl** | 아래 예시 |

```bash
# 회원가입
curl -X POST http://127.0.0.1:8000/api/v1/users/signup \
  -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"123"}'

# 영화 카드 생성 (포스터 이미지 직접 업로드, multipart)
curl -X POST http://127.0.0.1:8000/api/v1/movies \
  -F "user_id=1" -F "title=인터스텔라" -F "content=인생영화" -F "poster=@/경로/poster.jpg"

# 게시판 목록 / 상세
curl http://127.0.0.1:8000/api/v1/movies
curl http://127.0.0.1:8000/api/v1/movies/1
```

> Swagger에서 파일 선택 칸이 안 보이면 **브라우저 하드 새로고침**(`Cmd+Shift+R`).

---

## 3. 자주 쓰는 명령어

```bash
source venv/bin/activate            # 가상환경 켜기
python manage.py makemigrations     # 모델(models.py) 바꿨을 때
python manage.py migrate            # DB에 반영
python manage.py runserver          # 서버 실행 (포트 바꾸기: runserver 8080)
python manage.py flush              # 데이터만 싹 비우기 (깨끗한 데모용)
python manage.py createsuperuser    # 관리자 계정 → /admin
```

## 4. 종료/정리 (MySQL 썼을 때)

```bash
docker compose down                 # 도커 MySQL 내리기
brew services start mysql           # 아까 끈 로컬 MySQL 다시 켜기 (껐다면)
deactivate                          # 가상환경 끄기
```

---

## API 한눈에 (미니멀)

| 기능 | Method | URL |
|---|---|---|
| 회원가입 | POST | `/api/v1/users/signup` |
| 로그인 | POST | `/api/v1/users/login` |
| 게시판 목록(이미지+제목) | GET | `/api/v1/movies` |
| 카드 생성(+포스터, multipart) | POST | `/api/v1/movies` |
| 상세(제목·사진·글·댓글) | GET | `/api/v1/movies/{id}` |
| 댓글 작성 | POST | `/api/v1/movies/{id}/comments` |

## 폴더 구조

```
django-board-handson/
├── 실습가이드.md            ← 진행 흐름·이유·개념 (메인 문서)
├── config/settings/         ← base.py / dev.py / prod.py (환경 분리)
├── users/                   ← 회원가입/로그인
├── movies/                  ← 영화 글/댓글 (이미지 업로드, 목록/상세 Serializer)
├── docker-compose.yml       ← MySQL 도커
└── docs/http/board.http     ← API 테스트 모음 (+ 샘플 poster.jpg)
```

> ❓ 왜 이렇게 짰는지, 단계별 설명, 트러블슈팅은 **[실습가이드.md](실습가이드.md)** 에 다 있습니다.

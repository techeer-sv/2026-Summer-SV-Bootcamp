# 🎬 영화 리뷰 게시판 (Django + React)

회원가입/로그인부터 **영화 리뷰(사진 포함)·댓글**까지, **백엔드(Django REST API) → 프론트(React)** 로
이어지는 핸즈온 실습이에요. 한 저장소에 **backend / frontend** 가 함께 있는 모노레포입니다.

```
django-board-handson/
├── backend/     # Django + DRF REST API   (1주차 실습)     → backend/README.md
└── frontend/    # React + Vite + Axios 화면 (백엔드 이어받기) → frontend/README.md
```

## 무엇을 만드나

| | 백엔드 (backend) | 프론트 (frontend) |
|---|---|---|
| 목록 | `GET /movies` (이미지+제목) | 카드 그리드 게시판 |
| 상세 | `GET /movies/{id}` (글+댓글) | 상세 페이지 + 댓글 작성 |
| 등록 | `POST /movies` (multipart) | 리뷰 작성 폼(포스터 업로드) |
| 댓글 | `POST /movies/{id}/comments` | 상세 하단 댓글 |
| 회원 | `POST /users/signup·login` | (확장 예정) |

프론트는 백엔드에서 만든 그 API를 **axios로 이어받아** 화면에 그려요.

## 빠른 실행

**두 개를 각각 켜야 해요.** (터미널 2개)

```bash
# ① 백엔드 (터미널 1)
cd backend
source venv/bin/activate            # 윈도우: venv\Scripts\activate
pip install -r requirements.txt     # 최초 1회
python manage.py migrate            # 최초 1회
python manage.py runserver          # → http://localhost:8000  (Swagger: /swagger)

# ② 프론트 (터미널 2)
cd frontend
npm install                         # 최초 1회
npm run dev                         # → http://localhost:5173
```

브라우저에서 **http://localhost:5173** 접속. (백엔드가 먼저 떠 있어야 해요!)

## 연동 포인트 — CORS 🌐

프론트(5173)와 백엔드(8000)는 **포트가 달라서** 브라우저가 요청을 막아요(동일 출처 정책).
그래서 백엔드에 `django-cors-headers` 를 넣고 `http://localhost:5173` 을 허용해뒀어요.
→ 자세히: [backend/CONCEPTS.md # CORS](backend/CONCEPTS.md#cors) · [frontend/CONCEPTS.md # CORS](frontend/CONCEPTS.md#cors)

## 문서

| 문서 | 내용 |
|---|---|
| [backend/README.md](backend/README.md) | Django API 따라 만들기 (모델→뷰→URL, 이미지 업로드, CORS) |
| [backend/CONCEPTS.md](backend/CONCEPTS.md) | 백엔드 "왜" (settings 분리, serializer, FK, CORS, WSGI/ASGI…) |
| [frontend/README.md](frontend/README.md) | React 연동 따라하기 (axios 인스턴스, API 함수, CORS) |
| [frontend/CONCEPTS.md](frontend/CONCEPTS.md) | 프론트 "왜" (Vite, axios, FormData, 라우팅, CORS…) |

## 기술 스택

- **backend** — Python, Django 5, Django REST Framework, drf-spectacular(Swagger), Pillow, django-cors-headers, SQLite(dev)
- **frontend** — React 18, Vite 5, Axios, react-router-dom, npm

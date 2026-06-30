# 개념 정리 — "왜 이렇게 짰나"

> [README.md](README.md) 는 **따라하기**(손으로 만드는 순서), 이 문서는 그 뒤에 읽는 **"왜"** 예요.
> 실습 중 막히지 않게, 깊은 설명은 여기로 모았습니다. README의 `→ 자세히` 링크가 여기로 옵니다.

## 목차
- [settings 분리 (base/dev/prod)](#settings-분리)
- [앱을 도메인별로 나누는 이유](#앱-분리)
- [REST URI · APPEND_SLASH](#rest-uri)
- [마이그레이션이 실제로 하는 일](#마이그레이션)
- [작성자: FK vs IntegerField](#fk-vs-integerfield)
- [Serializer를 목록/상세/생성 3개로 나누는 이유](#serializer-분리)
- [이미지: 저장부터 화면까지](#이미지)
- [왜 APIView (vs ViewSet)](#왜-apiview)
- [WSGI vs ASGI](#wsgi-vs-asgi)
- [Django 기본 auth 를 안 쓴 이유](#django-auth)

---

## settings 분리

`settings.py` 한 파일을 `base.py` / `dev.py` / `prod.py` 셋으로 쪼갠 이유 — 개발과 배포는 값이 다르니까요.

| 항목 | dev (개발) | prod (배포) | 왜 다른가 |
|---|---|---|---|
| `DEBUG` | `True` | `False` | 개발은 에러를 자세히 / 운영은 노출되면 보안사고 |
| DB | **SQLite**(파일 1개) | 실제 DB(`.env`로 지정) | 개발은 설치 0 / 운영은 제대로 된 DB |
| `ALLOWED_HOSTS` | `*` | 운영 도메인만 | 개발 편의 / 운영 보안 |
| 비밀값 | 코드에 둬도 OK | `.env` 로 숨김 | 깃에 비번 올리면 유출 |

- `dev.py`/`prod.py` 는 맨 위에서 `from .base import *` 로 공통을 가져오고 **다른 부분만** 덮어써요.
- 개발은 SQLite라 도커도 DB 서버도 필요 없어요. 배포(prod)에서만 PostgreSQL·MySQL 같은 실제 DB를 `.env` 로 지정.
- **`.env` 를 쓰는 이유**: `SECRET_KEY`·DB 비번 같은 민감값을 코드에 적어 깃에 올리면 유출돼요. 그래서 `.env`(깃 제외)에 두고 읽어와요.
- 어떤 설정으로 도는지는 `DJANGO_SETTINGS_MODULE` 이 정해요: `manage.py`→기본 `config.settings.dev`, `wsgi/asgi`→기본 `config.settings.prod`.

## 앱 분리

`users`/`movies` 는 **장고 규칙이 아니라 우리가 만든 앱**이고 이름도 우리가 붙였어요.

- 장고는 "프로젝트를 여러 앱으로 나눠 써라"까지만 정하고, **몇 개로·무슨 이름인지는 자유.**
- 기준 = **비즈니스 도메인.** (배민이면 `users`·`restaurants`·`orders`·`delivery` …)
- **왜 나누나**: 응집도(관련된 것끼리)·유지보수(고칠 때 그 앱만)·협업·재사용. 작으면 한 앱에 다 넣어도 OK.
- **앱 ≠ 테이블.** 앱은 코드 묶음(폴더), 테이블은 그 안 모델이 만들어요. `movies` 앱 하나에 `movies`·`comments` 두 테이블.

## REST URI

**URI는 동사 말고 명사·복수형.**

- ✅ 명사 : `/movies`, `/movies/1`, `/comments`
- ❌ 동사 : `/createMovie`, `/movies/1/delete`, `/getMovies`
- 행동(생성·조회·삭제)은 **URL이 아니라 HTTP 메서드**(POST/GET/DELETE)가 표현해요.
- 그래서 `POST /movies` = 메서드 POST(행동) + 명사 movies(자원). 충돌 아님.
- **예외**: `signup`/`login` 은 둘 다 POST라 명사만으론 구분이 안 돼서 동사를 허용.

**`APPEND_SLASH = False`**: 장고 기본(True)은 URL 끝에 `/`를 붙여요. 끝 슬래시 없이 설계하려고 끔 → `/movies/1`✅ `/movies/1/`❌

## 마이그레이션

`makemigrations` 와 `migrate` 가 실제로 하는 일:

```
models.py 수정 ─(makemigrations)→ 0001_initial.py (설계도) ─(migrate)→ DB에 테이블 생성
```
- `makemigrations` : `models.py` 를 읽고 "이런 테이블·컬럼을 만들어라"는 **설계도 파일**(`movies/migrations/0001_initial.py`)을 만듦. **아직 DB는 안 건드림.**
- `migrate` : 그 설계도대로 **실제 DB에 테이블 생성/변경.** (SQLite면 `db.sqlite3` 안에)
- 마이그레이션 파일 = **스키마 변경 이력**(깃 관리). 모델 또 바꾸면 `0002_...` 가 쌓이고, `migrate` 는 그 차이만 반영.
- ⚠️ `makemigrations` 만 하고 `migrate` 를 안 하면 테이블이 안 생겨요. **둘 다** 하기.

## FK vs IntegerField

`Movie.user_id = IntegerField()` 는 **학습 단순화용**이에요.

> ⚠️ 실무에서는 거의 안 씁니다. 보통 `ForeignKey(User)`.

| | ① ForeignKey (실무 정석) | ② IntegerField (지금) |
|---|---|---|
| 코드 | `user = models.ForeignKey('users.User', on_delete=CASCADE)` | `user_id = models.IntegerField()` |
| `movie.user.email` | **객체로 바로 접근**(ORM) | 불가 (그냥 숫자) |
| 무결성 | 존재하는 유저만 | 없는 id도 그냥 저장됨 |

- 처음엔 FK를 걸면 글 만들 때 그 유저가 꼭 있어야 해서 테스트가 번거로워 정수로 단순화.
- 인증을 붙이면 보통 `user_id`를 클라가 안 보내고 뷰에서 `serializer.save(user=request.user)` + `read_only_fields=["user_id"]`.

## Serializer 분리

같은 영화라도 화면마다 필요한 게 달라서 목록/상세/생성용을 나눠요.

| 상황 | 시리얼라이저 | fields | 이유 |
|---|---|---|---|
| 목록 | `MovieListSerializer` | id·title·poster | 카드엔 포스터+제목만. content·댓글까지 보내면 **payload↑·쿼리↑·렌더링 느림** |
| 생성 | `MovieSerializer` | 입력 필드 | **검증이 핵심**(required·길이·이미지 형식) = write용 |
| 상세 | `MovieDetailSerializer` | 전부 + comments | 정보가 많이 필요 = 가장 무거움 |

- **꼭 3개?** 작으면 하나로도 OK. 하지만 댓글 500개 글 20개 목록 조회 시 `20×500` nested 직렬화로 **API가 터져요.** 그래서 분리.
- Serializer는 단순 변환기가 아니라 **검증(validation) 레이어.** (직렬화 = 객체→JSON / 역직렬화 = JSON→객체)
- **댓글 nested**: `comments = CommentSerializer(many=True, read_only=True)` → Movie 1 : Comment N 을 응답에 함께.

## 이미지

**핵심: 파일은 디스크에, DB엔 경로만.**
```
업로드한 poster.png
 ├─ 실제 파일  → media/posters/poster.png        (디스크)
 └─ DB movies.poster → "posters/poster.png"       (경로 문자열만!)
```
- `ImageField` = `FileField` + "진짜 이미지인지 검증"(Pillow가 함) → 그래서 Pillow 필요.
- 사진 자체를 DB에 넣으면 무거워지고 느려져요. 파일은 파일시스템(또는 S3), DB는 경로만.

**업로드 흐름** : 프론트가 `multipart/form-data` 로 POST → DRF `MultiPartParser` 가 파일 꺼냄 → `is_valid()` 검증 → `save()` 가 `media/posters/` 에 쓰고 DB엔 경로 → 응답 `poster` 는 전체 URL.

**보여주는 흐름** : 브라우저가 그 URL 요청 → (DEBUG=True) Django가 `MEDIA_ROOT` 에서 파일 찾아 반환 → `<img>` 에 표시.

| | 뜻 | 예 |
|---|---|---|
| `MEDIA_ROOT` | **디스크** 저장 위치 | `.../media` |
| `MEDIA_URL` | **웹 주소** 접두사 | `/media/` |

- **왜 form-data?** JSON은 글자용, 이미지는 바이너리라 안 맞음.
- **절대 URL**: 뷰에서 `context={"request": request}` 안 주면 `/media/...`(상대경로)로 나와 다른 포트 프론트에서 안 보임.
- **파일명 충돌**: 같은 이름 또 올리면 `poster_aB3xK.png` 처럼 랜덤 붙여 덮어쓰기 방지.
- **`blank=True, null=True`**: 포스터 없이도 등록 가능.
- **운영(prod)**: Django가 이미지 서빙 안 함 → nginx/S3. 그래서 `static(...)`이 `if DEBUG` 안에.

## 왜 APIView

DRF엔 `APIView` / `GenericAPIView` / `ViewSet` 이 있어요. 지금은 GET/POST 흐름을 **직접 눈으로 보려고 가장 단순한 `APIView`**. 실무 반복 CRUD엔 `ViewSet` 을 많이 써요.

## WSGI vs ASGI

- **WSGI(동기)** = 요청 하나 끝날 때까지 일꾼이 묶임. 일반 CRUD엔 충분(지금 우리).
- **ASGI(비동기)** = 기다리는 동안 다른 요청도 처리, **웹소켓 등 실시간** 가능.
- FastAPI는 ASGI 전용, Django는 원래 WSGI지만 ASGI도 지원(그래서 `wsgi.py`/`asgi.py` 둘 다 있음).

## Django auth

회원가입에 장고 기본 `auth`(User 모델 등)를 안 썼어요. 처음부터 빡빡하게 만들면 뒤 기능 테스트가 힘들어져서, 이메일/비번 아무거나 넣으면 가입되게 **아주 간단히** 시작한 거예요. 실무에선 `auth` + 비밀번호 해시 + 토큰을 씁니다.

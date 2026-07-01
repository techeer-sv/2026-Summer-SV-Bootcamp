# 개념 정리 — "왜 이렇게 짰나" (프론트)

> [README.md](README.md) 는 **따라하기**(연동하는 순서), 이 문서는 그 뒤에 읽는 **"왜"** 예요.
> 백엔드의 [../backend/CONCEPTS.md](../backend/CONCEPTS.md) 와 짝을 이뤄요 — 특히 **CORS**는 양쪽을 같이 보면 좋아요.

## 목차
- [이 프론트는 백엔드 실습의 '뒷편'](#이어받기)
- [Vite · npm · React가 각각 뭔가](#vite-npm-react)
- [Axios는 왜 fetch 대신 쓰나](#axios)
- [axios 인스턴스를 2개(json/form) 만든 이유](#axios-인스턴스)
- [API 계층을 따로 빼는 이유](#api-계층)
- [useState / useEffect — 화면이 데이터를 다루는 법](#state-effect)
- [라우팅(react-router) — URL이 페이지를 정한다](#라우팅)
- [CORS — 다른 포트끼리 어떻게 통하나](#cors)
- [FormData — 이미지를 보내는 법](#formdata)
- [환경변수(.env)와 import.meta.env](#env)

---

## 이어받기

이 프론트는 **백엔드 실습에서 만든 API를 화면으로 이어받는 파트**예요.

- 백엔드에선 Swagger/curl로 `POST /movies`(등록) → `GET /movies`(목록) → `GET /movies/{id}`(상세)
  를 **손으로** 두들겨봤죠. 프론트는 그 **똑같은 API**를 axios로 부르고, 결과를 화면에 그려요.
- 그래서 백엔드에서 나눴던 개념이 프론트에도 그대로 대응돼요:

| 백엔드(실습) | 프론트(지금) |
|---|---|
| `MovieListSerializer` (목록=이미지+제목) | `MovieListPage` — 카드 그리드 |
| `MovieDetailSerializer` (상세=전부+댓글) | `MovieDetailPage` — 글 + 댓글 |
| `POST /movies` (multipart, 포스터) | `MovieCreatePage` — `formAxios` + FormData |
| CORS 허용 설정 (백엔드) | axios `withCredentials` (프론트) |

## vite-npm-react

- **React** = UI 라이브러리. 화면을 **컴포넌트(부품)** 로 쪼개 조립해요. 데이터(state)가 바뀌면 화면이 자동 갱신.
- **Vite** = 개발 서버 + 빌드 도구. `npm run dev` 하면 몇 초 만에 서버(5173)가 뜨고, 코드 저장 시 즉시 반영(HMR).
  - 예전엔 CRA(create-react-app)를 썼지만 느려서, 요즘은 **Vite** 가 표준이에요.
  - `npm run build` 하면 배포용 정적 파일이 `dist/` 에 나와요.
- **npm** = 패키지 매니저. `npm install` 로 라이브러리를 받고(`node_modules/`), `package.json` 의 `scripts` 를 실행해요.

## axios

`fetch`(브라우저 내장)로도 API를 부를 수 있지만, 실무는 대부분 **Axios**를 써요.

| | fetch | Axios |
|---|---|---|
| JSON 변환 | `await res.json()` 직접 | **자동** (`res.data` 로 바로) |
| 에러 처리 | 4xx/5xx도 "성공"으로 봄 → 직접 체크 | 4xx/5xx면 **자동으로 `catch`** 로 감 |
| 공통 설정 | 매번 반복 | **인스턴스**(`axios.create`)로 재사용 |
| 타임아웃·인터셉터 | 직접 구현 | 기본 제공 |

- 그래서 "JSON 자동 변환 + 편한 에러 처리 + 인스턴스" 때문에 Axios를 골랐어요.

## axios-인스턴스

`src/configs/axios.config.js` 에서 `axios.create()` 로 **공통 설정을 박은 인스턴스**를 만들어요.
`baseURL`·`timeout`·`withCredentials`·`headers` 를 매 요청마다 쓰지 않으려는 거예요.

**왜 `jsonAxios` / `formAxios` 두 개인가** — 보내는 데이터 형식이 다르기 때문이에요.

| | jsonAxios | formAxios |
|---|---|---|
| Content-Type | `application/json` | `multipart/form-data` |
| 보내는 것 | 객체(→ 자동 JSON) | `FormData`(텍스트 + **파일**) |
| 쓰는 곳 | 목록·상세·댓글 | 영화 등록(포스터 이미지) |

- 이미지 같은 **바이너리 파일은 JSON에 못 실어요.** 그래서 파일이 낄 땐 `multipart/form-data` 가 필요하고,
  Content-Type이 달라서 인스턴스를 나눈 거예요. (하나로 두고 요청마다 헤더를 바꿔도 되지만, 나누면 실수가 줄어요.)
- 백엔드 `MovieView` 의 `parser_classes = [MultiPartParser]` 가 바로 이 multipart를 받는 짝이에요.
- `withCredentials: true` = 쿠키/인증정보를 요청에 포함. 백엔드 `CORS_ALLOW_CREDENTIALS = True` 와 한 쌍(→ [CORS](#cors)).

## api-계층

`src/api/moviesApi.js` 처럼 **API 호출을 컴포넌트에서 분리**했어요.

- **컴포넌트(pages)** 는 "무엇을 어떻게 보여줄지"(UI)에 집중.
- **api 함수** 는 "어떤 URL로 어떻게 가져올지"(통신)를 담당.
- 이렇게 나누면 ① 여러 화면에서 같은 함수 재사용 ② 주소·방식이 바뀌어도 이 파일만 수정
  ③ 화면 코드가 깔끔해져요. (백엔드에서 뷰/시리얼라이저를 나눈 것과 같은 '관심사 분리')

## state-effect

React 컴포넌트는 **state(상태)** 가 바뀌면 화면을 다시 그려요.

- **`useState`** — 화면이 기억할 값. 예: `movies`(목록), `loading`(로딩 중?), `error`, 입력값.
  `const [movies, setMovies] = useState([])` → `setMovies(...)` 를 부르면 화면이 갱신돼요.
- **`useEffect(fn, [])`** — 컴포넌트가 **처음 그려질 때 한 번** 실행. 목록을 불러오기 딱 좋아요.
  `[]`(의존성 배열)가 비면 "최초 1회", `[id]` 면 "id가 바뀔 때마다"(상세 페이지에서 사용).
- **비동기 3종 세트** — `async/await` 로 응답을 기다리고,
  `try`(성공) / `catch`(에러 알림) / `finally`(로딩 끄기) 로 상태를 관리해요.
- **refetch** — 댓글을 쓴 뒤 `getMovie(id)` 를 다시 불러 목록을 갱신해요. (서버 데이터를 최신으로)

## 라우팅

`react-router-dom` 으로 **URL에 따라 다른 페이지**를 보여줘요. (새로고침 없이 화면만 교체 = SPA)

```jsx
<Routes>
  <Route path="/" element={<MovieListPage />} />          {/* 목록 */}
  <Route path="/movies/:id" element={<MovieDetailPage />} /> {/* 상세, :id는 변수 */}
  <Route path="/new" element={<MovieCreatePage />} />      {/* 작성 */}
</Routes>
```
- `:id` 는 URL 변수 — 상세 페이지에서 `useParams()` 로 꺼내 `getMovie(id)` 에 넘겨요.
- `<Link to="/movies/1">` = 새로고침 없이 이동, `useNavigate()` = 코드로 이동(등록 성공 후 상세로).

## cors

**한 줄 요약: 프론트(5173)와 백엔드(8000)는 포트가 달라 브라우저가 막는데, 백엔드가 헤더로 허락해줘야 통해요.**

- 출처(origin) = `프로토콜 + 호스트 + 포트`. 포트만 달라도(5173↔8000) "다른 출처"예요.
- 브라우저의 **동일 출처 정책(SOP)** 이 다른 출처 응답을 JS가 읽는 걸 막아요(보안).
- 그래서 **백엔드**가 응답에 `Access-Control-Allow-Origin: http://localhost:5173` 같은 헤더를 붙여
  "이 출처는 허용"이라고 알려줘야 해요. 이게 **CORS**. → 설정은 백엔드에 있어요.
- **프론트가 할 일**은 사실 거의 없어요. axios `withCredentials: true` (쿠키 포함)를 켜둔 것 정도.
  이건 백엔드 `CORS_ALLOW_CREDENTIALS = True` 와 짝이에요.
- POST/파일 업로드는 진짜 요청 전에 브라우저가 `OPTIONS`(프리플라이트)로 먼저 물어봐요.
  여기서 막히면 콘솔에 `CORS policy ... blocked` 가 떠요.

> ⚠️ 자주 하는 착각: "프론트 코드를 고쳐야 CORS가 풀린다" → **아니에요.** 대부분 **백엔드 설정**이에요.
> 백엔드 쪽 자세한 설명 → [../backend/CONCEPTS.md # CORS](../backend/CONCEPTS.md#cors)

## formdata

포스터 이미지를 보낼 땐 JSON이 아니라 **`FormData`** 를 써요.

```js
const form = new FormData();
form.append('user_id', 1);
form.append('title', '인터스텔라');
form.append('content', '인생영화');
form.append('poster', file);     // <input type="file"> 로 고른 File 객체
await formAxios.post('/movies', form);
```
- **왜 FormData?** JSON은 글자(텍스트)용이라 이미지 같은 바이너리를 못 담아요. FormData는
  텍스트 필드와 파일을 함께 `multipart/form-data` 로 보낼 수 있어요.
- **Content-Type을 직접 안 정해요.** FormData를 넘기면 브라우저가 `boundary` 를 붙여
  알아서 헤더를 만들어줘요. (그래서 `formAxios` 헤더는 참고용이고, 실제 boundary는 브라우저가 채움)
- **키 이름은 백엔드 필드명과 똑같이** — `title`·`content`·`poster`·`user_id`. 그래야 서버가 알아봐요.
- **미리보기**: `URL.createObjectURL(file)` 로 업로드 전에 화면에 이미지를 보여줄 수 있어요.

## env

- Vite는 `.env` 의 변수 중 **`VITE_` 로 시작하는 것만** `import.meta.env.VITE_XXX` 로 코드에 노출해요.
  (아무 변수나 노출하면 비밀값이 새니까, 접두사로 "이건 프론트에 내보내도 됨"을 표시)
- `VITE_API_BASE_URL=http://localhost:8000/api/v1` — 백엔드 주소. 배포 때 이 값만 바꾸면 돼요.
- ⚠️ `.env` 를 수정하면 개발 서버를 **재시작**해야 반영돼요. (Vite는 시작할 때 .env를 읽음)
- ⚠️ 프론트 `.env` 값은 빌드 결과에 그대로 박혀요. **진짜 비밀(API 키 등)은 절대 넣지 마세요.**
  (그런 건 백엔드가 다뤄야 해요)

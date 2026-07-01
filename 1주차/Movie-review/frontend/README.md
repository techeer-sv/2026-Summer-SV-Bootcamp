# 🎬 영화 게시판 프론트엔드 (React + Vite + Axios)

> **[backend](../backend) 실습에서 만든 REST API를 화면으로 이어받는 파트**예요.
> 백엔드에서 Swagger·curl로 두들겨보던 그 API(`/movies`, `/movies/{id}`, 댓글)를
> 이번엔 **진짜 웹 화면**에서 axios로 불러다 씁니다.
> "왜 이렇게 짰나"가 궁금하면 → **[CONCEPTS.md](CONCEPTS.md)** (Vite, axios 인스턴스, CORS, FormData…)

## 만들 결과물

| 경로 | 화면 | 이어받는 백엔드 API |
|---|---|---|
| `/` | **게시판 목록** — 포스터+제목 카드 | `GET /movies` |
| `/movies/:id` | **상세** — 리뷰 글 + 댓글, 댓글 작성 | `GET /movies/{id}` · `POST /movies/{id}/comments` |
| `/new` | **리뷰 작성** — 포스터 이미지 업로드 | `POST /movies` (multipart) |

> 백엔드에서 만든 화면 표(목록=이미지+제목 / 상세=전부+댓글)를 그대로 프론트로 옮긴 거예요.

## 📑 목차

[0. 실행](#0-실행--두-개를-켠다) · [1. 뼈대(main·index·vite)](#1-앱-뼈대--htmlmainvite) · [2. 라우팅(App.jsx)](#2-라우팅-appjsx--url이-페이지를-정한다) · [3. axios 설정](#3-axios-설정-srcconfigsaxiosconfigjs) · [4. API 함수](#4-api-함수-srcapimoviesapijs) · [5. 페이지](#5-페이지-srcpages) · [6. CORS](#6-cors--연동의-진짜-관문-) · [부록](#부록-a-자주-나는-문제)
→ 개념·"왜" 모음: **[CONCEPTS.md](CONCEPTS.md)**

## 📂 파일 구조

이 저장소는 **backend(Django) + frontend(React)** 가 함께 있는 모노레포예요.
아래는 **frontend/** 안쪽 구조입니다. (백엔드는 → [../backend](../backend))

```
django-board-handson/
├── backend/                     # Django REST API (1주차 실습)
└── frontend/                    # ← 지금 이 문서
    ├── .env                     #   VITE_API_BASE_URL (백엔드 주소)
    ├── index.html               #   진입 HTML (#root 하나)
    ├── vite.config.js           #   Vite 설정 (React 플러그인 · 5173 포트)
    └── src/
        ├── main.jsx             #   진입점 — BrowserRouter로 App 감쌈
        ├── App.jsx              #   라우팅 (목록 · 상세 · 작성) + 공통 헤더
        ├── index.css            #   스타일
        ├── configs/
        │   └── axios.config.js  #   jsonAxios · formAxios 인스턴스 ★
        ├── api/
        │   └── moviesApi.js     #   API 호출 함수 모음
        └── pages/
            ├── MovieListPage.jsx    # 게시판 목록
            ├── MovieDetailPage.jsx  # 상세 + 댓글
            └── MovieCreatePage.jsx  # 리뷰 작성
```
> 단계 제목 옆 `(파일명)` = 그 단계에서 만지는 파일.

## 🔭 전체 데이터 흐름 (한 장 요약)

```
[브라우저 화면]                 [코드 계층]                         [백엔드]
 MovieListPage  ──호출──▶  moviesApi.getMovies() ──▶ jsonAxios.get('/movies') ──▶ Django GET /movies
      ▲                                                                                   
      └────────────────── setMovies(응답) 로 화면 갱신 ◀── response.data (JSON 자동 파싱) ◀─────┘
```
페이지는 **API 함수만** 부르고, API 함수는 **axios 인스턴스**로 백엔드를 호출해요. (계층 분리)

---

# 0. 실행 — 두 개를 켠다

프론트는 **혼자 못 돌아요.** 데이터를 주는 백엔드가 먼저 떠 있어야 해요. 터미널 2개를 씁니다.

```bash
# ① 백엔드 (터미널 1) — ../backend
cd ../backend
source venv/bin/activate            # 윈도우: venv\Scripts\activate
pip install -r requirements.txt     # 최초 1회 (django-cors-headers 포함)
python manage.py migrate            # 최초 1회
python manage.py runserver          # → http://localhost:8000

# ② 프론트 (터미널 2) — frontend
cd ../frontend
npm install                         # 최초 1회 (node_modules 생성)
npm run dev                         # → http://localhost:5173
```

브라우저에서 **http://localhost:5173** 접속하면 게시판이 보여요.
> ⚠️ 백엔드가 꺼져 있으면 목록이 안 뜨고 콘솔에 `Network Error` 가 나요. **백엔드 먼저!**

**명령어 요약**

| 명령 | 하는 일 |
|---|---|
| `npm install` | `package.json` 의 라이브러리 설치 (최초 1회) |
| `npm run dev` | 개발 서버 실행(5173) — 코드 저장 시 즉시 반영(HMR) |
| `npm run build` | 배포용 정적 파일 생성 → `dist/` |
| `npm run preview` | 빌드 결과를 로컬에서 미리보기 |

---

# 1. 앱 뼈대 — HTML·main·Vite

리액트 앱은 **HTML 한 장 + JS 진입점 하나**로 시작해요. "어디에 그릴지 → 무엇을 그릴지" 순서예요.

## 1-1. `index.html` — 그릴 자리(#root) 하나

```html
<body>
  <div id="root"></div>                      <!-- 리액트가 이 안에 화면을 그린다 -->
  <script type="module" src="/src/main.jsx"></script>  <!-- 진입점 JS -->
</body>
```
- SPA(Single Page App)라 HTML은 이 한 장뿐. 나머지는 전부 JS가 그려요.

## 1-2. `src/main.jsx` — 진입점

```jsx
ReactDOM.createRoot(document.getElementById('root')).render(   // ① #root를 찾아
  <React.StrictMode>            // ② 개발용 경고 도우미(문제되는 패턴 알려줌)
    <BrowserRouter>             // ③ 라우팅 기능을 앱 전체에 켬 (URL ↔ 화면)
      <App />                   // ④ 실제 앱
    </BrowserRouter>
  </React.StrictMode>,
);
import './index.css';           // ⑤ 전역 스타일
```
- **①** `#root`(1-1의 그 자리)를 찾아 리액트를 붙여요.
- **③** `<BrowserRouter>` 로 감싸야 안쪽에서 `<Routes>`·`<Link>`·`useNavigate` 같은 라우팅 기능을 쓸 수 있어요. **그래서 App보다 바깥에 둬요.**

## 1-3. `vite.config.js` — 개발 서버 설정

```js
export default defineConfig({
  plugins: [react()],          // JSX/React를 Vite가 이해하게
  server: { port: 5173 },      // 개발 서버 포트 (백엔드 CORS 허용 주소와 일치!)
});
```
> 왜 Vite/npm/React인지 자세히 → [CONCEPTS.md # Vite·npm·React](CONCEPTS.md#vite-npm-react)

---

# 2. 라우팅 (`App.jsx`) — URL이 페이지를 정한다

`App.jsx` 는 **어떤 주소에서 어떤 페이지를 보여줄지** 지도를 그려요. + 모든 페이지 공통 헤더도 여기.

```jsx
function App() {
  return (
    <div className="app">
      <header className="header">
        <Link to="/" className="logo">🎬 Movie Review</Link>       {/* 로고 → 목록으로 */}
        <Link to="/new" className="btn btn-primary">+ 리뷰 작성</Link>  {/* → 작성 페이지 */}
      </header>

      <main className="container">
        <Routes>
          <Route path="/"            element={<MovieListPage />} />    {/* 목록(홈) */}
          <Route path="/movies/:id"  element={<MovieDetailPage />} />  {/* 상세, :id=변수 */}
          <Route path="/new"         element={<MovieCreatePage />} />  {/* 작성 */}
        </Routes>
      </main>
    </div>
  );
}
```
- **`<Routes>` / `<Route>`** : "이 `path` 면 이 `element`(페이지)를 그려라"는 매핑. URL이 바뀌면 **새로고침 없이** 화면만 교체돼요(SPA의 핵심).
- **`:id`** : URL 변수. `/movies/1`, `/movies/2` … 어떤 숫자든 매칭되고, 상세 페이지에서 `useParams()` 로 그 값을 꺼내요(→ 5-2).
- **`<Link to="...">`** : `<a>` 태그 대신 써요. 페이지 전체를 새로 받지 않고 **필요한 부분만** 바꿔서 빨라요.
- **헤더는 `<Routes>` 밖**에 있어서 어느 페이지를 가도 항상 보여요.

> 라우팅을 더 깊이(Link vs navigate, useParams) → [CONCEPTS.md # 라우팅](CONCEPTS.md#라우팅)

---

# 3. axios 설정 (`src/configs/axios.config.js`)

매 요청마다 기본 URL·헤더·타임아웃을 반복해서 쓰긴 번거로워요. 그래서 `axios.create()` 로
**공통 설정을 박은 '템플릿' 인스턴스**를 미리 만들어 재사용해요. 우리는 **두 개**를 만듭니다.

```js
const BASE_URL = import.meta.env.VITE_API_BASE_URL;   // .env → http://localhost:8000/api/v1

// ① 일반 JSON 요청용 (목록·상세·댓글)
export const jsonAxios = axios.create({
  baseURL: BASE_URL,                       // '/movies' 만 써도 앞에 자동으로 붙음
  timeout: 10000,                          // 10초 안에 응답 없으면 취소
  withCredentials: true,                   // 쿠키/인증정보 포함 (백엔드 CORS와 짝)
  headers: { 'Content-Type': 'application/json' },
});

// ② 파일 업로드용 (포스터 이미지) = a.k.a. formAxios
export const formAxios = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  withCredentials: true,
  headers: { 'Content-Type': 'multipart/form-data' },
});
```

| | `jsonAxios` | `formAxios` |
|---|---|---|
| Content-Type | `application/json` | `multipart/form-data` |
| 보내는 것 | 객체(→ 자동 JSON) | `FormData`(텍스트 + **파일**) |
| 쓰는 곳 | 목록·상세·댓글 | 영화 등록(포스터) |

- **`baseURL`** 덕분에 각 함수에선 `'/movies'` 처럼 **뒤쪽만** 쓰면 돼요. 주소가 바뀌면 `.env` 만 고침.
- **`withCredentials: true`** = 쿠키/인증정보 포함. 백엔드 `CORS_ALLOW_CREDENTIALS = True` 와 **한 쌍**(→ 6. CORS).
- **왜 둘로 나눴나** : 포스터는 이미지 **파일**이라 JSON에 못 실어요. 파일이 낄 땐 `multipart/form-data` 가 필요해서
  Content-Type이 다른 인스턴스를 따로 만든 거예요. (백엔드 `MovieView` 의 `MultiPartParser` 가 받는 짝)

> 더 깊이(왜 fetch 아닌 axios, 인스턴스 이점) → [CONCEPTS.md # axios 인스턴스](CONCEPTS.md#axios-인스턴스)

---

# 4. API 함수 (`src/api/moviesApi.js`)

컴포넌트가 axios를 **직접** 부르지 않고, 여기 정의한 **API 함수만** 부르게 분리했어요.
(URL·HTTP 방식은 여기 숨김 → 화면 코드가 깔끔해지고, 주소가 바뀌어도 이 파일만 고침)

```js
import { jsonAxios, formAxios } from '../configs/axios.config';

// 목록 (GET /movies) → 영화 배열
export const getMovies = async () => {
  const res = await jsonAxios.get('/movies');
  return res.data;                 // [{id, title, poster}, ...]  ← JSON 자동 파싱
};

// 상세 (GET /movies/{id}) → 영화 1건(+댓글)
export const getMovie = async (movieId) => {
  const res = await jsonAxios.get(`/movies/${movieId}`);
  return res.data;                 // {id, title, content, poster, comments:[...]}
};

// 등록 (POST /movies) — 포스터가 있어 FormData(multipart)로 보냄
export const postMovie = async ({ user_id, title, content, poster }) => {
  const form = new FormData();     // ① 파일+텍스트를 담는 상자
  form.append('user_id', user_id); // ② 키 이름 = 백엔드 필드명과 동일해야 함!
  form.append('title', title);
  form.append('content', content);
  if (poster) form.append('poster', poster);   // ③ File 객체 그대로
  const res = await formAxios.post('/movies', form);
  return res.data;                 // 생성된 영화
};

// 댓글 (POST /movies/{id}/comments)
export const postComment = async (movieId, { user_id, content }) => {
  const res = await jsonAxios.post(`/movies/${movieId}/comments`, { user_id, content });
  return res.data;                 // 생성된 댓글
};
```

| 함수 | 하는 일 | 백엔드 | 인스턴스 |
|---|---|---|---|
| `getMovies()` | 목록 조회 | `GET /movies` | jsonAxios |
| `getMovie(id)` | 상세(+댓글) | `GET /movies/{id}` | jsonAxios |
| `postMovie({...})` | 영화 등록 | `POST /movies` | **formAxios** |
| `postComment(id, {...})` | 댓글 작성 | `POST /movies/{id}/comments` | jsonAxios |

- **`res.data`** : axios가 JSON을 **자동 파싱**해줘서 바로 써요. (fetch면 `await res.json()` 을 직접 해야 함)
- **①②③ (postMovie)** : 이미지는 JSON에 못 담으니 `FormData` 에 담아요. 키 이름(`title`·`poster`…)은 백엔드 필드명과 **똑같이**.

> 왜 화면과 통신을 분리하나 → [CONCEPTS.md # API 계층](CONCEPTS.md#api-계층)

---

# 5. 페이지 (`src/pages/`)

세 페이지 모두 흐름이 비슷해요: **`useState`(값 기억) → `useEffect`(처음에 불러오기) → `async/await`(요청) → 화면 갱신.**

## 5-1. 목록 (`MovieListPage.jsx`) — 불러와서 그리기

```jsx
const [movies, setMovies]   = useState([]);    // 영화 목록
const [loading, setLoading] = useState(true);  // 로딩 중?
const [error, setError]     = useState(null);  // 에러 메시지

useEffect(() => {                              // ① 페이지가 처음 그려질 때 한 번
  const fetchMovies = async () => {
    try {
      setLoading(true);
      setMovies(await getMovies());            // ② API 함수 호출 → 성공하면 목록 저장
    } catch (e) {
      setError('목록을 불러오지 못했어요.');   // ③ 실패하면 에러 문구
    } finally {
      setLoading(false);                       // ④ 성공/실패 상관없이 로딩 끔
    }
  };
  fetchMovies();
}, []);                                        // ⑤ []=최초 1회만
```
```jsx
if (loading) return <p>불러오는 중...</p>;      // 상태에 따라 다른 화면
if (error)   return <p>{error}</p>;
return (
  <div className="grid">
    {movies.map((m) => (                        // ⑥ 배열 → 카드들로
      <Link to={`/movies/${m.id}`} key={m.id} className="card">
        {m.poster ? <img src={m.poster} /> : <div className="no-image">No Image</div>}
        <div className="card-title">{m.title}</div>
      </Link>
    ))}
  </div>
);
```
- **①·⑤ `useEffect(fn, [])`** : 컴포넌트가 처음 뜰 때 **딱 한 번** 실행 → 목록 불러오기에 딱.
- **②** `getMovies()`(4번의 그 함수)를 `await` 로 기다려요.
- **⑥ `.map()`** : 영화 배열을 카드 JSX 배열로 변환. `key` 는 리액트가 항목을 구분하는 표식(필수).
- 카드는 `<Link to={/movies/id}>` 라 누르면 **상세로 이동**해요.

## 5-2. 상세 (`MovieDetailPage.jsx`) — URL의 id로 조회 + 댓글

```jsx
const { id } = useParams();                    // ① URL의 :id (예: /movies/3 → "3")

const fetchMovie = async () => {               // 상세 불러오기 (재사용 위해 함수로)
  setMovie(await getMovie(id));
};
useEffect(() => { fetchMovie(); }, [id]);      // ② id가 바뀌면 다시 조회
```
```jsx
const handleSubmitComment = async (e) => {
  e.preventDefault();                          // ③ 폼 기본 새로고침 막기
  await postComment(id, { user_id: userId, content: commentText });  // ④ 댓글 전송
  setCommentText('');                          // ⑤ 입력창 비우기
  await fetchMovie();                          // ⑥ 다시 조회 = 방금 쓴 댓글 반영(refetch)
};
```
- **① `useParams()`** : `App.jsx` 의 `:id` 자리 값을 꺼내요. 이걸 `getMovie(id)` 에 넘겨 그 영화를 조회.
- **② 의존성 `[id]`** : id가 바뀌면(다른 상세로 이동) 자동으로 다시 불러와요.
- **③ `e.preventDefault()`** : `<form>` 은 제출 시 페이지를 새로고침하려 해요. SPA에선 막아야 해요.
- **⑥ refetch** : 댓글은 서버에 저장되니, 저장 후 **상세를 다시 불러와** 최신 댓글 목록을 화면에 반영해요.
- 상세 데이터 `movie.comments` 를 `.map()` 으로 댓글 리스트로 그려요.

## 5-3. 작성 (`MovieCreatePage.jsx`) — 포스터 업로드 + 이동

```jsx
const navigate = useNavigate();                // ① 코드로 페이지 이동시키는 함수

const handleFileChange = (e) => {              // 파일 선택 시
  const file = e.target.files[0];
  setPoster(file);                             // ② File 객체 저장
  setPreview(file ? URL.createObjectURL(file) : null);  // ③ 업로드 전 미리보기
};

const handleSubmit = async (e) => {
  e.preventDefault();
  const created = await postMovie({ user_id, title, content, poster });  // ④ FormData 전송
  navigate(`/movies/${created.id}`);           // ⑤ 성공 → 방금 만든 상세로 이동
};
```
- **② `<input type="file">`** 에서 고른 파일은 `e.target.files[0]`(File 객체). 이걸 `postMovie` 가 FormData에 담아 보내요(4번 ①②③).
- **③ `URL.createObjectURL(file)`** : 서버에 올리기 전에 브라우저에서 바로 미리보기 이미지를 만들어요.
- **① ⑤ `useNavigate()`** : `<Link>`(클릭 이동)와 달리 **코드에서** 이동시킬 때 써요. 등록 성공 후 상세로 보냄.
- 로딩 중엔 버튼을 `disabled` 로 막아 중복 제출을 방지해요.

> useState/useEffect·라우팅·FormData를 더 깊이 → [CONCEPTS.md](CONCEPTS.md#state-effect)

---

# 6. CORS — 연동의 진짜 관문 🌐

프론트(5173)와 백엔드(8000)는 **포트가 달라서** 브라우저가 요청을 막아요(동일 출처 정책).
이게 **백엔드 실습을 이어받을 때 처음 만나는 벽**이에요. 그래서 **백엔드**에
`django-cors-headers` 를 넣고 `http://localhost:5173` 을 허용 목록에 넣어뒀어요.

프론트 쪽 짝은 axios의 **`withCredentials: true`**(쿠키/인증정보 포함) —
백엔드의 `CORS_ALLOW_CREDENTIALS = True` 와 한 쌍이에요.

> ⚠️ 흔한 착각: "프론트 코드를 고쳐야 CORS가 풀린다" → 대부분 **백엔드 설정**이에요.
> CORS 동작 원리(프리플라이트까지) → [CONCEPTS.md # CORS](CONCEPTS.md#cors)
> 백엔드 설정 방법 → [../backend/CONCEPTS.md # CORS](../backend/CONCEPTS.md#cors)

---

# 부록 A. 자주 나는 문제

| 증상 | 해결 |
|---|---|
| 콘솔 `CORS policy ... blocked` | 백엔드 켜져 있는지 + `CORS_ALLOWED_ORIGINS` 에 5173 있는지 |
| 목록 안 뜸 / `Network Error` | 백엔드(8000) 실행 중인지, `.env` 의 `VITE_API_BASE_URL` 확인 |
| 포스터 이미지가 안 보임 | 응답 `poster` 가 전체 URL인지(백엔드 `context={"request": request}`) |
| `.env` 바꿨는데 반영 안 됨 | `npm run dev` **재시작** (Vite는 시작 시 .env를 읽음) |
| 등록/댓글이 400 | `user_id` 를 보냈는지 (인증 없어 폼에서 직접 입력, 기본값 1) |
| `npm run dev` 가 안 됨 | `npm install` 을 먼저 했는지 (node_modules 있는지) |

# 부록 B. 명령어 치트시트

```bash
npm install          # 라이브러리 설치 (최초 1회)
npm run dev          # 개발 서버 (http://localhost:5173)
npm run build        # 배포용 빌드 → dist/
npm run preview      # 빌드 결과 미리보기
```

> 인증 기능이 아직 없어, 작성자 `user_id` 는 폼에서 직접 입력해요. (기본값 1)
> 로그인을 붙이면 이 부분만 바꾸면 돼요 → 백엔드 [../backend/README.md](../backend/README.md) 4. 확장하기 참고.

---

> 📘 **개념·"왜"가 더 궁금하면 → [CONCEPTS.md](CONCEPTS.md)** (Vite·npm·React, axios 인스턴스, API 계층, useState/useEffect, 라우팅, CORS, FormData, .env)

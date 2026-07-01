// src/App.jsx — 라우팅 정의. URL에 따라 어떤 페이지를 보여줄지 매핑한다.
import { Routes, Route, Link } from 'react-router-dom';
import MovieListPage from './pages/MovieListPage';
import MovieDetailPage from './pages/MovieDetailPage';
import MovieCreatePage from './pages/MovieCreatePage';

function App() {
  return (
    <div className="app">
      {/* 상단 헤더 (모든 페이지 공통) */}
      <header className="header">
        <Link to="/" className="logo">🎬 Movie Review</Link>
        <Link to="/new" className="btn btn-primary">+ 리뷰 작성</Link>
      </header>

      <main className="container">
        <Routes>
          {/* 게시판 목록 (홈) */}
          <Route path="/" element={<MovieListPage />} />
          {/* 상세 페이지 — :id 자리에 영화 id가 들어온다 */}
          <Route path="/movies/:id" element={<MovieDetailPage />} />
          {/* 리뷰 작성 */}
          <Route path="/new" element={<MovieCreatePage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

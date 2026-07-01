// src/pages/MovieListPage.jsx — 게시판(영화 목록) 페이지.
// GET /movies 로 목록을 받아 카드 그리드로 보여준다. 카드를 누르면 상세로 이동.
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getMovies } from '../api/moviesApi';

function MovieListPage() {
  const [movies, setMovies] = useState([]); // 영화 목록
  const [loading, setLoading] = useState(true); // 로딩 중 여부
  const [error, setError] = useState(null); // 에러 메시지

  // 컴포넌트가 처음 그려질 때 한 번 목록을 불러온다.
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        const data = await getMovies();
        setMovies(data);
      } catch (err) {
        console.error('목록 조회 실패:', err);
        setError('목록을 불러오지 못했습니다. 백엔드가 켜져 있는지 확인하세요.');
      } finally {
        setLoading(false);
      }
    };
    fetchMovies();
  }, []);

  if (loading) return <p className="state">불러오는 중...</p>;
  if (error) return <p className="state state-error">{error}</p>;

  return (
    <div>
      <h1 className="page-title">영화 리뷰 게시판</h1>

      {movies.length === 0 ? (
        <p className="state">
          아직 등록된 리뷰가 없어요. 오른쪽 위 <b>+ 리뷰 작성</b>으로 첫 글을 남겨보세요!
        </p>
      ) : (
        <div className="grid">
          {movies.map((movie) => (
            <Link to={`/movies/${movie.id}`} key={movie.id} className="card">
              <div className="card-thumb">
                {movie.poster ? (
                  <img src={movie.poster} alt={movie.title} />
                ) : (
                  <div className="no-image">🎬<br />No Image</div>
                )}
              </div>
              <div className="card-title">{movie.title}</div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default MovieListPage;

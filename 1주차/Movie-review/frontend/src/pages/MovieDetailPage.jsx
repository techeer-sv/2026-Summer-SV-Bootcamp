// src/pages/MovieDetailPage.jsx — 상세 페이지.
// GET /movies/{id} 로 영화 1건(+댓글)을 받아 보여주고, 댓글도 작성할 수 있다.
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getMovie, postComment } from '../api/moviesApi';

function MovieDetailPage() {
  const { id } = useParams(); // URL의 :id (예: /movies/3 → id === "3")

  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 댓글 입력 상태
  const [commentText, setCommentText] = useState('');
  const [userId, setUserId] = useState('1'); // 인증이 없어 작성자 id를 직접 받는다
  const [submitting, setSubmitting] = useState(false);

  // 상세 데이터 불러오기 (재사용 위해 함수로 분리)
  const fetchMovie = async () => {
    try {
      setLoading(true);
      const data = await getMovie(id);
      setMovie(data);
    } catch (err) {
      console.error('상세 조회 실패:', err);
      setError('영화를 찾을 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovie();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // 댓글 작성
  const handleSubmitComment = async (e) => {
    e.preventDefault(); // 폼 기본 새로고침 막기
    if (!commentText.trim()) {
      alert('댓글 내용을 입력해주세요.');
      return;
    }
    try {
      setSubmitting(true);
      await postComment(id, { user_id: userId, content: commentText });
      setCommentText(''); // 입력창 비우기
      await fetchMovie(); // 목록 새로고침(refetch) → 방금 쓴 댓글 반영
    } catch (err) {
      console.error('댓글 작성 실패:', err);
      alert('댓글 작성에 실패했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <p className="state">불러오는 중...</p>;
  if (error) return <p className="state state-error">{error}</p>;
  if (!movie) return null;

  return (
    <div className="detail">
      <Link to="/" className="back-link">← 목록으로</Link>

      <div className="detail-head">
        <div className="detail-thumb">
          {movie.poster ? (
            <img src={movie.poster} alt={movie.title} />
          ) : (
            <div className="no-image">🎬<br />No Image</div>
          )}
        </div>
        <div className="detail-meta">
          <h1>{movie.title}</h1>
          <p className="detail-sub">작성자 #{movie.user_id}</p>
          <p className="detail-content">{movie.content}</p>
        </div>
      </div>

      {/* 댓글 영역 */}
      <section className="comments">
        <h2>댓글 {movie.comments?.length ?? 0}</h2>

        <form className="comment-form" onSubmit={handleSubmitComment}>
          <input
            className="input input-user"
            type="number"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="user_id"
            title="작성자 user_id (인증 없어 직접 입력)"
          />
          <input
            className="input"
            type="text"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="댓글을 입력하세요"
          />
          <button className="btn btn-primary" type="submit" disabled={submitting}>
            {submitting ? '등록 중...' : '등록'}
          </button>
        </form>

        <ul className="comment-list">
          {movie.comments?.length === 0 && (
            <li className="state">첫 댓글을 남겨보세요.</li>
          )}
          {movie.comments?.map((c) => (
            <li key={c.id} className="comment-item">
              <span className="comment-user">#{c.user_id}</span>
              <span className="comment-text">{c.content}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default MovieDetailPage;

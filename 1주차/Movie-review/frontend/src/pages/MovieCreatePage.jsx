// src/pages/MovieCreatePage.jsx — 리뷰 작성 페이지.
// POST /movies (multipart) 로 제목/내용/포스터를 보낸다. 성공하면 상세로 이동.
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postMovie } from '../api/moviesApi';

function MovieCreatePage() {
  const navigate = useNavigate();

  const [userId, setUserId] = useState('1'); // 작성자 (인증 없어 직접 입력)
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [poster, setPoster] = useState(null); // File 객체
  const [preview, setPreview] = useState(null); // 미리보기 URL
  const [loading, setLoading] = useState(false);

  // 파일 선택 시 File 저장 + 미리보기 생성
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setPoster(file || null);
    setPreview(file ? URL.createObjectURL(file) : null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      alert('제목과 내용을 입력해주세요.');
      return;
    }
    try {
      setLoading(true);
      const created = await postMovie({
        user_id: userId,
        title,
        content,
        poster,
      });
      // 생성된 영화의 상세로 이동
      navigate(`/movies/${created.id}`);
    } catch (err) {
      console.error('리뷰 작성 실패:', err);
      alert('리뷰 작성에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-page">
      <h1 className="page-title">리뷰 작성</h1>

      <form className="review-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>작성자 user_id</span>
          <input
            className="input"
            type="number"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </label>

        <label className="field">
          <span>영화 제목</span>
          <input
            className="input"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="예: 인터스텔라"
          />
        </label>

        <label className="field">
          <span>리뷰 내용</span>
          <textarea
            className="input textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="영화에 대한 감상을 적어주세요"
            rows={6}
          />
        </label>

        <label className="field">
          <span>포스터 이미지 (선택)</span>
          <input type="file" accept="image/*" onChange={handleFileChange} />
        </label>

        {preview && (
          <div className="preview">
            <img src={preview} alt="미리보기" />
          </div>
        )}

        <div className="form-actions">
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? '등록 중...' : '등록하기'}
          </button>
          <button
            className="btn"
            type="button"
            onClick={() => navigate('/')}
            disabled={loading}
          >
            취소
          </button>
        </div>
      </form>
    </div>
  );
}

export default MovieCreatePage;

// src/api/moviesApi.js
// ------------------------------------------------------------------
// 백엔드 영화 리뷰 API 호출 함수 모음.
// 컴포넌트는 이 함수들만 호출하면 되고, 실제 URL/HTTP 방식은 여기 숨긴다.
//
// 백엔드 엔드포인트 (base = http://localhost:8000/api/v1)
//   GET    /movies                     목록  [{id, title, poster}]
//   POST   /movies                     생성  (multipart: user_id,title,content,poster)
//   GET    /movies/{id}                상세  {..., comments:[...]}
//   POST   /movies/{id}/comments       댓글  {user_id, content}
// ------------------------------------------------------------------
import { jsonAxios, formAxios } from '../configs/axios.config';

/** 게시판 목록 조회 (GET /movies) → 영화 배열 */
export const getMovies = async () => {
  const response = await jsonAxios.get('/movies');
  return response.data; // [{id, title, poster}, ...]
};

/** 상세 조회 (GET /movies/{id}) → 영화 1건 (댓글 포함) */
export const getMovie = async (movieId) => {
  const response = await jsonAxios.get(`/movies/${movieId}`);
  return response.data; // {id, user_id, title, content, poster, comments:[...]}
};

/**
 * 영화(리뷰) 생성 (POST /movies)
 * - 포스터 이미지가 있어서 FormData(multipart)로 보낸다 → formAxios 사용
 * @param {{user_id:number|string, title:string, content:string, poster?:File}} data
 */
export const postMovie = async ({ user_id, title, content, poster }) => {
  if (!title || !content) {
    throw new Error('제목과 내용은 필수입니다.');
  }

  // FormData 에 필드를 담는다. (키 이름은 백엔드 필드명과 똑같이!)
  const formData = new FormData();
  formData.append('user_id', user_id);
  formData.append('title', title);
  formData.append('content', content);
  if (poster) {
    formData.append('poster', poster); // File 객체 그대로
  }

  const response = await formAxios.post('/movies', formData);
  return response.data; // 생성된 영화
};

/**
 * 댓글 작성 (POST /movies/{id}/comments)
 * @param {number|string} movieId
 * @param {{user_id:number|string, content:string}} data
 */
export const postComment = async (movieId, { user_id, content }) => {
  if (!content) {
    throw new Error('댓글 내용을 입력해주세요.');
  }
  const response = await jsonAxios.post(`/movies/${movieId}/comments`, {
    user_id,
    content,
  });
  return response.data; // 생성된 댓글
};

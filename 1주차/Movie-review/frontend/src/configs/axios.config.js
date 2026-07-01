// src/configs/axios.config.js
// ------------------------------------------------------------------
// Axios 인스턴스 두 개를 만들어 재사용한다. (axios.create = 공통설정 템플릿)
//   1) jsonAxios : 일반 JSON 요청용 (목록/상세 조회, 댓글 작성 등)
//   2) formAxios : 파일 업로드용 (영화 포스터 이미지 = multipart/form-data)
// 왜 나누나? 영화 등록은 이미지(poster)를 같이 보내야 해서 JSON이 아니라
// multipart/form-data 로 보내야 한다. Content-Type이 달라서 인스턴스를 분리한다.
// ------------------------------------------------------------------
import axios from 'axios';

// .env 의 VITE_API_BASE_URL (예: http://localhost:8000/api/v1)
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

/**
 * JSON 전송용 인스턴스
 * - GET/POST 로 JSON 데이터를 주고받을 때 사용
 * - 객체를 넘기면 Axios가 자동으로 JSON 문자열로 변환해 준다
 */
export const jsonAxios = axios.create({
  baseURL: BASE_URL,
  timeout: 10000, // 10초 안에 응답 없으면 취소
  withCredentials: true, // 쿠키/인증정보 포함 (백엔드 CORS_ALLOW_CREDENTIALS와 짝)
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 파일 업로드용 인스턴스 (a.k.a. formAxios)
 * - 포스터 이미지처럼 파일을 포함해 보낼 때 사용
 * - FormData 를 넘기면 브라우저가 알아서 boundary 를 붙여준다
 *   (그래서 Content-Type 을 직접 지정하지 않는다)
 */
export const formAxios = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

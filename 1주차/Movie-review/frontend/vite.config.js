import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite 설정 — React 플러그인만 켠다. 개발 서버는 기본 5173 포트로 뜬다.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
})

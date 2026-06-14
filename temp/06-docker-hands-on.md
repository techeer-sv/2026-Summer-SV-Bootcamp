# 6. 컨테이너 기술 (도커) — 핸즈온 실습

## 초급: Docker로 웹서버 실행 및 컨테이너 다뤄보기

**목표**: 이미지와 컨테이너의 차이를 직접 실행해보며 체감하고, 기본 명령어에 익숙해진다.

**진행 순서**
1. `docker --version`으로 설치 확인
2. `docker run -d -p 8080:80 nginx` 실행 후 브라우저에서 `localhost:8080` 접속
3. `docker ps`, `docker logs <container>`, `docker stop`, `docker rm` 실습
4. 같은 이미지를 포트를 바꿔(`8081`, `8082`) 여러 개 동시에 실행해보기
5. `docker exec -it <container> sh`로 컨테이너 내부에 들어가 파일 구조 살펴보기
6. `docker images`, `docker rmi`로 이미지 정리

**결과물**
- 동시에 실행 중인 컨테이너 2개 이상의 `docker ps` 결과 캡처
- 컨테이너 내부에서 확인한 파일 구조 메모

---

## 고급: 내가 만든 앱 Dockerize + docker-compose 통합 실행

**목표**: 직접 만든 백엔드 앱을 이미지로 빌드하고, DB와 함께 docker-compose로 한 번에 띄운다.

**진행 순서**
1. (세션 5에서 만든) 백엔드 프로젝트에 `Dockerfile` 작성 (multi-stage build로 빌드/런타임 분리)
2. `docker build`로 이미지 빌드 후 단독 컨테이너 실행 테스트
3. Postgres/MySQL 컨테이너 추가
4. `docker-compose.yml` 작성 (app + db, 필요시 frontend 포함)
5. `.env` 파일로 DB 접속 정보 등 환경변수 분리
6. volume을 적용해 DB 데이터가 컨테이너 재시작 후에도 유지되는지 확인
7. 일반 base 이미지 vs alpine 기반 multi-stage 빌드의 이미지 크기 비교

**결과물**
- `docker-compose up` 한 줄로 앱+DB가 함께 뜨는 프로젝트
- 이미지 크기 비교 결과 (`docker images` 캡처)

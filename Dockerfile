# 1. Python 3.9.7 기반 이미지 사용
FROM python:3.9.7-slim-buster

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치를 위한 파일 복사
COPY requirements.txt .

# 4. 의존성 설치 (캐시 최소화)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. 애플리케이션 코드 복사
COPY . .

# 6. 컨테이너 실행 시 FastAPI 서버 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
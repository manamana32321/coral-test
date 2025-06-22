# 1. 베이스 이미지 선택 (arm64v8 아키텍처의 파이썬 3.12 이미지)
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt 복사 및 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 소스 코드 복사
COPY . .

# 5. 컨테이너가 시작될 때 실행할 명령어
CMD ["python", "pir_exporter.py"]
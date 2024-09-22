# 베이스 이미지 설정 (Python 3.9 사용)
FROM python:3.10.2-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y gcc

# Python 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Django 프로젝트 파일 전체 복사
COPY . .

# 환경 변수 설정 (예: Django의 환경 설정)
ENV PYTHONUNBUFFERED 1

# 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

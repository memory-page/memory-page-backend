#!/bin/bash

# 스크립트 종료 조건 설정 (에러 발생 시 종료)
set -e

echo "------------------------"
echo "$(date): 배포 시작"

# 기존 실행 중인 Gunicorn 프로세스 종료
echo "기존 웹 서버 프로세스를 종료합니다..."
pkill -f "gunicorn-main" || echo "기존 프로세스가 실행 중이 아닙니다."

# 새로운 Gunicorn 서버 실행
echo "새로운 웹 서버를 시작합니다..."

/home/hadoop/anaconda3/bin/poetry install --no-root
/home/hadoop/anaconda3/bin/poetry run gunicorn app.main:app \
    --name "gunicorn-main" \
    -w 7 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:5013 \
    --access-logfile ./gunicorn-access.log \
    --error-logfile ./gunicorn-error.log \
    --capture-output \
    --log-level info \
    --daemon

# 서버 실행 성공 여부 확인
sleep 5
if pgrep -f "gunicorn-main" > /dev/null; then
    echo "웹 서버가 성공적으로 실행되었습니다."
else
    echo "웹 서버 실행 실패. 로그를 확인하세요."
    exit 1
fi

echo "$(date): 배포 완료"
echo "------------------------"

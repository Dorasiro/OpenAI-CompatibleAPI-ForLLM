FROM ubuntu:24.04

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    curl \
    git \
    vim

WORKDIR /app

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone

# Python ライブラリ
RUN pip3 install --break-system-packages fastapi uvicorn requests

# アプリ本体
#COPY app.py /app/app.py

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
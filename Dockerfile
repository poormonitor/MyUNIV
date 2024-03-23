FROM python:3.11-slim

ARG CN="N"
ARG CN_MIRROR="mirrors.bfsu.edu.cn"

RUN [ "$CN" != "N" ] &&  \
    pip config set global.index-url "https://${CN_MIRROR}/pypi/web/simple" || true

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app
VOLUME /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "2", "--port", "8000"]

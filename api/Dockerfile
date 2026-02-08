FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN git init

EXPOSE 8000

CMD ["sh", "-c", "dvc repro && uvicorn app:app --host 0.0.0.0 --port 8000"]
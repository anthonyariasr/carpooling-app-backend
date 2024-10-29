FROM python:3.12.5-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt


CMD ["uvicorn", "app.app:app","--reload", "--host", "0.0.0.0", "--port", "8000"]
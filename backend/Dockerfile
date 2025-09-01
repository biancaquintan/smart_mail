FROM python:3.11-slim
WORKDIR /app

# dependências do sistema (compilar libs do sklearn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# baixar stopwords do NLTK
RUN python -m nltk.downloader stopwords

COPY . /app

# copiar o modelo treinado (caso já exista no repositório)
COPY models/model.joblib /models/model.joblib

ENV MODEL_PATH=/models/model.joblib

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Pre-download the ML model to save 30-60 seconds on every container start
RUN python -c "from transformers import pipeline; pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')"

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

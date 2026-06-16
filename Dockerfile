FROM python:3.11-slim

WORKDIR /app
COPY demo/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Install the quira library from source since it's a monorepo
COPY pyproject.toml .
COPY README.md .
COPY quira ./quira
RUN pip install -e .

COPY demo/backend ./demo/backend

CMD ["uvicorn", "demo.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

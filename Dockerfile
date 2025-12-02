FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry==2.2.1 && \
  poetry config virtualenvs.create false && \
  poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
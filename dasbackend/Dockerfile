FROM python:3.11-slim

WORKDIR /app
COPY ./src ./src

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --without dev

COPY src/ /app/app

EXPOSE 4200

# Run FastAPI
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "4200", "--reload"]


FROM python:3.12-bullseye

WORKDIR /workspace/

# poetryをpackage-modeで使っているため、README.mdがないとpoetry installに失敗する
COPY pyproject.toml poetry.lock README.md .env /workspace/
COPY src/ /workspace/src/
COPY data/ /workspace/data/
COPY rag/ /workspace/rag/
COPY lib/ /workspace/lib/

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/root/.local" \
    PYTHONUNBUFFERED=1
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV STREAMLIT_SERVER_HEADLESS true

# 必要なライブラリをすべてインストール
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install

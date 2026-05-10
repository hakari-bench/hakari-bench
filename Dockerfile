FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

WORKDIR /app

ENV PATH="/opt/venv/bin:${PATH}" \
    PORT=7860 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    HAKARI_BENCH_VIEWER_DATA_DIR=/data/viewer \
    HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID=hakari-bench/leaderboard_database \
    HAKARI_BENCH_VIEWER_HF_DATASET_PATH=duckdb/hakari_bench.duckdb

COPY pyproject.toml uv.lock README.md ./
COPY hakari_bench ./hakari_bench
COPY config ./config

RUN uv venv /opt/venv \
    && uv pip install --python /opt/venv/bin/python --no-deps -e . \
    && uv pip install --python /opt/venv/bin/python \
        "duckdb>=1.5.2" \
        "fastapi>=0.136.1" \
        "huggingface-hub>=1.12.0" \
        "pydantic>=2.13.3" \
        "pyyaml>=6.0.3" \
        "uvicorn[standard]>=0.46.0"

EXPOSE 7860

CMD ["sh", "-c", "uvicorn hakari_bench.viewer.space:create_space_app --factory --host 0.0.0.0 --port ${PORT:-7860}"]

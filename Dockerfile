# syntax=docker/dockerfile:1.7
FROM python:3.12-slim@sha256:bf73779de6dbd030f3d189eeeb246286965832761ace318c1518300f76c0840d

COPY --from=ghcr.io/astral-sh/uv:0.9.18@sha256:1f2af0857cdeac11a70fd1cea66c5b06bcdac804ea4147690816468f5bf9cea2 /uv /uvx /bin/

WORKDIR /app

ENV PATH="/opt/venv/bin:${PATH}" \
    PORT=7860 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    HAKARI_BENCH_VIEWER_DATA_DIR=/data/viewer \
    HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID=hakari-bench/leaderboard_database \
    HAKARI_BENCH_VIEWER_HF_DATASET_PATH=duckdb/hakari_bench.duckdb

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv \
    && uv pip install --python /opt/venv/bin/python \
        "duckdb>=1.5.2" \
        "fastapi>=0.136.1" \
        "huggingface-hub>=1.12.0" \
        "pydantic>=2.13.3" \
        "pyyaml>=6.0.3" \
        "uvicorn[standard]>=0.46.0"

COPY pyproject.toml uv.lock README.md ./
COPY hakari_bench ./hakari_bench
COPY config ./config
COPY task_docs ./task_docs

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /opt/venv/bin/python --no-deps -e .

RUN useradd --create-home --shell /usr/sbin/nologin hakari \
    && mkdir -p /data/viewer \
    && chown -R hakari:hakari /app /data/viewer /opt/venv

EXPOSE 7860

USER hakari

CMD ["sh", "-c", "uvicorn hakari_bench.viewer.space:create_space_app --factory --host 0.0.0.0 --port ${PORT:-7860}"]

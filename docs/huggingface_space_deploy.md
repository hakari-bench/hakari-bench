# Hugging Face Space Deployment

This document describes how to deploy the HAKARI-Bench leaderboard viewer to
the Docker Space at `hakari-bench/leaderboard` and how to publish the DuckDB
database consumed by that Space.

## Repositories

- Space: `hakari-bench/leaderboard`
- Space URL: `https://hakari-bench-leaderboard.hf.space/`
- Source repository: `https://github.com/hakari-bench/hakari-bench`
- GHCR image: `ghcr.io/hakari-bench/hakari-bench-leaderboard:hf-space-docker-latest`
- DuckDB dataset: `hakari-bench/leaderboard_database`
- DuckDB path in dataset: `duckdb/hakari_bench.duckdb`

The Space repo is intentionally minimal. The viewer application is built in
GitHub Actions, published to GHCR, and referenced from the Space `Dockerfile`.
The running container downloads the DuckDB file dynamically from the dataset
repo and caches it at `/data/viewer/hakari_bench.duckdb`.

## Required Permissions

The Hugging Face token or local git credential used for deployment must be able
to read and write repos under the `hakari-bench` organization, including force
pushing to `hakari-bench/leaderboard`. The token used for publishing the DuckDB
dataset must also be able to create or update
`hakari-bench/leaderboard_database`.

Verify Hugging Face authentication locally:

```bash
uv run --group viewer python - <<'PY'
from huggingface_hub import HfApi

print(HfApi().whoami())
PY
```

The GitHub Actions workflow publishes the Docker image with `GITHUB_TOKEN`, so
the workflow needs `packages: write`. The GHCR package must be public so
Hugging Face can pull the image without registry credentials.

## Publish the Viewer Image

The source repository builds and publishes the viewer image from the
`hf-space-docker` branch via `.github/workflows/build-leaderboard-image.yml`.
The workflow runs on manual dispatch and on pushes to `hf-space-docker` that
change viewer image inputs.

The workflow runs `uv run tox` before building the Docker image. After
validation passes, it builds the image, runs a container import smoke test, and
pushes one rolling tag:

```text
ghcr.io/hakari-bench/hakari-bench-leaderboard:hf-space-docker-latest
```

After a successful workflow run, confirm the image is anonymously pullable:

```bash
docker manifest inspect ghcr.io/hakari-bench/hakari-bench-leaderboard:hf-space-docker-latest
```

If a pinned or experimental revision is needed, publish a separate GHCR tag and
set the Space variable `HAKARI_BENCH_LEADERBOARD_IMAGE_TAG` to that tag before
rebuilding the Space. Normal production operation leaves the variable unset or
sets it to `hf-space-docker-latest`.

## Deploy or Rebuild the Space Repo

Deploy the Space by replacing its `main` branch with a minimal git commit. This
keeps local virtual environments, test files, generated outputs, and benchmark
source files out of the Space repo.

Create a temporary clone:

```bash
SPACE_WORKDIR=/tmp/hakari-bench-leaderboard-space
rm -rf "$SPACE_WORKDIR"
git clone https://huggingface.co/spaces/hakari-bench/leaderboard "$SPACE_WORKDIR"
cd "$SPACE_WORKDIR"
```

For a first migration or full reset, create an orphan branch:

```bash
git switch --orphan prebuilt-image-deploy
git rm -rf .
```

Create the Space metadata:

```bash
cat > README.md <<'EOF'
---
title: HAKARI-Bench Leaderboard
emoji: 📊
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
fullWidth: true
short_description: HAKARI-Bench retrieval leaderboard
---

# HAKARI-Bench Leaderboard

This Space hosts the public leaderboard for HAKARI-Bench, a Nano-style information retrieval benchmark suite for SentenceTransformers-compatible dense, sparse, reranker, late-interaction, and BM25 systems.

The leaderboard viewer runs from a prebuilt Docker image published by the HAKARI-Bench GitHub repository:

- Project repository: https://github.com/hakari-bench/hakari-bench
- Leaderboard database: https://huggingface.co/datasets/hakari-bench/leaderboard_database

The app downloads the current DuckDB leaderboard database at startup and serves the interactive benchmark tables, model comparisons, task documentation, and filtering views from that database.
EOF
```

Create the Space Dockerfile:

```bash
cat > Dockerfile <<'EOF'
ARG HAKARI_BENCH_LEADERBOARD_IMAGE_TAG=hf-space-docker-latest
FROM ghcr.io/hakari-bench/hakari-bench-leaderboard:${HAKARI_BENCH_LEADERBOARD_IMAGE_TAG}
EOF
```

Create a small ignore file:

```bash
cat > .gitignore <<'EOF'
.DS_Store
*.swp
EOF
```

Force push the minimal commit:

```bash
git add README.md Dockerfile .gitignore
git commit -m "Deploy prebuilt Docker leaderboard image"
git push -f origin HEAD:main
```

When the Space repo is already minimal and only the rolling GHCR tag changed,
trigger a rebuild with an empty commit:

```bash
git clone https://huggingface.co/spaces/hakari-bench/leaderboard /tmp/hakari-bench-leaderboard-space
cd /tmp/hakari-bench-leaderboard-space
git commit --allow-empty -m "Rebuild prebuilt Docker leaderboard image"
git push origin HEAD:main
```

## Space Image Tag Variable

The Space Dockerfile defaults to `hf-space-docker-latest`:

```dockerfile
ARG HAKARI_BENCH_LEADERBOARD_IMAGE_TAG=hf-space-docker-latest
FROM ghcr.io/hakari-bench/hakari-bench-leaderboard:${HAKARI_BENCH_LEADERBOARD_IMAGE_TAG}
```

Hugging Face Docker Spaces expose Space variables as Docker build args. Set
`HAKARI_BENCH_LEADERBOARD_IMAGE_TAG` in the Space settings when the Space should
pull a tag other than `hf-space-docker-latest`, then restart or rebuild the
Space.

## Publish the DuckDB Database

Choose the viewer DuckDB file to publish. For example:

```bash
export DUCKDB_PATH=/home/hotchpotch/src/github.com/hakari-bench/hakari-bench-wt/recreate_nano_datasets/output/viewer_combined_20260510_1340/hakari_bench.duckdb
```

Upload it to the dataset repo:

```bash
uv run --group viewer python - <<'PY'
import os
from pathlib import Path
from huggingface_hub import HfApi

duckdb_path = Path(os.environ["DUCKDB_PATH"])
api = HfApi()
api.create_repo(
    repo_id="hakari-bench/leaderboard_database",
    repo_type="dataset",
    exist_ok=True,
    private=False,
)
info = api.upload_file(
    repo_id="hakari-bench/leaderboard_database",
    repo_type="dataset",
    path_or_fileobj=str(duckdb_path),
    path_in_repo="duckdb/hakari_bench.duckdb",
    commit_message="Update leaderboard DuckDB",
)
print(info)
PY
```

Verify the uploaded file can be downloaded:

```bash
uv run --group viewer python - <<'PY'
from hakari_bench.viewer.store import HuggingFaceDuckDbSource, _download_hf_duckdb

path = _download_hf_duckdb(
    HuggingFaceDuckDbSource(
        repo_id="hakari-bench/leaderboard_database",
        filename="duckdb/hakari_bench.duckdb",
    )
)
print(path)
print(path.exists(), path.stat().st_size)
PY
```

## Runtime Configuration

The viewer image sets these defaults:

```text
HAKARI_BENCH_VIEWER_DATA_DIR=/data/viewer
HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID=hakari-bench/leaderboard_database
HAKARI_BENCH_VIEWER_HF_DATASET_PATH=duckdb/hakari_bench.duckdb
```

When the viewer uses the Hugging Face dataset source, it checks/downloads the
DuckDB source at startup and then caches the source check for 10 minutes per
running process. Requests served within that window use the already-local
`/data/viewer/hakari_bench.duckdb` file and do not call `hf_hub_download()`.
Remote DuckDB downloads are first synchronized into a shared remote latest cache
(`~/.cache/hakari-bench/duckdb/remote_latest_hakari_bench.duckdb` by default)
using Hugging Face file metadata and a sidecar SHA-1 to avoid repeated downloads
or local copies when the content has not changed.

The same viewer can be pointed at a different source locally or in a Space with:

- `HAKARI_BENCH_VIEWER_DUCKDB_PATH`
- `HAKARI_BENCH_VIEWER_SOURCE_DUCKDB_PATH`
- `HAKARI_BENCH_VIEWER_SOURCE_RESULTS_DIR`
- `HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID`
- `HAKARI_BENCH_VIEWER_HF_DATASET_PATH`
- `HAKARI_BENCH_VIEWER_HF_DATASET_REVISION`
- `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_PATH`
- `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_METADATA_PATH`
- `HAKARI_BENCH_VIEWER_FRAME_ANCESTORS`

The viewer also adds response security headers at runtime, including a
Content-Security-Policy. The default `frame-ancestors` allows Hugging Face
embedding hosts:

```text
https://huggingface.co https://*.huggingface.co
```

## Verification

Wait for the deployed Space commit to become `RUNNING`:

```bash
uv run --group viewer python - <<'PY'
import time
from huggingface_hub import HfApi

api = HfApi()
target_sha = "REPLACE_WITH_SPACE_COMMIT_SHA"
for _ in range(30):
    runtime = api.get_space_runtime("hakari-bench/leaderboard")
    sha = runtime.raw.get("sha") if runtime.raw else None
    print(runtime.stage, sha, flush=True)
    if runtime.stage == "RUNNING" and sha == target_sha:
        break
    time.sleep(5)
PY
```

Check the public endpoints:

```bash
curl -L -sS https://hakari-bench-leaderboard.hf.space/ | rg "HAKARI-bench leaderboard|/assets/app.css|/assets/viewer.js|/assets/favicon.png|/assets/htmx.min.js"
curl -L -sS 'https://hakari-bench-leaderboard.hf.space/leaderboard?view=All' | rg "Retrieval|NanoMMTEB-v2|Task facets"
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/favicon.png -o /tmp/hakari_favicon.png
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/app.css -o /tmp/hakari_app.css
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/viewer.js -o /tmp/hakari_viewer.js
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/htmx.min.js -o /tmp/hakari_htmx.min.js
```

Check Space logs if the app is not serving traffic:

```bash
uv run hf spaces logs hakari-bench/leaderboard -n 100
uv run hf spaces logs hakari-bench/leaderboard --build -n 100
```

Before considering a source repo change complete, run local validation:

```bash
uv run tox
```

The viewer also has a Playwright-backed browser smoke test:

```bash
uv run playwright install chromium
uv run --group all pytest -q tests/test_viewer_browser.py
```

## Rollback

For viewer code rollback, publish or select a known-good GHCR tag and set
`HAKARI_BENCH_LEADERBOARD_IMAGE_TAG` in the Space settings, then rebuild the
Space. For the normal rolling tag, reverting the source branch and rerunning the
image workflow updates `hf-space-docker-latest`.

For database rollback, restore `duckdb/hakari_bench.duckdb` in
`hakari-bench/leaderboard_database` from a known-good dataset commit.

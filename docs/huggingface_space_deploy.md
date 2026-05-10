# Hugging Face Space Deployment

This document describes how to deploy the HAKARI-Bench leaderboard viewer to
the Docker Space at `hakari-bench/leaderboard` and how to publish the DuckDB
database consumed by that Space.

## Repositories

- Space: `hakari-bench/leaderboard`
- DuckDB dataset: `hakari-bench/leaderboard_database`
- DuckDB path in dataset: `duckdb/hakari_bench.duckdb`
- Public Space URL: `https://hakari-bench-leaderboard.hf.space/`

The Space runs the FastAPI viewer from `hakari_bench.viewer.space:create_space_app`
and downloads the DuckDB file dynamically from the dataset repo. The database is
cached inside the Space at `/data/viewer/hakari_bench.duckdb`.

## Required Permissions

The Hugging Face token used for deployment must be able to:

- Read and write repos under the `hakari-bench` organization.
- Create or update a dataset repo for `hakari-bench/leaderboard_database`.
- Create or update a Docker Space for `hakari-bench/leaderboard`.
- Change Space visibility if the Space needs to be public.
- Read the DuckDB dataset from the running Space. Public datasets work without a
  Space secret; private datasets require an `HF_TOKEN` Space secret.

The current deployment was performed with an authenticated Hugging Face account
that is an admin of the `hakari-bench` organization and has fine-grained
permissions including organization read/write, repo access read, repo content
read, and repo write for `hakari-bench`.

Verify authentication locally:

```bash
uv run --group viewer python - <<'PY'
from huggingface_hub import HfApi

print(HfApi().whoami())
PY
```

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

## Deploy the Docker Space

The Space uses:

- `Dockerfile`
- `.dockerignore`
- `README.md` Space metadata with `sdk: docker`
- `hakari_bench/viewer/space.py`
- `hakari_bench/viewer/assets/` for local CSS, HTMX, and favicon assets

The Docker image installs only viewer runtime dependencies and starts:

```bash
uvicorn hakari_bench.viewer.space:create_space_app --factory --host 0.0.0.0 --port ${PORT:-7860}
```

The viewer does not depend on CDN-hosted browser assets. Regenerate the local
Tailwind CSS before deploying when viewer templates or styles change:

```bash
npx --yes tailwindcss@3.4.17 \
  -i hakari_bench/viewer/assets/app.tailwind.css \
  -o hakari_bench/viewer/assets/app.css \
  --content 'hakari_bench/viewer/**/*.py,tests/**/*.py' \
  --minify
```

Upload the current workspace to the Space:

```bash
uv run --group viewer python - <<'PY'
from pathlib import Path
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(
    repo_id="hakari-bench/leaderboard",
    repo_type="space",
    space_sdk="docker",
    exist_ok=True,
    private=False,
)
info = api.upload_folder(
    repo_id="hakari-bench/leaderboard",
    repo_type="space",
    folder_path=Path("."),
    commit_message="Deploy Docker leaderboard viewer",
    ignore_patterns=[
        ".git",
        ".git/**",
        ".venv/**",
        "__pycache__/**",
        ".pytest_cache/**",
        ".ruff_cache/**",
        ".tox/**",
        "output/**",
        "tmp/**",
    ],
    delete_patterns=[
        "output/**",
        "tmp/**",
    ],
)
print(info)
PY
```

If the Space was created private or needs public access, update visibility:

```bash
uv run hf repos settings hakari-bench/leaderboard --repo-type space --public
```

## Runtime Configuration

The Dockerfile sets these defaults:

```text
HAKARI_BENCH_VIEWER_DATA_DIR=/data/viewer
HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID=hakari-bench/leaderboard_database
HAKARI_BENCH_VIEWER_HF_DATASET_PATH=duckdb/hakari_bench.duckdb
```

The same viewer can be pointed at a different source locally or in a Space with:

- `HAKARI_BENCH_VIEWER_DUCKDB_PATH`
- `HAKARI_BENCH_VIEWER_SOURCE_DUCKDB_PATH`
- `HAKARI_BENCH_VIEWER_SOURCE_RESULTS_DIR`
- `HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID`
- `HAKARI_BENCH_VIEWER_HF_DATASET_PATH`
- `HAKARI_BENCH_VIEWER_HF_DATASET_REVISION`

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
curl -L -sS https://hakari-bench-leaderboard.hf.space/ | rg "HAKARI-bench leaderboard|/assets/app.css|/assets/favicon.svg|/assets/htmx.min.js"
curl -L -sS 'https://hakari-bench-leaderboard.hf.space/leaderboard?view=Overall' | rg "Core benchmarks|NanoMMTEB-v2|Language pages"
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/favicon.svg -o /tmp/hakari_favicon.svg
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/app.css -o /tmp/hakari_app.css
curl -L -sS -D - https://hakari-bench-leaderboard.hf.space/assets/htmx.min.js -o /tmp/hakari_htmx.min.js
```

Check logs if the Space is not serving traffic:

```bash
uv run hf spaces logs hakari-bench/leaderboard -n 100
uv run hf spaces logs hakari-bench/leaderboard --build -n 100
```

Before considering a deploy complete, run local validation:

```bash
uv run tox
```

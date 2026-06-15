"""Build the leaderboard viewer stylesheet from its Tailwind source.

`hakari_bench/viewer/assets/app.css` is a compiled, minified Tailwind v3 output
and must never be hand-edited. Edit the source
`hakari_bench/viewer/assets/app.tailwind.css` and regenerate with this script::

    uv run python scripts/build_viewer_css.py            # rebuild app.css
    uv run python scripts/build_viewer_css.py --watch     # rebuild on change
    uv run python scripts/build_viewer_css.py --check      # CI: verify in sync

The Tailwind version is pinned so rebuilds stay byte-stable; only real CSS
changes show up in the diff. Requires Node's ``npx`` on PATH (no package.json or
local node_modules is needed -- npx fetches the pinned CLI on demand).
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# Pin Tailwind so the compiled output is reproducible across machines. Bumping
# this is a deliberate change: rebuild and commit app.css in the same change.
TAILWIND_VERSION = "3.4.17"

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = REPO_ROOT / "tailwind.config.js"
SOURCE = REPO_ROOT / "hakari_bench" / "viewer" / "assets" / "app.tailwind.css"
OUTPUT = REPO_ROOT / "hakari_bench" / "viewer" / "assets" / "app.css"


def _tailwind_command(output: Path, *, watch: bool) -> list[str]:
    command = [
        "npx",
        "--yes",
        f"tailwindcss@{TAILWIND_VERSION}",
        "--config",
        str(CONFIG),
        "--input",
        str(SOURCE),
        "--output",
        str(output),
        "--minify",
    ]
    if watch:
        command.append("--watch")
    return command


def _run_tailwind(output: Path, *, watch: bool = False) -> None:
    if shutil.which("npx") is None:
        raise SystemExit(
            "error: `npx` was not found on PATH. Install Node.js (which provides npx) "
            "to build the viewer CSS."
        )
    subprocess.run(_tailwind_command(output, watch=watch), cwd=REPO_ROOT, check=True)


def _build() -> None:
    _run_tailwind(OUTPUT)
    print(f"Built {OUTPUT.relative_to(REPO_ROOT)} from {SOURCE.relative_to(REPO_ROOT)}.")


def _watch() -> None:
    print("Watching app.tailwind.css for changes (Ctrl-C to stop)...")
    _run_tailwind(OUTPUT, watch=True)


def _check() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / "app.css"
        _run_tailwind(candidate)
        built = candidate.read_text(encoding="utf-8")
    committed = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else ""
    if built == committed:
        print("app.css is in sync with app.tailwind.css.")
        return 0
    print(
        "error: app.css is out of date. Run `uv run python scripts/build_viewer_css.py` "
        "and commit the result.",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--watch", action="store_true", help="Rebuild continuously when the source changes.")
    group.add_argument("--check", action="store_true", help="Verify app.css matches the source without writing it.")
    args = parser.parse_args()

    if args.check:
        return _check()
    if args.watch:
        _watch()
        return 0
    _build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

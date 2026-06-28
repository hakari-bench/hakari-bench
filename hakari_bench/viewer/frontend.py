"""Serve the compiled React frontend (viewer-frontend/dist) from FastAPI.

In production the React app is built to ``viewer-frontend/dist`` with a ``/static``
base. This module mounts those assets and serves ``index.html`` for the SPA entry
routes (``/`` and ``/docs``), taking precedence over the legacy htmx HTML routes
while leaving the JSON ``/api`` endpoints untouched.
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi.responses import FileResponse


def _spa_content_security_policy(frame_ancestors: str) -> str:
    # The built index.html keeps a tiny inline theme-init script, so script-src
    # needs 'unsafe-inline'. Everything else is same-origin (/static, /api).
    return "; ".join(
        [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data:",
            "connect-src 'self'",
            "object-src 'none'",
            "frame-src 'none'",
            "form-action 'self'",
            "base-uri 'none'",
            f"frame-ancestors {frame_ancestors}",
        ]
    )


def resolve_frontend_dist(frontend_dist: Path | None) -> Path | None:
    if frontend_dist is not None:
        return frontend_dist
    env_value = os.environ.get("HAKARI_VIEWER_FRONTEND_DIST")
    if env_value:
        return Path(env_value)
    return Path("viewer-frontend/dist")


def mount_frontend(app, dist_dir: Path, *, frame_ancestors: str) -> bool:
    """Mount the built SPA. Returns True when a build was found and mounted."""

    from starlette.routing import Route
    from starlette.staticfiles import StaticFiles

    index_path = dist_dir / "index.html"
    if not index_path.is_file():
        return False

    app.mount("/static", StaticFiles(directory=dist_dir), name="frontend-static")
    csp = _spa_content_security_policy(frame_ancestors)

    async def spa_index(_request) -> FileResponse:
        return FileResponse(index_path, headers={"Content-Security-Policy": csp})

    # Insert at the front so the SPA wins over the legacy htmx "/" and "/docs".
    spa_routes = [
        Route("/", spa_index),
        Route("/docs", spa_index),
        Route("/docs/{rest:path}", spa_index),
    ]
    for route in reversed(spa_routes):
        app.router.routes.insert(0, route)
    return True

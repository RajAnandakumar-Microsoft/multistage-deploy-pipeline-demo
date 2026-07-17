"""Minimal hello-world web app for a multi-stage deployment pipeline sample.

Serves a landing page on ``/`` and a health probe on ``/healthz``. Reads
``APP_ENV`` and ``APP_VERSION`` from the environment so the running stage and
image version are visible in the response — handy for demonstrating promotion
and rollback across the pipeline's deployment waves.
"""

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_ENV = os.environ.get("APP_ENV", "unknown")
APP_VERSION = os.environ.get("APP_VERSION", "0.1.0")
PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    """Tiny request handler: landing page on ``/`` and health on ``/healthz``."""

    def _send(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 - http.server API name
        if self.path == "/healthz":
            self._send(200, "ok")
            return
        self._send(
            200,
            "Hello from the multi-stage deployment pipeline sample!\n"
            f"environment: {APP_ENV}\n"
            f"version: {APP_VERSION}\n",
        )

    def log_message(self, *_args) -> None:
        # Silence the default stderr access logging for clean container logs.
        return


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"listening on :{PORT} (env={APP_ENV}, version={APP_VERSION})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

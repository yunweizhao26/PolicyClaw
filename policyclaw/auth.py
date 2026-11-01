from __future__ import annotations

import os, subprocess, threading, time

_TOKEN_CACHE: tuple[str, float] | None = None
_TOKEN_LOCK = threading.Lock()


def access_token(*, force_refresh: bool = False) -> str:
    global _TOKEN_CACHE
    now = time.monotonic()
    with _TOKEN_LOCK:
        if _TOKEN_CACHE and not force_refresh and now < _TOKEN_CACHE[1]:
            return _TOKEN_CACHE[0]
        gcloud = os.environ.get("GCLOUD_BIN", "gcloud")
        try:
            result = subprocess.run([gcloud, "auth", "application-default", "print-access-token"],
                                    check=True, capture_output=True, text=True)
        except (OSError, subprocess.CalledProcessError) as error:
            raise RuntimeError("Google ADC unavailable; run `gcloud auth application-default login` "
                               "or set GCLOUD_BIN") from error
        token = result.stdout.strip()
        if not token:
            raise RuntimeError("gcloud returned an empty Google access token")
        _TOKEN_CACHE = (token, now + 3000)
        return token


def clear_access_token() -> None:
    global _TOKEN_CACHE
    with _TOKEN_LOCK:
        _TOKEN_CACHE = None

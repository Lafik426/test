from __future__ import annotations

from datetime import datetime
import json
import ssl
import warnings
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE_URL = "https://api.github.com"


class GitHubUser:
    def __init__(self, username: str, verify_ssl: bool = True) -> None:
        self.username = username
        self.verify_ssl = verify_ssl

    def _ssl_context(self) -> ssl.SSLContext | None:
        if self.verify_ssl:
            return None
        warnings.warn(
            "SSL verification is disabled; use only for local troubleshooting.",
            RuntimeWarning,
            stacklevel=2,
        )
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def _get(self, endpoint: str) -> list[dict[str, Any]]:
        url = f"{API_BASE_URL}{endpoint}"
        request = Request(url, headers={"Accept": "application/vnd.github+json"})
        try:
            with urlopen(request, timeout=10, context=self._ssl_context()) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise RuntimeError(f"GitHub API error: {exc.code} {exc.reason}") from exc
        except URLError as exc:
            raise RuntimeError(f"Network error: {exc.reason}") from exc

    def fetch_repos(self) -> list[dict[str, Any]]:
        repos = self._get(f"/users/{self.username}/repos")
        return sorted(repos, key=lambda repo: datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ"))

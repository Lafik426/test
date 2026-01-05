#!/usr/bin/env python3
"""Fetch and display GitHub user repositories sorted by creation date."""

from __future__ import annotations

import argparse
import json
import ssl
import warnings
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE_URL = "https://api.github.com"


@dataclass
class GitHubUser:
    username: str
    verify_ssl: bool = True

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
        return sorted(repos, key=lambda repo: _parse_datetime(repo["created_at"]))


def _parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


def build_payload(repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": repo["name"],
            "html_url": repo["html_url"],
            "created_at": repo["created_at"],
            "description": repo.get("description"),
        }
        for repo in repos
    ]


def write_output(payload: list[dict[str, Any]], output: str | None) -> None:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(serialized)
    else:
        print(serialized)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch GitHub repositories for a user and output them sorted by creation date."
        )
    )
    parser.add_argument("username", nargs="?", default="octocat")
    parser.add_argument("--output", "-o", help="Write output to a JSON file")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification (use only for local troubleshooting)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    user = GitHubUser(args.username, verify_ssl=not args.insecure)
    repos = user.fetch_repos()
    payload = build_payload(repos)
    write_output(payload, args.output)


if __name__ == "__main__":
    main()

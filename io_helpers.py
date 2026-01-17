from __future__ import annotations

import json
from typing import Any


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

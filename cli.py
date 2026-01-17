from __future__ import annotations

import argparse


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

from __future__ import annotations

from github_api import GitHubUser
from io_helpers import build_payload, write_output
from cli import parse_args


def main() -> None:
    args = parse_args()
    user = GitHubUser(args.username, verify_ssl=not args.insecure)
    repos = user.fetch_repos()
    payload = build_payload(repos)
    write_output(payload, args.output)


if __name__ == "__main__":
    main()

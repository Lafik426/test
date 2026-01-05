# test

## GitHub repository fetcher

`github_repos.py` fetches repositories for a GitHub user, sorts them by creation date, and outputs
JSON to stdout or to a file.

### Usage

```bash
./github_repos.py octocat
./github_repos.py octocat --output repos.json
./github_repos.py octocat --insecure
```

### Notes

- Uses the public GitHub API without authentication.
- Defaults to the `octocat` user when no username is provided.
- If you see an SSL certificate verification error, install system CA certificates or
  run with `--insecure` for local troubleshooting.

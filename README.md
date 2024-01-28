# fuzzignore.py

This is a tool to automatically load and create a gitignore template abusing the power of `fzf`.
This requires a github authentication token to work, get one before starting.

## Usage

```language=python
fuzzignore.py --auth-token [TOKEN]
```
If omitted, the token will be loaded from the `GITHUB_AUTH_TOKEN` environment variable.


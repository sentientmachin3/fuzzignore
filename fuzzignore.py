#!/usr/bin/env python3

import argparse
import os
import sys

import requests
from pyfzf.pyfzf import FzfPrompt


def cli_args():
    parser = argparse.ArgumentParser(
        description="Fzf-centric tool to download and create gitignore files",
        prog="fuzzignore.py",
    )
    parser.add_argument(
        "--auth-token",
        dest="auth_token",
        help="Github auth token (defaults to env var GITHUB_AUTH_TOKEN)",
        default=os.environ.get("GITHUB_AUTH_TOKEN", None),
    )
    args = vars(parser.parse_args())
    if not args["auth_token"]:
        parser.error("Auth token not provided")
    return args


def get_template_names(auth_token: str) -> list[str]:
    templates_url = "https://api.github.com/gitignore/templates"
    response = requests.get(
        templates_url, headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()


def get_template(template_name: str, auth_token: str) -> str:
    template_url = f"https://api.github.com/gitignore/templates/{template_name}"
    response = requests.get(
        template_url,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/vnd.github.raw+json",
        },
    )
    return response.text


if __name__ == "__main__":
    args = cli_args()
    auth_token = args["auth_token"]
    template_names = get_template_names(auth_token)
    fzf = FzfPrompt()
    selection = fzf.prompt(template_names, "--cycle")[0]

    if not selection:
        sys.exit(0)

    content = get_template(selection, auth_token)
    with open(".gitignore", "w") as f:
        f.write(content)

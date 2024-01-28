#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen


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
    request = Request(
        templates_url, headers={"Authorization": f"Bearer {auth_token}"}, method="GET"
    )
    return json.loads(urlopen(request).read().decode("utf-8"))


def get_template(template_name: str, auth_token: str) -> str:
    template_url = f"https://api.github.com/gitignore/templates/{template_name}"
    request = Request(
        template_url,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/vnd.github.raw+json",
        },
        method="GET",
    )
    return urlopen(request).read().decode("utf-8")


def write_gitignore(content: str):
    if Path(".gitignore").exists():
        print(".gitignore already exists")
        sys.exit(0)
    with open(".gitignore", "w") as f:
        f.write(content)


def fzf_select(templates: str):
    echo = subprocess.Popen(["echo", templates], stdout=subprocess.PIPE)
    ps = subprocess.Popen(["fzf", "--cycle"], stdin=echo.stdout, stdout=subprocess.PIPE)
    selection, ret_code = ps.communicate()[0], ps.returncode
    if ret_code != 0:
        sys.exit(ret_code)
    return selection.decode("utf-8").strip()


if __name__ == "__main__":
    args = cli_args()
    auth_token = args["auth_token"]

    template_names = "\n".join(get_template_names(auth_token))
    selection = fzf_select(template_names)
    content = get_template(selection, auth_token)
    write_gitignore(content)

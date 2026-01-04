#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env GITHUB_TOKEN="$(cat ~/workspace/etc/cred/github_ro.token)" "$DIR/make_repos.py"

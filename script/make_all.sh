#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$DIR/make_posters.py"
"$DIR/make_publis.py"
"$DIR/make_repos.sh"

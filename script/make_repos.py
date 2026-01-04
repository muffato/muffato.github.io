#!/usr/bin/env python3
"""Generate `repos.md` from a hardcoded list of topics and repositories.

The script queries the GitHub API for each repository's description and
last update time. It writes into `repos.md`, preserving the file header
up to the marker '{:/comment}' (same pattern as other scripts).

Set `GITHUB_TOKEN` in the environment to increase rate limits.
"""

import os
import sys
from typing import Dict, List, Optional
import requests
import collections
import datetime

DEFAULT_TIMEOUT = 30
session = requests.Session()

# Hardcoded topics: mapping from anchor `name` -> `description`
TOPICS: Dict[str, str] = {
    'COMPARA': '![icon](/assets/img/icon/ensembl.png) Ensembl Compara',
    'EHIVE': '![icon](/assets/img/icon/guihive.png) eHive workflow manager',
    'SANGERTOL': '![icon](/assets/img/icon/tol.png) Tree of Life Nextflow pipelines',
    'NFCORE': '![icon](/assets/img/icon/nfcore.png) nf-core',
    'SHPC': '![icon](/assets/img/icon/shpc.png) Singularity HPC for container-based computing',
    'GENOMICUS': '![icon](/assets/img/icon/genomicus.png) Genomicus and ancestral genome reconstruction',
}

# Hardcoded repository mapping: topic name -> list of repositories (owner/repo)
REPOS: Dict[str, List[str]] = {
    'COMPARA': [
        'Ensembl/treebest',
        'Ensembl/ensembl-compara',
        # 'Ensembl/ensj-healthcheck',
        'muffato/docker-ensembl-linuxbrew-compara',
        'muffato/docker-ensembl-linuxbrew-basic-dependencies',
        # 'muffato/ensembl-mysql-monitor',
        # 'muffato/ensembl-tools',
        'muffato/pyEnsemblRest',
    ],
    'EHIVE': [
        'Ensembl/ensembl-hive',
        'Ensembl/guiHive',
        'Ensembl/ensembl-hive-docker-swarm',
        'Ensembl/ensembl-hive-pbspro',
        'Ensembl/ensembl-hive-slurm',
        'Ensembl/ensembl-hive-sge',
        'Ensembl/ensembl-hive-htcondor',
        'Ensembl/XML-To-Blockly',
        'muffato/eHive-Blockly',
    ],
    'SANGERTOL': [
        'sanger-tol/blobtoolkit',
        'sanger-tol/insdcdownload',
        'sanger-tol/ensemblrepeatdownload',
        'sanger-tol/ensemblgenedownload',
        'sanger-tol/readmapping',
        'sanger-tol/genomenote',
        'sanger-tol/sequencecomposition',
        'sanger-tol/variantcalling',
        'sanger-tol/variantcomposition',
        'sanger-tol/nf-core-modules',
    ],
    'NFCORE': [
        'nf-core/modules',
        'nf-core/tools',
        'nf-core/nft-utils',
    ],
    'SHPC': [
        'singularityhub/singularity-hpc',
    ],
    'GENOMICUS': [
        'muffato/ensembl-download-java',
        'muffato/pywaltrap',
        'muffato/phd-thesis-scripts',
        'DyogenIBENS/LibsDyogen',
        'DyogenIBENS/Agora',
    ],
}


def github_headers() -> Dict[str, str]:
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def fetch_repo_meta(full_name: str) -> Optional[Dict[str, str]]:
    """Return dict with keys: html_url, description, updated_at (YYYY-MM-DD)."""
    url = f'https://api.github.com/repos/{full_name}'
    try:
        r = session.get(url, headers=github_headers(), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
    except Exception as exc:
        print(f'ERROR fetching {full_name}: {exc}', file=sys.stderr)
        return None
    data = r.json()
    updated = data.get('updated_at') or data.get('pushed_at') or ''
    updated_date = ''
    if updated:
        try:
            # ISO 8601 like 2025-01-03T12:34:56Z -> keep YYYY-MM
            updated_date = '-'.join(updated.split('-', 2)[:2])
        except Exception:
            updated_date = updated
    return {
        'html_url': data.get('html_url', ''),
        'description': data.get('description') or '',
        'updated_at': updated_date,
    }


def make_page() -> None:
    grouped: Dict[str, List[Dict[str, str]]] = collections.defaultdict(list)
    for topic, repo_list in REPOS.items():
        for full in repo_list:
            meta = fetch_repo_meta(full)
            if not meta:
                # keep a minimal placeholder
                meta = {
                    'html_url': f'https://github.com/{full}',
                    'description': '',
                    'updated_at': '',
                }
            item = {'name': full, **meta}
            grouped[topic].append(item)

    # sort each group by updated_at desc (missing dates go last)
    for items in grouped.values():
        items.sort(key=lambda x: x.get('updated_at') or '', reverse=True)

    # Print a short index of topics (assume every topic has at least one repo)
    for name, desc in TOPICS.items():
        print('*', '[' + desc + '](#' + name + ')')
    print()

    # Print markdown content per topic using the topic description and anchor
    for name, desc in TOPICS.items():
        items = grouped[name]
        print('##', desc, '{#' + name + '}')
        print()
        print('<dl>')
        for it in items:
            repo_name = it['name']
            url = it.get('html_url') or f'https://github.com/{repo_name}'
            repo_desc = (it.get('description') or '').replace('\n', ' ').strip()
            updated = it.get('updated_at') or ''
            print('<dt>' + f'[{repo_name}]({url})' + '</dt>')
            print('<dd>')
            if repo_desc:
                print(repo_desc + ' \\\\')
            if updated:
                print('Last update: ' + updated)
            print('</dd>')
        print('</dl>')
        print()


if __name__ == '__main__':
    repos_path = os.path.join(os.path.dirname(__file__), os.pardir, 'repos.md')
    print(repos_path)
    header_lines: List[str] = []
    with open(repos_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            header_lines.append(line)
            if line.startswith('{:/comment}'):
                print("found")
                break
    with open(repos_path, 'w', encoding='utf-8') as sys.stdout:
        sys.stdout.writelines(header_lines)
        make_page()

#!/usr/bin/env python3
"""Script to fetch my poster list (F1000Research and Zenodo) and write it as a Markdown page.
"""

import collections
import enum
import itertools
import os
import sys
import html
from dataclasses import dataclass
from typing import List, Tuple, Optional
from urllib.parse import quote

import requests

CROSSREF_URL = 'https://api.crossref.org/works'
ZENODO_URL = 'https://zenodo.org/api/records'

session = requests.Session()
DEFAULT_TIMEOUT = 30

PubCategories = enum.Enum('PubCategories', 'ENSEMBL EHIVE TOLIT')

category_descriptions = {
    PubCategories.ENSEMBL: '![icon](/assets/img/icon/ensembl.png) Ensembl and ![icon](/assets/img/icon/treefam.png) TreeFam methods',
    PubCategories.EHIVE: '![icon](/assets/img/icon/guihive.png) eHive workflow manager',
    PubCategories.TOLIT: '![icon](/assets/img/icon/tol.png) Tree of Life Informatics Infrastructure',
}

# Simple keyword mapping: check lowercase title for these keywords
category_keywords = [
    ('hive', PubCategories.EHIVE),
    ('ensembl', PubCategories.ENSEMBL),
    ('treefam', PubCategories.ENSEMBL),
    ('phylogenetic', PubCategories.ENSEMBL),
    ('comparative', PubCategories.ENSEMBL),
    ('tree of life', PubCategories.TOLIT),
    ('weskit', PubCategories.TOLIT),
    ('nf-core', PubCategories.TOLIT),
]

# Hardcoded DOIs to include even when CrossRef does not list Muffato
EXTRA_DOIS = {
    '10.7490/f1000research.1114127.1': 'Mateus Patricio, Matthieu Muffato, Wasiu Akanni, Carla Cummins, Bronwen Aken, Paul Flicek',
}


@dataclass
class Poster:
    title: str
    doi: str
    author_string: str
    author_list: List[str]
    resource_urls: List[str]
    published_date: Tuple[int, int, int]


def classify(p: Poster) -> PubCategories:
    title = p.title.lower()
    for kw, cat in category_keywords:
        if kw in title:
            return cat
    return PubCategories.TOLIT


def extract_urls_from_crossref(item: dict) -> List[str]:
    urls = []
    res = item.get('resource')
    if isinstance(res, list):
        for r in res:
            if isinstance(r, dict):
                u = r.get('URL')
                if u:
                    urls.append(u)
    elif isinstance(res, dict):
        primary = res.get('primary', {})
        if isinstance(primary, dict):
            u = primary.get('URL')
            if u:
                urls.append(u)
    return urls


def parse_crossref_date(item: dict) -> Tuple[int, int, int]:
    for key in ('published-print', 'published-online', 'published', 'issued'):
        v = item.get(key)
        if v and isinstance(v, dict):
            parts = v.get('date-parts') or []
            if parts:
                p = parts[0]
                y = int(p[0]) if len(p) > 0 and isinstance(p[0], int) else 0
                m = int(p[1]) if len(p) > 1 and isinstance(p[1], int) else 0
                d = int(p[2]) if len(p) > 2 and isinstance(p[2], int) else 0
                return (y, m, d)
    return (0, 0, 0)


def normalize_crossref_item(item: dict, require_muffato: bool = True) -> Optional[Poster]:
    doi = item.get('DOI', '') or ''
    if not doi:
        return None

    publisher = item.get('publisher', '') or ''
    urls = extract_urls_from_crossref(item)
    if 'f1000' not in publisher.lower() and not any('f1000research.com' in (u or '') for u in urls):
        return None

    # authors
    authors = item.get('author', []) or []
    author_names: List[str] = []
    for a in authors:
        given = a.get('given', '') or ''
        family = a.get('family', '') or ''
        if given and family:
            author_names.append(f"{given} {family}")
        elif family:
            author_names.append(family)
        elif given:
            author_names.append(given)
    author_str = ', '.join(author_names)
    if require_muffato and 'Muffato' not in author_str:
        return None

    title = ''
    if item.get('title'):
        title = item['title'][0]

    pubdate = parse_crossref_date(item)

    return Poster(title=title, doi=doi, author_string=author_str, author_list=author_names, resource_urls=urls, published_date=pubdate)


def retrieve_posters_crossref_f1000():
    params = {'filter': 'prefix:10.7490', 'query.author': 'muffato', 'rows': 200}
    r = session.get(CROSSREF_URL, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    struct = r.json()
    for item in struct.get('message', {}).get('items', []):
        parsed = normalize_crossref_item(item, require_muffato=True)
        if parsed:
            yield parsed


def retrieve_posters_by_dois(dois_map: dict):
    for doi, author_override in dois_map.items():
        url = CROSSREF_URL + '/' + quote(doi, safe='')
        r = session.get(url, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        struct = r.json()
        item = struct.get('message')
        if not item:
            continue
        parsed = normalize_crossref_item(item, require_muffato=False)
        if not parsed:
            continue
        parsed.author_string = author_override
        parsed.author_list = [a.strip() for a in author_override.split(',') if a.strip()]
        yield parsed


def extract_urls_from_zenodo(rec: dict) -> List[str]:
    urls = []
    if not isinstance(rec, dict):
        return urls
    links = rec.get('links') or {}
    if isinstance(links, dict):
        for k in ('html', 'doi', 'self'):
            u = links.get(k)
            if u:
                urls.append(u)
    return urls


def parse_zenodo_date(metadata: dict) -> Tuple[int, int, int]:
    pubdate_str = metadata.get('publication_date') or metadata.get('created') or ''
    if not pubdate_str:
        return (0, 0, 0)
    parts = pubdate_str.split('-')
    try:
        y = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        m = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        d = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (y, m, d)
    except Exception:
        return (0, 0, 0)


def normalize_zenodo_record(rec: dict) -> Poster:
    metadata = rec.get('metadata') if isinstance(rec, dict) else {}
    if metadata is None:
        metadata = {}
    title = metadata.get('title') or ''
    creators = metadata.get('creators', []) or []
    author_names: List[str] = []
    for c in creators:
        name = (c.get('name') or '').strip()
        if ',' in name:
            parts = [p.strip() for p in name.split(',', 1)]
            if len(parts) == 2:
                family, given = parts[0], parts[1]
                author_names.append(f"{given} {family}")
            else:
                author_names.append(name)
        else:
            author_names.append(name)
    author_str = ', '.join(author_names)
    doi = ''
    if isinstance(rec, dict):
        doi = rec.get('doi') or doi
    doi = doi or metadata.get('doi') or ''
    urls = extract_urls_from_zenodo(rec)
    pubdate = parse_zenodo_date(metadata)
    return Poster(title=title, doi=doi, author_string=author_str, author_list=author_names, resource_urls=urls, published_date=pubdate)


def retrieve_posters_zenodo():
    params = {'q': 'metadata.creators.person_or_org.identifiers.identifier:"0000-0002-7860-3560"', 'size': 10, 'type': 'poster'}
    r = session.get(ZENODO_URL, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    struct = r.json()
    if isinstance(struct, dict):
        items = struct.get('hits', {}).get('hits') or struct.get('hits') or struct.get('results') or []
    elif isinstance(struct, list):
        items = struct
    else:
        items = []
    for rec in items:
        yield normalize_zenodo_record(rec)


def format_authors(p: Poster) -> str:
    def _underline(text: str) -> str:
        return text.replace('Matthieu Muffato', '<u>Matthieu Muffato</u>')

    if 'Muffato' in p.author_string:
        # underline Muffato in author string
        return _underline(p.author_string)
    if p.author_list:
        return p.author_list[0] + ', _et al._'
    return ''


def print_poster(p: Poster):
    title = html.unescape(p.title).strip()
    print('<dt>' + title + '</dt>')
    print('<dd>')
    print(format_authors(p) + ' \\\\')
    if p.doi:
        print('DOI: [' + p.doi + '](https://doi.org/' + p.doi + ')')
    print('</dd>')


def make_page():
    posters = collections.defaultdict(list)
    existing_dois = set()

    for p in itertools.chain(
        retrieve_posters_crossref_f1000(),
        retrieve_posters_by_dois(EXTRA_DOIS),
        retrieve_posters_zenodo(),
    ):
        if p.doi and p.doi in existing_dois:
            continue
        if p.doi:
            existing_dois.add(p.doi)
        posters[classify(p)].append(p)

    for items in posters.values():
        items.sort(key=lambda x: x.published_date or (0, 0, 0), reverse=True)

    for category in PubCategories:
        if posters[category]:
            print('*', '[' + category_descriptions[category] + '](#' + category.name + ')')
    print()
    for category in PubCategories:
        if posters[category]:
            print('##', category_descriptions[category], '{#' + category.name + '}')
            print()
            print('<dl>')
            for p in posters[category]:
                print_poster(p)
            print('</dl>')
            print()


if __name__ == '__main__':
    posters_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'posters.md')
    header_lines = []
    with open(posters_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            header_lines.append(line)
            if line.startswith('{:/comment}'):
                break
    # write output to stdout as before
    with open(posters_path, 'w', encoding='utf-8') as sys.stdout:
        sys.stdout.writelines(header_lines)
        make_page()

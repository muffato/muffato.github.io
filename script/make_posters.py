#!/usr/bin/env python3
"""Script to fetch my poster list (F1000Research) and write it as a Markdown page"""

import collections
import enum
import os
import sys
import requests
import html

base_url = 'https://api.crossref.org/works'

PubCategories = enum.Enum('PubCategories', 'ENSEMBL EHIVE TOLIT')

category_descriptions = {
    PubCategories.ENSEMBL: '![icon](/assets/img/icon/ensembl.png) Ensembl and ![icon](/assets/img/icon/treefam.png) TreeFam methods',
    PubCategories.EHIVE: '![icon](/assets/img/icon/guihive.png) eHive workflow manager',
    PubCategories.TOLIT: '![icon](/assets/img/icon/tol.png) Tree of Life Informatics Infrastructure',
}

category_keywords = [
    ('title', 'hive', PubCategories.EHIVE),
    ('title', 'ensembl', PubCategories.ENSEMBL),
    ('title', 'treefam', PubCategories.ENSEMBL),
    ('title', 'phylogenetic', PubCategories.ENSEMBL),
    ('title', 'comparative', PubCategories.ENSEMBL),
    ('title', 'tree of life', PubCategories.TOLIT),
    ('title', 'weskit', PubCategories.TOLIT),
    ('title', 'nf-core', PubCategories.TOLIT),
]

def classify(publi):
    title = publi.get('title', '').lower()
    for (field, keyword, category) in category_keywords:
        if keyword in title:
            return category
    return PubCategories.TOLIT

def retrieve_posters():
    params = {
        'query.author': 'Matthieu Muffato',
        'rows': 200,
    }
    r = requests.get(base_url, params=params)
    r.raise_for_status()
    struct = r.json()
    for item in struct.get('message', {}).get('items', []):
        doi = item['DOI']
        # prefer F1000 Research items
        publisher = item.get('publisher', '')
        resource_urls = []
        if isinstance(item.get('resource'), list):
            for res in item['resource']:
                if isinstance(res, dict):
                    resource_urls.append(res.get('URL', ''))
        if item.get('resource') and isinstance(item.get('resource'), dict):
            primary = item['resource'].get('primary', {})
            if isinstance(primary, dict):
                resource_urls.append(primary.get('URL', ''))

        if 'f1000' not in publisher.lower() and not any('f1000research.com' in u for u in resource_urls):
            continue

        # build author string
        authors = item.get('author', [])
        author_names = []
        for a in authors:
            given = a.get('given', '')
            family = a.get('family', '')
            if given and family:
                author_names.append(given + ' ' + family)
            elif family:
                author_names.append(family)
            elif given:
                author_names.append(given)
        author_string = ', '.join(author_names)
        if 'Muffato' not in author_string:
            continue

        title = ''
        if item.get('title'):
            title = item['title'][0]

        # determine published date: prefer 'published-print', then 'published-online', then 'issued'
        pubdate = None
        for key in ('published-print', 'published-online', 'published', 'issued'):
            v = item.get(key)
            if v and isinstance(v, dict) and v.get('date-parts'):
                parts = v['date-parts'][0]
                # normalize to (year, month, day)
                y = parts[0] if len(parts) > 0 else 0
                m = parts[1] if len(parts) > 1 else 0
                d = parts[2] if len(parts) > 2 else 0
                pubdate = (y, m, d)
                break
        if pubdate is None:
            pubdate = (0, 0, 0)

        yield {
            'title': title,
            'doi': doi,
            'authorString': author_string,
            'authorList': author_names,
            'resource_urls': resource_urls,
            'published_date': pubdate,
        }


def retrieve_posters_zenodo():
    """Query Zenodo for posters and yield records in the same internal format.

    Uses a simple query which the user reported works well for posters by
    the same author.
    """
    zenodo_url = 'https://zenodo.org/api/records'
    # Use the dedicated 'type' parameter and a simple name query
    params = {
        'q': 'muffato',
        'size': 10,
        'type': 'poster',
    }
    r = requests.get(zenodo_url, params=params, timeout=30)
    r.raise_for_status()
    struct = r.json()

    # Support both list-style and dict-with-hits responses
    if isinstance(struct, dict):
        items = struct.get('hits', {}).get('hits') or struct.get('hits') or struct.get('results') or []
    elif isinstance(struct, list):
        items = struct
    else:
        items = []

    for rec in items:
        # 'rec' may already be the metadata-level dict or a full record
        metadata = rec.get('metadata') if isinstance(rec, dict) else {}
        if metadata is None:
            metadata = {}

        title = metadata.get('title') or ''

        # creators: try to normalize names to 'Given Family'
        creators = metadata.get('creators', [])
        author_names = []
        for c in creators:
            name = c.get('name', '').strip()
            if ',' in name:
                parts = [p.strip() for p in name.split(',', 1)]
                if len(parts) == 2:
                    family, given = parts[0], parts[1]
                    author_names.append(given + ' ' + family)
                else:
                    author_names.append(name)
            else:
                author_names.append(name)

        author_string = ', '.join(author_names)

        # DOI: try a few common places
        doi = ''
        if isinstance(rec, dict):
            doi = rec.get('doi') or doi
        doi = doi or metadata.get('doi') or ''

        # resource urls
        resource_urls = []
        if isinstance(rec, dict):
            links = rec.get('links', {})
            if isinstance(links, dict):
                for k in ('html', 'doi', 'self'):
                    u = links.get(k)
                    if u:
                        resource_urls.append(u)

        # publication date -> (y,m,d)
        pubdate = None
        pubdate_str = metadata.get('publication_date') or metadata.get('created') or ''
        if pubdate_str:
            parts = pubdate_str.split('-')
            try:
                y = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
                m = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                d = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                pubdate = (y, m, d)
            except Exception:
                pubdate = (0, 0, 0)
        if pubdate is None:
            pubdate = (0, 0, 0)

        yield {
            'title': title,
            'doi': doi,
            'authorString': author_string,
            'authorList': author_names,
            'resource_urls': resource_urls,
            'published_date': pubdate,
        }

def print_poster(publi):
    title = html.unescape(publi['title']).strip()
    print('<dt>' + title + '</dt>')
    print('<dd>')
    authors = publi['authorList']
    # format authors similar to make_publis.py
    families = [n.split()[-1] for n in authors]
    mypos = None
    for i, fam in enumerate(families):
        if fam == 'Muffato':
            mypos = i
            break
    if mypos is None:
        if authors:
            print(authors[0] + ', _et al._ \\\\')
    else:
        if mypos < 7:
            if len(authors) > 7:
                print(', '.join(authors[:mypos+1]) + ', _et al._ \\\\')
            else:
                print(publi['authorString'] + ' \\\\')
        else:
            print(authors[0] + ', _et al._ \\\\')
    print('DOI: [' + publi['doi'] + '](https://doi.org/' + publi['doi'] + ')')
    print('</dd>')

def make_page():
    posters = collections.defaultdict(list)
    existing_dois = set()

    # First, collect Crossref results
    for publi in retrieve_posters():
        doi = (publi.get('doi') or '').strip()
        if doi:
            existing_dois.add(doi)
        posters[classify(publi)].append(publi)

    # Then, collect Zenodo results and avoid duplicates by DOI
    for publi in retrieve_posters_zenodo():
        doi = (publi.get('doi') or '').strip()
        if doi and doi in existing_dois:
            continue
        if doi:
            existing_dois.add(doi)
        posters[classify(publi)].append(publi)
    # sort each category by published date (most recent first)
    for cat, items in posters.items():
        items.sort(key=lambda x: x.get('published_date', (0, 0, 0)), reverse=True)

    for category in PubCategories:
        if posters[category]:
            print('*', '['+category_descriptions[category]+'](#'+category.name+')')
    print()
    for category in PubCategories:
        print('##', category_descriptions[category], '{#'+category.name+'}')
        print()
        print('<dl>')
        for publi in posters[category]:
            print_poster(publi)
        print('</dl>')
        print()

if __name__ == '__main__':
    posters_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'posters.md')
    lines = []
    with open(posters_path, 'r') as fh:
        for line in fh:
            lines.append(line)
            # stop before the generated section marker
            if line.startswith('{:/comment}'):
                break
    with open(posters_path, 'w') as sys.stdout:
        sys.stdout.writelines(lines)
        make_page()

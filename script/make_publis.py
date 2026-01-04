#!/usr/bin/env python3
"""Script to fetch my publication list and write it as a Markdown page"""

import collections
import enum
import os
import sys
from typing import Any
import requests
import html
import itertools
from urllib.parse import quote

orcid = '0000-0002-7860-3560'

base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest'
endpoint = '/search'
args = {
    'query': 'AUTHORID:' + orcid,
    'format': 'json',
    'resultType': 'core',
    'pageSize': 200,
    'sort': 'FIRST_PDATE_D desc',
}

PubCategories = enum.Enum(
    'PubCategories', 'ENSEMBL GENOMICUS QFO TOLIT GENOMES ENSEMBL_NAR'
)

category_descriptions = {
    PubCategories.ENSEMBL: '![icon](/assets/img/icon/ensembl.png) Ensembl and ![icon](/assets/img/icon/treefam.png) TreeFam methods',
    PubCategories.GENOMICUS: '![icon](/assets/img/icon/genomicus.png) Genomicus and ancestral genome reconstruction',
    PubCategories.QFO: '![icon](/assets/img/icon/orthology.png) Quest for Orthologs consortium ',
    PubCategories.TOLIT: '![icon](/assets/img/icon/tol.png) Tree of Life Informatics Infrastructure',
    PubCategories.GENOMES: '![icon](/assets/img/icon/zebrafish.png) Genome analysis',
    PubCategories.ENSEMBL_NAR: '![icon](/assets/img/icon/ensembl.png) Ensembl yearly NAR updates',
}

category_keywords = [
    ('title', 'quest', PubCategories.QFO),
    ('title', 'ancest', PubCategories.GENOMICUS),
    ('title', 'genomicus', PubCategories.GENOMICUS),
    ('title', 'treefam', PubCategories.ENSEMBL),
    ('doi', '10.1093/nar/', PubCategories.ENSEMBL_NAR),
    ('title', 'ensembl', PubCategories.ENSEMBL),
    ('authors', 'tree of life', PubCategories.GENOMES),
]

# Force some publications into a category
known_categories = {
    '10.1093/database/bav127': PubCategories.ENSEMBL,  # ncRNA orthologies in the vertebrate lineage
    '10.1186/1471-2105-15-268': PubCategories.GENOMICUS,  # PhylDiag: identifying complex synteny blocks that include tandem duplications using phylogenetic gene trees
    '10.1002/bies.20707': PubCategories.GENOMICUS,  # Paleogenomics in vertebrates, or the recovery of lost genomes from the mist of time
    '10.1016/j.celrep.2015.02.046': PubCategories.GENOMICUS,  # The 3D organization of chromatin explains evolutionary fragile genomic regions
    '10.1093/sysbio/syv033': PubCategories.ENSEMBL,  # Current Methods for Automated Filtering of Multiple Sequence Alignments Frequently Worsen Single-Gene Phylogenetic Inference
    '10.5334/jors.451': PubCategories.TOLIT,  # Automated Discovery of Container Executables
}

# Discard these
sub_publications = {
    # Baboon
    '10.1126/sciadv.aau6947': set(
        [
            '10.1186/s13100-018-0118-3',
            '10.1186/s13100-018-0115-6',
            '10.1093/gbe/evx130',
            '10.1093/gbe/evx184',
            '10.1186/s13100-019-0187-y',
        ]
    ),
    # Hagfish
    '10.1038/s41559-023-02299-z': set(
        [
            '10.1101/2023.04.08.536076',
        ]
    ),
}

# Hardcoded DOIs to include via CrossRef
EXTRA_DOIS = {
    '10.5334/jors.451',
}


def retrieve_publications_crossref(dois):
    """Fetch minimal publication dicts from CrossRef for the given DOIs.
    Returns objects compatible with the `publi` dicts yielded by EuropePMC.
    """
    for doi in dois:
        url = 'https://api.crossref.org/works/' + quote(doi, safe='')
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        struct = r.json()
        item = struct.get('message')
        if not item:
            continue
        title = item.get('title', [''])[0]
        authors = item.get('author', []) or []
        author_names = []
        author_list_entries = []
        for a in authors:
            given = a.get('given', '') or ''
            family = a.get('family', '') or ''
            if given and family:
                full = f"{given} {family}"
            elif family:
                full = family
            else:
                full = given
            author_names.append(full)
            author_list_entries.append({'fullName': full, 'lastName': family or ''})
        authorString = ', '.join(author_names)
        publi = {
            'doi': item.get('DOI', ''),
            'title': title,
            'authorString': authorString,
            'authorList': {'author': author_list_entries},
            'pubTypeList': {'pubType': ''},
        }
        # journal/container info
        container = item.get('container-title', []) or []
        if container:
            journal = {'title': container[0]}
            journal_info: dict[str, Any] = {'journal': journal}
            if item.get('volume'):
                journal_info['volume'] = item.get('volume')
            if item.get('issue'):
                journal_info['issue'] = item.get('issue')
            # attempt to set a publication year
            issued = item.get('issued') or item.get('published-print') or {}
            parts = issued.get('date-parts') if isinstance(issued, dict) else None
            if parts and parts[0]:
                year = parts[0][0]
                journal_info['dateOfPublication'] = str(year)
            publi['journalInfo'] = journal_info
        if item.get('page'):
            publi['pageInfo'] = item.get('page')
        # firstPublicationDate fallback
        issued = item.get('issued') or item.get('published-print') or {}
        if isinstance(issued, dict):
            parts = issued.get('date-parts') or []
            if parts and parts[0]:
                p = parts[0]
                publi['firstPublicationDate'] = '-'.join(str(x) for x in p)
        yield publi


def classify(publi):
    """Classify a publication into one of the above categories"""
    doi = publi['doi']
    if doi in known_categories:
        return known_categories[doi]
    title = publi['title'].lower()
    authors = publi['authorString'].lower()
    for field, keyword, category in category_keywords:
        if field == "title":
            if keyword in title:
                return category
        elif field == "doi":
            if publi['doi'].startswith(keyword):
                return category
        elif field == "authors":
            if keyword in authors:
                return category
        else:
            raise ValueError("Unknown field: " + field)
    return PubCategories.GENOMES


def retrieve_publications():
    """Fetch the complete list of publications from EuropePMC"""
    r = requests.get(base_url + endpoint, params=args)
    struct = r.json()
    for publi in struct['resultList']['result']:
        if ('Muffato' not in publi['authorString']) and ('consortium' not in publi['authorString'].lower()) and ('tree of life programme' not in publi['authorString'].lower()):
            print('SKIP', publi.get('pmcid'), publi['doi'], publi['title'], publi['authorString'].lower(), file=sys.stderr)
            continue
        if "correction" in publi["pubTypeList"]["pubType"]:
            print('ERRATUM', publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
            continue
        yield publi


def print_publication(publi):
    """Print a publication entry in markdown"""
    title = html.unescape(publi['title']).strip()
    print('<dt>' + title + '</dt>')
    print('<dd>')
    authors = publi['authorList']['author']

    def _underline_name(text):
        return text.replace('Muffato M', '<u>Muffato M</u>').replace('Matthieu Muffato', '<u>Matthieu Muffato</u>')

    if 'Muffato' not in publi['authorString']:
        print(authors[0]['fullName'], '_et al._', '\\\\')
    else:
        mypos = [i for (i, a) in enumerate(authors) if a.get('lastName', '') == 'Muffato'][0]
        if mypos < 7:
            if len(authors) > 7:
                joined = ', '.join([a['fullName'] for a in authors[: mypos + 1]])
                print(_underline_name(joined) + ', _et al._ \\\\')
            else:
                print(_underline_name(publi['authorString']), '\\\\')
        else:
            print(authors[0]['fullName'], '_et al._', '\\\\')
    if "journalInfo" in publi:
        journal_string = '_' + publi["journalInfo"]["journal"]["title"] + '_'
        if "volume" in publi["journalInfo"]:
            journal_string += ', ' + publi["journalInfo"]["volume"]
        if "issue" in publi["journalInfo"]:
            journal_string += ' (' + publi["journalInfo"]["issue"] + ')'
        if "pageInfo" in publi:
            if publi["pageInfo"].startswith('bav'):
                journal_string += ', ' + publi["pageInfo"]
            else:
                journal_string += ', pages ' + publi["pageInfo"]
        if "volume" in publi["journalInfo"] and publi["journalInfo"]["dateOfPublication"] != publi["journalInfo"]["volume"]:
            journal_string += ', ' + publi["journalInfo"]["dateOfPublication"]
    else:
        journal_string = '_' + publi["bookOrReportDetails"]["publisher"] + '_'
        journal_string += ', ' + publi["firstPublicationDate"]
    print(journal_string, '\\\\')
    print(f'DOI: [{publi["doi"]}](https://doi.org/{publi["doi"]})')
    print('</dd>')


def make_page():
    """Print the entire page in Markdown"""
    indexed_sub_publications = {}
    for ref, subs in sub_publications.items():
        for sub in subs:
            indexed_sub_publications[sub] = ref
    publis = collections.defaultdict(list)
    subs = {}
    for publi in itertools.chain(
        retrieve_publications(),
        retrieve_publications_crossref(EXTRA_DOIS),
    ):
        if publi['doi'] in indexed_sub_publications:
            subs[publi['doi']] = publi
            continue
        category = classify(publi)
        print(category, publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
        publis[category].append(publi)
    for category in PubCategories:
        print('*', '['+category_descriptions[category]+'](#'+category.name+')')
    print()
    for category in PubCategories:
        print('##', category_descriptions[category], '{#' + category.name + '}')
        print()
        print('<dl>')
        for publi in publis[category]:
            print_publication(publi)
            for sub_doi in sub_publications.get(publi['doi'], []):
                sub_publi = subs[sub_doi]
                # print_publication(publi, 'SUB')
                print('SUB', sub_publi.get('pmcid'), sub_publi['doi'], sub_publi['title'], file=sys.stderr)
            # print()
        print('</dl>')
        print()


if __name__ == '__main__':
    publis_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'publis.md')
    print(publis_path)
    header_lines = []
    with open(publis_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            header_lines.append(line)
            if line.startswith('{:/comment}'):
                print("found")
                break
    with open(publis_path, 'w', encoding='utf-8') as sys.stdout:
        sys.stdout.writelines(header_lines)
        make_page()

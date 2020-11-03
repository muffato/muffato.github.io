#!/usr/bin/env python3
"""Script to fetch my publication list and write it as a Markdown page"""

import collections
import enum
import os
import sys
import requests

orcid = '0000-0002-7860-3560'

base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest'
endpoint = '/search'
args = {
        'query': 'AUTHORID:' + orcid,
        'format': 'json',
        'resultType': 'core',
        'pageSize': 200,
        'sort': 'P_PDATE_D desc',
}

PubCategories = enum.Enum('PubCategories', 'ENSEMBL GENOMICUS QFO GENOMES ENSEMBL_NAR')

category_descriptions = {
        PubCategories.ENSEMBL: '![icon](/assets/img/icon/ensembl.png) Ensembl and ![icon](/assets/img/icon/treefam.png) TreeFam',
        PubCategories.GENOMICUS: '![icon](/assets/img/icon/genomicus.png) Genomicus and ancestral genome reconstruction',
        PubCategories.QFO: 'Quest for Orthologs',
        PubCategories.GENOMES: 'Genome analysis',
        PubCategories.ENSEMBL_NAR: '![icon](/assets/img/icon/ensembl.png) Ensembl yearly NAR updates',
}

category_keywords = [
        ('quest', PubCategories.QFO),
        ('genomicus', PubCategories.GENOMICUS),
        ('treefam', PubCategories.ENSEMBL),
        ('^10.1093/nar/', PubCategories.ENSEMBL_NAR),
        ('ensembl', PubCategories.ENSEMBL),
    ]

# Force some publications into a category
known_categories = {
        '10.1093/database/bav127': PubCategories.ENSEMBL,        # ncRNA orthologies in the vertebrate lineage
        '10.1186/1471-2105-15-268': PubCategories.GENOMICUS,     # PhylDiag: identifying complex synteny blocks that include tandem duplications using phylogenetic gene trees
        '10.1002/bies.20707': PubCategories.GENOMICUS,           # Paleogenomics in vertebrates, or the recovery of lost genomes from the mist of time
        '10.1016/j.celrep.2015.02.046': PubCategories.GENOMICUS, # The 3D organization of chromatin explains evolutionary fragile genomic regions
        '10.1093/sysbio/syv033': PubCategories.ENSEMBL,          # Current Methods for Automated Filtering of Multiple Sequence Alignments Frequently Worsen Single-Gene Phylogenetic Inference
    }

# Discard these
sub_publications = {
        # Baboon
        '10.1126/sciadv.aau6947': set([
            '10.1186/s13100-018-0118-3',
            '10.1186/s13100-018-0115-6',
            '10.1093/gbe/evx130',
            '10.1093/gbe/evx184',
            '10.1186/s13100-019-0187-y',
            ]),
    }

def classify(publi):
    """Classify a publication into one of the above categories"""
    doi = publi['doi']
    if doi in known_categories:
        return known_categories[doi]
    title = publi['title'].lower()
    for (keyword, category) in category_keywords:
        if keyword[0] == '^':
            if '/' in keyword:
                if publi['doi'].startswith(keyword[1:]):
                    return category
            else:
                if title.startswith(keyword[1:]):
                    return category
        elif keyword in title:
            return category
    return PubCategories.GENOMES

def retrieve_publications():
    """Fetch the complete list of publications from EuropePMC"""
    r = requests.get(base_url + endpoint, params=args)
    struct = r.json()
    for publi in struct['resultList']['result']:
        if ('Muffato' not in publi['authorString']) and ('consortium' not in publi['authorString'].lower()):
            print('SKIP', publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
            continue
        if 'Preprint' in publi['pubTypeList']['pubType']:
            print('PREPRINT', publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
            continue
        if 'commentCorrectionList' in publi:
            types = set(x['type'] for x in publi['commentCorrectionList']['commentCorrection'])
            if 'Erratum for' in types:
                print('ERRATUM', publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
                continue
            # if 'Preprint of' in types:
                # print('CPREPRINT', publi.get('pmcid'), publi['doi'], publi['title'])
                # continue
        yield publi

def print_publication(publi):
    """Print a publication entry in markdown"""
    print('<dt>' + publi['title'] + '</dt>')
    print('<dd>')
    authors = publi['authorList']['author']
    if 'Muffato' not in publi['authorString']:
        print(authors[0]['fullName'], '_et al._', '\\\\')
    else:
        mypos = [i for (i, a) in enumerate(authors) if a.get('lastName', '') == 'Muffato'][0]
        if mypos < 7:
            if len(authors) > 7:
                print(*[a['fullName'] for a in authors[:mypos+1]], '_et al._ \\\\', sep=', ')
            else:
                print(publi['authorString'], '\\\\')
        else:
            print(authors[0]['fullName'], '_et al._', '\\\\')
    journal_string = '_' + publi["journalInfo"]["journal"]["title"] + '_'
    journal_string += ' ' + publi["journalInfo"]["volume"]
    if "issue" in publi["journalInfo"]:
        journal_string += '(' + publi["journalInfo"]["issue"] + ')'
    if "pageInfo" in publi:
        journal_string += ':' + publi["pageInfo"]
    if publi["journalInfo"]["dateOfPublication"] != publi["journalInfo"]["volume"]:
        journal_string += ', ' + publi["journalInfo"]["dateOfPublication"]
    print(journal_string, '\\\\')
    print(f'DOI: [{publi["doi"]}](https://doi.org/{publi["doi"]})')
    print('</dd>')

def make_page():
    """Print the entire page in Markdown"""
    indexed_sub_publications = {}
    for (ref, subs) in sub_publications.items():
        for sub in subs:
            indexed_sub_publications[sub] = ref
    publis = collections.defaultdict(list)
    subs = {}
    for publi in retrieve_publications():
        if publi['doi'] in indexed_sub_publications:
            subs[publi['doi']] = publi
            continue
        category = classify(publi)
        print(category, publi.get('pmcid'), publi['doi'], publi['title'], file=sys.stderr)
        publis[category].append(publi)
    for category in PubCategories:
        if publis[category]:
            print('*', '['+category_descriptions[category]+'](#'+category.name+')')
    print()
    for category in PubCategories:
        print('##', category_descriptions[category], '{#'+category.name+'}')
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
    lines = []
    with open(publis_path, 'r') as fh:
        for line in fh:
            lines.append(line)
            if line.startswith('{:/comment}'):
                print("found")
                break
    with open(publis_path, 'w') as sys.stdout:
        sys.stdout.writelines(lines)
        make_page()

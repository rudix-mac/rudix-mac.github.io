#!/usr/bin/python

import sys
import argparse
import logging
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

GITHUB_URL = 'https://raw.githubusercontent.com/rudix-mac/packages/master'

MACOS_VERSIONS = {
    'macos10.11': 'OS X El Capitan (Version 10.11)',
    'macos10.14': 'macOS Mojave (Version 10.14)',
    'macos10.15': 'macOS Catalina (Version 10.15)',
}

MacOSpkgs = {
    'macos10.11': [],
    'macos10.14': [],
    'macos10.15': [],
}

BeginPackageTable =  """<table>
<caption>%s</caption>
<tr><th>Title</th><th>Package</th></tr>
"""
PackageRow = '<tr><td>%s</td><td><a href="%s/%s">%s</a></td></tr>\n'
EndPackageTable = "</table>\n"


def read_metadata(f):
    rows = csv.reader(f)
    titles = next(rows)
    return titles, list(rows)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--quiet', action="store_true", 
    )
    parser.add_argument(
        '--verbose', action="store_true", 
    )
    parser.add_argument(
        '--url', default=GITHUB_URL,
    )
    parser.add_argument(
        '--manifest',
        default=sys.stdin, type=argparse.FileType('r'),
    )
    parser.add_argument(
        '--metadata',
        default=open('metadata.csv', 'r'), type=argparse.FileType('r'),
    )
    parser.add_argument(
        '--begin',
        default=open('index_begin.html', 'r'), type=argparse.FileType('r'),
    )
    parser.add_argument(
        '--end',
        default=open('index_end.html', 'r'), type=argparse.FileType('r'),
    )
    parser.add_argument(
        '--output',
        default=open('index.html', 'w'), type=argparse.FileType('w'),
    )
    args = parser.parse_args()
    if args.quiet:
        logger.setLevel(logging.ERROR)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    return args


def create_table(html, macosver, metadata, url):
    title = '%s' % MACOS_VERSIONS[macosver]
    html += BeginPackageTable % (title)
    for package in MacOSpkgs[macosver]:
        logger.debug('create_table:%s:%s', macosver, package)
        for row in metadata:
            logger.debug('create_table:metadata:%s', row)
            name_version = '%s-%s' % (row[0], row[1])
            if package.startswith(name_version):
                html += PackageRow % (
                    row[2], url, package, package)
    html += EndPackageTable
    return html


def process():
    tables = MACOS_VERSIONS.keys()
    args = parse_args()
    packages = [x.strip() for x in args.manifest.readlines()]
    titles, metadata = read_metadata(args.metadata)
    html = args.begin.read()
    for package in packages:
        if package.endswith('-macos10.11.pkg'):
            MacOSpkgs['macos10.11'].append(package)
#        elif package.endswith('-macos10.14.pkg'):
#            MacOSpkgs['macos10.14'].append(package)
        elif package.endswith('-macos10.15.pkg'):
            MacOSpkgs['macos10.15'].append(package)
        else:
            MacOSpkgs['macos10.11'].append(package)
    html = create_table(html, 'macos10.15', metadata, args.url)
    #html = create_table(html, 'macos10.14', metadata, args.url)
    html = create_table(html, 'macos10.11', metadata, args.url)
    html += EndPackageTable
    html += args.end.read()
    args.output.write(html)


if __name__  == '__main__':
    process()

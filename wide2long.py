#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@c-path.org>
Date   : 2020-09-01
Purpose: Wide to long
"""

import argparse
import csv
import os
import sys
from typing import NamedTuple, TextIO, List


class Args(NamedTuple):
    file: TextIO
    out_file: TextIO
    delimiter: str
    anchor_fields: List[str]
    drop_fields: List[str]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Wide to long',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='FILE', type=argparse.FileType('rt'))

    parser.add_argument('-d',
                        '--delimiter',
                        help='Input file delimiter',
                        metavar='delim',
                        type=str,
                        default='')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename',
                        metavar='out',
                        type=str,
                        default='')

    parser.add_argument('-a',
                        '--anchor',
                        help='Anchor fields',
                        metavar='anchor',
                        nargs='*',
                        type=str)

    parser.add_argument('-D',
                        '--drop',
                        help='Drop fields',
                        metavar='crop',
                        nargs='*',
                        type=str)

    args = parser.parse_args()

    basename, ext = os.path.splitext(args.file.name)

    if not args.outfile:
        args.outfile = basename + '_long' + ext

    if not args.delimiter:
        args.delimiter = ',' if ext == '.csv' else '\t'

    return Args(file=args.file,
                out_file=args.outfile,
                delimiter=args.delimiter,
                anchor_fields=args.anchor,
                drop_fields=args.drop)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    reader = csv.DictReader(args.file, delimiter=args.delimiter)
    fields = reader.fieldnames
    anchors = args.anchor_fields or [fields[0]]

    if bad_anchors := list(filter(lambda f: f not in fields, anchors)):
        sys.exit('--anchor {} not present in file'.format(
            ', '.join(bad_anchors)))

    out_flds = anchors + ['variable', 'value']
    skip = anchors + (args.drop_fields or [])
    var_cols = [f for f in fields if f not in skip]

    writer = csv.DictWriter(open(args.out_file, 'wt'), fieldnames=out_flds)
    writer.writeheader()

    num_written = 0
    for row in reader:
        base = {f: row[f] for f in anchors}
        for fld in var_cols:
            num_written += 1
            writer.writerow({**base, **{'variable': fld, 'value': row[fld]}})

    print(f'Done, wrote {num_written:,} to "{args.out_file}".')


# --------------------------------------------------
if __name__ == '__main__':
    main()

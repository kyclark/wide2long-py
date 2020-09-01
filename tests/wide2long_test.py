#!/usr/bin/env python3
"""tests for wide2long.py"""

import os
import csv
import random
import re
import string
from subprocess import getstatusoutput

PRG = './wide2long.py'
ADDRESSES_CSV = './tests/addresses.csv'
ADDRESSES_TSV = './tests/addresses.tsv'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PRG} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_input():
    """ Dies on bad input """

    bad = random_string()
    rv, out = getstatusoutput(f'{PRG} {bad}')
    assert rv != 0
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_bad_anchor():
    """ Dies on bad input """

    bad = random_string()
    rv, out = getstatusoutput(f'{PRG} {ADDRESSES_CSV} -a {bad}')
    assert rv != 0
    assert out.rstrip() == f'--anchor {bad} not present in file'


# --------------------------------------------------
def test_default():
    """ Run with defaults """

    out_file = './tests/addresses_long.csv'
    if os.path.isfile(out_file):
        os.remove(out_file)

    try:
        rv, out = getstatusoutput(f'{PRG} {ADDRESSES_CSV}')
        assert rv == 0
        assert out.strip() == f'Done, wrote 99 to "{out_file}".'
        assert os.path.isfile(out_file)

        reader = csv.DictReader(open(out_file), delimiter=',')
        rows = list(reader)
        assert len(rows) == 99

        assert rows[0]['first_name'] == 'James'
        assert rows[0]['variable'] == 'last_name'
        assert rows[0]['value'] == 'Butt'

        assert rows[-1]['first_name'] == 'Sage'
        assert rows[-1]['variable'] == 'web'
        assert rows[-1]['value'] == 'http://www.truhlarandtruhlarattys.com'

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_options():
    """ Run with options """

    out_file = random_string()
    if os.path.isfile(out_file):
        os.remove(out_file)

    try:
        cmd = (f'{PRG} -a first_name last_name -D company_name '
               f'-o {out_file} {ADDRESSES_TSV}')
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert out.strip() == f'Done, wrote 81 to "{out_file}".'
        assert os.path.isfile(out_file)

        reader = csv.DictReader(open(out_file), delimiter='\t')
        rows = list(reader)
        assert len(rows) == 81

        assert rows[0]['first_name'] == 'James'
        assert rows[0]['last_name'] == 'Butt'
        assert rows[0]['variable'] == 'address'
        assert rows[0]['value'] == '6649 N Blue Gum St'

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def random_string():
    """generate a random string"""

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

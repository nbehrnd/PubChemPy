# -*- coding: utf-8 -*-
"""
test_download
~~~~~~~~~~~~~

Test downloading.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import csv
import shutil
import tempfile

import pytest

from pubchempy import *


@pytest.fixture(scope='module')
def tmp_dir():
    dir = tempfile.mkdtemp()
    yield dir
    shutil.rmtree(dir)


def test_image_download(tmp_dir):
    download('PNG', os.path.join(tmp_dir, 'aspirin.png'), 'Aspirin', 'name')
    with pytest.raises(IOError):
        download('PNG', os.path.join(tmp_dir, 'aspirin.png'), 'Aspirin', 'name')
    download('PNG', os.path.join(tmp_dir, 'aspirin.png'), 'Aspirin', 'name', overwrite=True)


def test_csv_download_SMILES_depreciated(tmp_dir):
    """Test the download using a depreciated SMILES keyword

    For backward compatibility of source code using pubchempy.py as module,
    this tests the download by `CanonicalSMILES` (a keyword depreciated by
    the PubChem database since July 2025) resolved as `ConnectivitySMILES`.

    Keyword `SMILES` here seeks for any SMILES string about a compound, which
    either defaults to the canonical (or `ConnectivitySMILES`, PubChem's
    keyword since July 2025) as for e.g., benzene, or an isomeric (or now
    `AbsoluteSMILES`) one as for a compound with assigned stereochemistry e.g.,
    (S)-alanine (CID 5950).  For now, this check is used in conjunction with
    the complementary `test_csv_download_SMILES_contemporary` below."""
    download('CSV', os.path.join(tmp_dir, 's.csv'), [1, 2, 3, 5950], operation='property/CanonicalSMILES,SMILES')
    with open(os.path.join(tmp_dir, 's.csv')) as f:
        rows = list(csv.reader(f))
        assert rows[0] == ['CID', 'ConnectivitySMILES', 'SMILES']
        assert rows[1][0] == '1'
        assert rows[2][0] == '2'
        assert rows[3][0] == '3'
        assert rows[3][1] == 'C1=CC(C(C(=C1)C(=O)O)O)O'
        assert rows[3][2] == 'C1=CC(C(C(=C1)C(=O)O)O)O'
        assert rows[4][0] == '5950'
        assert rows[4][1] == 'CC(C(=O)O)N'
        assert rows[4][2] == 'C[C@@H](C(=O)O)N'

def test_csv_download_SMILES_contemporary(tmp_dir):
    """Test the download using a current SMILES keyword

    This test complementary to `test_csv_download_SMILES_depreciated` probes
    the search for `ConnectivitySMILES` (void of information about isotopes
    and stereochemistry) and `SMILES`.  Here, `SMILES` either defaults to
    `ConnectivitySMILES` or -- if assigned -- to `AbsoluteSMILES` (which since
    July 2025 replaces the now depreciated keyword `IsomericSMILES`) as for
    instance (S)-alanine (CID 5950).

    TODO: The two tests both define and use `SMILES` about _any_ SMILES locally.
    It might be useful to amend `pubchempy.py` with `SMILES` as a (fallback)
    criterion, for instance if the assignment of an `AbsoluteSMILES` in addition
    to a `ConnectivitySMILES` by the PubChem database is unknown to the user of
    `pubchempy.py`."""
    download('CSV', os.path.join(tmp_dir, 's2.csv'), [1, 2, 3, 5950], operation='property/ConnectivitySMILES,SMILES')
    with open(os.path.join(tmp_dir, 's2.csv')) as f:
        rows = list(csv.reader(f))
        assert rows[0] == ['CID', 'ConnectivitySMILES', 'SMILES']
        assert rows[1][0] == '1'
        assert rows[2][0] == '2'
        assert rows[3][0] == '3'
        assert rows[3][1] == 'C1=CC(C(C(=C1)C(=O)O)O)O'
        assert rows[3][2] == 'C1=CC(C(C(=C1)C(=O)O)O)O'
        assert rows[4][0] == '5950'
        assert rows[4][1] == 'CC(C(=O)O)N'
        assert rows[4][2] == 'C[C@@H](C(=O)O)N'


import pytest
from pathlib import Path
from Code.utils import get_data, save_data
from Code.SpreadsheetsManager import SpreadsheetsManager
import os 

TEST_DIR = Path(__file__).parent
FILES_DIR = TEST_DIR.parent / "Files_tests"
JSON_DIR = TEST_DIR.parent / "Json"

TEST_ALGS_XLSX = FILES_DIR / "test_algs.xlsx"
TEST_MEMO_XLXS = FILES_DIR / "test_memo.xlsx"
TEST_LPS_XLSX = FILES_DIR / "test_lps.xlsx"

TEST_JSON_FILE = JSON_DIR / "test_UF.json"

NUM_OF_EXPECTED_ALGS = 8

EXPECTED_MEMO_WORDS = ['Ada', 'Arbuz', 'Acid', 'Bat', 'Baca', 'Kubek', 'Czas', 'Cable']
EXPECTED_LPS = ['ZH', 'ZW', 'ZU', 'WZ', 'WU', 'UH', 'UZ', 'UW']

@pytest.fixture
def algs_spreadsheet_manager():
    return SpreadsheetsManager(TEST_ALGS_XLSX)

@pytest.fixture
def lps_spreadsheet_manager():
    return SpreadsheetsManager(TEST_LPS_XLSX)

@pytest.fixture
def memo_spreadsheet_manager():
    return SpreadsheetsManager(TEST_MEMO_XLXS)


def test_update_algs(algs_spreadsheet_manager):
    algs_spreadsheet_manager.update_algs()
    data = get_data(TEST_JSON_FILE)
    assert len(data) == NUM_OF_EXPECTED_ALGS
    assert data.get('UF;UB;UR')
    assert not data.get('UF;LU;DB')
    
    os.remove(TEST_JSON_FILE)


def test_update_memo(algs_spreadsheet_manager, memo_spreadsheet_manager):
    algs_spreadsheet_manager.update_algs()
    memo_spreadsheet_manager.update_memo()
    
    data = get_data(TEST_JSON_FILE)
    for record, expected_memo in zip(data.values(), EXPECTED_MEMO_WORDS):
        assert record['memo'] == expected_memo
    
    os.remove(TEST_JSON_FILE)
    
    
def test_update_lps(algs_spreadsheet_manager, lps_spreadsheet_manager):
    algs_spreadsheet_manager.update_algs()
    lps_spreadsheet_manager.update_lps()
    
    data = get_data(TEST_JSON_FILE)
    for record, expected_memo in zip(data.values(), EXPECTED_LPS):
        assert record['lp'] == expected_memo
    
    os.remove(TEST_JSON_FILE)
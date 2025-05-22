import pytest
from pathlib import Path

from Code.SpreadsheetsManager import SpreadsheetsManager

TEST_DIR = Path(__file__).parent
FILES_DIR = TEST_DIR.parent / "Files"
JSON_DIR = TEST_DIR.parent / "Json2"

def lp_manager():
    return SpreadsheetsManager(FILES_DIR / "lps.xlsx")


def test_update_lps():
    lp_manager().update_lps()

    updated_file = lp_manager().get_data(JSON_DIR / "edges_UF.json")

    assert updated_file["UF;BD;BL"]["algorithms"][0]["lp"] == "OM"  
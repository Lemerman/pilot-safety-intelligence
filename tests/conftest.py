import os
import sys
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from models.base import DATA_DIR, DB_PATH


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.makedirs(DATA_DIR, exist_ok=True)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

import os
import shutil
import pytest

from models.base import DATA_DIR, DB_PATH


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.makedirs(DATA_DIR, exist_ok=True)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

import os
import tempfile

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def temp_dir_name():
    with tempfile.TemporaryDirectory() as tempdirname:
        yield tempdirname


@pytest.fixture
def constitution_articles_path():
    return os.path.join(FIXTURES_DIR, "constitution.json")

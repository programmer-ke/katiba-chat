import json
import os
import tempfile
import pytest



FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def temp_dir_name():
    with tempfile.TemporaryDirectory() as tempdirname:
        yield tempdirname


@pytest.fixture(scope="session")
def constitution_articles():
    with open(os.path.join(FIXTURES_DIR, 'constitution.json'), 'r') as f:
        articles = json.load(f)
    return articles

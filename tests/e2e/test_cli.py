"""CLI test cases"""

import subprocess


def test_can_search_articles():
    query = "Who holds sovereign power?"
    result = subprocess.run(
        [f"python -m katiba_chat '{query}'"],
        shell=True,
        capture_output=True,
        check=True,
    )
    assert len(result.stdout) > 0
    text = result.stdout.decode("utf-8")
    assert "chapter" in text.lower()

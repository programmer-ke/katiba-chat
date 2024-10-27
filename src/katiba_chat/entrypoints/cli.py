"""CLI Interface"""
import json
import os
import pathlib
import sys

from .. import core
from ..adapters import retrieval


ARTICLES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'constitution_articles.json')


def main(query: str):

    index_dirname = user_data_dir("whoosh_index")
    index = retrieval.WhooshIndex(ARTICLES_PATH, index_dirname)
    query = core.Query(query)
    
    results = core.search(index, query)
    for r in results:
        print(r, "\n", file=sys.stdout)


def user_data_dir(file_name):
    r"""
    Get the OS specific location for the destination path

    Uses well known paths for data file by OS:

    Linux: XDG_DATA_HOME if defined, or ~/.local/share/<application>
    Windows: LOCALAPPDATA if defined, or C:\Users\<username>\AppData\Local\<application>
    Mac: ~/Library/Application Support/<application>
    """

    home = pathlib.Path.home()
    # get os specific path
    if sys.platform.startswith("win"):
        defined_location = os.getenv("LOCALAPPDATA")
        os_path = pathlib.Path(defined_location) if defined_location else home / "AppData"/ "Local"
    elif sys.platform.startswith("darwin"):
        os_path = pathlib.Path("~/Library/Application Support")
    elif sys.platform.startswith("linux"):
        defined_location = os.getenv("XDG_DATA_HOME")
        os_path = pathlib.Path(defined_location) if defined_location else home / ".local" / "share"

    # join with app dir
    path = os_path / "katiba_chat"

    # then with destination file
    return path.expanduser() / file_name


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <query>", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    main(query)

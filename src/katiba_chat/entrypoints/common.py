"""Common dependencies for all the entrypoints"""

import os
import pathlib
import sys

from decouple import config

from ..adapters import generation

LLM_API_KEY = config("LLM_API_KEY")
LLM_BASE_URL = config(
    "LLM_BASE_URL", default=generation.OpenAICompatibleLLM.OPENAI_BASE_URL
)
LLM_MODEL_NAME = config("LLM_MODEL_NAME")
ARTICLES_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "constitution_articles.json"
)

PROMPT_TEMPLATE = """
You are an expert in kenyan legal and constitutional affairs.
Answer the `QUESTION` based on the provided `CONTEXT`.
Use only facts from the `CONTEXT` when answering the `QUESTION`.
The `CONTEXT` contains the relevant articles from the Kenya 2010 constitution.

# QUESTION
{query}

# CONTEXT
{context}
"""


def user_data_dir(file_name):
    r"""
    Get the OS specific location for the destination path

    Uses well known paths for application data files by OS.

    Linux: XDG_DATA_HOME if defined, or ~/.local/share/<application>
    Windows: LOCALAPPDATA if defined,
      or C:\Users\<username>\AppData\Local\<application>
    Mac: ~/Library/Application Support/<application>
    """

    home = pathlib.Path.home()
    # get os specific path
    if sys.platform.startswith("win"):
        defined_location = os.getenv("LOCALAPPDATA")
        os_path = (
            pathlib.Path(defined_location)
            if defined_location
            else home / "AppData" / "Local"
        )
    elif sys.platform.startswith("darwin"):
        os_path = pathlib.Path("~/Library/Application Support")
    else:
        defined_location = os.getenv("XDG_DATA_HOME")
        os_path = (
            pathlib.Path(defined_location)
            if defined_location
            else home / ".local" / "share"
        )

    # join with app dir
    path = os_path / "katiba_chat"

    # then with destination file
    return path.expanduser() / file_name

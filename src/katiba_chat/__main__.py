"""CLI entrypoint"""

import sys

from .entrypoints.cli import entrypoint as cli_entrypoint

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} '<query>'", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    cli_entrypoint(query)

"""Allow the app to be started with python -m todo."""

import sys

from todo.cli import main

if __name__ == "__main__":
    sys.exit(main())

"""Start the Proserve Client Task Inventory Management.

Run from this folder:

    python -m pip install -r requirements.txt
    python main.py
    python harness/run_all.py
"""

import sys

from todo.cli import main

if __name__ == "__main__":
    sys.exit(main())

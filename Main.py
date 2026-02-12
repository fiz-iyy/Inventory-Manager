import os
from pathlib import Path

from gui import InventoryApp


def main() -> None:
    os.chdir(Path(__file__).resolve().parent)
    app = InventoryApp()
    app.run()


if __name__ == "__main__":
    main()

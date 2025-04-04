import sys
from pathlib import Path
from tkinter import Tk

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from views.main_menu import MainMenu
from shared.logger import Logger

def main() -> None:
    try:
        root: Tk = Tk()
        app = MainMenu(root)
        app.start_app()
    except Exception as e:
        Logger.error(f"Error in main(): {e}")

if __name__ == "__main__":
    main()
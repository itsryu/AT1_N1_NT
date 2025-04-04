import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from shared.logger import Logger
from cli.views.main_menu import MainMenu

def main() -> None:
    try:
        MainMenu().display()
    except Exception as e:
        Logger.error(f"Erro: {e}")

if __name__ == "__main__":
    main()
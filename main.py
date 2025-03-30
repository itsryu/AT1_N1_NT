from tkinter import Tk
from views.main_menu import MainMenu
from utils.logger import Logger

def main() -> None:
    try:
        root: Tk = Tk()
        app = MainMenu(root)
        app.start_app()
    except Exception as e:
        Logger.error(f"Error in main(): {e}")

if __name__ == "__main__":
    main()
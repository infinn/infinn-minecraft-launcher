import tkinter as tk
from src.components.main_window import MainWindow
from src.config import WINDOW_TITLE


if __name__ == "__main__":
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    app = MainWindow(root)

    root.mainloop()

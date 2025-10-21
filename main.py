import tkinter as tk
from src.components.main_window import MainWindow
from src.config import WINDOW_TITLE, BG_BLACK


if __name__ == "__main__":
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    root.resizable(False, False)
    root.configure(bg=BG_BLACK)
    root.iconbitmap('./logo.ico') 

    app = MainWindow(root)

    root.mainloop()

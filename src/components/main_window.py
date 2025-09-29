import tkinter as tk
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_GRAY, TXT_WHITE

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        master.configure(background='#161717')
        
        self._create_widgets()

    def _create_widgets(self):
        app_name_txt = tk.Label(self.master, text="Minecraft Launcher", fg=TXT_WHITE, bg=BG_BLACK, font=("Arial", 50))
        app_name_txt.pack(pady=20)

        username_entry = tk.Entry(self.master, fg=TXT_WHITE, bg=BG_BLACK)
        username_entry.pack(pady=20)



        button = tk.Button(self.master, text="Click Me", command=self._on_button_click, fg=TXT_WHITE, bg=BG_BLACK)
        button.pack(pady=10)

        version_txt = tk.Label(self.master, text="MinecraftLauncher v0.1 (by Infinn)",  fg=BG_GRAY, bg=BG_BLACK)
        version_txt.pack()

    def _on_button_click(self):
        print("Botón presionado.")
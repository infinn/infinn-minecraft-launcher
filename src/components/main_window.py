import tkinter as tk
import os

from tkinter import ttk
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_GRAY, TXT_WHITE
from src.utils import MineManager


USER_WINDOWS = os.environ['USERNAME']

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        master.configure(background=BG_BLACK)

        self.mine = MineManager(USER_WINDOWS)

        self._create_widgets(self.mine.get_local_version())

        

    def _create_widgets(self, versions):
        app_name_lbl = tk.Label(self.master, text="Minecraft Launcher", fg=TXT_WHITE, bg=BG_BLACK, font=("Arial", 30))
        app_name_lbl.pack(pady=20)


        # --- User section ---
        data_frame = tk.Frame(self.master)
        data_frame.configure(background=BG_GRAY)
        
        data_frame.pack(pady=20, padx=20, ipady=20, ipadx=20, fill="both", expand=True) 

        data_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        data_frame.grid_columnconfigure(1, weight=2, minsize=300) 
        
        # username entry 
        username_lbl = tk.Label(data_frame, text="Username:", fg=TXT_WHITE, bg=BG_GRAY)
        username_lbl.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        self.username_entry = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 

        # version 
        version_lbl = tk.Label(data_frame, text="Version:", fg=TXT_WHITE, bg=BG_GRAY)
        version_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="nsew") 
        
        self.verision_cmbbx = ttk.Combobox(data_frame, state="readonly", values=versions)
        self.verision_cmbbx.grid(row=1, column=1, columnspan=2, pady=10) 
        self.verision_cmbbx.current(0)

        # memory
        memory_lbl = tk.Label(data_frame, text="Memory:", fg=TXT_WHITE, bg=BG_GRAY)
        memory_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="nsew") 

        # directory
        directory_lbl = tk.Label(data_frame, text="Directory:", fg=TXT_WHITE, bg=BG_GRAY)
        directory_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="nsew") 

        self.directory_user_lbl = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK)
        self.directory_user_lbl.grid(row=2, column=1, padx=5, pady=5, sticky="nsew") 
        self.directory_user_lbl.insert(0, self.mine.get_minecrat_directory())



        # --- Status section ---
        status_frame = tk.Frame(self.master)
        status_frame.configure(background=BG_GRAY)

        status_frame.pack(pady=20, padx=20, ipady=20, ipadx=20, fill="both", expand=True) 

        status_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        status_frame.grid_columnconfigure(1, weight=2, minsize=300) 

        # status
        status_lbl = tk.Label(status_frame, text="Status:", fg=TXT_WHITE, bg=BG_GRAY)
        status_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 

        self.status_info = tk.Label(status_frame, text="Running", fg=TXT_WHITE, bg=BG_GRAY)
        self.status_info.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 

        self.progressbar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=100)
        self.progressbar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew") 



        # --- Button section ---
        buttons_frame = tk.Frame(self.master)
        buttons_frame.configure(background=BG_BLACK)

        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        buttons_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        buttons_frame.grid_columnconfigure(1, weight=1, minsize=100) 

        download_button_btn = tk.Button(buttons_frame, text="Download", command=self._on_button_click, fg=TXT_WHITE, bg=BG_BLACK)
        download_button_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        launch_button_btn = tk.Button(buttons_frame, text="Launch", command=self._on_play_button, fg=TXT_WHITE, bg=BG_BLACK)
        launch_button_btn.grid(row=0, column=1, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 



        version_app_lbl = tk.Label(self.master, text="MinecraftLauncher v0.1 (by Infinn)", fg=BG_GRAY, bg=BG_BLACK)
        version_app_lbl.pack()

    def _on_button_click(self):
        print("test")

    def _on_play_button(self):
        print(self.verision_cmbbx.get())
        print(self.username_entry.get())
        self.progressbar.step(50)
        self.status_info.config(text="Starting", fg="yellow")
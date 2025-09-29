import tkinter as tk
from tkinter import ttk
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_GRAY, TXT_WHITE

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        master.configure(background=BG_BLACK)
        
        self._create_widgets()

    def _create_widgets(self):
        app_name_lbl = tk.Label(self.master, text="Minecraft Launcher", fg=TXT_WHITE, bg=BG_BLACK, font=("Arial", 50))
        app_name_lbl.pack(pady=20)



        # --- User section ---
        data_frame = tk.Frame(self.master)
        data_frame.configure(background=BG_GRAY)
        
        data_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        data_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        data_frame.grid_columnconfigure(1, weight=2, minsize=300) 
        
        # username entry 
        username_lbl = tk.Label(data_frame, text="Username:", fg=TXT_WHITE, bg=BG_GRAY)
        username_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 

        username_entry = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK)
        username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 

        # version 
        version_lbl = tk.Label(data_frame, text="Version:", fg=TXT_WHITE, bg=BG_GRAY)
        version_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="nsew") 
        
        verision_cmbbx = ttk.Combobox(data_frame, state="readonly", values=["Python", "C", "C++", "Java"])
        verision_cmbbx.grid(row=1, column=1, columnspan=2, pady=10) 

        # memoria
        memory_lbl = tk.Label(data_frame, text="Memory:", fg=TXT_WHITE, bg=BG_GRAY)
        memory_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="nsew") 

        # directory
        directory_lbl = tk.Label(data_frame, text="Directory:", fg=TXT_WHITE, bg=BG_GRAY)
        directory_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="nsew") 



        # --- Status section ---
        status_frame = tk.Frame(self.master)
        status_frame.configure(background=BG_GRAY)

        status_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        status_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        status_frame.grid_columnconfigure(1, weight=2, minsize=300) 

        # status
        status_lbl = tk.Label(status_frame, text="Status:", fg=TXT_WHITE, bg=BG_GRAY)
        status_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 

        status_info = tk.Label(status_frame, text="Running", fg=TXT_WHITE, bg=BG_GRAY)
        status_info.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 



        # --- Button section ---
        buttons_frame = tk.Frame(self.master)
        buttons_frame.configure(background=BG_BLACK)

        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        buttons_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        buttons_frame.grid_columnconfigure(1, weight=1, minsize=100) 

        download_button_btn = tk.Button(buttons_frame, text="Download", command=self._on_button_click, fg=TXT_WHITE, bg=BG_BLACK)
        download_button_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 

        launch_button_btn = tk.Button(buttons_frame, text="Launch", command=self._on_button_click, fg=TXT_WHITE, bg=BG_BLACK)
        launch_button_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 



        version_app_lbl = tk.Label(self.master, text="MinecraftLauncher v0.1 (by Infinn)", fg=BG_GRAY, bg=BG_BLACK)
        version_app_lbl.pack()

    def _on_button_click(self):
        print("Botón presionado.")
import os
import tkinter as tk

from tkinter import ttk
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_SECTION, TXT_WHITE, BORDER_BLACK, BORDER_WHITE, BTN_GRAY
from tkinter import filedialog

_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logo.ico")

class SettingsWindows:
    def __init__(self, main_loop, mine_manager):
        self.setting_windows = tk.Toplevel(main_loop)
        self.setting_windows.geometry("400x500")
        self.setting_windows.title("Settings")
        self.setting_windows.configure(background=BG_BLACK)

        if os.path.exists(_icon_path):
            self.setting_windows.iconbitmap(_icon_path)

        self.mine = mine_manager

        self.new_directory = ""

        self._create_widgets()
        
    
    def _create_widgets(self):
        data_frame = tk.Frame(self.setting_windows)
        data_frame.configure(background=BG_SECTION, highlightthickness=1.5, highlightbackground=BORDER_BLACK)
        
        data_frame.pack(pady=20, padx=20, ipady=20, ipadx=20, fill="x") 

        data_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        data_frame.grid_columnconfigure(1, weight=2, minsize=200) 
        data_frame.grid_columnconfigure(2, weight=3, minsize=50) 

        # directory
        directory_lbl = tk.Label(data_frame, text="Directory:", fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 10))
        directory_lbl.grid(row=4, column=0, padx=5, pady=5, sticky="e") 

        self.directory_user_lbl = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK, font=("Minecraft", 10))
        self.directory_user_lbl.grid(row=4, column=1, padx=5, pady=5, sticky="nsew") 

        self.directory_btn = tk.Button(data_frame, text="Search", command=self._on_directory_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1, font=("Minecraft", 10))
        self.directory_btn.grid(row=4, column=2, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        # --- Button section ---
        buttons_frame = tk.Frame(self.setting_windows)
        buttons_frame.configure(background=BG_BLACK)

        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        buttons_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        buttons_frame.grid_columnconfigure(1, weight=1, minsize=100) 

        cancel_button_btn = tk.Button(buttons_frame, text="Cancel", command=self.setting_windows.destroy, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1, font=("Minecraft", 10))
        cancel_button_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        save_button_btn = tk.Button(buttons_frame, text="Save", command=self._on_save_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK,borderwidth=1, font=("Minecraft", 10))
        save_button_btn.grid(row=0, column=1, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        # --- Set variable from save --- 

        # path
        self.directory_user_lbl.insert(0, self.mine.MINECRAFT_DIRECTORY)


    def _on_save_button(self):
        self.mine.set_minecrat_directory(self.new_directory)
        self.setting_windows.destroy()
    
    def _on_directory_button(self):
        folder_selected = filedialog.askdirectory()

        if folder_selected:
            self.directory_user_lbl.delete(0, "end")
            self.directory_user_lbl.insert(0, folder_selected)

            self.new_directory = folder_selected
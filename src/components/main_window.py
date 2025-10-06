import tkinter as tk
import os
import asyncio
import threading

from tkinter import ttk
from tkinter import filedialog
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_SECTION, TXT_WHITE, BORDER_BLACK, BORDER_WHITE, BTN_GRAY
from src.utils import MineManager
from src.components.settings_window import SettingsWindows


USER_WINDOWS = os.environ['USERNAME']

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        master.configure(background=BG_BLACK)

        self.mine = MineManager(USER_WINDOWS)

        self.mine.callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max,
        }

        self._create_widgets()

        

    def _create_widgets(self):
        app_name_lbl = tk.Label(self.master, text="Infinn Launcher", fg=TXT_WHITE, bg=BG_BLACK, font=("Arial", 30))
        app_name_lbl.pack(pady=20)


        # --- User section ---
        data_frame = tk.Frame(self.master)
        data_frame.configure(background=BG_SECTION, highlightthickness=1.5, highlightbackground=BORDER_BLACK)
        
        data_frame.pack(pady=20, padx=20, ipady=20, ipadx=20, fill="x") 

        data_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        data_frame.grid_columnconfigure(1, weight=2, minsize=300) 
        data_frame.grid_columnconfigure(2, weight=3, minsize=50) 
        
        # username entry 
        username_lbl = tk.Label(data_frame, text="Username:", fg=TXT_WHITE, bg=BG_SECTION)
        username_lbl.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="e") 

        self.username_entry = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew", columnspan=2) 

        # version 
        version_lbl = tk.Label(data_frame, text="Version:", fg=TXT_WHITE, bg=BG_SECTION, justify=tk.RIGHT)
        version_lbl.grid(row=1, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="e") 
        
        self.verision_cmbbx = ttk.Combobox(data_frame, state="readonly")
        self.verision_cmbbx.grid(row=1, column=1, columnspan=2, pady=10, sticky="nsew") 

        self.only_local_var = tk.BooleanVar()
        self.only_local_checkbtn = tk.Checkbutton(data_frame, text="local", bg=BG_SECTION, fg=TXT_WHITE, variable=self.only_local_var, command=self._update_version)
        self.only_local_checkbtn.grid(row=2, column=0, columnspan=2) 

        self.only_released_var = tk.BooleanVar()
        self.only_released_checkbtn = tk.Checkbutton(data_frame, text="released", fg=TXT_WHITE, bg=BG_SECTION, variable=self.only_released_var, command=self._update_version)
        self.only_released_checkbtn.grid(row=2, column=1, columnspan=2, sticky="w") 




        # --- Status section ---
        status_frame = tk.Frame(self.master)
        status_frame.configure(background=BG_SECTION, highlightthickness=1.5, highlightbackground=BORDER_BLACK)

        status_frame.pack(pady=20, padx=20, ipady=20, ipadx=20, fill="x") 

        status_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        status_frame.grid_columnconfigure(1, weight=2, minsize=350) 

        # status
        status_lbl = tk.Label(status_frame, text="Status:", fg=TXT_WHITE, bg=BG_SECTION)
        status_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e") 

        self.status_info = tk.Label(status_frame, text="Waiting", fg=TXT_WHITE, bg=BG_SECTION)
        self.status_info.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

        self.progressbar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=100)
        self.progressbar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2) 

        # logs
        self.logs_text = tk.Text(status_frame, height=5, state='disabled')
        self.logs_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)
        self.logs_text.config(fg=TXT_WHITE, bg=BG_BLACK)


        # --- Button section ---
        buttons_frame = tk.Frame(self.master)
        buttons_frame.configure(background=BG_BLACK)

        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True) 

        buttons_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        buttons_frame.grid_columnconfigure(1, weight=1, minsize=100) 

        download_button_btn = tk.Button(buttons_frame, text="Download", command=self._on_download_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1)
        download_button_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        launch_button_btn = tk.Button(buttons_frame, text="Launch", command=self._on_play_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK,borderwidth=1)
        launch_button_btn.grid(row=0, column=1, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 



        version_app_lbl = tk.Label(self.master, text="MinecraftLauncher v0.1 (by Infinn)", fg=BG_SECTION, bg=BG_BLACK)
        version_app_lbl.pack()


        settings_btn = tk.Button(buttons_frame, text="setting", command=self._on_setting_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1)
        settings_btn.grid(row=1, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew") 

        # --- Set variable from save --- 

        # username
        self.username_entry.insert(0, self.mine.configuration["username"])
        
        # version
        self.verision_cmbbx.config(values=self.mine.get_version())
        self.verision_cmbbx.current(0)

        self.only_local_checkbtn.select()
        self.only_released_checkbtn.select()
        

        #logs
        self._set_log("Welcome")


    def _on_play_button(self):
        self.status_info.config(text="Starting", fg="yellow")
        self._set_log("Starting Minecraft", "title")

        username = self.username_entry.get()
        version = self.verision_cmbbx.get().split(" ")[0]

        if version and username:
            options = {
                "user":self.username_entry.get(),
                "version":self.verision_cmbbx.get().split(" ")[0]
            }
            
            self.progressbar.config(mode="indeterminate")
            self.progressbar.start(10)
            
            self.mine.play_minecraft(options)

        if not version:
            tk.messagebox.showwarning(title="Error", message="No se ha ingresado una versión")
            self.verision_cmbbx.focus()
            self._set_log("not version selected", "error")
            self.status_info.config(text="Error in version", fg="red")
        if not username:
            tk.messagebox.showwarning(title="Error", message="No se ha ingresado el username")
            self.username_entry.focus()
            self._set_log("not username", "error")
            self.status_info.config(text="Error in username", fg="red")
    
    def _on_download_button(self):
        version = self.verision_cmbbx.get().split(" ")[0]
        self.status_info.config(text="Downloading...", fg="yellow")
        self._set_log("Start Download", "title")

        thread = threading.Thread(
            target=self._start_installation_thread,
            args=(version,),
            daemon=True
        )
        thread.start()
    
    def _start_installation_thread(self, version):
        self._set_log("Start Installation")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            loop.run_until_complete(self.mine.install_minecraft(version))
            
        except Exception as e:
            self._set_log(e, "error")
            
        finally:
            loop.close()

    def set_status(self, text: str):
        self.status_info.config(text=text, fg="yellow")
        self._set_log(text, "installing")
        self.master.update_idletasks()

    def set_progress(self, value: int):
        self.progressbar["value"] = value
        self.master.update_idletasks()

    def set_max(self, max_value: int):
        self.progressbar["maximum"] = max_value
        self.master.update_idletasks()

    def _update_version(self):
        only_local = self.only_local_var.get()
        only_release = self.only_released_var.get()

        new_version = self.mine.get_version(only_local, only_release)

        self.verision_cmbbx.config(values=new_version)
        self.master.update_idletasks()

    def _set_log(self, text, type="info"):
        if type == "title":
            self.logs_text.configure(state='normal')
            self.logs_text.insert("end", f"--- {text} --- \n")
            self.logs_text.configure(state='disabled')
        else:
            self.logs_text.configure(state='normal')
            self.logs_text.insert("end", f"[{type}] {text} \n")
            self.logs_text.configure(state='disabled')

    def _on_setting_button(self):
        SettingsWindows(self.master, self.mine)
import tkinter as tk
import os, ctypes
import asyncio
import threading
import json

from tkinter import ttk
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_BLACK, BG_SECTION, TXT_WHITE, BORDER_BLACK, BORDER_WHITE, BTN_GRAY
from src.utils import MineManager, load_configuration, get_parse_version, play_minecraft
from src.components.settings_window import SettingsWindows
from src.Globals import Globals
from src.core.version_collection import VersionUtils


USER_WINDOWS = os.environ['USERNAME']

class MainWindow:
    def __init__(self, master):
        self.master = master
        
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        master.configure(background=BG_BLACK)

        self._init_configurtation()
        load_configuration()

        self.VerUtils = VersionUtils()

        self.is_download_btn = False
        self.is_play_btn = False

        self.mine = MineManager(USER_WINDOWS)

        self.mine.callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max,
        }
        
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../font/Minecraft.ttf"))
        ctypes.windll.gdi32.AddFontResourceW(font_path)

        self._create_widgets()

    def _init_configurtation(self):
        if os.path.isfile(Globals.cacheFile):
            try:
                with open(Globals.cacheFile, "r", encoding="utf-8") as f:
                    data = json.load(f)

                Globals.minecraftDir = data.get("minecraftDir", Globals.defaultMinecraftDir)
                Globals.firstLaunch = False
                Globals.latestVersionUsage = data.get("latestVersionUsage", Globals.defaultMinecraftDir)

            except Exception as e:
                Globals.minecraftDir = Globals.defaultMinecraftDir

        else:
            Globals.minecraftDir = Globals.defaultMinecraftDir
            Globals.firstLaunch = True

            self._save_cache(Globals.minecraftDir)
    
    def _save_cache(self, minecraft_dir):
        data = {
            "minecraftDir": minecraft_dir,
            "latestVersionUsage": ""
        }

        try:
            with open(Globals.cacheFile, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Error al guardar el cache:", e)

    def _create_widgets(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        image_path = os.path.join(base_path, "image", "mine_logo.png")

        app_logo = tk.PhotoImage(file=image_path)
        app_name_lbl = tk.Label(self.master, image=app_logo, bg=BG_BLACK)
        app_name_lbl.image = app_logo
        app_name_lbl.pack(pady=40)

        # --- User section ---
        data_frame = tk.Frame(self.master)
        data_frame.configure(background=BG_SECTION, highlightthickness=1.5, highlightbackground=BORDER_BLACK)
        
        data_frame.pack(pady=5, padx=20, fill="x") 

        data_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        data_frame.grid_columnconfigure(1, weight=2, minsize=100) 
        data_frame.grid_columnconfigure(2, weight=3, minsize=100) 
        
        # username entry 
        username_lbl = tk.Label(data_frame, text="Username:", fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 10))
        username_lbl.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="e") 

        self.username_entry = tk.Entry(data_frame, fg=TXT_WHITE, bg=BG_BLACK, font=("Minecraft", 10))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew", columnspan=2) 

        # version 
        version_lbl = tk.Label(data_frame, text="Version:", fg=TXT_WHITE, bg=BG_SECTION, justify=tk.RIGHT, font=("Minecraft", 10))
        version_lbl.grid(row=1, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="e") 
        
        self.verision_cmbbx = ttk.Combobox(data_frame, state="readonly", font=("Minecraft", 10))
        self.verision_cmbbx.grid(row=1, column=1, columnspan=2, padx=5, pady=10, sticky="nsew") 
        self.verision_cmbbx.bind("<<ComboboxSelected>>", self._on_change_version)

        self.only_local_var = tk.BooleanVar()
        self.only_local_checkbtn = tk.Checkbutton(data_frame, text="local", bg=BG_SECTION, fg=TXT_WHITE, variable=self.only_local_var, command=self._update_version, font=("Minecraft", 10))
        self.only_local_checkbtn.grid(row=2, column=1, columnspan=1, sticky="w") 

        self.only_released_var = tk.BooleanVar()
        self.only_released_checkbtn = tk.Checkbutton(data_frame, text="released", fg=TXT_WHITE, bg=BG_SECTION, variable=self.only_released_var, command=self._update_version, font=("Minecraft", 10))
        self.only_released_checkbtn.grid(row=2, column=2, columnspan=1, sticky="w") 


        # --- Button section ---
        buttons_frame = tk.Frame(self.master)
        buttons_frame.configure(background=BG_BLACK)

        buttons_frame.pack(pady=20, padx=20, fill="x") 

        buttons_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        buttons_frame.grid_columnconfigure(1, weight=1, minsize=100) 

        self.play_btn = tk.Button(buttons_frame, text="Play", command=self._on_main_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1, font=("Minecraft", 10))
        self.play_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew", columnspan=2) 

        # --- Status section ---
        status_frame = tk.Frame(self.master)
        status_frame.configure(background=BG_SECTION, highlightthickness=1.5, highlightbackground=BORDER_BLACK)

        status_frame.pack(pady=5, padx=20, fill="x") 

        status_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        status_frame.grid_columnconfigure(1, weight=2, minsize=250) 

        # status
        status_lbl = tk.Label(status_frame, text="Status:", fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 10))
        status_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e") 

        self.status_info = tk.Label(status_frame, text="Waiting", fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 10))
        self.status_info.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

        self.progressbar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=100)
        self.progressbar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2) 

        # logs
        self.logs_text = tk.Text(status_frame, height=5, state='disabled', font=("Minecraft", 10))
        self.logs_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)
        self.logs_text.config(fg=TXT_WHITE, bg=BG_BLACK)
        
        settings_btn = tk.Button(self.master, text="setting", command=self._on_setting_button, fg="white", bg=BTN_GRAY, highlightthickness=1.5, highlightbackground=BORDER_BLACK, borderwidth=1, font=("Minecraft", 10))
        settings_btn.pack()

        version_app_lbl = tk.Label(self.master, text="MinecraftLauncher v0.1 (by Infinn)", fg=BG_SECTION, bg=BG_BLACK, font=("Minecraft", 10))
        version_app_lbl.pack()

        # --- Set variable from save --- 

        # username
        self.username_entry.insert(0, self.mine.configuration["username"])
        
        # version
        version_list = get_parse_version(self.VerUtils.getInstalledVersions())

        self.verision_cmbbx.config(values=version_list)
        self.verision_cmbbx.current(0)

        self.only_local_checkbtn.select()
        self.only_released_checkbtn.select()
        

        #logs
        self._set_log("Welcome")


    def _on_play_button(self):
        self.launch_button_btn["state"] = "disabled"
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
            
            play_minecraft(options)

        if not version:
            tk.messagebox.showwarning(title="Error", message="No se ha ingresado una versión")
            self.verision_cmbbx.focus()
            self._set_log("not version selected", "error")
            self.status_info.config(text="Error in version", fg="red")
            self.launch_button_btn["state"] = "normal"
        if not username:
            tk.messagebox.showwarning(title="Error", message="No se ha ingresado el username")
            self.username_entry.focus()
            self._set_log("not username", "error")
            self.status_info.config(text="Error in username", fg="red")
            self.launch_button_btn["state"] = "normal"
    
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

        new_version = []

        if only_local:
            version_source = self.VerUtils.getInstalledVersions()
        else:
            version_source = self.VerUtils.getVersionList()

        if only_release:
            filtered_versions = [
                version for version in version_source 
                if version.get('type') == 'release'
        ]
        else:
            filtered_versions = version_source

        new_version = [
            f"{v['id']} ({v['type']})"
            for v in filtered_versions
        ]

        self.verision_cmbbx.config(values=new_version)
        self.verision_cmbbx.current(0)
        self._on_change_version("test")
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

    def _on_change_version(self, event):
        version_select = self.verision_cmbbx.get().split(" ")[0]
        version_download = self.VerUtils.getInstalledVersions()

        is_download = any(v['id'] == version_select for v in version_download)

        if is_download:
            self.play_btn.config(text="Play")
            self.is_download_btn = False
            self.is_play_btn = True
        else:
            self.play_btn.config(text="Download")
            self.is_download_btn = True
            self.is_play_btn = False

    def _on_main_button(self):

        if self.is_play_btn:
            self._on_play_button()

        elif self.is_download_btn:
            self._on_download_button()

        else:
            self._set_log("Error in play")
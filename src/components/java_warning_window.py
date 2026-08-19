import os
import tkinter as tk
import webbrowser

from src.config import BG_BLACK, BG_SECTION, TXT_WHITE, BORDER_BLACK, BTN_GRAY


JAVA_DOWNLOAD_URL = "https://www.java.com/"

_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logo.ico")


class JavaWarningWindow:
    def __init__(self, main_loop):
        self.window = tk.Toplevel(main_loop)
        self.window.geometry("400x250")
        self.window.title("Java Not Found")
        self.window.configure(background=BG_BLACK)
        self.window.resizable(False, False)
        self.window.grab_set()

        if os.path.exists(_icon_path):
            self.window.iconbitmap(_icon_path)

        self._create_widgets()

    def _create_widgets(self):
        warning_frame = tk.Frame(self.window)
        warning_frame.configure(
            background=BG_SECTION,
            highlightthickness=1.5,
            highlightbackground=BORDER_BLACK,
        )
        warning_frame.pack(pady=20, padx=20, fill="x")

        warning_icon = tk.Label(
            warning_frame, text="!", fg="#ffcc00", bg=BG_SECTION,
            font=("Minecraft", 24, "bold"),
        )
        warning_icon.pack(pady=(15, 5))

        warning_title = tk.Label(
            warning_frame, text="Java Not Found",
            fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 12, "bold"),
        )
        warning_title.pack(pady=(0, 5))

        warning_msg = tk.Label(
            warning_frame,
            text="Minecraft requires Java to run.\nPlease install Java to continue.",
            fg=TXT_WHITE, bg=BG_SECTION, font=("Minecraft", 10),
            justify=tk.CENTER,
        )
        warning_msg.pack(pady=(0, 15))

        buttons_frame = tk.Frame(self.window)
        buttons_frame.configure(background=BG_BLACK)
        buttons_frame.pack(pady=10, padx=20, fill="x")

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        download_btn = tk.Button(
            buttons_frame, text="Download Java",
            command=self._on_download, fg="white", bg=BTN_GRAY,
            highlightthickness=1.5, highlightbackground=BORDER_BLACK,
            borderwidth=1, font=("Minecraft", 10),
        )
        download_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew")

        close_btn = tk.Button(
            buttons_frame, text="Close",
            command=self.window.destroy, fg="white", bg=BTN_GRAY,
            highlightthickness=1.5, highlightbackground=BORDER_BLACK,
            borderwidth=1, font=("Minecraft", 10),
        )
        close_btn.grid(row=0, column=1, padx=5, pady=5, ipady=5, ipadx=5, sticky="nsew")

    def _on_download(self):
        webbrowser.open(JAVA_DOWNLOAD_URL)

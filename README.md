<div align="center">

![Minecraft logo](/image/mine_logo.png)

# Infinn Launcher

A lightweight, dark-themed Minecraft Java Edition launcher built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)

</div>

---

## Features

- **Version Management** — Browse and select from both locally installed versions and the full Mojang version manifest
- **One-Click Install** — Download and install any official Minecraft version with real-time progress tracking
- **Smart Play/Download** — The main button automatically switches between *Play* and *Download* based on whether the selected version is installed
- **Offline-Mode Launch** — Enter any username and play (no Microsoft authentication required)
- **Custom Game Directory** — Change your `.minecraft` folder path from the settings dialog
- **Java Auto-Detection** — Checks for Java on startup and prompts to download if missing
- **Persistent Settings** — Remembers your game directory and last-used version between sessions
- **Dark Theme UI** — Clean, modern dark interface with the Minecraft font

## Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows 10/11 |
| **Python** | 3.11 or higher |
| **Java** | Java Runtime (required to launch Minecraft) |
| **Internet** | Required for version manifest and downloads |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Infinn/infinn-minecraft-launcher.git
cd infinn-minecraft-launcher
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the launcher

```bash
python main.py
```

## Usage

1. **Launch** the application with `python main.py`
2. **Enter** your Minecraft username
3. **Select** a version from the dropdown
   - Toggle *Local only* to show only installed versions
   - Toggle *Released only* to hide snapshots, betas, and alphas
4. **Download** or **Play** — the button adapts to the selected version's install state
5. **Configure** your `.minecraft` directory via the settings gear icon

## Project Structure

```
infinn-minecraft-launcher/
├── main.py                         # Entry point
├── logo.ico                        # Window icon
├── requirements.txt                # Python dependencies
├── image/
│   └── mine_logo.png               # UI logo
└── src/
    ├── config.py                   # Window dimensions, colors, version constant
    ├── Globals.py                  # Global runtime state
    ├── utils.py                    # File I/O, install logic, cache, Java/internet checks
    ├── profile.py                  # Profile model (per-profile launcher settings)
    ├── font/
    │   └── Minecraft.ttf           # Bundled Minecraft font
    ├── core/
    │   └── version_collection.py   # Mojang manifest fetcher, version list builder
    └── components/
        ├── main_window.py          # Primary UI — version picker, play/download, logs
        ├── settings_window.py      # Settings dialog — game directory picker
        └── java_warning_window.py  # Java-not-found warning popup
```

## Architecture

```
main.py
  └─> MainWindow
        ├─> VersionUtils          (fetches Mojang manifest + scans local versions)
        ├─> MineManager           (configuration.json I/O, install orchestration)
        ├─> Cache helpers         (reads/writes src/cache.json)
        └─> SettingsWindows       (modal dialog for .minecraft path)
```

**Startup flow:** The launcher reads the cached `.minecraft` path, fetches the Mojang version manifest over HTTP, scans local installed versions, checks for Java, and renders the UI.

**Install flow:** Downloads run in a background thread with a dedicated `asyncio` event loop. Progress callbacks update the UI progress bar and log panel in real time.

**Launch flow:** Builds the Minecraft launch command via `minecraft_launcher_lib` and executes it as a subprocess.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| GUI | Tkinter / ttk |
| Minecraft Lib | [minecraft-launcher-lib](https://pypi.org/project/minecraft-launcher-lib/) |
| HTTP | requests |
| Font | Bundled `Minecraft.ttf` (loaded via Windows GDI) |

## Important Notes

- **Windows-only** — The launcher uses Windows-specific APIs (`ctypes.windll`, `subprocess.CREATE_NO_WINDOW`) and will not run on Linux or macOS.
- **Offline-mode** — This launcher does not implement Microsoft/Mojang authentication. Usernames are used for offline-mode sessions only.
- **Java required** — Minecraft requires a Java installation. The launcher will detect and warn you if Java is not found.

## Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/Infinn/infinn-minecraft-launcher.git
cd infinn-minecraft-launcher
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

No build step, no test suite — just run `python main.py`.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

**Infinn** — [GitHub](https://github.com/Infinn)

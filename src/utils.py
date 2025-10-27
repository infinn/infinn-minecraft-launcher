import json
import os
import minecraft_launcher_lib
import subprocess
import ctypes

from src.config import VERSION_LAUNCHER
from src.Globals import Globals

class MineManager:
    def __init__(self, user):
        self.MINECRAFT_DIRECTORY = f"C://Users//{user}//AppData//Roaming//.minecraft"
        self.SRC_JSON = f"{self.MINECRAFT_DIRECTORY}//configuration.json"

        self.configuration = {}

        self._ensure_file()
        
        self.callback = {}
    
    def _ensure_file(self):
        if not os.path.isfile(self.SRC_JSON):
            self._create_default_file()
        else:
            with open(self.SRC_JSON, "r", encoding="utf-8") as f:
                try:
                    self.configuration = json.load(f)
                except json.JSONDecodeError:
                    self._create_default_file()

    def _create_default_file(self):
        default_data = {
            "username": "",
            "uuid": "",
            "token": "",

            "executablePath": "java",
            "defaultExecutablePath": "java",
            "jvmArguments": [],
            "launcherName": "infinn-launcher",
            "launcherVersion": VERSION_LAUNCHER,
            "gameDirectory": self.MINECRAFT_DIRECTORY,
            "demo": False,
            "customResolution": False,
            "resolutionWidth": "854",
            "resolutionHeight": "480"
        }
        with open(self.SRC_JSON, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        self.configuration = default_data
    
    def get_version(self, only_local=True, only_released=True):
        local_version = []
        mojang_version = []

        mine_version_local = minecraft_launcher_lib.utils.get_installed_versions(self.MINECRAFT_DIRECTORY)

        for version in mine_version_local:
            if only_released and version["type"] != "release":
                continue
            local_version.append(version["id"] + f' ({version["type"]}) [local]')

        if not only_local:
            version_list = minecraft_launcher_lib.utils.get_version_list()
            for version in version_list:
                if only_released and version["type"] != "release":
                    continue
                mojang_version.append(version["id"] + f' ({version["type"]})')

        return local_version if only_local else local_version + mojang_version
    
    def set_minecrat_directory(self, path):
        self.MINECRAFT_DIRECTORY = path
        self.SRC_JSON = f"{self.MINECRAFT_DIRECTORY}//configuration.json"

    def get_user_ram(self):
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

        total_gb = stat.ullTotalPhys / (1024**3)
        disponible_gb = stat.ullAvailPhys / (1024**3)
        usado_gb = total_gb - disponible_gb

        return {
            "total": round(total_gb, 2),
            "disponible": round(disponible_gb, 2),
            "usado": round(usado_gb, 2),
            "porcentaje": stat.dwMemoryLoad
        }
    
    async def install_minecraft(self, version):
        minecraft_launcher_lib.install.install_minecraft_version(
            version,
            self.MINECRAFT_DIRECTORY,
            callback={
                "setStatus": self.callback["setStatus"],
                "setProgress": self.callback["setProgress"],
                "setMax": self.callback["setMax"],
            }
        )

    def play_minecraft(self, config):
        options = {
            'username': config["user"],
            'uuid': '',
            'token': '',
            
            "launcherName": "infinn-launcher",
            "launcherVersion": VERSION_LAUNCHER,
        }

        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(config["version"], self.MINECRAFT_DIRECTORY, options)
        subprocess.run(minecraft_command)

def load_configuration():
    _ensureMinecraftDirectoryExists()
    _ensure_configuration_file()

    pass

def _ensure_configuration_file():
        json_path = f"{Globals.minecraftDir}//configuration.json"

        if not os.path.isfile(json_path):
            _create_default_file()
        else:
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    Globals.userConfiguration = json.load(f)
                except json.JSONDecodeError:
                    _create_default_file()


def _create_default_file():
        json_path = f"{Globals.minecraftDir}//configuration.json"
        default_data = {
            "username": "",
            "uuid": "",
            "token": "",

            "executablePath": "java",
            "defaultExecutablePath": "java",
            "jvmArguments": [],
            "launcherName": "infinn-launcher",
            "launcherVersion": VERSION_LAUNCHER,
            "gameDirectory": Globals.minecraftDir,
            "demo": False,
            "customResolution": False,
            "resolutionWidth": "854",
            "resolutionHeight": "480"
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)

def _ensureMinecraftDirectoryExists():

    if os.path.isdir(Globals.minecraftDir):
        return
    
    try:
        os.makedirs(Globals.minecraftDir)

    except Exception:
        Globals.minecraftDir = Globals.defaultMinecraftDir
        _ensureMinecraftDirectoryExists()

def get_parse_version(versionList):
    parse_list = []
    for version in versionList:
        parse_list.append(version["id"] + f' ({version["type"]})')
    return(parse_list)
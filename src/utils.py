import json
import os
import minecraft_launcher_lib
import subprocess
import ctypes

from src.config import VERSION_LAUNCHER

class MineManager:
    def __init__(self, user):
        self.MINECRAFT_DIRECTORY = f"C://Users//{user}//AppData//Roaming//.minecraft"
        self.SRC_JSON = f"{self.MINECRAFT_DIRECTORY}//configuration.json"

        self._ensure_file()
        
        self.mine.callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max,
        }
    
    def _ensure_file(self):
        """
        if not os.path.exists(self.MINECRAFT_DIRECTORY):
            os.makedirs(self.MINECRAFT_DIRECTORY)
        """
        if not os.path.isfile(self.SRC_JSON):
            with open(self.SRC_JSON, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)  # archivo JSON vacío

    def get_local_version(self):
        local_version = []

        mine_version_local = minecraft_launcher_lib.utils.get_installed_versions(self.MINECRAFT_DIRECTORY)

        for version in mine_version_local:
            local_version.append(version["id"] + f' ({ version["type"] }) [local]')

        return local_version
    
    
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

    async def play_minecraft(self, config):
        with open(self.SRC_JSON, "r") as file:
            data = json.load(file)
        
        if 'Nombre' in data and 'RAM' in data and 'Version' in data:
            mine_user = data['Nombre']
            ram = data['RAM']
            version = data['Version']
            java_ruta = data.get('Java', None)
        
        options = {
            'username': mine_user,
            'uuid': '',
            'token': '',
            'executablePath':f'{java_ruta}',

            "jvmArguments": [
                f"-Xmx{ram}G",
                f"-Xms{ram}G",
                ],  # The jvmArguments
            "launcherVersion": VERSION_LAUNCHER,
        }

        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, self.MINECRAFT_DIRECTORY, options)
        subprocess.run(minecraft_command)
import json
import minecraft_launcher_lib
import subprocess

class MineManager:
    def __init__(self, user):
        self.MINECRAFT_DIRECTORY = f"C://Users//{user}//AppData//Roaming//.minecraft"
        self.SRC_JSON = f"{self.MINECRAFT_DIRECTORY}//configuration.json"

        
        self.callback = {
            "setStatus": "set_status",
            "setProgress": "set_progress",
            "setMax": "set_max"
        }
        
    def get_local_version(self):
        local_version = []

        mine_version_local = minecraft_launcher_lib.utils.get_installed_versions(self.MINECRAFT_DIRECTORY)

        for version in mine_version_local:
            local_version.append(version["id"] + f' ({ version["type"] }) [local]')

        return local_version
    
    def get_minecrat_directory(self):
        return self.MINECRAFT_DIRECTORY
    
    def set_minecrat_directory(self, path):
        self.MINECRAFT_DIRECTORY = path
        self.SRC_JSON = f"{self.MINECRAFT_DIRECTORY}//configuration.json"
    
    async def install_minecraft(self, version):
        minecraft_launcher_lib.install.install_minecraft_version(version, self.MINECRAFT_DIRECTORY, callback=self.callback)

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
            "launcherVersion": "0.0.1",
        }

        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, self.MINECRAFT_DIRECTORY, options)
        subprocess.run(minecraft_command)
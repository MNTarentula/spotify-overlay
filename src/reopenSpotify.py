import shutil
import subprocess
import os
class reop:
    def __init__(self):
        appdata_path = os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe")
        self.exe_path = shutil.which("spotify") or appdata_path

    def start(self):
        if os.path.exists(self.exe_path):
            self.process = subprocess.Popen([self.exe_path])
        else:
            print("Spotify path not found:", self.exe_path)

    def stop(self):
        subprocess.run(["taskkill", "/f", "/im", "spotify.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    


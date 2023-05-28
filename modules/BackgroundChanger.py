import subprocess
import urllib.request
import os

from modules.Base import Base


class BackgroundChanger(Base):
    """Module used to change the background of the current host"""

    def __init__(self, host) -> None:
        super().__init__(host)
        self.image_path = os.path.join(os.path.expanduser('~'), "background.jpg")
        self.background_img_url = "https://r4.wallpaperflare.com/wallpaper/371/264/21/itzmauuuroo-hackers" \
                                  "-anonymous-hd-wallpaper-d36bf36dadd97bc55fd692e7a84ba848.jpg"
        self.status = None
        self.status_message = None

    def run(self) -> None:
        """Change the background of the current host"""
        self.download_image(self.background_img_url, self.image_path)
        exit_status = 1

        try:
            if self.current_host.details["os"] == "Windows":
                command = f"reg add 'HKEY_CURRENT_USER\\Control Panel\\Desktop'" \
                          f"/v Wallpaper /t REG_SZ /d '{self.image_path}' /f"
                subprocess.call(command, shell=True)
                command = 'RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters'
                exit_status = subprocess.call(command, shell=True)
            elif self.current_host.details["os"] == "MacOS":
                command = f"osascript -e 'tell application \"Finder\" " \
                          f"to set desktop picture to POSIX file \"{self.image_path}\"'"
                exit_status = subprocess.call(command, shell=True)
            else:
                self.status = False
                self.status_message = "OS not implemented"
        except Exception as e:
            self.status = False
            self.status_message = str(e)

        if exit_status == 0:
            self.status = True
            self.status_message = "Background changed successfully"
        else:
            self.status = False
            self.status_message = "Background could not be changed"

    def log(self) -> list:
        """Returns a status and status message"""
        return [
            {
                "status": self.status,
                "status_message": self.status_message
            }
        ]

    def download_image(self, url, file_path) -> None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)

        with open(file_path, 'wb') as file:
            file.write(response.read())

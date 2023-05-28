import os
from datetime import datetime

from PIL import ImageGrab

from repo.modules.Base import Base


class Screenshot(Base):
    """Module used to take a screenshot of the current host"""

    def __init__(self, host) -> None:
        super().__init__(host)
        self.screenshot_filename = None
        self.screenshot = None

    def run(self) -> None:
        """Take a screenshot of the current host"""
        self.screenshot_filename = f"{self.current_host.hostname}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        self.screenshot = ImageGrab.grab(bbox=None)

    def log(self) -> list:
        """Return the filename of the screenshot made"""
        self.screenshot.save(
            os.path.join(
                os.getcwd(), "repo", "data", self.screenshot_filename
            ),
            format="PNG",
            quality=80
        )

        return [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": self.screenshot_filename,
            }
        ]

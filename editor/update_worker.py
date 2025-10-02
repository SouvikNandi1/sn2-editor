import urllib.request
from PyQt6.QtCore import QObject, pyqtSignal

from .version import __version__

VERSION_URL = "https://raw.githubusercontent.com/sn-2-0/sn2/main/editor_version.txt"

class UpdateWorker(QObject):
    """A worker to check for updates in a separate thread."""
    update_found = pyqtSignal(str, str) # Signal to emit when an update is found (new_version, download_url)
    finished = pyqtSignal() # Signal to emit when the worker is done

    def run(self):
        try:
            with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
                data = response.read().decode('utf-8').strip().splitlines()
                latest_version = data[0]
                # The second line of the version file can be the download URL
                download_url = data[1] if len(data) > 1 else "https://github.com/sn-2-0/sn2"

            # Simple version comparison
            local_parts = [int(p) for p in __version__.split('.')]
            latest_parts = [int(p) for p in latest_version.split('.')]

            if latest_parts > local_parts:
                self.update_found.emit(latest_version, download_url)
        except Exception as e:
            print(f"Update check failed: {e}")
        finally:
            self.finished.emit() # Always emit finished signal
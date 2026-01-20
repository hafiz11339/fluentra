# from cryptography.fernet import Fernet
# import os
# from typing import Optional
# from src.settings import settings

# _KEY: Optional[bytes] = None

# def _ensure_key() -> bytes:
#     global _KEY
#     if _KEY is not None:
#         return _KEY

#     key_str = settings.ENCRYPTION_KEY or os.environ.get("ENCRYPTION_KEY")
#     if not key_str:
#         # generate a key for this process (persist in env for process lifetime)
#         key_str = Fernet.generate_key().decode()
#         os.environ["ENCRYPTION_KEY"] = key_str

#     _KEY = key_str.encode()
#     return _KEY


# def encrypt_text(plaintext: str) -> str:
#     key = _ensure_key()
#     f = Fernet(key)
#     token = f.encrypt(plaintext.encode())
#     return token.decode()


# def decrypt_text(token: str) -> str:
#     key = _ensure_key()
#     f = Fernet(key)
#     return f.decrypt(token.encode()).decode()


from cryptography.fernet import Fernet
import os
from typing import Optional
from src.settings import settings

_KEY: Optional[bytes] = None

def _ensure_key() -> bytes:
    global _KEY
    if _KEY is not None:
        return _KEY

    # Get key from settings or environment
    key_str = settings.ENCRYPTION_KEY or os.environ.get("ENCRYPTION_KEY")

    if not key_str:
        # generate a key for this process (persist in env for process lifetime)
        key_bytes = Fernet.generate_key()  # bytes already
        os.environ["ENCRYPTION_KEY"] = key_bytes.decode()
    else:
        key_bytes = key_str.encode()  # convert string to bytes

    # Validate key length
    if len(key_bytes) != 44:  # Fernet 32-byte key base64 encoded = 44 bytes
        raise ValueError("Fernet key must be 32 url-safe base64-encoded bytes.")

    _KEY = key_bytes
    return _KEY


def encrypt_text(plaintext: str) -> str:
    key = _ensure_key()
    f = Fernet(key)
    token = f.encrypt(plaintext.encode())
    return token.decode()


def decrypt_text(token: str) -> str:
    key = _ensure_key()
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

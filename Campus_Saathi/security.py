import hashlib
import secrets
import hmac

def hash_password(password):
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 200000
    )
    return salt.hex() + "$" + hashed.hex()

def verify_password(password, saved_password):
    try:
        salt_hex, saved_hash = saved_password.split("$", 1)
        salt = bytes.fromhex(salt_hex)

        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 200000
        ).hex()

        return hmac.compare_digest(hashed, saved_hash)

    except (ValueError, TypeError):
        return False

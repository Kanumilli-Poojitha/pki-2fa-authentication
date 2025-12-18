from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64
import os
import time
import pyotp

from decrypt_seed import decrypt_seed

app = FastAPI()

PRIVATE_KEY_PATH = "/app/student_private.pem"
SEED_FILE = "/data/seed.txt"


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


@app.post("/decrypt-seed")
def decrypt_seed_api(data: dict):
    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise HTTPException(status_code=400, detail="Missing encrypted_seed")

    try:
        private_key = load_private_key()
        hex_seed = decrypt_seed(encrypted_seed, private_key)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "seed decrypted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed missing")

    hex_seed = open(SEED_FILE).read().strip()
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)

    return {
        "code": totp.now(),
        "valid_for": 30 - (int(time.time()) % 30)
    }


@app.post("/verify-2fa")
def verify_2fa(data: dict):
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed missing")

    hex_seed = open(SEED_FILE).read().strip()
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    return {"valid": totp.verify(code, valid_window=1)}
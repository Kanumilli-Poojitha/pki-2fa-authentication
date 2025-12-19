from fastapi import FastAPI, HTTPException
import os
import time
import base64

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import pyotp

app = FastAPI()


# ---------------------------
# POST /decrypt-seed
# ---------------------------
@app.post("/decrypt-seed")
def decrypt_seed(data: dict):
    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise HTTPException(status_code=400, detail="Missing encrypted_seed")

    try:
        with open("student_private.pem", "rb") as f:
            private_key = load_pem_private_key(f.read(), password=None)

        encrypted_bytes = base64.b64decode(encrypted_seed)

        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        hex_seed = decrypted_bytes.decode().strip()

        if len(hex_seed) != 64:
            raise ValueError("Invalid seed length")

        os.makedirs("/data", exist_ok=True)
        with open("/data/seed.txt", "w") as f:
            f.write(hex_seed)

        return {"status": "success"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


# ---------------------------
# GET /generate-2fa
# ---------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists("/data/seed.txt"):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open("/data/seed.txt") as f:
        hex_seed = f.read().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    valid_for = 30 - (int(time.time()) % 30)

    return {
        "code": code,
        "valid_for": valid_for
    }


# ---------------------------
# POST /verify-2fa
# ---------------------------
@app.post("/verify-2fa")
def verify_2fa(data: dict):
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists("/data/seed.txt"):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open("/data/seed.txt") as f:
        hex_seed = f.read().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    return {"valid": totp.verify(code, valid_window=1)}


# ---------------------------
# Local run
# ---------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
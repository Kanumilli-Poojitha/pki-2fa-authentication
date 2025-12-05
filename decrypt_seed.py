from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

# Load your private key
with open("student_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

# Load encrypted seed (base64 string)
with open("encrypted_seed.txt", "r") as f:
    b64_seed = f.read().strip()

encrypted_seed = base64.b64decode(b64_seed)

# Decrypt using OAEP SHA-256
seed = private_key.decrypt(
    encrypted_seed,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Decrypted seed:", seed.decode())

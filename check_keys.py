from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Generate public key from private key
public_key_from_private = private_key.public_key()
public_bytes = public_key_from_private.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Load existing student_public.pem
with open("student_public.pem", "rb") as f:
    original_public_bytes = f.read()

# Compare
if public_bytes == original_public_bytes:
    print("✅ Private key matches the public key!")
else:
    print("❌ Private key does NOT match the public key!")

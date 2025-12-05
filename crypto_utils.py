from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_bytes: bytes) -> str:
    """
    Decrypts an RSA-encrypted seed using the student's private key.
    Returns a 64-character hex string.
    """
    # Load your private key
    with open("student_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Decrypt
    seed_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Convert to string
    seed_hex = seed_bytes.decode()

    if len(seed_hex) != 64:
        raise ValueError("Decrypted seed must be 64 hex characters.")

    return seed_hex

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import stat

def generate_rsa_keypair(key_size: int = 4096):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys(private_key, public_key, priv_path="student_private.pem", pub_path="student_public.pem"):
    # Serialize private key
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    # Serialize public key
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(priv_path, "wb") as f:
        f.write(priv_bytes)

    with open(pub_path, "wb") as f:
        f.write(pub_bytes)

    print("Private key written to student_private.pem")
    print("Public key written to student_public.pem")

if __name__ == "__main__":
    priv, pub = generate_rsa_keypair()
    save_keys(priv, pub)

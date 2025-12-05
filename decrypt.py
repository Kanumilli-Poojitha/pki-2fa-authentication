import base64
import os
from crypto_utils import decrypt_seed  # Import root-level crypto_utils.py
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

# Load private key from file
def load_private_key_from_file(filename: str):
    with open(filename, 'rb') as f:
        private_key_data = f.read()
    return load_pem_private_key(private_key_data, password=None, backend=default_backend())

# Main execution
if __name__ == "__main__":
    PRIVATE_KEY_FILE = "/app/student_private.pem"
    ENCRYPTED_SEED_FILE = "/app/encrypted_seed.txt"
    OUTPUT_SEED_FILE = "/data/seed.txt"  # Absolute path inside container

    # Ensure /data directory exists
    os.makedirs("/data", exist_ok=True)

    try:
        # Load private key
        private_key = load_private_key_from_file(PRIVATE_KEY_FILE)
        
        # Read encrypted seed
        with open(ENCRYPTED_SEED_FILE, "r") as f:
            encrypted_seed_b64 = f.read().strip()
        
        # Base64 decode and decrypt
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
        hex_seed = decrypt_seed(encrypted_bytes)
        print("Decrypted seed:", hex_seed)
        
        # Save to /data/seed.txt
        with open(OUTPUT_SEED_FILE, "w") as f:
            f.write(hex_seed)
        print(f"Seed saved to {OUTPUT_SEED_FILE}")
    
    except Exception as e:
        print("Decryption failed:", str(e))

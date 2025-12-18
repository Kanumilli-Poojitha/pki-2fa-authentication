from cryptography.hazmat.primitives.serialization import load_pem_private_key
from decrypt_seed import decrypt_seed
from pathlib import Path

PRIVATE_KEY = "student_private.pem"
ENCRYPTED_SEED = "encrypted_seed.txt"
OUTPUT = "seed.txt"


if __name__ == "__main__":
    private_key = load_pem_private_key(
        Path(PRIVATE_KEY).read_bytes(),
        password=None
    )

    encrypted_seed = Path(ENCRYPTED_SEED).read_text().strip()
    seed = decrypt_seed(encrypted_seed, private_key)

    Path(OUTPUT).write_text(seed)
    print("Seed decrypted:", seed)
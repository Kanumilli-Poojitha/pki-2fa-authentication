#!/usr/bin/env python3
import time
from totp_gen import generate_totp_code  # correct import

# Path to seed file inside container
SEED_FILE = "/app/data/seed.txt"

try:
    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    code = generate_totp_code(seed_hex)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"{timestamp} - 2FA Code: {code}")

except FileNotFoundError:
    print("Seed file not found")
except Exception as e:
    print(f"Error: {e}")
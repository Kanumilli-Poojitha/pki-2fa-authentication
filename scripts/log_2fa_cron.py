#!/usr/bin/env python3
import time
import sys
import os

# ✅ Explicitly add /app to Python path for cron
sys.path.append("/app")

from totp_gen import generate_totp_code

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
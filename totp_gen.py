import base64
import pyotp
import time

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate a 6-digit TOTP code based on the provided hex seed using pyotp.
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a TOTP code within a window of +/- valid_window intervals.
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)

def totp_time_remaining(interval: int = 30) -> int:
    """
    Return seconds remaining before the current TOTP code expires.
    """
    return interval - (int(time.time()) % interval)

# Optional: test if script is run directly
if __name__ == "__main__":
    hex_seed = "fc34b7cd08c9786fbc01a5093fed79e894e39dfea2f5a73ce335ad212cbf8cb8"
    code = generate_totp_code(hex_seed)
    print("Generated TOTP:", code)
    print("Verification:", verify_totp_code(hex_seed, code))
    print("Time remaining:", totp_time_remaining())

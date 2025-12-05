import time
import hmac
import hashlib
import struct

def load_seed(path="data_seed.txt"):
    with open(path, "r") as f:
        return bytes.fromhex(f.read().strip())

def generate_totp_code(seed, time_step=30, digits=6):
    counter = int(time.time() // time_step)
    msg = struct.pack(">Q", counter)
    h = hmac.new(seed, msg, hashlib.sha1).digest()
    o = h[19] & 15
    token = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % (10 ** digits)
    return str(token).zfill(digits)

if __name__ == "__main__":
    seed = load_seed()
    otp = generate_totp_code(seed)
    print("Your TOTP is:", otp)

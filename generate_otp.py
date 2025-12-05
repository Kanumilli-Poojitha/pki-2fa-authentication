import os
import random
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(private_key_path, message):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    signature = private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    with open("otp_signature.bin", "wb") as sig_file:
        sig_file.write(signature)

    print("Signature saved as otp_signature.bin")

if __name__ == "__main__":
    otp = str(random.randint(100000, 999999))
    print("Generated OTP:", otp)

    with open("otp.txt", "w") as file:
        file.write(otp)

    print("OTP saved to otp.txt")

    sign_message("student_private.pem", otp)

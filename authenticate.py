from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def verify_signature(public_key_path, message, signature_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    with open(signature_path, "rb") as sig_file:
        signature = sig_file.read()

    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

if __name__ == "__main__":
    message = input("Enter OTP sent to you: ")

    result = verify_signature("student_public.pem", message, "otp_signature.bin")

    if result:
        print("Authentication Successful! ✔")
    else:
        print("Authentication Failed ✘")

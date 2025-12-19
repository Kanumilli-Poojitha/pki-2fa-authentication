import requests

STUDENT_ID = "23P31A42G6"
GITHUB_REPO_URL = "https://github.com/Kanumilli-Poojitha/pki-2fa-authentication"

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

# ⚠️ PUBLIC KEY MUST BE SINGLE LINE WITH \n
PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtSwHykuyoTUK5dsSGpgJeGWAxl2/gttpbUIX/Ltftc8rsyaXIoNS9dq5s2YCUbjCSAj8qDU1/6vjRcf8JU+Dnl8IwnVUcl4nKQ2/UzhphoijzWE4NM3YLT8Moyk++zxc4EPhmqDbCHMrUfbG/HcwwbdfJuR6H8oEPtDBJdf/E5KNU8fFmt1zJgZ///H33VwkSVJBmCDJFUPUj0AEzhbXZZTDpbZy7kh1Q7fKT6o3vCa+XfFlCAJv29bwDnH6jn5TjxqHXYD4Q9KpvoRPvwUtlZ5JiYNo11ykrFw5rL8eKAVeSaaTpOQsXVwnNYquHGPdG77xem5QmAoU70FS+ISfd8OIKkw8TxcYhIWx7ChoXCv524Lczev8qd1a2paNI+Bxibst0ITYiZ2bu0u8QRFOrCUhF7hbWNya+7NcLz/MNGbiKXZNReERsadIfqa3PbhajDl8OJprpMEBYHQab5HP4wLJdonkLfe0U8jzPZuoAYMIX1PlAqTwu5N9F6Gqyb35IFZpK3GOvXjmQgSPY6s4gnDDTCGZv7Niqrher0SsSN1S/uLqlqwTIviLoUW71rWg/6vSkOJWcOMr2yiKkzjC96ZZjnQeol71dbYuIZliOg3LcBsTUHCqVXWWAm/bFdlnrUagD+tFJ38gyfmRyLTQ3sZyg0VKi/c8YswctxnV8ycCAwEAAQ==\n-----END PUBLIC KEY-----\n"

# ====== REQUEST ======
payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": PUBLIC_KEY
}

response = requests.post(API_URL, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.text)

response.raise_for_status()

encrypted_seed = response.json()["encrypted_seed"]

# ====== SAVE RESULT (DO NOT COMMIT THIS FILE) ======
with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

print("✅ Encrypted seed saved to encrypted_seed.txt")
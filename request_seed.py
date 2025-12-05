import requests

STUDENT_ID = "23P31A42G6"
GITHUB_REPO_URL = "https://github.com/Kanumilli-Poojitha/pki-2fa-authentication"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0M/ol11CgP7WMYKxWoRl
eWHnNWqtbypCZkUmp+2K/UoHuTMC7CQInUvU6XNpk5aF39OPBjO5PO1dMCdGCY+X
Si0wEwCS9HjvZ8Yuj0FndxUkI5qOcCq55SFsFeDTFr6Ib3Znz/noIbD1eRgoZiyP
zG/stxnInt1i0rjb06p/1xIJ4XKSrWQaAk3qRZ7Wj0PgR37H8JTZiRUtbqMLKm1K
gJGNK2gaCKD7M1XSGNqV4IiYktnoZ8D/bgozwYecVbqJsVM9omKqQQ+SXsCZjvhd
1CJXq0PPj9KVLz0jgwcDZEVUrpCsAHpGV/iy+n2i58fWHi7xCzqheQnry827KzlT
+LFTcoWReTKe7KbJTL+ynRhz29d0aCeH3n7blGVIdCYLxx3EsymcPlHaSVoSnaJG
LutJTuQD3bWsWybwSQR5timYtK1RRF87R4+5JgztBGpf/+VRKsoL5Aa3wB1thZy9
mzhJ6b+VAqoBSeA82kLqHLriKRRuW/7xauumXFOvdlylCyn1wDFG9SIOFBRJBE/x
Kbh677JaUWFsMRjVyhLN/Nea8eZ35BMKksHkJGSjMoqldtiYPKMCcCR8NERiNll1
n25QCNqrgMrShVbGnFp+xUqPHCXMwAzztwjv3wXqpEpPg3s5TQwc9prrhwgOiiPT
Bwl0q29v60i/AmCcg2iMED8CAwEAAQ==
-----END PUBLIC KEY-----"""

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": PUBLIC_KEY
}

response = requests.post(API_URL, json=payload)

encrypted_seed = response.json()["encrypted_seed"]

with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

print("Encrypted seed saved to encrypted_seed.txt")

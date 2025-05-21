from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import base64
import json
from time import sleep
import requests
def get_salt(username: str,r) -> str:
    """
    Gọi AjaxCommon.GetPrivateKey để lấy salt (đồng bộ).
    """
    ENDPOINT = (
    "https://sinhvien.epu.edu.vn/ajaxpro/AjaxCommon,PMT.Web.PhongDaoTao.ashx"
    )
    headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "X-AjaxPro-Method": "GetPrivateKey",
    }
    payload = json.dumps({"salt": username})
    while True:
        try:
            resp = r.post(ENDPOINT, data=payload, headers=headers,verify=False,timeout=10)
            if resp.status_code != 200:
                print(f"❌ LẤY SALT THẤT BẠI !!!")
                sleep(2)
                continue

            data = resp.json()
            # Nếu có lỗi:
            if data.get("error"):
                raise Exception(f"GetPrivateKey error: {data['error']}")
            print("✅ LẤY SALT THÀNH CÔNG")
            return data.get("value")
        except requests.exceptions.RequestException as e:
            print(f"❌ LẤY SALT THẤT BẠI !!!")
            sleep(2)
            continue
def derive_key(salt: str,PASSPHRASE) -> bytes:

    return PBKDF2(
        salt.encode('utf-8'),
        PASSPHRASE,
        dkLen=16,
        count=1000,
        hmac_hash_module=SHA1
    )
def pkcs7_pad(data: bytes) -> bytes:
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len]) * pad_len
def encrypt(username,password,r) -> str:
    # Passphrase và IV cố định
    PASSPHRASE = "CryptographyPMT-EMS"
    IV_HEX = "e84ad660c4721ae0e84ad660c4721ae0"
    IV = bytes.fromhex(IV_HEX)
    salt = get_salt(username,r)
    key = derive_key(salt,PASSPHRASE)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded = pkcs7_pad(password.encode('utf-8'))
    ct_bytes = cipher.encrypt(padded)
    return base64.b64encode(ct_bytes).decode('utf-8')
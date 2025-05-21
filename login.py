import requests
import urllib3
from bs4 import BeautifulSoup
from time import sleep
from PIL import Image
import io
import pytesseract
import hashlib
from encrypt import encrypt
# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def requestEPU(r):
    while True:
        try:
            response = r.get('https://sinhvien.epu.edu.vn/', verify=False, timeout=10)
            sleep(2)
            if response.status_code == 200:
                print("✅ REQUESTS TRANG SINH VIÊN EPU THÀNH CÔNG")
                return response
        except requests.exceptions.RequestException as e:
            print(f"❌ REQUESTS TRANG SINH VIÊN EPU LẤY THAM SỐ THẤT BẠI !!!")
            sleep(2)
            continue
def getLink(r):
    url_captcha = 'https://sinhvien.epu.edu.vn/ajaxpro/AjaxConfirmImage,PMT.Web.PhongDaoTao.ashx'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,vi-VN;q=0.9",
        "content-type": "text/plain; charset=UTF-8",
        "origin": "https://sinhvien.epu.edu.vn",
        "referer": "https://sinhvien.epu.edu.vn/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-ajaxpro-method": "CreateConfirmImage"
    }
    payload = "{}"
    while True:
        try:
            reponse = r.post(url_captcha, headers=headers, data=payload, verify=False, timeout=10)
            if reponse.status_code == 200:
                print("✅ LẤY LINK CAPTCHA VÀ HASH MD5 THÀNH CÔNG")
                return reponse
        except requests.exceptions.RequestException as e:
            print(f"❌ LẤY LINK CAPTCHA VÀ HASH MD5 THẤT BẠI !!!")
            sleep(2)
            continue
def getCaptcha(r):
    result = getLink(r)
    link = result.json()['value'][0]
    captcha_hash_md5 = result.json()['value'][1]
    url_img = 'https://sinhvien.epu.edu.vn' + link
    while True:
        try:
            response = r.get(url_img, verify=False, timeout=10)
            if response.status_code == 200:
                # Đọc ảnh từ bytes bằng PIL, không lưu file
                image = Image.open(io.BytesIO(response.content))
                # Nhận diện chữ bằng pytesseract
                text = pytesseract.image_to_string(image, config='--psm 7').strip()
                print(f"✅ ĐỌC CAPTCHA THÀNH CÔNG: {text}")
                print(f"✅ HASH MD5 CAPTCHA: {captcha_hash_md5}")
                return text, captcha_hash_md5
        except requests.exceptions.RequestException as e:
            print(f"❌ LẤY CAPTCHA THẤT BẠI !!!")
            sleep(2)
            continue
def summit(ma_sv, matkhau_mahoaMD5, captcha_text, captcha_hash, viewstate, viewstategen, encode_matkhau,r):
    url = "https://sinhvien.epu.edu.vn/Default.aspx"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sinhvien.epu.edu.vn",
        "Referer": "https://sinhvien.epu.edu.vn/Default.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "vi,en-US;q=0.9",
    }
    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategen,
        "ctl00$ucPhieuKhaoSat1$RadioButtonList1": "0",
        "ctl00$DdListMenu": "-1",
        "ctl00$ucRight1$txtMaSV": ma_sv,
        "ctl00$ucRight1$txtMatKhau": encode_matkhau,
        "ctl00$ucRight1$rdSinhVien": "1",
        "ctl00$ucRight1$txtSercurityCode": captcha_text,
        "txtSecurityCodeValue": captcha_hash,
        "ctl00$ucRight1$txtEncodeMatKhau": matkhau_mahoaMD5,
        "ctl00$ucRight1$btnLogin": "Đăng Nhập"
    }   
    # Gửi yêu cầu đăng nhập
    try:
        resp = r.post(url, headers=headers, data=data, verify=False, allow_redirects=False,timeout=10)
        return resp
    except requests.exceptions.RequestException as e:
        return None

def login(username, password):
    print("🔑 ĐANG ĐĂNG NHẬP VÀO SINH VIÊN EPU")
    print("Mã sinh viên :",username)
    print("Password :",password)
    try:
        r = requests.Session()
        while True:
            # 1. Requests đến trang sinh viên EPU lấy các tham số cơ bản [ Sử dụng hàm requestEPU ] .
            response = requestEPU(r)
            # 2. Thực hiện tách html lấy các tham số cần thiết [ viewstate,viewstategen ]
            soup = BeautifulSoup(response.text, 'html.parser')
            # Lấy __VIEWSTATE
            viewstate = soup.find("input", {"name": "__VIEWSTATE"})
            viewstate_value = viewstate["value"] if viewstate and viewstate.has_attr("value") else None
            if viewstate_value is None:
                print("❌ Không tìm thấy __VIEWSTATE")
                continue
            print("✅ LẤY ĐƯỢC __VIEWSTATE")    
            # Lấy __VIEWSTATEGENERATOR
            viewstategen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})
            viewstategen_value = viewstategen["value"] if viewstategen and viewstategen.has_attr("value") else None
            if viewstategen_value is None:
                print("❌ Không tìm thấy __VIEWSTATEGENERATOR")
                continue
            print("✅ LẤY ĐƯỢC __VIEWSTATEGENERATOR")
            # 3. Gọi hàm getCaptcha để lấy captcha,captcha_hash_md5
            captcha, captcha_hash_md5 = getCaptcha(r)
            #4 Mã hóa password hash md5
            md5hex = hashlib.md5(password.encode()).hexdigest()
            print(f"✅ MÃ HÓA PASSWORD HASH MD5 THÀNH CÔNG: {md5hex}")
            ciphertext = encrypt(username,password,r)
            print(f"✅ MÃ HÓA PASSWORD THÀNH CÔNG: {ciphertext}")
            response = summit(username,md5hex,captcha,captcha_hash_md5,viewstate_value,viewstategen_value,ciphertext,r)
            if response.status_code == 302 and "location" in response.headers and "/HoSoSinhVien.aspx" in response.headers["location"]:
                print("✅ Đăng nhập thành công!")
                return r
            else:
                print("❌ Đăng nhập thất bại")
                print("❌ Mã trạng thái:", response.status_code)
                
    except ValueError as e:
        print(f"Error creating session: {e}")

import requests
from bs4 import BeautifulSoup
def getHoSoSinhVien(r):
    while True:
        try:
            url = "https://sinhvien.epu.edu.vn/HoSoSinhVien.aspx"
            resp = r.get(url, verify=False, timeout=10)
            if resp.status_code == 200:
                print("✅ Lấy thông tin hồ sơ sinh viên thành công")
                soup = BeautifulSoup(resp.text, 'html.parser')
                title_group = soup.find("div", class_="title-group")
                if title_group:
                    full_text = title_group.get_text(strip=True)
                    if "THÔNG TIN SINH VIÊN" in full_text:
                        name = full_text.replace("THÔNG TIN SINH VIÊN", "").strip()
                        return {"name": name}
            else:
                print("❌ Lấy thông tin hồ sơ sinh viên thất bại, đang thử lại...")
        except requests.exceptions.RequestException as e:
            print("❌ Lấy thông tin hồ sơ sinh viên thất bại, đang thử lại...")

        
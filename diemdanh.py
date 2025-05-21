import requests
from bs4 import BeautifulSoup
def getDiemDanh(r):
    while True:
        try:
            url = "https://sinhvien.epu.edu.vn/ThongTinDiemDanh.aspx"
            resp = r.get(url, verify=False, timeout=10)
            if resp.status_code == 200:
                print("✅ Lấy thông tin điểm danh thành công")
                soup = BeautifulSoup(resp.text, 'html.parser')
                tbl  = soup.select_one('table.grid.grid-color2')

                courses, totals = {}, {}

                for tr in tbl.select('tr'):
                    cls = tr.get('class') or []
                    tds = tr.find_all('td')

                    # --- Hàng tổng ---
                    if 'row-sum' in cls:
                        label = tds[0].get_text(strip=True)
                        nums  = [int(td.get_text(strip=True) or 0)
                                for td in tds if td.get_text(strip=True).isdigit()]

                        if label == 'Tổng' and len(nums) >= 2:
                            totals['Tổng'] = {
                                'Nghi có phép': nums[0],
                                'Nghỉ ko phép': nums[1]
                            }
                        elif label.startswith('Tổng số ngày nghỉ') and nums:
                            totals['Tổng số ngày nghỉ'] = nums[0]

                    # --- Hàng môn học (8 cột) ---
                    elif len(tds) == 8:
                        code = tds[1].get_text(strip=True)
                        if not code.isdigit():  # skip header/quater
                            continue

                        txt = lambda i: tds[i].get_text(strip=True)
                        num = lambda i: int(txt(i)) if txt(i) else 0

                        courses[code] = {
                            'tên':           txt(2),
                            'ĐVHT':          num(3),
                            'Nghi có phép':  num(4),
                            'Nghỉ ko phép':  num(5),
                            'Số tiết nghỉ':  num(6),
                            'Số % nghỉ':     txt(7),
                        }
                return courses, totals
            else:
                    print("❌ Lấy thông tin hồ sơ sinh viên thất bại, đang thử lại...")
        except requests.exceptions.RequestException as e:
            print("❌ Lấy thông tin hồ sơ sinh viên thất bại, đang thử lại...")
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import re
def dataProcessing(soup):
    table = soup.select_one('div.div-ChiTietLich table')
    if not table:
        return {}

    rows = table.find_all('tr')

    # --- Xử lý lấy days theo format "Thứ 2 | 19/05/2025" ---
    header_row = rows[0]
    header_ths = header_row.find_all('th')[1:]  # Bỏ cột đầu 'Ca học'
    days = []
    for th in header_ths:
        # Lấy text gốc, thay \r\n và khoảng trắng bằng dấu cách
        text = th.get_text(separator=' ').strip()
        # Chuẩn hóa "thu" thành "Thứ"
        text = text.replace('thu', 'Thứ')
        # Xóa nhiều khoảng trắng thành 1 khoảng trắng
        text = re.sub(r'\s+', ' ', text)
        # Tách text thành các phần theo dấu cách
        parts = text.split(' ')
        # Tìm phần chứa ngày tháng
        date_part = ''
        for p in parts:
            if '/' in p:
                date_part = p
                break
        # Tạo kết quả cuối dạng "Thứ 2 | 19/05/2025"
        day_part = ' '.join(parts[:2]) if len(parts) >= 2 else parts[0]
        day_str = f"{day_part} | {date_part}" if date_part else day_part
        days.append(day_str)
    # --- Kết thúc xử lý ---

    # Extract rows for each time slot
    time_slots = []
    for row in rows[1:]:
        th = row.find('th')
        if not th:
            continue
        time_of_day = th.get_text(strip=True).lower()  # 'sáng','chiều','tối'
        cells = row.find_all('td')
        time_slots.append((time_of_day, cells))

    # Build schedule dict
    schedule = {day: {} for day in days}
    for time_of_day, cells in time_slots:
        for idx, day in enumerate(days):
            entries = []
            
            # Guard for missing cell
            if idx < len(cells):
                cell = cells[idx]
                # Find divs of class div-LichHoc or div-LichThi
                for div in cell.find_all('div', class_=lambda c: c and (c.startswith('div-LichHoc') or c.startswith('div-LichThi'))):
                    classes = div.get('class', [])
                    entry_type = 'hoc' if 'div-LichHoc' in classes else 'thi'
                    content = list(div.stripped_strings)
                    entries.append({'type': entry_type, 'content': content})
            schedule[day][time_of_day] = entries

    return schedule
def getLich(r, timeInput = None):
    while True:
        try:
            url = "https://sinhvien.epu.edu.vn/LichHocLichThiTuan.aspx"
            resp = r.get(url, verify=False, timeout=10)
            if resp.status_code == 200:
                print("✅ Lấy thông tin thời khóa biểu [ Hiện Tại ] thành công")
                soup = BeautifulSoup(resp.text, 'html.parser')
                #__VIEWSTATE
                __VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"})
                viewstate_value = __VIEWSTATE["value"] if __VIEWSTATE and __VIEWSTATE.has_attr("value") else None
                if viewstate_value is None:
                    print("❌ Không tìm thấy __VIEWSTATE của Lịch Học")
                    continue
                print("✅ LẤY ĐƯỢC __VIEWSTATE của Lịch Học") 
                #__VIEWSTATEGENERATOR  
                __VIEWSTATEGENERATOR = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})
                viewstategen_value = __VIEWSTATEGENERATOR["value"] if __VIEWSTATEGENERATOR and __VIEWSTATEGENERATOR.has_attr("value") else None
                if viewstategen_value is None:
                    print("❌ Không tìm thấy __VIEWSTATEGENERATOR của Lịch Học")
                    continue
                print("✅ LẤY ĐƯỢC __VIEWSTATEGENERATOR của Lịch Học")
                this_week = dataProcessing(soup)
                time_now = datetime.now()
                time = f"{time_now.day}/{time_now.month}/{time_now.year}"
                if(timeInput == "Hiện Tại"):
                    payload = {
                        "__EVENTTARGET": "",
                        "__EVENTARGUMENT": "",
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": viewstate_value,
                        "__VIEWSTATEGENERATOR": viewstategen_value,
                        "ctl00$ucPhieuKhaoSat1$RadioButtonList1": 0,
                        "ctl00$DdListMenu": -1,
                        "ctl00$ContentPlaceHolder$rLoaiLich": -1,
                        "ctl00$ContentPlaceHolder$btnTruoc": "< Tuần trước",
                        "ctl00$ContentPlaceHolder$txtDate": time
                    }
                    resp = r.post(url,data = payload, verify=False, timeout=10)
                    if resp.status_code == 200:
                        print("✅ Lấy thông tin thời khóa biểu [ Tuần Trước ] thành công")
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        last_week = dataProcessing(soup)
                    else:
                        continue
                    payload = {
                        "__EVENTTARGET": "",
                        "__EVENTARGUMENT": "",
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": viewstate_value,
                        "__VIEWSTATEGENERATOR": viewstategen_value,
                        "ctl00$ucPhieuKhaoSat1$RadioButtonList1": 0,
                        "ctl00$DdListMenu": -1,
                        "ctl00$ContentPlaceHolder$rLoaiLich": -1,
                        "ctl00$ContentPlaceHolder$btnTruoc": "< Tuần sau",
                        "ctl00$ContentPlaceHolder$txtDate": time
                    }
                    if resp.status_code == 200:
                        print("✅ Lấy thông tin thời khóa biểu [ Tuần Trước ] thành công")
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        next_week = dataProcessing(soup)
                    else:
                        continue
                    return this_week,last_week,next_week
                    
                else:
                    pass
                        
            else:
                print("❌ Lấy thông tin thời khóa biểu thất bại, đang thử lại...")
                sleep(2)
        except requests.exceptions.RequestException as e:
            print("❌ Lấy thông tin thời khóa biểu thất bại, đang thử lại...")
            sleep(2)

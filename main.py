from login import login
from hoso import getHoSoSinhVien
from diemdanh import getDiemDanh
from getLich import getLich
username = "23810310247"
passwword = "Nhutrunghai2005@"
def main():
    r = login(username, passwword)
    dataHoso = getHoSoSinhVien(r)
    courses,totals = getDiemDanh(r)
    this_week,last_week,next_week = getLich(r)
    print("=="*50)
    print("Thông tin hồ sơ sinh viên")
    print("Tên:", dataHoso['name'])
    print("Tổng số môn học:", len(courses))
    print("Tổng số ngày nghỉ:", totals['Tổng số ngày nghỉ'])
    print("Lịch học:") 
    print(this_week)
    print(last_week)
    print(next_week)
    # for day, times in lichHoc.items():
    #     print(f"{day}:")
    #     for time_of_day, entries in times.items():
    #         print(f"  {time_of_day}:")
    #         for entry in entries:
    #             print(f"    - {entry['type']}: {entry['content']}")
    # for code, course in courses.items():
    #     print(f"Mã môn học: {code}")
    #     print(f"Tên môn học: {course['tên']}")
    #     print(f"ĐVHT: {course['ĐVHT']}")
    #     print(f"Nghỉ có phép: {course['Nghi có phép']}")
    #     print(f"Nghỉ không phép: {course['Nghỉ ko phép']}")
    #     print(f"Số tiết nghỉ: {course['Số tiết nghỉ']}")
    #     print(f"Số % nghỉ: {course['Số % nghỉ']}")
    #     print("-"*50)
main()
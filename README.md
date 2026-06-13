<div align="center">

# 🎓 EPU Student Toolkit

### Bộ script Python hỗ trợ thao tác với thông tin sinh viên EPU

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-111827?style=for-the-badge)
![Student Tool](https://img.shields.io/badge/Student_Tool-2563EB?style=for-the-badge)

</div>

---

## 📌 Giới thiệu

**EPU Student Toolkit** là tập hợp các script Python hỗ trợ thao tác với một số dữ liệu sinh viên như đăng nhập, lấy lịch học, xem hồ sơ và điểm danh.

> Repo này mang tính học tập/thử nghiệm automation với Python, phù hợp để luyện xử lý request, mã hóa dữ liệu và đọc dữ liệu HTML.

---

## 🧩 Các file chính

| File | Chức năng |
|---|---|
| `main.py` | Entry chính để chạy/tổng hợp luồng xử lý |
| `login.py` | Xử lý đăng nhập |
| `getLich.py` | Lấy lịch học |
| `hoso.py` | Xử lý thông tin hồ sơ |
| `diemdanh.py` | Chức năng liên quan điểm danh |
| `encrypt.py` | Hàm mã hóa/hỗ trợ bảo mật dữ liệu |
| `lichhoc.html` | File HTML lịch học mẫu/đã lưu |

---

## 🔄 Luồng hoạt động tổng quát

```text
Nhập thông tin cần thiết
        ↓
Đăng nhập / tạo request
        ↓
Lấy dữ liệu sinh viên
        ↓
Parse HTML/response
        ↓
Hiển thị hoặc lưu kết quả
```

---

## 🚀 Cách chạy tham khảo

```bash
python main.py
```

Nếu thiếu thư viện, hãy kiểm tra import trong các file Python và cài bổ sung bằng `pip`.

---

## ⚠️ Lưu ý bảo mật

- Không commit tài khoản, mật khẩu, token hoặc cookie thật lên GitHub.
- Nếu project cần biến môi trường, nên tạo `.env.example` thay vì lưu thông tin thật.
- Đây là project học tập, nên sử dụng có trách nhiệm và tuân thủ quy định của hệ thống liên quan.

---

## 🧭 Roadmap

- [ ] Thêm `requirements.txt`
- [ ] Thêm `.env.example`
- [ ] Chuẩn hóa cách chạy CLI
- [ ] Tách module xử lý request và parse dữ liệu
- [ ] Thêm README hướng dẫn cấu hình chi tiết
- [ ] Thêm ví dụ output đã ẩn thông tin nhạy cảm

---

<div align="center">

Project Python automation phục vụ học tập và thực hành.  
Author: [Nhữ Trung Hải](https://github.com/nhutrunghai)

</div>

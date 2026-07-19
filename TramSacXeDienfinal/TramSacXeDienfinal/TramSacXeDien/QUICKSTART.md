# 🚀 Hướng Dẫn Nhanh - Quick Start

## Bước 1: Chuẩn Bị

Đảm bảo bạn đã cài đặt Python 3.8 trở lên:
```bash
python --version
```

## Bước 2: Cài Đặt Thư Viện

Vào thư mục TramSacXeDien và chạy:
```bash
pip install -r requirements.txt
```

## Bước 3: Chạy Ứng Dụng

### Cách 1: Windows (Dễ nhất)
Nhấp đôi vào file `run.bat`

### Cách 2: Terminal/Command Line
```bash
python app.py
```

### Cách 3: Sử dụng Flask
```bash
flask run
```

## Bước 4: Mở Trình Duyệt

Truy cập: **http://127.0.0.1:5000/**

## 📊 Sử Dụng Cơ Bản

1. **Tạo Dữ Liệu**: Nhập số khu vực (30 là mặc định) → Tạo Dữ Liệu
2. **Chọn Thuật Toán**: 
   - Hill Climbing (nhanh)
   - Simulated Annealing (chất lượng cao)
   - So Sánh Cả 2 (xem cái nào tốt hơn)
3. **Xem Kết Quả**:
   - Kết Quả: Chi phí tối ưu và vị trí trạm
   - Biểu Đồ: Trực quan hóa dữ liệu
   - So Sánh: So sánh hiệu suất

## ⚡ Tips

- **Dữ liệu nhiều**: Chọn ít trạm hơn để tính toán nhanh
- **Chất lượng cao**: Dùng Simulated Annealing (chậm hơn nhưng kết quả tốt)
- **Tốc độ**: Dùng Hill Climbing (nhanh nhưng kết quả tạm được)

## 🔧 Khắc Phục Lỗi Nhanh

| Lỗi | Giải Pháp |
|-----|----------|
| Flask not found | `pip install flask` |
| Port 5000 in use | Sửa port trong app.py |
| Ứng dụng chậm | Giảm số khu vực hoặc số khởi động |

## 📝 Cấu Trúc Thư Mục

```
TramSacXeDien/
├── app.py              ← Flask server
├── config.py           ← Cấu hình
├── requirements.txt    ← Dependencies
├── run.bat             ← Chạy ngay (Windows)
├── README.md           ← Tài liệu đầy đủ
├── QUICKSTART.md       ← File này
├── TramSacXeDien/      ← Code chính
│   ├── dataset.py      ← Thuật toán
│   └── main.py         ← Script CLI
├── templates/
│   └── index.html      ← Trang web
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🎯 Ví Dụ Cơ Bản

1. Mở ứng dụng
2. Chọn 30 khu vực, nhấn "Tạo Dữ Liệu"
3. Nhấn "Simulated Annealing" 
4. Đợi 5-10 giây
5. Xem kết quả trong các tab

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra Python version
2. Cài lại requirements: `pip install --upgrade -r requirements.txt`
3. Xem console output để tìm lỗi
4. Đọc README.md chi tiết hơn

---

**Vậy là xong! Chúc bạn sử dụng vui vẻ 🎉**

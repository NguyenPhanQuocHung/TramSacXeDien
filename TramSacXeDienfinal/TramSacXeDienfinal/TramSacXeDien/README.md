# 🔋 Tối Ưu Hóa Vị Trí Trạm Sạc Xe Điện

**Charging Station Placement Optimizer - Web Interface**

Một ứng dụng web hiện đại để tối ưu hóa vị trí trạm sạc xe điện sử dụng các thuật toán tìm kiếm metaheuristic.

## 📋 Tính Năng

- ✅ **Tạo dữ liệu ngẫu nhiên**: Sinh ra các khu vực dân cư với tọa độ và dân số
- ✅ **Random Restart Hill Climbing**: Thuật toán tìm kiếm địa phương với khởi động lại ngẫu nhiên
- ✅ **Simulated Annealing**: Thuật toán metaheuristic dựa trên mô phỏng nhiệt độ
- ✅ **So sánh thuật toán**: Đánh giá hiệu suất của cả hai phương pháp
- ✅ **Biểu đồ tương tác**: Trực quan hóa vị trí trạm sạc, phân bố dân số, và lịch sử chi phí
- ✅ **Giao diện thân thiện**: Thiết kế responsive và dễ sử dụng

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8 hoặc cao hơn
- pip (trình quản lý gói Python)

### Bước 1: Clone hoặc Tải Dự Án

```bash
cd TramSacXeDien
```

### Bước 2: Tạo Môi Trường Ảo (Tùy Chọn Nhưng Khuyến Khích)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Các Thư Viện Phụ Thuộc

```bash
pip install -r requirements.txt
```

## 🏃 Chạy Ứng Dụng

### Phương Pháp 1: Chạy Trực Tiếp

```bash
python app.py
```

### Phương Pháp 2: Sử Dụng Flask

```bash
flask run
```

Ứng dụng sẽ khởi động tại `http://127.0.0.1:5000/`

### Phương Pháp 3: Sử Dụng Script (Windows)

Nếu có file `run.bat`:
```bash
run.bat
```

## 📖 Hướng Dẫn Sử Dụng

### 1. Tạo Dữ Liệu
- Nhập số lượng khu vực dân cư (10-100)
- Nhấn nút "Tạo Dữ Liệu"
- Hệ thống sẽ tạo ra các khu vực với tọa độ và dân số ngẫu nhiên

### 2. Cấu Hình Thuật Toán
- **Số trạm sạc (K)**: Số lượng trạm sạc cần tối ưu hóa (1-20)
- **Số lần khởi động lại**: Cho RRHC, số lần chạy từ các điểm khởi đầu khác nhau

### 3. Chọn Thuật Toán
- **Hill Climbing**: Chạy Random Restart Hill Climbing
- **Simulated Annealing**: Chạy Simulated Annealing
- **So Sánh Cả 2**: So sánh hiệu suất của cả hai thuật toán

### 4. Xem Kết Quả
- **Tab "Kết Quả"**: Hiển thị chi phí tối ưu, vị trí trạm sạc, và thông tin chi tiết
- **Tab "Biểu Đồ"**: Trực quan hóa vị trí trạm sạc trên bản đồ và phân bố dân số
- **Tab "So Sánh"**: So sánh chi tiết giữa hai thuật toán

## 📁 Cấu Trúc Dự Án

```
TramSacXeDien/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── TramSacXeDien/
│   ├── dataset.py             # Các hàm tối ưu hóa
│   ├── main.py                # Script chạy từ dòng lệnh
│   └── __init__.py
├── templates/
│   └── index.html             # Giao diện web
└── static/
    ├── css/
    │   └── style.css          # Stylesheet
    └── js/
        └── main.js            # JavaScript logic
```

## 🔧 Các Thuật Toán

### Random Restart Hill Climbing (RRHC)
- **Mô tả**: Thuật toán tìm kiếm địa phương chạy nhiều lần từ các điểm khởi đầu khác nhau
- **Ưu điểm**: Dễ hiểu, nhanh, có thể tránh được local optima tốt
- **Nhược điểm**: Có thể bị mắc kẹt ở local optima

### Simulated Annealing (SA)
- **Mô tả**: Thuật toán metaheuristic lấy cảm hứng từ quá trình làm nguội kim loại
- **Ưu điểm**: Có khả năng thoát khỏi local optima, tìm được global optima tốt hơn
- **Nhược điểm**: Cần điều chỉnh tham số, chậm hơn RRHC

## 📊 Công Thức Tính Chi Phí

$$\text{Cost} = \sum_{i=0}^{n-1} \min_j (\text{distance}(i, j)) \times \text{population}(i)$$

Trong đó:
- `distance(i, j)`: Khoảng cách Euclidean giữa khu vực i và trạm sạc j
- `population(i)`: Dân số khu vực i
- Mục tiêu: Tối thiểu hóa tổng chi phí

## 🔌 API Endpoints

- `GET /` - Trang chính
- `POST /api/generate_data` - Tạo dữ liệu
- `POST /api/run_algorithm` - Chạy một thuật toán
- `POST /api/compare_algorithms` - So sánh cả hai thuật toán
- `GET /api/get_visualization` - Lấy dữ liệu biểu đồ

## 🐛 Khắc Phục Sự Cố

### Lỗi: "ModuleNotFoundError: No module named 'flask'"
**Giải pháp**: Cài đặt Flask bằng `pip install flask`

### Lỗi: "Port 5000 already in use"
**Giải pháp**: Sửa file app.py, thay `port=5000` thành port khác

### Ứng dụng chạy chậm
**Giải pháp**: 
- Giảm số lượng khu vực
- Giảm số lần khởi động lại
- Sử dụng RRHC thay vì SA

## 📝 Ghi Chú

- Tất cả các tính toán được thực hiện phía máy chủ (server-side)
- Dữ liệu không được lưu trữ vĩnh viễn, chỉ trong session hiện tại
- Ứng dụng hỗ trợ các trình duyệt hiện đại (Chrome, Firefox, Safari, Edge)

## 👨‍💻 Phát Triển

Để sửa đổi hoặc mở rộng ứng dụng:

1. **Backend** (Python/Flask): Sửa `app.py` hoặc `TramSacXeDien/dataset.py`
2. **Frontend** (HTML/CSS/JS): Sửa files trong `templates/` và `static/`
3. **Thuật toán**: Sửa các hàm tối ưu hóa trong `TramSacXeDien/dataset.py`

## 📄 Giấy Phép

Dự án này được phát triển cho mục đích giáo dục.

## 📞 Hỗ Trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
- Phiên bản Python (≥ 3.8)
- Tất cả dependencies đã được cài đặt
- Port 5000 không bị chiếm dụng
- Console không có lỗi (xem output khi chạy ứng dụng)

---

**Developed with ❤️ for Optimization Problems**

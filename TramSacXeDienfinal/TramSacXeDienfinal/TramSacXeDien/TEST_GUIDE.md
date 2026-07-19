# 🧪 Hướng Dẫn Test & Sử Dụng

Hướng dẫn này giúp bạn test xem ứng dụng web có hoạt động đúng không.

## ✅ Pre-Setup Checklist

Trước khi chạy, kiểm tra:

- [ ] Python 3.8+ đã cài: `python --version`
- [ ] Bạn ở thư mục `TramSacXeDien`
- [ ] File `app.py` có trong thư mục
- [ ] Folder `templates/` và `static/` tồn tại

## 🚀 Bước 1: Cài Đặt & Chạy

### Option A: Windows (Dễ nhất)
```batch
run.bat
```

### Option B: Terminal
```bash
pip install -r requirements.txt
python app.py
```

### Kết quả mong đợi:
```
WARNING in app.run_simple (...)
* Running on http://127.0.0.1:5000
```

## 🌐 Bước 2: Mở Trình Duyệt

Truy cập: **http://127.0.0.1:5000/**

### Kiểm tra:
- [ ] Trang load không lỗi
- [ ] Tiêu đề "⚡ Tối Ưu Hóa Trạm Sạc Xe Điện" hiển thị
- [ ] Giao diện xanh-đỏ gradient
- [ ] Form input visible

## 📝 Bước 3: Test Tạo Dữ Liệu

1. Kiểm tra input "Số lượng khu vực" = 30 (mặc định)
2. **Nhấn nút "Tạo Dữ Liệu"**

### Kiểm tra:
- [ ] ✓ Thông báo xanh lá: "Đã tạo 30 khu vực thành công!"
- [ ] Không có lỗi trong console (F12 → Console)
- [ ] Biểu đồ "Vị Trí Trạm Sạc" xuất hiện
- [ ] Biểu đồ "Phân Bố Dân Số" xuất hiện (20 cột)

### Nếu lỗi:
```
Lỗi: ModuleNotFoundError
→ pip install -r requirements.txt

Lỗi: AttributeError
→ Kiểm tra dataset.py có hàm generate_data

Lỗi: 404 Not Found
→ Kiểm tra templates/index.html tồn tại
```

## 🔧 Bước 4: Test Hill Climbing

1. Nhập: Số trạm sạc = 5, Số lần = 100
2. **Nhấn "Hill Climbing"** (button xanh)

### Kiểm tra:
- [ ] Thông báo: "Đang chạy thuật toán..."
- [ ] Sau 5-10s: "Thuật toán chạy thành công!"
- [ ] Tab "Kết Quả" hiển thị:
  - Algorithm: "Random Restart Hill Climbing"
  - Chi Phí: Số dương (ví dụ: 150,234.56)
  - Số Trạm Sạc: 5
  - Vị Trí Trạm: [a, b, c, d, e] (5 số)
- [ ] Biểu đồ Chi Phí cập nhật
- [ ] Biểu đồ Vị Trí Trạm cập nhật (K điểm xanh)

## ⚙️ Bước 5: Test Simulated Annealing

1. **Nhấn "Simulated Annealing"** (button xanh dưới)

### Kiểm tra:
- [ ] Thông báo: "Đang chạy thuật toán..."
- [ ] Sau 10-20s: "Thuật toán chạy thành công!"
- [ ] Tab "Kết Quả" hiển thị:
  - Algorithm: "Simulated Annealing"
  - Chi Phí: Số dương (thường nhỏ hơn HC)
  - Số Trạm Sạc: 5
  - Vị Trí Trạm: 5 số khác nhau
- [ ] Chi tiết có "Số bước" và "Nhiệt độ cuối"

## 🔄 Bước 6: Test So Sánh

1. **Nhấn "So Sánh Cả 2"** (button xanh)

### Kiểm tra:
- [ ] Thông báo: "Đang so sánh các thuật toán..."
- [ ] Sau 20-30s: "So sánh hoàn tất!"
- [ ] Tự động chuyển sang Tab "So Sánh"
- [ ] Hiển thị 2 card:
  - **Hill Climbing**: Cost, Avg, Max, Std, Vị trí
  - **Simulated Annealing**: Cost, Bước, Nhiệt độ, Vị trí
- [ ] Có mũi tên ✓ hoặc ✗ cho cái nào tốt hơn
- [ ] % cải thiện (ví dụ: 5.23%)
- [ ] 2 biểu đồ dưới cùng

## 📊 Bước 7: Test Tab "Biểu Đồ"

1. Nhấn Tab **"Biểu Đồ"**

### Kiểm tra:
- [ ] 2 Biểu đồ hiển thị:
  - Bubble chart (xanh = khu vực, xanh đậm = trạm)
  - Bar chart (dân số 20 khu đầu)
- [ ] Hover lên điểm hiển thị thông tin

## 📈 Bước 8: Test Tab "So Sánh"

1. Nhấn Tab **"So Sánh"**

### Kiểm tra:
- [ ] 2 Card hiển thị chi tiết 2 thuật toán
- [ ] 2 Biểu đồ:
  - Biểu đồ chi phí theo chu kỳ
  - Biểu đồ so sánh hiệu suất (2 cột)
- [ ] Có chú giải (legend)

## 🔀 Bước 9: Test Responsive

1. Mở **F12** → Device toolbar (Ctrl+Shift+M)
2. Thay đổi kích thước: Mobile (375px), Tablet (768px), Desktop

### Kiểm tra:
- [ ] Mobile: Layout chồng nhau (1 cột)
- [ ] Tablet: Layout ổn định
- [ ] Desktop: Layout bình thường
- [ ] Nút & input responsive
- [ ] Biểu đồ thu nhỏ đúng

## 🎯 Bước 10: Test Scenarios

### Scenario 1: Ít dữ liệu, ít trạm
```
Khu vực: 10
Trạm: 2
Kết quả mong đợi: Rất nhanh (< 1s)
```

### Scenario 2: Nhiều dữ liệu, nhiều trạm
```
Khu vực: 100
Trạm: 10
Kết quả mong đợi: Chậm hơn (20-30s)
```

### Scenario 3: So sánh
```
30 khu, 5 trạm, RRHC 50x
Kết quả mong đợi: SA thường tốt hơn HC 10-20%
```

## 🐛 Troubleshooting

### Vấn đề: Trang không load
**Giải pháp:**
```bash
# Console sẽ báo lỗi. Kiểm tra:
1. Folder templates/ có index.html?
2. Folder static/ có js/main.js & css/style.css?
3. Flask chạy không lỗi?
```

### Vấn đề: API trả về lỗi 500
**Giải pháp:**
```python
# Kiểm tra terminal/console:
1. ModuleNotFoundError? → pip install -r requirements.txt
2. Error in dataset.py? → Kiểm tra import
3. Port lỗi? → Đổi port trong app.py
```

### Vấn đề: Biểu đồ không vẽ
**Giải pháp:**
1. Kiểm tra main.js load đúng (F12 → Network)
2. Kiểm tra Chart.js CDN có load (F12 → Network)
3. Console có lỗi? (F12 → Console)

### Vấn đề: Ứng dụng chậm
**Giải pháp:**
```python
# config.py
SA_MAX_STEPS = 5000  # Giảm từ 15000 xuống
# hoặc trong giao diện:
Khu vực: 30 → 20
Num Restarts: 100 → 50
```

## ✅ Verification Checklist

Hoàn thành tất cả các test này:

### Frontend Tests
- [ ] Trang load đúng
- [ ] Form input hoạt động
- [ ] Nút bấm responsive
- [ ] Tab chuyển đổi
- [ ] Biểu đồ vẽ
- [ ] Hover tooltip hoạt động
- [ ] Mobile responsive

### Backend Tests
- [ ] API /api/generate_data trả về JSON
- [ ] API /api/run_algorithm trả về chi phí
- [ ] API /api/compare_algorithms trả về so sánh
- [ ] Error handling hoạt động
- [ ] Không có 500 error

### Algorithm Tests
- [ ] HC chi phí giảm dần
- [ ] SA chi phí giảm dần
- [ ] Số trạm = K đúng
- [ ] Chi phí không âm
- [ ] Vị trí trong phạm vi

### Performance Tests
- [ ] Dữ liệu 30: < 1s
- [ ] HC 100x: 5-10s
- [ ] SA 15000 steps: 10-20s
- [ ] So sánh: 20-30s

## 📊 Ví Dụ Kết Quả

Sau khi chạy thành công, bạn sẽ thấy:

```
Khu vực: 30
Trạm: 5

Hill Climbing:
- Chi phí: 234,567.89
- Trung bình: 245,000.00
- Max: 267,890.00
- Vị trí: [3, 8, 15, 22, 28]

Simulated Annealing:
- Chi phí: 198,234.56
- Bước: 14,923
- Nhiệt độ cuối: 0.12
- Vị trí: [2, 9, 14, 21, 27]

Kết luận: SA tốt hơn 15.54%
```

## 🎓 Debug Tips

### Xem request/response
```javascript
// Mở console (F12) và xem:
// 1. Network tab → API calls
// 2. Console tab → JavaScript errors
// 3. Elements tab → DOM structure
```

### Xem server log
```
# Terminal nơi chạy python app.py
# Sẽ hiển thị tất cả requests
```

### Kiểm tra cấu trúc file
```bash
# Windows Command Prompt
tree /F

# hoặc
dir /S
```

## 🎉 Thành Công!

Nếu tất cả test đều pass, ứng dụng của bạn:
✅ **Hoàn toàn hoạt động!**

Bây giờ bạn có thể:
- 📊 Sử dụng cho nghiên cứu
- 🎓 Demo cho sinh viên
- 🚀 Deploy lên server
- 🔧 Mở rộng thêm tính năng

---

**Chúc bạn sử dụng vui vẻ!** 🎉

Nếu gặp vấn đề, hãy kiểm tra lại các bước này hoặc đọc README.md chi tiết hơn.

# Thiết kế hệ thống hiện tại

Tài liệu bổ sung ngày 16/10/2026, mô tả mã nguồn đang có.

## Kiến trúc

```text
Trình duyệt (HTML/CSS/JavaScript trong server.py)
    → GET /api/students?q=...
ThreadingHTTPServer (127.0.0.1:18765)
    → SQLite students.db → JSON → bảng kết quả

benchmark.py → API → results.csv
analyze.py → results.csv → analyzed_results.csv + measured_chart.png
k6_search.js → API (kịch bản tùy chọn độc lập)
```

Mỗi yêu cầu tìm kiếm mở kết nối SQLite riêng với timeout 10 giây. Giao diện nằm trong hằng PAGE; không có bước build frontend.

## Cơ sở dữ liệu

| Cột | Kiểu | Ý nghĩa |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Khóa chính |
| code | TEXT | Mã mẫu |
| name | TEXT | Tên mẫu |
| class_name | TEXT | Lớp mẫu |

Khởi tạo i từ 1 đến 5.000: code là `SV{i:05}`, name là `Sinh viên {i}`, class_name là `CNTT{(i%8)+1:02}`. Có chỉ mục idx_code; LIKE có wildcard đầu và OR nên không thể mặc định kết luận chỉ mục tăng tốc truy vấn.

## API

GET `/` trả HTTP 200, HTML UTF-8. GET `/api/students?q=SV00001` trả JSON:

```json
{"count":1,"students":[{"code":"SV00001","name":"Sinh viên 1","class_name":"CNTT02"}]}
```

q là tùy chọn, mặc định chuỗi rỗng. Các đường dẫn GET khác trả 404. Không có API ghi dữ liệu.

## Đo tải và phân tích

CSV có level (số luồng tối đa), trial (0–99 mỗi mức), latency_ms (thời gian gửi và đọc xong phản hồi), status và timestamp (Unix time). Ngoại lệ gửi yêu cầu được ghi status=0.

Phân tích dùng StandardScaler và IsolationForest: 200 cây, contamination=0.08, random_state=42; đặc trưng level và latency_ms. Kết quả bổ sung ai_anomaly và fixed_threshold_alert. Ngưỡng cố định là quantile 0,95 tại mức 1 luồng.

Benchmark tính P95 theo vị trí `int(0.95*(n-1))` trong dãy đã sắp xếp; pandas dùng nội suy quantile mặc định nên hai giá trị P95 có thể khác nhau.

Mô hình huấn luyện và chấm cùng dữ liệu; chưa có tập kiểm tra riêng hoặc nhãn lỗi thật. Contamination định hướng tỷ lệ cảnh báo. Cần nhiều lần chạy, warm-up, kiểm soát tải máy, CPU/RAM và nhãn độc lập để đánh giá hiệu quả.

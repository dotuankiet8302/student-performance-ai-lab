# Báo cáo chạy thử

Ngày lập: 16/10/2026. Môi trường: Windows, Python 3.12, SQLite và HTTP loopback. Kiểm tra chức năng bằng HTTP trực tiếp; chưa kiểm thử toàn bộ thao tác giao diện bằng trình duyệt tự động.

## Kiểm tra chức năng đã thực hiện

| Ca | Đầu vào / thao tác | Kết quả quan sát | Đánh giá |
| --- | --- | --- | --- |
| TC01 | Đếm bảng students | 5.000 bản ghi | Đạt |
| TC02 | PRAGMA integrity_check | ok | Đạt |
| TC03 | GET `/` | 200, HTML chứa Tra cứu sinh viên | Đạt |
| TC04 | q=SV00001 | 1 hồ sơ | Đạt |
| TC05 | q=CNTT01 | 25 hồ sơ | Đạt |
| TC06 | q=Sinh viên 5000 | 1 hồ sơ | Đạt |
| TC07 | q=NO_MATCH_987654 | 0 hồ sơ | Đạt |
| TC08 | q rỗng | 25 hồ sơ | Đạt |
| TC09 | q=' OR 1=1-- | 0 hồ sơ | Đạt với đầu vào này |
| TC10 | GET `/missing` | HTTP 404 | Đạt |

TC09 không phải đánh giá bảo mật toàn diện.

## Đo tải bằng benchmark.py

100 yêu cầu mỗi mức tới `/api/students?q=SV001`, không đặt độ trễ nhân tạo trong lần chạy này.

| Luồng tối đa | Yêu cầu | P95 theo benchmark (ms) | Lỗi HTTP / kết nối |
| ---: | ---: | ---: | ---: |
| 1 | 100 | 17,72 | 0 |
| 5 | 100 | 15,73 | 0 |
| 10 | 100 | 16,34 | 0 |
| 20 | 100 | 30,30 | 0 |
| 50 | 100 | 1015,29 | 0 |

Tổng 500/500 yêu cầu HTTP 200. Số luồng không phải số người dùng thực hoặc RPS. Độ trễ cao ở 50 luồng chưa đủ để kết luận nguyên nhân. Đây là một lần chạy cục bộ, chưa chứng minh năng lực production.

Dữ liệu: [results.csv](../results.csv). Chạy lại sẽ ghi đè, cần sao lưu để so sánh.

## Phân tích AI

Chạy analyze.py thành công sau khi bổ sung thư viện: P95 pandas tại 1 luồng khoảng 17,95 ms; 40 cờ Isolation Forest và 66 cờ vượt ngưỡng. P95 khác bảng do cách tính quantile, xem [thiết kế](THIET_KE_HE_THONG.md).

Kết quả: [analyzed_results.csv](../analyzed_results.csv).

![Biểu đồ độ trễ và cờ AI](../measured_chart.png)

Không có nhãn lỗi độc lập nên chưa thể suy ra precision, recall, F1 hoặc kết luận AI tốt hơn ngưỡng cố định.

## Chưa kiểm thử

- k6 và các ngưỡng của k6.
- Thí nghiệm LAB_DELAY_MS=120 so sánh baseline.
- Nhiều lần lặp, CPU/RAM, đánh giá trên tập riêng.
- Toàn diện về trình duyệt, khả năng truy cập, bảo mật và triển khai.

## Kết luận trong phạm vi thử nghiệm

Website và pipeline benchmark → CSV → phân tích → biểu đồ hoạt động trong môi trường đã thử. Chưa sửa mã nguồn ứng dụng trong đợt kiểm tra này. Cần khảo sát thêm độ trễ ở mức đồng thời cao.

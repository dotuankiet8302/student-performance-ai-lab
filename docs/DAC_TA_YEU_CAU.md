# Đặc tả yêu cầu phần mềm

Phiên bản 1.0 — 16/10/2026. Tài liệu bổ sung dựa trên mã nguồn và kết quả chạy thử, không phải tài liệu có trước khi phát triển.

## Mục tiêu và phạm vi

Student Performance + AI Lab phục vụ tra cứu sinh viên, đo độ trễ API và khảo sát phát hiện bất thường bằng Isolation Forest. Hệ thống dùng 5.000 hồ sơ tổng hợp, không sử dụng thông tin sinh viên thật.

Phạm vi hiện tại: tra cứu, đo tải cục bộ, xuất CSV, phân tích và biểu đồ. Chưa có đăng nhập, phân quyền, thêm/sửa/xóa sinh viên hoặc quản lý điểm. Đây chưa phải hệ thống quản lý sinh viên đầy đủ.

## Người dùng

| Đối tượng | Nhu cầu |
| --- | --- |
| Người tra cứu | Tìm theo mã, tên hoặc lớp |
| Người kiểm thử | Chạy benchmark và đọc số liệu độ trễ |
| Người phân tích | So sánh cảnh báo AI với ngưỡng cố định |

## Yêu cầu chức năng và tiêu chí chấp nhận

| Mã | Chức năng | Hành vi mong đợi |
| --- | --- | --- |
| FR01 | Khởi tạo | Tạo bảng nếu chưa có; thêm 5.000 hồ sơ nếu bảng rỗng |
| FR02 | Trang chủ | GET `/` trả HTML tiếng Việt, tự tìm `SV001` khi tải trang |
| FR03 | Tìm kiếm | GET `/api/students?q=...` tìm chuỗi con trong mã, tên hoặc lớp bằng LIKE có tham số |
| FR04 | Giới hạn | Dùng tối đa 40 ký tự đầu của q, trả tối đa 25 hồ sơ; q rỗng trả tối đa 25 hồ sơ |
| FR05 | Hiển thị | Bảng có mã, họ tên, lớp; hiển thị số hồ sơ trả về và thời gian đo từ trình duyệt |
| FR06 | Không khớp | HTTP 200, count=0 và students là mảng rỗng |
| FR07 | Không có đường dẫn | GET đường dẫn không tồn tại trả HTTP 404 |
| FR08 | Benchmark | 100 yêu cầu mỗi mức 1, 5, 10, 20, 50 luồng; xuất 500 dòng CSV |
| FR09 | Phân tích | Chuẩn hóa level, latency_ms; xuất cờ AI, cờ ngưỡng và biểu đồ |
| FR10 | Chèn độ trễ | LAB_DELAY_MS dương thêm thời gian chờ tối đa 500 ms mỗi yêu cầu API |

## Ràng buộc và yêu cầu phi chức năng

- Python 3.10 trở lên; server và benchmark chỉ dùng thư viện chuẩn.
- Máy chủ chỉ lắng nghe `127.0.0.1:18765`, dữ liệu SQLite, API JSON UTF-8.
- Truy vấn dùng tham số SQL; `%` và `_` vẫn là wildcard của LIKE.
- Chưa có chỉ tiêu hiệu năng được nghiệm thu. Ngưỡng k6 là cấu hình thực nghiệm.
- Cờ AI chưa được đối chiếu với nhãn lỗi thật, không thay thế kết luận kiểm thử.

## Luồng tra cứu

1. Người dùng mở trang, hệ thống tự tìm SV001.
2. Nhập mã, tên hoặc lớp, bấm Tìm kiếm.
3. Trình duyệt mã hóa truy vấn, gọi API; máy chủ truy vấn SQLite.
4. API trả tối đa 25 hồ sơ, giao diện cập nhật bảng và thời gian đo.

## Giới hạn đã biết

`count` là số hồ sơ trả về, không phải tổng số khớp. Chưa có phân trang hoặc ORDER BY. Giao diện chưa xử lý lỗi mạng rõ ràng; dùng innerHTML dựng bảng nên nếu mở rộng sang dữ liệu người dùng nhập cần escape hoặc dùng textContent. LAB_DELAY_MS không phải số chưa được xử lý thân thiện.

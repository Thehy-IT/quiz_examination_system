# 🗺️ Lộ trình Phát triển - Quiz Examination System

Tài liệu này ghi lại các giai đoạn phát triển của ứng dụng, từ nền tảng ban đầu đến các tính năng hoàn chỉnh và các bước cải tiến trong tương lai.
 
## ✅ Phase 1: UI Foundation & Design System (Đã hoàn thành)
*Mục tiêu: Xây dựng bộ khung vững chắc cho toàn bộ ứng dụng.*
- [x] **Nền tảng dự án**: Thiết lập cấu trúc thư mục module hóa (`components`, `views`, `utils`, `data`).
- [x] **Hệ thống Design**: Định nghĩa các hằng số về giao diện (màu sắc, khoảng cách, typography) trong `constants.py`.
- [x] **Quản lý Trạng thái**: Thiết lập `app_state.py` để quản lý trạng thái toàn cục.
- [x] **Dữ liệu Mẫu**: Tạo `mock_data.py` để mô phỏng hoạt động của ứng dụng trước khi có database.

## ✅ Phase 2: Core Components & Navigation (Đã hoàn thành)
*Mục tiêu: Xây dựng các khối giao diện cơ bản và luồng điều hướng chính.*
- [x] **Thư viện Component**: Xây dựng các thành phần giao diện tái sử dụng (`create_primary_button`, `create_card`, etc.).
- [x] **Hệ thống Điều hướng**: Hoàn thiện `create_sidebar` và `create_app_bar` với logic phân quyền.
- [x] **Giao diện Responsive**: Xử lý việc tự động chuyển đổi giữa sidebar và drawer khi thay đổi kích thước cửa sổ.
- [x] **Trang Đăng nhập**: Hoàn thiện giao diện và logic cơ bản cho trang đăng nhập.
 
## ✅ Phase 3: Instructor/Admin Views (Đã hoàn thành)
*Mục tiêu: Hoàn thiện tất cả các tính năng dành cho vai trò Giảng viên và Quản trị viên.*
- [x] **Dashboard**: Hiển thị các số liệu thống kê tổng quan.
- [x] **Quản lý Bài thi (Quiz Management)**: Giao diện CRUD hoàn chỉnh cho bài thi, bao gồm các bộ lọc, tìm kiếm, form tạo/sửa chi tiết (thời gian, mật khẩu, xáo trộn, v.v.).
- [x] **Quản lý Câu hỏi (Question Management)**: Giao diện CRUD cho câu hỏi, hỗ trợ nhiều loại câu hỏi khác nhau.
- [x] **Tạo từ Ngân hàng câu hỏi**: Cho phép tạo bài thi nhanh bằng cách chọn các câu hỏi có sẵn.
- [x] **Xem trước Bài thi**: Giảng viên có thể trải nghiệm bài thi dưới góc nhìn của sinh viên.
- [x] **Xem Kết quả & Phân tích**: Trực quan hóa kết quả thi của sinh viên qua biểu đồ và bảng thống kê.
- [x] **Quản lý Người dùng (Admin)**: Giao diện CRUD cho tài khoản người dùng, bao gồm phân quyền và gán lớp.
- [x] **Quản lý Lớp học (Admin)**: Giao diện CRUD cho lớp học.
- [x] **Cài đặt tài khoản**: Cho phép thay đổi mật khẩu.

## ✅ Phase 4: Examinee (Student) Views (Đã hoàn thành)
*Mục tiêu: Hoàn thiện tất cả các tính năng dành cho vai trò Sinh viên.*
- [x] **Dashboard**: Hiển thị danh sách các bài thi có sẵn cho lớp của sinh viên.
- [x] **Giao diện Làm bài**: Giao diện làm bài thi tập trung, có đồng hồ đếm ngược, bảng điều hướng câu hỏi, và chức năng đánh dấu câu hỏi.
- [x] **Xử lý Bài thi**: Hỗ trợ làm bài thi có mật khẩu và tự động lưu câu trả lời.
- [x] **Xem Kết quả**: Hiển thị điểm số và kết quả ngay sau khi nộp bài.
- [x] **Xem lại Bài làm**: Cho phép xem lại chi tiết câu trả lời và đáp án đúng (nếu giảng viên cho phép).
- [x] **Lịch sử Làm bài**: Theo dõi tất cả các lần thi đã tham gia.
- [x] **Tổng quan Kết quả**: Biểu đồ trực quan hóa tiến độ học tập qua các bài thi.
- [x] **Thông tin Cá nhân**: Xem thông tin và đổi mật khẩu.

## ✅ Phase 5: Testing & Documentation (Đã hoàn thành)
*Mục tiêu: Đảm bảo chất lượng và tài liệu hóa dự án.*
- [x] **Kiểm thử Giao diện**: Tạo file `test_ui.py` để xác minh các component cơ bản.
- [x] **Tài liệu hóa**: Hoàn thiện `README.md` và `todo.md` để hướng dẫn sử dụng và theo dõi tiến độ.
- [x] **Kiểm tra Responsive**: Đảm bảo giao diện hoạt động tốt trên các kích thước màn hình khác nhau.

---
 
## 🚀 Phase 6: Backend Integration - Database Foundation (Các bước tiếp theo)
*Mục tiêu: Chuyển đổi từ dữ liệu mẫu sang cơ sở dữ liệu thực tế.*
- [ ] **Dependencies**: Thêm `SQLAlchemy` và `passlib` vào `requirements.txt`.
- [ ] **Database Models**: Tạo file `database/models.py` để định nghĩa các bảng (`User`, `Class`, `Quiz`, `Question`, `Attempt`, v.v.) bằng SQLAlchemy ORM.
- [ ] **Database Engine**: Tạo file `database/engine.py` để quản lý việc kết nối và khởi tạo session.
- [ ] **Initialization Script**: Viết hàm `init_db()` để tự động tạo các bảng và dữ liệu ban đầu.

## 🚀 Phase 7: Backend Integration - Authentication (Các bước tiếp theo)
*Mục tiêu: Xây dựng hệ thống xác thực người dùng an toàn với database.*
- [ ] **Auth Service**: Tạo `services/auth_service.py` để xử lý việc mã hóa và xác thực mật khẩu.
- [ ] **Cập nhật Logic Đăng nhập**: Thay thế việc kiểm tra `mock_data` bằng cách gọi `auth_service` và truy vấn database.
- [ ] **Cập nhật Logic Đổi mật khẩu**: Tích hợp `auth_service` vào chức năng đổi mật khẩu.

## 🚀 Phase 8: Backend Integration - CRUD Operations (Các bước tiếp theo)
*Mục tiêu: Chuyển đổi toàn bộ các chức năng đọc/ghi dữ liệu sang tương tác với database.*
- [ ] **Service Layer**: Xây dựng các service (`user_service`, `quiz_service`, v.v.) để chứa logic nghiệp vụ và tương tác với database.
- [ ] **Chuyển đổi các View**: Cập nhật tất cả các view (Quản lý người dùng, lớp, bài thi, làm bài, xem kết quả) để gọi các hàm từ service layer thay vì đọc từ `mock_data`.
- [ ] **Lưu kết quả thi**: Đảm bảo kết quả mỗi lần làm bài được lưu vào bảng `Attempt` trong database.
- [ ] **Dọn dẹp**: Xóa file `mock_data.py` sau khi hoàn tất chuyển đổi.

## 🚀 Phase 9: Advanced Features & Refinements (Tương lai)
*Mục tiêu: Nâng cao và hoàn thiện sản phẩm.*
- [ ] **Cập nhật Real-time**: Tích hợp `page.pubsub` để cập nhật giao diện tức thì.
- [ ] **Import/Export Dữ liệu**: Thêm chức năng nhập/xuất câu hỏi từ file Excel/CSV.
- [ ] **Cài đặt Nâng cao**: Giới hạn số lần làm bài, thông báo trong ứng dụng, v.v.
- [ ] **Đa ngôn ngữ (i18n)**: Hỗ trợ giao diện tiếng Anh và tiếng Việt.
- [ ] **Kiểm thử Nâng cao**: Viết unit test và integration test cho các service.
- [ ] **Đóng gói & Phân phối**: Đóng gói ứng dụng thành file thực thi (.exe, .app) bằng `flet pack`.
- [ ] **Tinh chỉnh UI/UX**: Cải thiện giao diện và trải nghiệm người dùng.

## Progress Tracking
- **Total Tasks**: 29 (Grouped)
- **Completed**: 17
- **In Progress**: 0
- **Remaining**: 12
- **Current Phase**: Phase 6 - Backend Integration - Database Foundation
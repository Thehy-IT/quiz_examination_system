# Modern Quiz App - Development Roadmap

Tài liệu này theo dõi lộ trình phát triển của ứng dụng, phản ánh cấu trúc hiện tại và các bước tiếp theo một cách chi tiết.

## ✅ Phase 1: UI Foundation & Design System (Đã hoàn thành)
- [x] 1. Thiết lập dự án Flet và cấu trúc thư mục (`components`, `views`, `utils`, `data`).
- [x] 2. Định nghĩa hệ thống design (`constants.py`): Colors, Spacing, Typography.
- [x] 3. Tạo các hàm trợ giúp UI cơ bản (`ui_helpers.py`): `create_card`, `create_badge`, etc.
- [x] 4. Thiết lập quản lý trạng thái toàn cục (`app_state.py`).
- [x] 5. Tạo dữ liệu mẫu (`mock_data.py`) cho users, quizzes, questions, classes.

## ✅ Phase 2: Core Components & Navigation (Đã hoàn thành)
- [x] 6. Xây dựng thư viện component: `create_primary_button`, `create_text_input`, etc.
- [x] 7. Xây dựng hệ thống navigation (`navigation.py`): `create_sidebar`, `create_app_bar`.
- [x] 8. Xử lý responsive layout (chuyển đổi giữa sidebar và drawer).
- [x] 9. Hoàn thiện trang đăng nhập (`login_view.py`).

## ✅ Phase 3: Instructor/Admin Views (Đã hoàn thành)
- [x] 10. **Dashboard**: Xây dựng trang Dashboard cho Giảng viên/Admin với các số liệu thống kê (`show_instructor_dashboard`).
- [x] 11. **Class Management (Admin)**: Xây dựng trang Quản lý Lớp học (`show_class_management`) cho Admin (tạo, xóa, xem danh sách).
- [x] 12. **User Management (Admin)**: Xây dựng trang Quản lý Người dùng (`show_user_management`) cho Admin (tạo, sửa, xóa, lọc).
- [x] 13. **Quiz Management**: Xây dựng trang Quản lý Bài thi (`show_quiz_management`) với các chức năng lọc, tìm kiếm và kích hoạt/vô hiệu hóa.
- [x] 14. **Quiz Creation Form**: Hoàn thiện form tạo/sửa bài thi với các tùy chọn chi tiết (thời gian, mật khẩu, xáo trộn câu hỏi/đáp án, gán cho lớp học).
- [x] 15. **Question Management**: Xây dựng trang Quản lý Câu hỏi chi tiết cho từng bài thi (`show_question_management`).
- [x] 16. **Multiple Question Types**: Hỗ trợ nhiều loại câu hỏi (trắc nghiệm, đúng/sai, điền vào chỗ trống, chọn nhiều đáp án, tự luận ngắn).
- [x] 17. **Quiz Preview**: Xây dựng trang Xem trước Bài thi (`show_quiz_preview`) cho phép giảng viên trải nghiệm bài thi như sinh viên.
- [x] 18. **Results & Analytics**: Xây dựng trang Xem Kết quả (`show_instructor_results_page`) với biểu đồ điểm, thống kê và bảng kết quả chi tiết.
- [x] 19. **Settings**: Xây dựng trang Cài đặt (`show_settings_page`) để xem thông tin và đổi mật khẩu.

## ✅ Phase 4: Examinee (Student) Views (Đã hoàn thành)
- [x] 20. Xây dựng trang Dashboard cho Sinh viên, liệt kê các bài thi có sẵn.
- [x] 21. Xây dựng giao diện làm bài thi (`show_quiz_taking_view`) với điều hướng câu hỏi.
- [x] 22. Xử lý logic chấm điểm và tính thời gian làm bài.
- [x] 23. Xây dựng trang hiển thị Kết quả sau khi nộp bài.
- [x] 24. Xây dựng trang Lịch sử làm bài (`show_attempt_history_view`).

## ✅ Phase 5: Testing & Documentation (Đã hoàn thành)
- [x] 25. Tạo file kiểm thử `test_ui.py` để xác minh các component và cấu trúc.
- [x] 26. Viết tài liệu `README.md` chi tiết, hướng dẫn cài đặt và sử dụng.
- [x] 27. Cập nhật `todo.md` để phản ánh tiến độ dự án.

---
 
## 🚀 Phase 6: Backend Integration - Database Foundation (Các bước tiếp theo)
- [ ] 28. **Dependencies**: Thêm `SQLAlchemy` và `passlib` (để mã hóa mật khẩu) vào `requirements.txt`.
- [ ] 29. **Database Models**: Tạo thư mục `database` và file `models.py` để định nghĩa các bảng: `User`, `Class`, `Quiz`, `Question`, `Option`, `Attempt` sử dụng SQLAlchemy ORM.
- [ ] 30. **Database Engine**: Tạo file `database/engine.py` chứa hàm khởi tạo engine, session và Base cho models.
- [ ] 31. **Initialization Script**: Viết hàm `init_db()` trong `database/engine.py` để tạo tất cả các bảng và chèn dữ liệu người dùng mặc định (admin, instructor, student) với mật khẩu đã được mã hóa.
- [ ] 32. **App Integration**: Gọi `init_db()` một lần khi ứng dụng khởi động trong `main.py`.

## 🚀 Phase 7: Backend Integration - Authentication (Các bước tiếp theo)
- [ ] 33. **Auth Service**: Tạo file `services/auth_service.py` chứa các hàm mã hóa và xác thực mật khẩu (sử dụng `passlib`).
- [ ] 34. **Login Logic**: Cập nhật `login_view.py` để gọi hàm xác thực từ `auth_service.py` và truy vấn `User` từ database thay vì `mock_data`.
- [ ] 35. **Password Change**: Cập nhật trang Cài đặt (`show_settings_page`) để sử dụng `auth_service.py` và cập nhật mật khẩu đã mã hóa trong database.

## 🚀 Phase 8: Backend Integration - CRUD Operations (Các bước tiếp theo)
- [ ] 36. **Service Layer**: Tạo thư mục `services` và các file service cho từng module (ví dụ: `user_service.py`, `quiz_service.py`, `class_service.py`). Các service này sẽ chứa logic nghiệp vụ và tương tác với database.
- [ ] 37. **User Management**: Chuyển đổi `show_user_management` từ `mock_data` sang sử dụng các hàm CRUD trong `user_service.py`.
- [ ] 38. **Class Management**: Chuyển đổi `show_class_management` từ `mock_data` sang sử dụng các hàm CRUD trong `class_service.py`.
- [ ] 39. **Quiz & Question Management**: Chuyển đổi các trang quản lý bài thi và câu hỏi sang sử dụng `quiz_service.py`.
- [ ] 40. **Quiz Taking**: Khi sinh viên nộp bài, lưu lại kết quả (điểm, thời gian, câu trả lời) vào bảng `Attempt` và các bảng liên quan trong database.
- [ ] 41. **Results & History Views**: Đọc dữ liệu kết quả và lịch sử làm bài từ database thay vì `mock_data` cho cả giảng viên và sinh viên.
- [ ] 42. **Cleanup**: Xóa file `mock_data.py` sau khi tất cả các view đã được chuyển đổi hoàn toàn sang dùng database.

## 🚀 Phase 9: Advanced Features & Refinements (Tương lai)
- [ ] 43. **Real-time Updates**: Tích hợp `page.pubsub` để cập nhật giao diện real-time (ví dụ: giảng viên thấy kết quả ngay khi sinh viên nộp bài).
- [ ] 44. **File I/O**: Thêm chức năng import/export câu hỏi từ file Excel/CSV cho một bài thi (sử dụng `pandas` hoặc `openpyxl`).
- [ ] 45. **Advanced Quiz Settings**: Thêm các cài đặt nâng cao cho bài thi (giới hạn số lần làm bài, cho phép xem lại đáp án chi tiết sau khi thi).
- [ ] 46. **In-App Notifications**: Xây dựng hệ thống thông báo trong ứng dụng (ví dụ: khi có bài thi mới).
- [ ] 47. **Internationalization (i18n)**: Tách các chuỗi văn bản ra file riêng để hỗ trợ đa ngôn ngữ (Anh/Việt).
- [ ] 48. **Unit & Integration Testing**: Viết test case chi tiết cho các `service` và logic nghiệp vụ bằng `pytest`.
- [ ] 49. **Deployment**: Đóng gói ứng dụng thành file thực thi (.exe, .app) để có thể chạy trên các máy khác mà không cần cài đặt Python (sử dụng `flet pack`).
- [ ] 50. **UI/UX Polish**: Tinh chỉnh lại giao diện, thêm hiệu ứng chuyển động, và cải thiện trải nghiệm người dùng dựa trên phản hồi.

## Progress Tracking
- **Total Tasks**: 50
- **Completed**: 27
- **In Progress**: 0
- **Remaining**: 23
- **Current Phase**: Phase 6 - Backend Integration - Database Foundation
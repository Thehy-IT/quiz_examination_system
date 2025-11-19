# 🎯 Quiz Examination System

Một ứng dụng thi trắc nghiệm hiện đại được xây dựng bằng Python và Flet, có giao diện người dùng sạch sẽ, điều hướng chuyên nghiệp và các tính năng quản lý bài kiểm tra toàn diện.

## ✨ Features

### 🎨 Hệ thống Design Hiện đại
- **Giao diện Sáng (Light Theme)**: Giao diện chuyên nghiệp, sạch sẽ.
- **Màu sắc nhất quán**: Bảng màu chính là màu xanh dương cùng với các màu ngữ nghĩa (thành công, lỗi, cảnh báo).
- **Hệ thống Typography**: Phân cấp văn bản được xây dựng cẩn thận.
- **Hệ thống Spacing**: Khoảng cách nhất quán dựa trên bội số của 4px.
- **Thư viện Component**: Các thành phần giao diện có thể tái sử dụng.

### 🧭 Điều hướng Chuyên nghiệp
- **Sidebar Điều hướng**: Hệ thống menu gọn gàng, phân quyền theo vai trò người dùng.
- **Trạng thái Active**: Phản hồi trực quan rõ ràng cho mục đang được chọn.
- **Hồ sơ Người dùng**: Hiển thị avatar và vai trò.
- **Bố cục Responsive**: Tự động thích ứng với các kích thước màn hình khác nhau (desktop và mobile).

### 👥 Vai trò Người dùng

#### 🎓 Giảng viên (Instructor) / Quản trị viên (Admin)
- **Dashboard**: Xem các số liệu thống kê tổng quan.
- **Quản lý Bài thi**: Tạo, sửa, xóa và tổ chức các bài thi.
- **Xây dựng Câu hỏi**: Thêm câu hỏi với nhiều định dạng khác nhau.
- **Xem trước Bài thi**: Trải nghiệm bài thi dưới góc nhìn của sinh viên.
- **Xem Kết quả & Phân tích**: Xem biểu đồ điểm, thống kê và kết quả chi tiết của sinh viên.
- **Quản lý Lớp học & Người dùng**: Quản lý lớp và tài khoản người dùng trong hệ thống (chỉ dành cho Admin).

#### 📚 Sinh viên (Examinee)
- **Dashboard**: Xem danh sách các bài thi có sẵn cho lớp của mình.
- **Giao diện Làm bài**: Tương tác với bài thi, theo dõi thời gian và điều hướng câu hỏi.
- **Xem Kết quả**: Nhận kết quả và điểm số ngay sau khi nộp bài.
- **Lịch sử Làm bài**: Theo dõi hiệu suất qua các lần thi.
- **Xem lại Bài làm**: Xem lại chi tiết câu trả lời của mình (nếu được giảng viên cho phép).

### 🎯 Tính năng Bài thi
- **Nhiều loại Câu hỏi**: Hỗ trợ Trắc nghiệm (chọn một), Đúng/Sai, Điền vào chỗ trống, Chọn nhiều đáp án, và Tự luận ngắn.
- **Cài đặt Nâng cao**: Tùy chọn đặt mật khẩu, xáo trộn câu hỏi, xáo trộn đáp án, và cho phép xem lại bài làm.
- **Theo dõi Thời gian**: Tự động đếm ngược thời gian làm bài.
- **Chấm điểm Tự động**: Tính toán kết quả và phần trăm điểm số ngay lập tức.
- **Điều hướng Câu hỏi**: Dễ dàng chuyển đổi giữa các câu hỏi, đánh dấu câu hỏi cần xem lại.

## 🚀 Bắt đầu

### Yêu cầu
- Python 3.7+
- pip (Python package installer)

### Cài đặt & Chạy ứng dụng

1.  **Clone hoặc tải về** dự án về máy của bạn.
2.  Mở terminal và **di chuyển đến thư mục gốc của dự án** (`quiz_examination_system`).
3.  **Cài đặt các thư viện cần thiết**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Chạy ứng dụng**:
    > **Quan trọng**: Đảm bảo bạn đang ở trong thư mục gốc của dự án (`quiz_examination_system`).
    ```bash
    python -m quiz_app.main
    ```

### Chạy với Docker (Tùy chọn)

Nếu bạn đã cài đặt Docker, bạn có thể build và chạy ứng dụng trong một container. Từ thư mục gốc của dự án:

1.  **Build Docker image**:
    ```bash
    docker build -t quiz-app-group15 .
    ```
2.  **Chạy container**:
    ```bash
    docker run -p 8080:8080 --name quiz-container quiz-app-group15
    ```
    Sau đó, mở trình duyệt và truy cập `http://localhost:8080`.

### Thông tin Đăng nhập (Tài khoản mẫu)

| Vai trò | Username | Password |
| :--- | :--- | :--- |
| Quản trị viên | `admin` | `admin` |
| Giảng viên | `instructor` | `instructor` |
| Sinh viên | `THEHY` | `THEHY` |
| Sinh viên | `TAI` | `TAI` |
| Sinh viên | `HUNG` | `HUNG` |

## 🎯 Luồng làm việc Hoàn chỉnh

### Đối với Giảng viên/Admin:
1.  **Đăng nhập** với tài khoản `instructor` hoặc `admin`.
2.  **Xem Dashboard** với các thống kê nhanh.
3.  **Điều hướng đến "Quiz Management"** qua sidebar.
4.  **Tạo bài thi mới** với các tùy chọn (tiêu đề, mô tả, thời gian, mật khẩu, lớp học...).
5.  Nhấn **"Manage Questions"** để vào trang quản lý câu hỏi cho bài thi vừa tạo.
6.  **Thêm câu hỏi** với nhiều loại khác nhau và thiết lập đáp án đúng.
7.  Nhấn **"Preview Quiz"** để xem trước bài thi.
8.  (Admin) Điều hướng đến **"User Management"** hoặc **"Classes Management"** để quản lý người dùng và lớp học.
9.  Điều hướng đến **"View Results"** để xem kết quả và phân tích điểm số của sinh viên.

### Đối với Sinh viên:
1.  **Đăng nhập** với tài khoản sinh viên (ví dụ: `THEHY`).
2.  **Xem các bài thi có sẵn** trên trang chủ.
3.  **Bắt đầu làm bài** (nhập mật khẩu nếu được yêu cầu).
4.  Trả lời các câu hỏi, **điều hướng** bằng các nút "Previous/Next" hoặc bảng điều hướng.
5.  **Đánh dấu (flag)** các câu hỏi cần xem lại.
6.  **Nộp bài** và xem kết quả chi tiết (điểm số, phần trăm).
7.  Điều hướng đến **"My Attempts"** để xem lại lịch sử các bài đã làm.

## 🏗️ Kiến trúc Kỹ thuật

### Cấu trúc Thư mục cơ bản

Dự án được tổ chức theo cấu trúc module rõ ràng để dễ dàng bảo trì và mở rộng.

```
quiz_examination_system/
├── assets/
│   └── logo.png
├── quiz_app/
│   ├── __init__.py
│   ├── main.py                 # Điểm khởi chạy chính của ứng dụng
│   ├── app_state.py            # Quản lý trạng thái toàn cục
│   ├── components/             # Các thành phần UI tái sử dụng
│   │   ├── navigation.py, question_widgets.py, ui_helpers.py
│   ├── data/
│   │   └── mock_data.py        # Dữ liệu mẫu cho ứng dụng
│   ├── utils/
│   │   └── constants.py        # Các hằng số (màu sắc, spacing, typography)
│   └── views/                  # Các màn hình (trang) của ứng dụng
│       ├── examinee_views.py, instructor_admin_views.py, login_view.py
├── README.md                   # Tài liệu này
├── requirements.txt            # Các thư viện Python cần thiết
└── todo.md                     # Lộ trình phát triển
```

### Thư viện Component
- `create_primary_button()`: Nút hành động chính.
- `create_secondary_button()`: Nút hành động phụ.
- `create_text_input()`: Trường nhập liệu cho form.
- `create_card()`: Khung chứa nội dung.
- `create_sidebar()`: Sidebar điều hướng.
- `create_badge()`: Nhãn trạng thái.
- `create_question_by_type()`: "Nhà máy" sản xuất widget cho từng loại câu hỏi.

## 🛠️ Tính năng cho Lập trình viên

### Chế độ Phát triển (Development Mode)
- **Bỏ qua Đăng nhập**: Tệp `main.py` được cấu hình để cho phép lập trình viên bỏ qua màn hình đăng nhập, giúp phát triển giao diện nhanh hơn.
  ```python
  # Trong quiz_app/main.py, bỏ comment ở khối người dùng và view mong muốn

  # Vào với tư cách sinh viên
  # app_state.current_user = mock_data.mock_users['THEHY']
  # show_examinee_dashboard()
  
  # Vào với tư cách giảng viên
  app_state.current_user = mock_data.mock_users['instructor']
  show_instructor_dashboard()
  
  # Chế độ bình thường (bắt đầu từ trang đăng nhập)
  # show_login()

## 🔮 Các cải tiến trong Tương lai
Dựa trên `todo.md`, các bước tiếp theo bao gồm:
- **Phase 6: Tích hợp Backend - Nền tảng Database**: Chuyển từ `mock_data` sang sử dụng SQLite với SQLAlchemy, định nghĩa models và khởi tạo database.
- **Phase 7: Tích hợp Backend - Xác thực**: Xây dựng service xác thực, mã hóa mật khẩu và cập nhật logic đăng nhập.
- **Phase 8: Tích hợp Backend - CRUD Operations**: Chuyển đổi tất cả các chức năng quản lý (người dùng, lớp, bài thi) sang tương tác với database.
- **Phase 9: Tính năng Nâng cao**: Thêm các chức năng như import/export câu hỏi, cập nhật real-time, đóng gói ứng dụng và hỗ trợ đa ngôn ngữ.

## 📄 Giấy phép

Mã nguồn mở - bạn có thể tự do sử dụng và chỉnh sửa cho các dự án của mình.

---

**Xây dựng với ❤️ bằng Python và Flet**

*Một ứng dụng thi trắc nghiệm hiện đại với thiết kế UI/UX chuyên nghiệp*

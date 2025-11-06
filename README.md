# HỆ THỐNG KHẢO THÍ TRẮC NGHIỆM (QUIZ EXAMINATION SYSTEM)

## GIỚI THIỆU DỰ ÁN (PROJECT INTRODUCTION)

Dự án phát triển Hệ thống Khảo thí Trắc nghiệm, được thiết kế để phục vụ nhiều nhóm người dùng khác nhau (Admin, Instructor, Student) với các chức năng cơ bản như quản lý tài khoản, ngân hàng câu hỏi, cấu hình bài thi và xem kết quả.

* **Môn học (Subject):** Kỹ thuật Phần mềm (Software Engineering)
* **Giảng viên (Instructor):** Trần Thị Mỹ Tiên
* **Nhóm Thực hiện (Implementation Team):** 15
* **Đơn vị:** Đại học Giao thông Vận tải Thành phố Hồ Chí Minh (Ho Chi Minh City University of Transport)
* **Phiên bản (Version):** 1.0 
* **Ngày hoàn thành tài liệu:** 10/11/2025

---

## STAGE 3 – TRIỂN KHAI (IMPLEMENTATION)

### 3.1. NGÔN NGỮ & CÔNG NGHỆ (LANGUAGE & TECHNOLOGY)

Dựa trên yêu cầu phi chức năng (Non-functional Requirements) về Maintainability và Compatibility:

| Hạng mục (Item) | Chi tiết (Details) | Yêu cầu từ SRS  |
| :--- | :--- | :--- |
| **Backend** | Python (Django/Flask) | Code viết bằng Python, sử dụng framework có cấu trúc tốt như Django hoặc Flask.  |
| **Frontend** | ... | Giao diện Responsive, tương thích với Chrome, Edge, Firefox, và hiển thị tốt trên thiết bị di động.  |
| **Database** | txt | Dựa trên sơ đồ Database Schema đã thiết kế.  |
| **Deployment** | Docker | Hệ thống có thể triển khai bằng Docker.  |

### 3.2. CÁC CHỨC NĂNG CHÍNH ĐƯỢC TRIỂN KHAI (KEY FUNCTIONALITIES)

Triển khai các phân hệ chính theo DFD Cấp 1 (DFD Level 1): 

| Process (DFD 1.0)  | Chức năng chi tiết (Detailed Functions)  | Actor liên quan  |
| :--- | :--- | :--- |
| **1.0 Manage Accounts & Classes**  | Quản lý tài khoản (Admin: tạo, sửa, xóa, phân quyền)  & Quản lý lớp học (Admin: tạo, sửa, xóa, thêm thành viên)  | Admin  |
| **2.0 Manage Exam Content**  | Quản lý Ngân hàng Câu hỏi (Question Bank) : Thêm, sửa, xóa câu hỏi (đa dạng loại câu hỏi: Multiple choice, True/False) và Phân loại theo độ khó.  | Instructor  |
| **3.0 Conduct Exam**  | Cấu hình Bài thi (Quiz configuration) , Lấy bài thi (Taking an Exam) , Tự động lưu/nộp bài. | Instructor, Student  |
| **4.0 Process Results & Grading**  | Chấm điểm Tự động/Thủ công (Automatic/Manual Scoring) , Xem kết quả/thống kê (View results, View statistics). | Instructor, Student |

### 3.3. TIÊU CHUẨN CODE (CODING STANDARDS)

* **Tính dễ bảo trì (Maintainability):** Mỗi module (user, exam, question, result) phải được thiết kế độc lập. 
* **Quy tắc Code:** Mã nguồn phải tuân theo quy tắc đặt tên biến và hàm, có comments trong các phần logic phức tạp. 
* **Bảo mật:** Mật khẩu phải được mã hóa (ví dụ: SHA-256, bcrypt) trước khi lưu. 

---

## STAGE 4 – KIỂM THỬ (TESTING)

Kiểm thử được thực hiện để đảm bảo hệ thống đáp ứng cả yêu cầu chức năng và phi chức năng.

### 4.1. KIỂM THỬ ĐƠN VỊ & TÍCH HỢP (UNIT & INTEGRATION TESTING)

* **Mục tiêu:** Kiểm tra tính đúng đắn của từng thành phần (module) và sự tương tác giữa chúng.
* **Ví dụ Test Case (Unit Test Cases):**
    * Xác minh thuật toán mã hóa mật khẩu (`passwordHash` trong `User` table) hoạt động chính xác. 
    * Kiểm tra hàm chấm điểm tự động (`Automatic Scoring`) có tính đúng điểm cho các loại câu hỏi khác nhau (Single Choice, Multiple Choice). 
    * Kiểm tra logic phân quyền: Đảm bảo **Student** chỉ có thể xem kết quả của chính mình. 

### 4.2. KIỂM THỬ HỆ THỐNG & HIỆU NĂNG (SYSTEM & PERFORMANCE TESTING)

* **Kiểm thử Hiệu năng (Performance Test):**
    * Thời gian phản hồi (Response Time) trung bình cho mỗi yêu cầu (ví dụ: loading page, submitting assignment) **≤ 3 giây**. 
    * Đảm bảo hệ thống xử lý được **50-110 người dùng đồng thời** mà không giảm hiệu suất đáng kể.
* **Kiểm thử Độ tin cậy (Reliability Test):**
    * Kiểm tra tính năng tự động lưu dữ liệu cục bộ (locally save data) khi mất kết nối Internet và đồng bộ hóa khi kết nối lại. 

### 4.3. QUẢN LÝ LỖI (BUG MANAGEMENT)

* **Gỡ lỗi (Debugging):** Tiến hành sửa các lỗi phát sinh trong quá trình kiểm thử.
* **Yêu cầu:** Ghi lại chi tiết lỗi, phân loại mức độ ưu tiên (severity), và kiểm tra lại (re-test) sau khi sửa.

---

## LIÊN HỆ & HỖ TRỢ (CONTACT & SUPPORT)

* **Thành viên Phụ trách Chính (Main Contributor):** Huynh The Hy (Chịu trách nhiệm cuối cùng cho tài liệu yêu cầu). 
* **Hotline Hỗ trợ (Support Hotline):** 038578241 

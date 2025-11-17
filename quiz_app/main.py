# quiz_app/main.py

import flet as ft

# Import các module đã tách
from . import app_state
from .data import mock_data
from .views.login_view import show_login
from .views.instructor_admin_views import show_instructor_dashboard
from .views.examinee_views import show_examinee_dashboard

def main_page(page: ft.Page):
    """Điểm vào chính của ứng dụng Flet"""
    
    # Gán đối tượng page cho biến trạng thái toàn cục để các module khác có thể truy cập
    app_state.current_page = page
    
    # Cấu hình trang
    page.title = "Modern Quiz App"
    page.theme_mode = "light"
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 800
    page.window_min_height = 600
    page.padding = 0
    page.spacing = 0
    
    def handle_resize(e):
        """
        Xử lý sự kiện thay đổi kích thước cửa sổ để cập nhật layout.
        Hàm này sẽ gọi lại hàm vẽ giao diện hiện tại để điều chỉnh cho phù hợp.
        """
        if app_state.current_view_handler:
            app_state.current_view_handler()
            return

    page.on_resize = handle_resize

    # --- BỎ QUA ĐĂNG NHẬP ĐỂ PHÁT TRIỂN GIAO DIỆN ---
    # Để bỏ qua màn hình đăng nhập, hãy làm theo các bước sau:
    # 1. Đặt người dùng hiện tại (current_user) thành một người dùng mẫu.
    # 2. Gọi hàm hiển thị dashboard tương ứng.
    # 3. Để bật lại trang đăng nhập, hãy xóa/bình luận các dòng dưới và bỏ bình luận dòng `show_login()`.

    # --- Chế độ phát triển ---
    # app_state.current_user = mock_data.mock_users['THEHY']  # Đăng nhập với tư cách 'examinee' 
    # show_examinee_dashboard()              # Đi thẳng vào dashboard của sinh viên
    app_state.current_user = mock_data.mock_users['instructor']
    show_instructor_dashboard()         # Đi thẳng vào dashboard

    # --- Chế độ hoạt động bình thường ---
    # show_login()                       # Bắt đầu từ trang đăng nhập

if __name__ == "__main__":
    # Chạy ứng dụng. Để chạy từ thư mục gốc, bạn có thể dùng lệnh: python -m quiz_app.main
    ft.app(target=main_page)
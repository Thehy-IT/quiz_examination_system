# QUIZ_EXAMINATION_SYSTEM/quiz_app/main.py

# File này là điểm khởi đầu, là "cổng chính" của toàn bộ ứng dụng.
# Khi chạy project, file này sẽ được thực thi đầu tiên.
import flet as ft

# --- Import các module cốt lõi ---
# Tụi mình import các module đã được tổ chức lại một cách gọn gàng.
from . import app_state
from .data import mock_data
from .views.login_view import show_login
from .views.instructor_admin_views import show_instructor_dashboard
from .views.examinee_views import show_examinee_dashboard


def main_page(page: ft.Page):
    """Điểm vào chính của ứng dụng Flet"""
    
    # --- Cấu hình trang chính (Page) ---
    # Thiết lập các thuộc tính cơ bản cho cửa sổ ứng dụng.
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
        Hàm này xử lý sự kiện khi người dùng thay đổi kích thước cửa sổ.
        Đây là chìa khóa để làm cho giao diện của tụi mình "responsive" (thích ứng).
        Nó sẽ gọi lại hàm vẽ view hiện tại (được lưu trong app_state.current_view_handler)
        để sắp xếp lại các control cho phù hợp với kích thước mới.
        """
        if app_state.current_view_handler:
            app_state.current_view_handler()
            return

    page.on_resize = handle_resize

    # Đây là một bước cực kỳ quan trọng:
    # Gán đối tượng `page` vào `app_state` để các module khác (views, components)
    # có thể truy cập và điều khiển trang chính (ví dụ: chuyển trang, hiển thị dialog,...).
    app_state.current_page = page
    
    # =============================================================================
    # CHẾ ĐỘ PHÁT TRIỂN (DEV MODE) - "CHEAT CODE" ĐỂ TEST GIAO DIỆN
    # =============================================================================
    # Để không phải đăng nhập lại mỗi lần sửa code, anh em có thể bỏ comment ở một trong
    # các khối dưới đây để vào thẳng trang mình cần.
    # Nhớ comment lại và bật `show_login()` khi cần test luồng hoàn chỉnh nhé!

    # --- Chế độ dev cho Giảng viên/Admin ---
    # app_state.current_user = mock_data.mock_users['instructor']
    # show_instructor_dashboard()

    # --- Chế độ dev cho Sinh viên ---
    # app_state.current_user = mock_data.mock_users['student']
    # show_examinee_dashboard()

    # --- Chế độ hoạt động bình thường ---
    show_login()                       # Bắt đầu từ trang đăng nhập (luồng chuẩn)

if __name__ == "__main__":
    # Cú pháp chuẩn của Python để chạy ứng dụng khi file này được thực thi trực tiếp.
    # Để chạy app, mở terminal ở thư mục gốc (quiz_examination_system) và gõ: python -m quiz_app.main
    ft.app(target=main_page)
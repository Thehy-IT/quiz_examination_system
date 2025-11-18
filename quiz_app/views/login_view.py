# c:\Users\VTPT\Downloads\CODE\quiz_examination_system\quiz_app\views\login_view.py
# File này định nghĩa giao diện và logic cho màn hình đăng nhập của ứng dụng.

import flet as ft

# --- Phần import ---
# Import các module cần thiết từ các file khác trong project.
from .. import app_state
from ..data import mock_data
from ..utils.constants import Colors, Spacing, Typography, BorderRadius

# Import các hàm "trợ thủ" (helper) để tái sử dụng code tạo UI,
# và import các view khác để có thể chuyển trang.
from ..components.ui_helpers import (
    create_text_input, 
    create_card, 
    create_subtitle, 
    create_primary_button, 
    create_app_background
)
from .instructor_admin_views import show_instructor_dashboard
from .examinee_views import show_examinee_dashboard


def show_login():
    """
    Hàm này chịu trách nhiệm dựng (render) toàn bộ giao diện trang đăng nhập.
    Mỗi khi được gọi, nó sẽ vẽ lại từ đầu.
    """
    
    # Dọn dẹp trang hiện tại trước khi vẽ giao diện mới.
    # `app_state` là một object global để quản lý trạng thái của toàn ứng dụng.
    app_state.current_page.clean()
    app_state.current_page.appbar = None
    
    # Khai báo các control (widget) cho form đăng nhập.
    # Mình dùng hàm helper `create_text_input` để code gọn hơn.
    username_field = create_text_input("Username", width=400, icon=ft.Icons.PERSON)
    password_field = create_text_input("Password", password=True, width=400, icon=ft.Icons.PASSWORD)
    error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    # --- Logic xử lý đăng nhập ---
    def handle_login_click(e):
        # Lấy giá trị từ 2 ô input, dùng `or ""` để phòng trường hợp giá trị là `None`.
        username = username_field.value or ""
        password = password_field.value or ""
        
        # B1: Kiểm tra validation cơ bản, xem người dùng có nhập đủ thông tin không.
        if not username.strip() or not password.strip():
            error_text.value = "Please enter both username and password"
            app_state.current_page.update()
            return
        
        # B2: "Xác thực" người dùng với dữ liệu giả lập (mock data).
        user = mock_data.mock_users.get(username.strip())
        if not user or user['password'] != password:
            error_text.value = "Invalid username or password"
            password_field.value = ""
            app_state.current_page.update()
            return
        
        # B3: Đăng nhập thành công, lưu thông tin người dùng vào state toàn cục.
        app_state.current_user = user
        error_text.value = ""
        
        # B4: Dựa vào vai trò (role) của user để chuyển hướng đến trang tương ứng.
        if user['role'] in ['instructor', 'admin']:
            show_instructor_dashboard()
        else:
            show_examinee_dashboard()
    
    # --- Bố cục giao diện (UI Layout) ---
    # Tạo một cái "thẻ" (Card) để chứa toàn bộ form đăng nhập.
    login_form = create_card(
        content=ft.Column([
            # Logo của ứng dụng
            ft.Image(src="assets/logo.png", width=100, height=100, fit=ft.ImageFit.CONTAIN),
            ft.Container(height=Spacing.LG),
            # Tiêu đề chính với hiệu ứng màu gradient, trông cho "xịn" hơn.
            ft.ShaderMask(
                content=ft.Text(
                    "QUIZ EXAMINATION SYSTEM",
                    size=Typography.SIZE_3XL,
                    weight=ft.FontWeight.W_700,
                    text_align=ft.TextAlign.CENTER
                ),
                blend_mode=ft.BlendMode.SRC_IN,
                shader=ft.LinearGradient(
                    colors=[Colors.PRIMARY, Colors.SUCCESS]
                )
            ),
            create_subtitle("Sign in to your account to continue"),
            # Thêm khoảng trống để các thành phần không dính vào nhau.
            ft.Container(height=Spacing.XXL),
            username_field,
            ft.Container(height=Spacing.LG),
            password_field,
            # Nút "Quên mật khẩu?", tạm thời chỉ in ra console khi click.
            ft.Container(
                content=ft.Text(
                    "Quên mật khẩu?",
                    size=Typography.SIZE_SM,
                    color=Colors.PRIMARY,
                    weight=ft.FontWeight.W_500,
                ),
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(top=Spacing.SM),
                width=400,
                ink=True,
                on_click=lambda e: print("Forgot Password clicked!"), # Hành động tạm thời
            ),
            ft.Container(height=Spacing.LG),
            error_text,
            ft.Container(height=Spacing.XL),
            # Nút đăng nhập chính, khi click sẽ gọi hàm `handle_login_click`.
            create_primary_button("Sign In", on_click=handle_login_click, width=400, icon=ft.Icons.LOGIN),
            ft.Container(height=Spacing.LG),
            # Dòng text nhỏ để hướng dẫn đăng nhập với tài khoản demo.
            ft.Text(
                "Demo credentials: instructor/instructor, student/student",
                size=Typography.SIZE_XS,
                color=Colors.TEXT_MUTED,
                text_align=ft.TextAlign.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=Spacing.XXXXL
     )
    
    # Tinh chỉnh thêm cho cái card đăng nhập.
    login_form.width = 900
    login_form.color = ft.Colors.TRANSPARENT
    login_form.elevation = 20
    login_form.height = 660
    login_form.shape = ft.RoundedRectangleBorder(radius=BorderRadius.XXL)

    # --- Tạo hiệu ứng nền kính trong suốt (Glassmorphism) ---
    # Đây là phần "ăn tiền" để làm cho form có hiệu ứng mờ ảo như kính.
    login_form.content.gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[
            ft.Colors.with_opacity(0.5, Colors.PRIMARY_LIGHTER),
            ft.Colors.with_opacity(0.6, Colors.GRAY_100),
            ft.Colors.with_opacity(0.7, Colors.PRIMARY_LIGHTEST),
        ]
    )
    login_form.content.bgcolor = None # Bỏ màu nền để gradient và blur có tác dụng
    login_form.content.blur = ft.Blur(20, 20, ft.BlurTileMode.MIRROR)
    login_form.content.border = ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.WHITE))
    login_form.content.border_radius = BorderRadius.XXL

    # Đặt form vào một cột (Column) để căn giữa theo chiều dọc và ngang.
    login_content = ft.Column(
        [login_form],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Sử dụng hàm helper để tạo background cho toàn bộ trang.
    login_container = create_app_background(login_content)
    # Thêm container chứa toàn bộ giao diện vào trang.
    app_state.current_page.add(login_container)
    
    # Lưu lại hàm `show_login` vào state. Việc này hữu ích khi cần vẽ lại view,
    # ví dụ như khi thay đổi kích thước cửa sổ.
    app_state.current_view_handler = show_login
    app_state.current_page.update()
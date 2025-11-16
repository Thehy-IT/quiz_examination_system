# QUIZ_EXAMINATION_SYSTEM/quiz_app/views/login_view.py

import flet as ft

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
from ..utils.constants import Colors, Spacing, Typography, BorderRadius

# Import các hàm trợ giúp UI và các hàm view khác để điều hướng
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
    """Hiển thị trang đăng nhập hiện đại của ứng dụng"""
    
    # Sử dụng các biến trạng thái toàn cục từ app_state
    app_state.current_page.clean()
    app_state.current_page.appbar = None
    
    # Các trường nhập liệu cho form
    username_field = create_text_input("Username", width=400, icon=ft.Icons.PERSON)
    password_field = create_text_input("Password", password=True, width=400, icon=ft.Icons.PASSWORD)
    error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    def handle_login_click(e):
        username = username_field.value or ""
        password = password_field.value or ""
        
        # Kiểm tra validation
        if not username.strip() or not password.strip():
            error_text.value = "Please enter both username and password"
            app_state.current_page.update()
            return
        
        # Kiểm tra thông tin đăng nhập với mock_data
        user = mock_data.mock_users.get(username.strip())
        if not user or user['password'] != password:
            error_text.value = "Invalid username or password"
            password_field.value = ""
            app_state.current_page.update()
            return
        
        # Đăng nhập thành công
        app_state.current_user = user
        error_text.value = ""
        
        # Điều hướng đến trang dashboard phù hợp
        if user['role'] in ['instructor', 'admin']:
            show_instructor_dashboard()
        else:
            show_examinee_dashboard()
    
    # Form đăng nhập
    login_form = create_card(
        content=ft.Column([
            ft.Image(src="assets/logo.png", width=100, height=100, fit=ft.ImageFit.CONTAIN),
            ft.Container(height=Spacing.LG),
            # --- Tạo hiệu ứng Gradient cho tiêu đề ---
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
            ft.Container(height=Spacing.XXL),
            username_field,
            ft.Container(height=Spacing.LG),
            password_field,
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
            create_primary_button("Sign In", on_click=handle_login_click, width=400, icon=ft.Icons.LOGIN),
            ft.Container(height=Spacing.LG),
            ft.Text(
                "Demo credentials: instructor/instructor, student/student",
                size=Typography.SIZE_XS,
                color=Colors.TEXT_MUTED,
                text_align=ft.TextAlign.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=Spacing.XXXXL
     )
    login_form.width = 900
    login_form.color = ft.Colors.TRANSPARENT
    login_form.elevation = 20
    login_form.height = 660
    login_form.shape = ft.RoundedRectangleBorder(radius=BorderRadius.XXL)

    # --- Tạo hiệu ứng nền kính trong suốt (Glassmorphism) ---
    login_form.content.gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[
            ft.Colors.with_opacity(0.5, Colors.PRIMARY_LIGHTER),
            ft.Colors.with_opacity(0.6, Colors.GRAY_100),
            ft.Colors.with_opacity(0.7, Colors.PRIMARY_LIGHTEST),
        ]
    )
    login_form.content.bgcolor = None
    login_form.content.blur = ft.Blur(20, 20, ft.BlurTileMode.MIRROR)
    login_form.content.border = ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.WHITE))
    login_form.content.border_radius = BorderRadius.XXL

    # Nội dung chính của trang đăng nhập
    login_content = ft.Column(
        [login_form],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Bọc nội dung bằng nền có hiệu ứng
    login_container = create_app_background(login_content)
    app_state.current_page.add(login_container)
    
    # Gán hàm xử lý hiện tại để có thể responsive
    app_state.current_view_handler = show_login
    app_state.current_page.update()
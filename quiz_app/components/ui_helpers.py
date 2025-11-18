# QUIZ_EXAMINATION_SYSTEM/quiz_app/components/ui_helpers.py

# File này là "hộp đồ nghề" UI của tụi mình.
# Mỗi hàm ở đây giống như một cái khuôn (factory function), giúp tạo ra các
# component (nút bấm, ô nhập liệu, thẻ card,...) với style nhất quán trong toàn bộ app.
# Nhờ vậy mà giao diện trông chuyên nghiệp và dễ bảo trì hơn rất nhiều.

import flet as ft

# Import các hằng số thiết kế từ module constants
# Dấu ".." biểu thị việc đi lên một cấp thư mục (từ components -> quiz_app) rồi vào utils
from ..utils.constants import Colors, Spacing, Typography, BorderRadius
from .. import app_state # Cần truy cập app_state để update UI, ví dụ như khi toggle password visibility.


def create_primary_button(text, on_click=None, width=None, disabled=False, icon=None):
    """Hàm "nhà máy" để tạo nút bấm chính (màu nền đậm).
    Việc dùng hàm này đảm bảo mọi nút chính trong app đều có chung style, từ màu sắc, bo góc đến hiệu ứng khi hover."""
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        icon=icon,
        width=width,
        height=44,
        disabled=disabled,
        style=ft.ButtonStyle(
            # Style cho các trạng thái khác nhau của nút (bình thường, khi di chuột qua, khi bị vô hiệu hóa).
            # Đây là cách làm rất chuyên nghiệp để UI có phản hồi tốt với người dùng.
            bgcolor={
                ft.ControlState.DEFAULT: Colors.PRIMARY,
                ft.ControlState.HOVERED: Colors.PRIMARY_LIGHT,
                ft.ControlState.DISABLED: Colors.GRAY_300
            },
            color={
                ft.ControlState.DEFAULT: Colors.WHITE,
                ft.ControlState.DISABLED: Colors.GRAY_500
            },
            shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
            elevation=2
        )
    )

def create_secondary_button(text, on_click=None, width=None):
    """Tạo nút bấm phụ (chỉ có viền). Thường dùng cho các hành động ít quan trọng hơn như "Cancel" hoặc "Back"."""
    return ft.OutlinedButton(
        text=text,
        on_click=on_click,
        width=width,
        height=44,
        style=ft.ButtonStyle(
            color=Colors.PRIMARY,
            side=ft.BorderSide(width=2, color=Colors.PRIMARY),
            shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
        )
    )

def create_text_input(label, password=False, width=None, multiline=False, min_lines=1, icon=None, can_reveal=False):
    """Tạo một ô nhập liệu (TextField) với style nhất quán.
    Hàm này còn xử lý logic phức tạp cho việc hiển thị/ẩn mật khẩu."""
    
    def toggle_password_visibility(e):
        # Đây là một hàm closure, nó có thể truy cập và thay đổi biến `text_field` ở bên ngoài.
        text_field.password = not text_field.password
        e.control.icon = ft.Icons.VISIBILITY_OFF if text_field.password else ft.Icons.VISIBILITY
        app_state.current_page.update()

    # Logic để thêm icon "con mắt" cho ô nhập mật khẩu.
    suffix_icon = None
    if password and can_reveal:
        suffix_icon = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            on_click=toggle_password_visibility,
            icon_color=Colors.TEXT_MUTED
        )

    text_field = ft.TextField(
        label=label,
        password=password,
        # Dùng tính năng `can_reveal_password` có sẵn của Flet nếu mình không dùng icon tự custom.
        can_reveal_password=password and not can_reveal,
        width=width,
        prefix_icon=icon,
        multiline=multiline,
        min_lines=min_lines,
        border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300,
        focused_border_color=Colors.PRIMARY,
        bgcolor=Colors.WHITE,
        color=Colors.TEXT_PRIMARY,
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        cursor_color=Colors.PRIMARY,
        suffix=suffix_icon
    )
    return text_field

def create_card(content, padding=Spacing.XL, elevation=2):
    """Tạo một thẻ Card, là một khối container có đổ bóng và bo góc, dùng để nhóm các nội dung liên quan."""
    return ft.Card(
        content=ft.Container(
            content=content,
            padding=padding,
            border_radius=BorderRadius.LG,
        ),
        elevation=elevation,
        surface_tint_color=Colors.WHITE
    )

def create_section_title(title, size=Typography.SIZE_XL):
    """Tạo tiêu đề cho một khu vực (section). Giúp duy trì sự nhất quán về mặt chữ trong toàn bộ app."""
    return ft.Text(
        title,
        size=size,
        weight=ft.FontWeight.W_600,
        color=Colors.TEXT_PRIMARY
    )

def create_page_title(title, color=Colors.TEXT_PRIMARY):
    """Tạo tiêu đề chính cho cả một trang, thường có kích thước lớn nhất."""
    return ft.Text(
        title,
        size=Typography.SIZE_3XL,
        weight=ft.FontWeight.W_700,
        color=color
    )

def create_subtitle(text):
    """Tạo một dòng tiêu đề phụ, thường đi kèm với tiêu đề chính để giải thích thêm."""
    return ft.Text(
        text,
        size=Typography.SIZE_BASE,
        color=Colors.TEXT_SECONDARY
    )

def create_badge(text, color=Colors.PRIMARY):
    """Tạo một "huy hiệu" (badge) nhỏ, dùng để hiển thị các thông tin ngắn gọn như trạng thái, tag,..."""
    return ft.Container(
        content=ft.Text(
            text,
            size=Typography.SIZE_XS,
            weight=ft.FontWeight.W_600,
            color=Colors.WHITE
        ),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=Spacing.XS),
        border_radius=BorderRadius.SM
    )

def create_app_background(content_control):
    """Tạo một background có hiệu ứng cho toàn bộ ứng dụng.
    Kỹ thuật ở đây là dùng `ft.Stack` để xếp chồng các lớp lên nhau:
    - Lớp dưới cùng là `LinearGradient`.
    - Các lớp ở giữa là các hình khối trang trí (shape) với độ mờ.
    - Lớp trên cùng là nội dung chính của trang (`content_control`)."""
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                Colors.PRIMARY_LIGHTEST,
                Colors.GRAY_100,
                Colors.PRIMARY_LIGHTER,
            ]
        ),
        content=ft.Stack([
            # Các hình khối trang trí cho background thêm phần "ảo diệu".
            ft.Container(
                width=150,
                height=150,
                bgcolor=ft.Colors.with_opacity(0.25, Colors.PRIMARY_LIGHT),
                border_radius=ft.border_radius.all(75),
                top=20,
                left=40,
            ),
            ft.Container(
                width=200,
                height=200,
                bgcolor=ft.Colors.with_opacity(0.08, Colors.SUCCESS),
                border_radius=ft.border_radius.all(100),
                bottom=20,
                right=50,
            ),
            ft.Container(
                width=100,
                height=100,
                bgcolor=ft.Colors.with_opacity(0.15, Colors.WARNING),
                border_radius=ft.border_radius.all(50),
                top=150,
                right=150,
            ),
            ft.Container(
                width=300,
                height=150,
                bgcolor=ft.Colors.with_opacity(0.07, Colors.PRIMARY),
                border_radius=BorderRadius.XXL,
                bottom=60,
                left=100,
            ),
            # Nội dung chính của trang được đặt lên trên cùng.
            content_control
        ])
    )
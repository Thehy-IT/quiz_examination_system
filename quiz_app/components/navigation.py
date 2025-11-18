# QUIZ_EXAMINATION_SYSTEM/quiz_app/components/navigation.py

import flet as ft

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
from ..utils.constants import Colors, Spacing, Typography, BorderRadius

# LƯU Ý: Các hàm hiển thị trang (show_...) sẽ được import BÊN TRONG các hàm
# để tránh lỗi "circular import", vì các file view sau này cũng sẽ cần 
# import các component từ file này.

# =============================================================================
# CÁC HÀM XỬ LÝ SỰ KIỆN LIÊN QUAN ĐẾN ĐIỀU HƯỚNG
# =============================================================================

def handle_logout(e=None):
    """Xử lý sự kiện đăng xuất của người dùng"""
    # Import hàm hiển thị trang đăng nhập tại đây
    from ..views.login_view import show_login
    
    app_state.current_user = None
    show_login()

def open_drawer(e):
    """Mở ngăn kéo điều hướng (sidebar) trên màn hình nhỏ"""
    if app_state.sidebar_drawer:
        app_state.sidebar_drawer.open = True
        app_state.sidebar_drawer.update()

def create_app_bar():
    """Tạo AppBar cho giao diện responsive với nút menu"""
    return ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer, tooltip="Menu"),
        leading_width=40
    )

# =============================================================================
# COMPONENT HEADER
# =============================================================================

def create_app_header():
    """Tạo header chính của ứng dụng với thông tin người dùng và thông báo"""
    if not app_state.current_user:
        return ft.Container()

    user_role = app_state.current_user.get('role')
    notifications = mock_data.mock_notifications.get(user_role, [])
    unread_count = sum(1 for n in notifications if not n['read'])

    def mark_as_read(notification):
        def on_click(e):
            notification['read'] = True
            # Trong ứng dụng thực tế, bạn sẽ cập nhật trạng thái này ở backend
            # Ở đây, ta chỉ cần vẽ lại header để cập nhật giao diện
            app_state.current_page.controls[0].content.controls[0].controls[0] = create_app_header()
            app_state.current_page.update()
        return on_click

    notification_items = []
    if notifications:
        for n in notifications:
            notification_items.append(
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(n['text'], size=Typography.SIZE_SM, color=Colors.TEXT_PRIMARY, weight=ft.FontWeight.W_600 if not n['read'] else ft.FontWeight.NORMAL),
                            ft.Text(n['timestamp'], size=Typography.SIZE_XS, color=Colors.TEXT_MUTED),
                        ], expand=True),
                        ft.Icon(ft.Icons.CIRCLE, color=Colors.PRIMARY, size=10) if not n['read'] else ft.Container(width=10)
                    ]),
                    on_click=mark_as_read(n)
                )
            )
    else:
        notification_items.append(
            ft.PopupMenuItem(
                content=ft.Text("No notifications", color=Colors.TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                enabled=False
            )
        )

    notification_button = ft.PopupMenuButton(
        content=ft.Stack([
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                icon_color=Colors.TEXT_SECONDARY,
                tooltip="Notifications"
            ),
            ft.Container(
                content=ft.Text(str(unread_count), size=10, color=Colors.WHITE, weight=ft.FontWeight.W_600),
                bgcolor=Colors.ERROR,
                padding=ft.padding.symmetric(horizontal=5),
                border_radius=10,
                right=5,
                top=5,
                visible=unread_count > 0
            )
        ]),
        items=notification_items
    )

    return ft.Container(
        content=ft.Row([
            # Bên trái có thể dùng cho breadcrumbs hoặc thanh tìm kiếm sau này
            ft.Container(expand=True),

            # Bên phải chứa thông tin người dùng
            ft.Row([
                notification_button,
                ft.VerticalDivider(width=1, color=Colors.GRAY_200),
                ft.Column([
                    ft.Text(
                        app_state.current_user.get('username', "User"),
                        size=Typography.SIZE_SM,
                        weight=ft.FontWeight.W_600,
                        color=Colors.TEXT_PRIMARY
                    ),
                    ft.Text(
                        app_state.current_user.get('role', "Role").title(),
                        size=Typography.SIZE_XS,
                        color=Colors.TEXT_SECONDARY
                    )
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(width=Spacing.MD),
                ft.CircleAvatar(
                    content=ft.Text(app_state.current_user['username'][0].upper(), color=Colors.WHITE, weight=ft.FontWeight.W_600),
                    bgcolor=Colors.PRIMARY,
                    radius=20
                ),
            ], spacing=Spacing.MD)
        ]),
        padding=ft.padding.symmetric(horizontal=Spacing.XXL, vertical=Spacing.MD),
        border=ft.border.only(bottom=ft.BorderSide(width=1, color=Colors.GRAY_200))
    )

# =============================================================================
# COMPONENTS SIDEBAR
# =============================================================================

def create_sidebar_item(icon, text, is_active=False, on_click=None):
    """Tạo một mục trong sidebar"""
    return ft.Container(
        content=ft.Row([
            ft.Icon(
                icon,
                size=20,
                color=Colors.PRIMARY if is_active else Colors.TEXT_SECONDARY
            ),
            ft.Text(
                text,
                size=Typography.SIZE_BASE,
                weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
                color=Colors.PRIMARY if is_active else Colors.TEXT_SECONDARY
            )
        ], spacing=Spacing.LG),
        padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.MD),
        border_radius=BorderRadius.MD,
        bgcolor=Colors.PRIMARY_LIGHTEST if is_active else None,
        border=ft.border.only(right=ft.BorderSide(width=3, color=Colors.PRIMARY)) if is_active else None,
        ink=True,
        on_click=on_click
    )

def create_sidebar(user_role, active_page="dashboard"):
    """Tạo thanh điều hướng sidebar"""
    # Import các module view tại đây để tránh lỗi circular import
    from ..views import instructor_admin_views, examinee_views

    sidebar_items = []
    
    if user_role in ['instructor', 'admin']:
        sidebar_items.append(create_sidebar_item(ft.Icons.HOME, "Home", active_page == "dashboard", on_click=lambda e: instructor_admin_views.show_instructor_dashboard()))
        
        if user_role == 'instructor':
            sidebar_items.append(create_sidebar_item(ft.Icons.QUIZ, "Quiz Management", active_page == "quizzes", on_click=lambda e: instructor_admin_views.show_quiz_management()))
            sidebar_items.append(create_sidebar_item(ft.Icons.EMOJI_EVENTS, "View Results", active_page == "results", on_click=lambda e: instructor_admin_views.show_results_overview()))

        if user_role == 'admin':
            sidebar_items.append(create_sidebar_item(ft.Icons.SCHOOL, "Classes Management", active_page == "classes", on_click=lambda e: instructor_admin_views.show_class_management()))
            sidebar_items.append(create_sidebar_item(ft.Icons.PEOPLE, "User Management", active_page == "users", on_click=lambda e: instructor_admin_views.show_user_management()))
        sidebar_items.extend([
            create_sidebar_item(ft.Icons.SETTINGS, "Settings", active_page == "settings", on_click=lambda e: instructor_admin_views.show_settings_page()),
        ])
    else:  # examinee
        sidebar_items = [
            create_sidebar_item(ft.Icons.HOME, "Home", active_page == "home", on_click=lambda e: examinee_views.show_examinee_dashboard()),
            create_sidebar_item(ft.Icons.LIBRARY_BOOKS, "My Attempts", active_page == "attempts", on_click=lambda e: examinee_views.show_my_attempts()),
            create_sidebar_item(ft.Icons.EMOJI_EVENTS, "Results", active_page == "results", on_click=lambda e: examinee_views.show_student_results_overview()),
            create_sidebar_item(ft.Icons.PERSON, "Profile", active_page == "profile", on_click=lambda e: examinee_views.show_profile_page()),
        ]
    
    # Thêm mục Đăng xuất
    sidebar_items.append(ft.Divider(color=Colors.GRAY_200))
    sidebar_items.append(
        create_sidebar_item(ft.Icons.LOGOUT, "Logout", on_click=handle_logout)
    )
    
    return ft.Container(
        content=ft.Column([
            # Phần Logo/Thương hiệu
            ft.Container(
                content=ft.Column([
                    ft.Image(src="assets/logo.png", width=80, height=80),
                    ft.Container(height=Spacing.SM),
                    ft.ShaderMask(
                        content=ft.Text(
                            "QUIZ EXAMINATION SYSTEM",
                            size=Typography.SIZE_LG,
                            weight=ft.FontWeight.W_700,
                            text_align=ft.TextAlign.CENTER
                        ),
                        blend_mode=ft.BlendMode.SRC_IN,
                        shader=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[Colors.PRIMARY, Colors.PRIMARY_LIGHTER, Colors.SUCCESS]
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            ft.Divider(color=Colors.GRAY_200),
            
            # Các mục điều hướng
            ft.Container(
                content=ft.Column(sidebar_items, spacing=Spacing.XS),
                expand=True,
                padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.LG)
            ),
            
            # Phần thông tin hỗ trợ
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUPPORT_AGENT, color=Colors.TEXT_SECONDARY, size=24),
                    ft.Column([
                        ft.Text(
                            "Technical Support",
                            size=Typography.SIZE_SM,
                            weight=ft.FontWeight.W_600,
                            color=Colors.TEXT_PRIMARY
                        ),
                        ft.Text("0385782400", size=Typography.SIZE_BASE, color=Colors.PRIMARY, weight=ft.FontWeight.W_500)
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.START)
                ], spacing=Spacing.MD),
                padding=Spacing.XL,
                border=ft.border.only(top=ft.BorderSide(width=1, color=Colors.GRAY_200)),
                alignment=ft.alignment.center
            )
        ]),
        width=280,
        height=None,
        bgcolor=Colors.WHITE,
        border=ft.border.only(right=ft.BorderSide(width=1, color=Colors.GRAY_200)),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(4, 0),
        ),
        clip_behavior=ft.ClipBehavior.NONE
    )
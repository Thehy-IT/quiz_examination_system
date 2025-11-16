# QUIZ_EXAMINATION_SYSTEM/quiz_app/components/ui_helpers.py

import flet as ft

# Import các hằng số thiết kế từ module constants
# Dấu ".." biểu thị việc đi lên một cấp thư mục (từ components -> quiz_app) rồi vào utils
from ..utils.constants import Colors, Spacing, Typography, BorderRadius
from .. import app_state # Cần truy cập app_state.current_page để update UI


def create_primary_button(text, on_click=None, width=None, disabled=False, icon=None):
    """Create a primary button with consistent styling"""
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        icon=icon,
        width=width,
        height=44,
        disabled=disabled,
        style=ft.ButtonStyle(
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
    """Create a secondary button with consistent styling"""
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
    """Create a text input with consistent styling"""
    
    def toggle_password_visibility(e):
        text_field.password = not text_field.password
        e.control.icon = ft.Icons.VISIBILITY_OFF if text_field.password else ft.Icons.VISIBILITY
        app_state.current_page.update()

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
        can_reveal_password=password and not can_reveal, # Use built-in reveal if custom one is not used
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
    """Create a card container with consistent styling"""
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
    """Create a section title with consistent styling"""
    return ft.Text(
        title,
        size=size,
        weight=ft.FontWeight.W_600,
        color=Colors.TEXT_PRIMARY
    )

def create_page_title(title, color=Colors.TEXT_PRIMARY):
    """Create a main page title"""
    return ft.Text(
        title,
        size=Typography.SIZE_3XL,
        weight=ft.FontWeight.W_700,
        color=color
    )

def create_subtitle(text):
    """Create subtitle text"""
    return ft.Text(
        text,
        size=Typography.SIZE_BASE,
        color=Colors.TEXT_SECONDARY
    )

def create_badge(text, color=Colors.PRIMARY):
    """Create a small badge"""
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
    """Creates the standard application background with a gradient and decorative shapes."""
    return ft.Container(
        expand=True,
        # The alignment is important to center the content if it doesn't expand
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
            # Decorative shapes
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
            # The main content is placed on top of the shapes
            content_control
        ])
    )
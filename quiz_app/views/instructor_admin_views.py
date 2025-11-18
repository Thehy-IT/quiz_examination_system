# QUIZ_EXAMINATION_SYSTEM/quiz_app/views/instructor_admin_views.py

import flet as ft
import datetime
import random

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
from ..utils.constants import Colors, Spacing, Typography, BorderRadius

# Import các hàm trợ giúp và component
from ..components.ui_helpers import (
    create_text_input, create_card, create_page_title, create_subtitle,
    create_primary_button, create_secondary_button, create_section_title, create_badge
)
from ..components.navigation import create_sidebar, create_app_bar, create_app_header
from ..components.question_widgets import create_question_by_type


def show_instructor_dashboard():
    """Hiển thị trang tổng quan cho giảng viên/admin"""
    app_state.current_page.clean()
    
    sidebar = create_sidebar(app_state.current_user['role'], "dashboard")
    
    def create_activity_item(log):
        icon_map = {
            'created a new quiz': (ft.Icons.QUIZ, Colors.PRIMARY),
            'đã tạo một bài thi mới': (ft.Icons.QUIZ, Colors.PRIMARY),
            'completed the quiz': (ft.Icons.CHECK_CIRCLE, Colors.SUCCESS),
            'đã hoàn thành bài thi': (ft.Icons.CHECK_CIRCLE, Colors.SUCCESS),
            'created a new user': (ft.Icons.PERSON_ADD, Colors.WARNING),
            'đã tạo người dùng mới': (ft.Icons.PERSON_ADD, Colors.WARNING),
            'created a new class': (ft.Icons.SCHOOL, Colors.PRIMARY_LIGHT),
            'đã tạo một lớp học mới': (ft.Icons.SCHOOL, Colors.PRIMARY_LIGHT),
        }
        icon, color = icon_map.get(log['action'], (ft.Icons.INFO, Colors.GRAY_400))

        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Container(width=Spacing.LG),
                ft.Column([
                    ft.Row([
                        ft.Text(log['user'], weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY),
                        ft.Text(log['action'], color=Colors.TEXT_SECONDARY),
                        ft.Text(f"'{log['details']}'", weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY),
                    ], spacing=Spacing.XS),
                    ft.Text(
                        f"Thời gian: {log['timestamp']}",
                        size=Typography.SIZE_XS,
                        color=Colors.TEXT_MUTED
                    )
                ], spacing=2)
            ]),
            padding=ft.padding.symmetric(vertical=Spacing.MD),
            border=ft.border.only(bottom=ft.BorderSide(1, Colors.GRAY_200))
        )

    stats_cards_list = []
    if app_state.current_user['role'] == 'admin':
        stats_cards_list.extend([
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SCHOOL, color=Colors.PRIMARY), ft.Text("Tổng số lớp học", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_data.mock_classes)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.PEOPLE_OUTLINE, color=Colors.SUCCESS), ft.Text("Tổng số người dùng", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_data.mock_users)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.FACE, color=Colors.WARNING), ft.Text("Tổng số sinh viên", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len([u for u in mock_data.mock_users.values() if u['role'] == 'examinee'])), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            )
        ])
    else: # instructor
        stats_cards_list.extend([
            create_card(
                content=ft.Column([
                    ft.Row([
                        ft.Image(src="assets/logo.png", width=24, height=24),
                        ft.Text("Total Quizzes", color=Colors.TEXT_SECONDARY)
                    ]),
                    ft.Text(
                        str(len([q for q in mock_data.mock_quizzes if q['created_by'] == app_state.current_user['id']])),
                        size=Typography.SIZE_3XL,
                        weight=ft.FontWeight.W_700,
                        color=Colors.TEXT_PRIMARY
                    )
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.HELP_OUTLINE, color=Colors.SUCCESS),
                        ft.Text("Total Questions", color=Colors.TEXT_SECONDARY)
                    ]),
                    ft.Text(
                        str(sum(len(mock_data.mock_questions.get(q['id'], [])) for q in mock_data.mock_quizzes if q['created_by'] == app_state.current_user['id'])),
                        size=Typography.SIZE_3XL,
                        weight=ft.FontWeight.W_700,
                        color=Colors.TEXT_PRIMARY
                    )
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PEOPLE, color=Colors.WARNING),
                        ft.Text("Active Students", color=Colors.TEXT_SECONDARY)
                    ]),
                    ft.Text(
                        "24", # Placeholder
                        size=Typography.SIZE_3XL,
                        weight=ft.FontWeight.W_700,
                        color=Colors.TEXT_PRIMARY
                    )
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            )
        ])
    
    stats_cards = ft.Row(stats_cards_list, spacing=Spacing.XL)
    
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title(f"Chào mừng trở lại, {app_state.current_user['username']}!"),
                            create_subtitle("Đây là tổng quan về các hoạt động trên hệ thống.") if app_state.current_user['role'] == 'admin' else create_subtitle("Here's what's happening with your quizzes today.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    stats_cards,
                    ft.Container(height=Spacing.XXXXL),
                    ft.Column([
                        ft.Column([
                            create_section_title("Lịch sử hoạt động"),
                            ft.Container(height=Spacing.LG),
                            create_card(
                                content=ft.Column([create_activity_item(log) for log in mock_data.mock_activity_log]),
                                padding=ft.padding.symmetric(horizontal=Spacing.XL)
                            )
                        ]) if app_state.current_user['role'] == 'admin' else
                        
                        ft.Column([
                            create_section_title("Recent Quizzes"),
                            ft.Container(height=Spacing.LG),
                            ft.Column(
                                [
                                    create_card(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Column([
                                                    ft.Text(quiz['title'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY),
                                                    ft.Text(quiz['description'], size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY)
                                                ], expand=True),
                                            ]),
                                            ft.Container(height=Spacing.SM),
                                            ft.Row([
                                                ft.Text(f"{quiz['questions_count']} questions", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                                                ft.Container(expand=True),
                                                create_secondary_button("Edit", on_click=lambda e, q=quiz: show_question_management(q), width=80),
                                                ft.Container(width=Spacing.SM),
                                                create_primary_button("View", on_click=lambda e: show_results_overview(), width=80)
                                            ])
                                        ]),
                                        padding=Spacing.XL
                                    ) for quiz in [q for q in mock_data.mock_quizzes if q['created_by'] == app_state.current_user['id']][:3]
                                ],
                                spacing=Spacing.LG
                            ) if any(q for q in mock_data.mock_quizzes if q['created_by'] == app_state.current_user['id']) else ft.Container(
                                content=ft.Text("No quizzes created yet. Create your first quiz to get started!", color=Colors.TEXT_MUTED),
                                padding=Spacing.XL
                            ),
                            ft.Container(height=Spacing.XL),
                            create_section_title("Các lớp được phân công"),
                            ft.Container(height=Spacing.LG),
                            ft.Column(
                                [
                                    create_card(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=Colors.PRIMARY),
                                            ft.Container(width=Spacing.LG),
                                            ft.Text(
                                                cls['name'],
                                                size=Typography.SIZE_LG,
                                                weight=ft.FontWeight.W_600,
                                                color=Colors.TEXT_PRIMARY
                                            )
                                        ]),
                                        padding=Spacing.LG
                                    ) for cls in [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
                                ],
                                spacing=Spacing.LG
                            ) if any(c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']) else ft.Container(
                                content=ft.Text("Bạn chưa được phân công vào lớp nào.", color=Colors.TEXT_MUTED),
                                padding=Spacing.XL
                            ),
                            ft.Container(height=Spacing.XL),
                            create_primary_button("Create New Quiz", on_click=lambda e: show_quiz_management(), width=200)
                        ])
                    ])
                ]),
                padding=Spacing.XXXXL,
                expand=True,
                bgcolor=Colors.GRAY_50
            )
        ]),
        padding=Spacing.XXXXL,
        expand=True
    )
    
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_instructor_dashboard

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

def show_quiz_management():
    """Hiển thị trang quản lý bài thi"""
    # Xóa tất cả các nội dung hiện có trên trang hiện tại để chuẩn bị tải nội dung mới.
    app_state.current_page.clean()
    
    sidebar = create_sidebar(app_state.current_user['role'], "quizzes")
    
    # Tạo trường nhập văn bản để tìm kiếm bài thi theo tiêu đề.
    search_field = create_text_input("Search by quiz title...", width=300, icon=ft.Icons.SEARCH)

    #Lọc, khởi tạo các tùy chọn lọc, tạo các dropdown lọc
    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_filter_options = [ft.dropdown.Option(key="all", text="Tất cả các lớp")]
    class_filter_options.extend([ft.dropdown.Option(key=str(cls['id']), text=cls['name']) for cls in instructor_classes])
    
    class_filter_dropdown = ft.Dropdown(label="Lọc theo lớp", width=220, value="all", options=class_filter_options)
    status_filter_dropdown = ft.Dropdown(label="Lọc theo trạng thái", width=180, value="all", options=[
        ft.dropdown.Option(key="all", text="Tất cả trạng thái"),
        ft.dropdown.Option(key="active", text="Active"),
        ft.dropdown.Option(key="disabled", text="Disabled"),
    ])
    shuffle_filter_dropdown = ft.Dropdown(label="Lọc theo xáo trộn", width=200, value="all", options=[
        ft.dropdown.Option(key="all", text="Tất cả (Xáo trộn)"),
        ft.dropdown.Option(key="questions", text="Chỉ xáo trộn câu hỏi"),
        ft.dropdown.Option(key="answers", text="Chỉ xáo trộn đáp án"),
        ft.dropdown.Option(key="both", text="Xáo trộn cả hai"),
        ft.dropdown.Option(key="none", text="Không xáo trộn"),
    ])

    # Tạo một cột để chứa danh sách các bài thi đã được lọc và hiển thị.
    quiz_list_view = ft.Column(spacing=Spacing.LG)

    # Hàm xóa bài thi
    def handle_delete_quiz(quiz_to_delete):
        def on_delete(e):
            mock_data.mock_quizzes = [q for q in mock_data.mock_quizzes if q['id'] != quiz_to_delete['id']]
            if quiz_to_delete['id'] in mock_data.mock_questions:
                del mock_data.mock_questions[quiz_to_delete['id']]
            show_quiz_management()
        return on_delete

    # Hàm cập nhật danh sách bài thi dựa trên các bộ lọc và tìm kiếm
    def update_quiz_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        selected_class_id = class_filter_dropdown.value
        selected_status = status_filter_dropdown.value
        selected_shuffle = shuffle_filter_dropdown.value
        
        user_quizzes = [q for q in mock_data.mock_quizzes if q['created_by'] == app_state.current_user['id']]
        filtered_quizzes = [q for q in user_quizzes if search_term in q['title'].lower()]

        if selected_class_id and selected_class_id != "all":
            filtered_quizzes = [q for q in filtered_quizzes if str(q.get('class_id')) == selected_class_id]
        if selected_status and selected_status != "all":
            is_active = (selected_status == "active")
            filtered_quizzes = [q for q in filtered_quizzes if q.get('is_active', False) == is_active]
        if selected_shuffle and selected_shuffle != "all":
            if selected_shuffle == "questions":
                filtered_quizzes = [q for q in filtered_quizzes if q.get('shuffle_questions') and not q.get('shuffle_answers')]
            elif selected_shuffle == "answers":
                filtered_quizzes = [q for q in filtered_quizzes if not q.get('shuffle_questions') and q.get('shuffle_answers')]
            elif selected_shuffle == "both":
                filtered_quizzes = [q for q in filtered_quizzes if q.get('shuffle_questions') and q.get('shuffle_answers')]
            elif selected_shuffle == "none":
                filtered_quizzes = [q for q in filtered_quizzes if not q.get('shuffle_questions') and not q.get('shuffle_answers')]

        # Cập nhật giao diện danh sách bài thi
        quiz_list_view.controls.clear()
        # Hiển thị các bài thi đã lọc hoặc thông báo không tìm thấy
        if filtered_quizzes:
            for quiz in filtered_quizzes:
                quiz_list_view.controls.append(create_quiz_card(quiz))
        else:
            quiz_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=Colors.GRAY_400),
                    ft.Container(height=Spacing.SM),
                    ft.Text("No quizzes found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                    ft.Text(f"Your search for '{search_field.value}' did not match any quizzes.", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        app_state.current_page.update()

    # Kết nối các sự kiện thay đổi để cập nhật danh sách bài thi khi người dùng tương tác.
    search_field.on_change = update_quiz_list
    class_filter_dropdown.on_change = update_quiz_list
    status_filter_dropdown.on_change = update_quiz_list
    shuffle_filter_dropdown.on_change = update_quiz_list

    # Biểu mẫu tạo bài thi mới
    quiz_title_field = create_text_input("Quiz Title", width=400)
    quiz_description_field = create_text_input("Description", width=400, multiline=True, min_lines=3)
    quiz_start_time_field = create_text_input("Start Time (YYYY-MM-DD HH:MM)", width=250, icon=ft.Icons.CALENDAR_MONTH)
    quiz_end_time_field = create_text_input("End Time (YYYY-MM-DD HH:MM)", width=250, icon=ft.Icons.CALENDAR_MONTH) # thêm trường end_time: hạn của quiz
    quiz_duration_field = create_text_input("Duration (minutes)", width=140, icon=ft.Icons.TIMER)
    quiz_password_field = create_text_input("Quiz Password (optional)", password=True, width=400, icon=ft.Icons.LOCK, can_reveal=True)
    shuffle_questions_switch = ft.Switch(label="Xáo trộn câu hỏi", value=False)
    shuffle_answers_switch = ft.Switch(label="Xáo trộn đáp án", value=True)
    show_answers_switch = ft.Switch(label="Allow student to view the answers after the exam", value=False)

    # Chọn lớp cho bài thi
    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_dropdown = ft.Dropdown(
        label="Select Class for this Quiz", width=400, border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300, focused_border_color=Colors.PRIMARY,
        options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in instructor_classes]
    )
    # Báo lỗi cho form tạo bài thi
    quiz_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

    # Hàm hiển thị form tạo bài thi mới
    def show_create_form(e):
        quiz_form_container.visible = True
        quiz_title_field.value = ""
        quiz_description_field.value = ""
        quiz_error_text.value = ""
        quiz_start_time_field.value = ""
        quiz_end_time_field.value = "" # xóa giá trị cũ của End time
        quiz_duration_field.value = ""
        quiz_password_field.value = ""
        class_dropdown.value = None
        shuffle_questions_switch.value = False
        shuffle_answers_switch.value = True
        show_answers_switch.value = False
        app_state.current_page.update()

    # Hàm ẩn form tạo bài thi mới
    def hide_create_form(e):
        quiz_form_container.visible = False
        app_state.current_page.update()

    # Hàm xử lý tạo bài thi mới
    def handle_create_quiz(e):
        title = quiz_title_field.value or ""
        description = quiz_description_field.value or ""
        start_time_str = quiz_start_time_field.value or ""
        end_time_str = quiz_end_time_field.value or "" # Lay gia tri cua End Time
        duration_str = quiz_duration_field.value or ""
        password = quiz_password_field.value or None
        class_id = class_dropdown.value
        shuffle_questions = shuffle_questions_switch.value
        shuffle_answers = shuffle_answers_switch.value
        show_answers_after_quiz = show_answers_switch.value

        if not title.strip() or not class_id:
            quiz_error_text.value = "Quiz title and class are required"
            app_state.current_page.update()
            return

        try:
            start_dt = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            quiz_error_text.value = "Invalid start time format. Use YYYY-MM-DD HH:MM"
            app_state.current_page.update()
            return

         # Kiểm tra và xác thực End Time nếu được cung cấp
        if end_time_str:
            try:
                end_dt = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
                if end_dt <= start_dt:
                    quiz_error_text.value = "End time must be after start time."
                    app_state.current_page.update()
                    return
            except ValueError:
                quiz_error_text.value = "Invalid end time format. Use YYYY-MM-DD HH:MM"
                app_state.current_page.update()
                return


        if not duration_str.isdigit() or int(duration_str) <= 0:
            quiz_error_text.value = "Duration must be a positive number of minutes"
            app_state.current_page.update()
            return
        
        duration_minutes = int(duration_str)

        new_id = max(q['id'] for q in mock_data.mock_quizzes) + 1 if mock_data.mock_quizzes else 1
        new_quiz = {
            'id': new_id, 'title': title.strip(), 'description': description.strip(),
            'created_by': app_state.current_user['id'], 'created_at': '2025-01-15',
            'creator': app_state.current_user['username'], 'questions_count': 0,
            'start_time': start_time_str.strip(), 'duration_minutes': duration_minutes,
            'end_time': end_time_str.strip() if end_time_str else None, # luu End Time
            'class_id': int(class_id), 'password': password.strip() if password else None,
            'is_active': True, 'shuffle_questions': shuffle_questions,
            'shuffle_answers': shuffle_answers, 'show_answers_after_quiz': show_answers_after_quiz
        }
        mock_data.mock_quizzes.append(new_quiz)
        
        quiz_error_text.value = ""
        hide_create_form(e)
        show_quiz_management()

    # Container cho form tạo bài thi mới
    quiz_form_container = create_card(
        content=ft.Column([
            create_section_title("Create New Quiz"), ft.Container(height=Spacing.LG),
            quiz_title_field, ft.Container(height=Spacing.LG),
            quiz_description_field, ft.Container(height=Spacing.LG),
            class_dropdown, ft.Container(height=Spacing.LG),
            ft.Row([quiz_start_time_field, quiz_end_time_field, quiz_duration_field], spacing=Spacing.MD), # them truong end_time
            ft.Container(height=Spacing.LG), quiz_password_field, ft.Container(height=Spacing.LG),
            ft.Row([shuffle_questions_switch, shuffle_answers_switch], spacing=Spacing.XL),
            ft.Container(height=Spacing.LG), show_answers_switch, ft.Container(height=Spacing.MD),
            quiz_error_text, ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Create Quiz", on_click=handle_create_quiz, width=120),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Cancel", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    # Mặc định ẩn form tạo bài thi
    quiz_form_container.visible = False
    
    # Hàm tạo giao diện Card cho một bài thi cụ thể
    def create_quiz_card(quiz):
        class_name = next((c['name'] for c in mock_data.mock_classes if c['id'] == quiz.get('class_id')), "Unassigned")
        shuffle_info = []
        if quiz.get('shuffle_questions'): shuffle_info.append("Câu hỏi")
        if quiz.get('shuffle_answers'): shuffle_info.append("Đáp án")

        def toggle_active_state(e):
            for q in mock_data.mock_quizzes:
                if q['id'] == quiz['id']:
                    q['is_active'] = e.control.value
                    break
            show_quiz_management()

        return create_card(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(quiz['title'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                        ft.Text(quiz['description'] or "No description", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY)
                    ], expand=True, spacing=Spacing.XS),
                    ft.Column([
                        create_badge(f"Xáo trộn: {', '.join(shuffle_info) if shuffle_info else 'Không'}", color=Colors.PRIMARY_LIGHT),
                        ft.Row([
                            create_badge("Active" if quiz.get('is_active', False) else "Disabled", color=Colors.SUCCESS if quiz.get('is_active', False) else Colors.GRAY_400),
                            create_badge(class_name, color=Colors.WARNING),
                        ], spacing=Spacing.SM),
                        ft.Container(height=Spacing.XS),
                        ft.Switch(value=quiz.get('is_active', False), on_change=toggle_active_state, label="Active", label_position=ft.LabelPosition.LEFT),
                    ], alignment=ft.CrossAxisAlignment.END, spacing=Spacing.XS),
                ]),
                ft.Container(height=Spacing.SM),
                ft.Row([
                    ft.Text(f"{quiz['questions_count']} questions", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(f"Created: {quiz['created_at']}", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(f"| Starts: {quiz.get('start_time', 'N/A')}", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(f"| Ends: {quiz.get('end_time', 'N/A')}", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED), # Hiển thị End Time
                    ft.Text(f"| Duration: {quiz.get('duration_minutes', 'N/A')} min", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Container(expand=True),
                    create_secondary_button("Preview", on_click=lambda e, q=quiz: show_quiz_preview(q), width=80),
                    ft.Container(width=Spacing.SM),
                    create_secondary_button("Delete", on_click=handle_delete_quiz(quiz), width=80),
                    ft.Container(width=Spacing.SM),
                    create_primary_button("Manage Questions", on_click=lambda e, q=quiz: show_question_management(q), width=150)
                ])
            ]),
            padding=Spacing.LG
        )

    # Khởi tạo danh sách bài thi ban đầu
    update_quiz_list()
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Row([
                        ft.Column([
                            create_page_title("Quiz Management"),
                            create_subtitle("Create and manage your quizzes")
                        ], expand=True, spacing=Spacing.XS),
                        search_field, status_filter_dropdown, shuffle_filter_dropdown, class_filter_dropdown,
                        create_primary_button("Create New Quiz", on_click=show_create_form, width=150)
                    ]),
                    ft.Container(height=Spacing.XXL), quiz_form_container, ft.Container(height=Spacing.XL),
                    create_section_title("Your Quizzes"), ft.Container(height=Spacing.LG),
                    quiz_list_view if quiz_list_view.controls else create_card(
                        content=ft.Column([
                            ft.Image(src="assets/logo.png", width=48, height=48),
                            ft.Text("No quizzes created yet", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                            ft.Text("Create your first quiz to get started!", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=Spacing.XXXXL
                    )
                ]),
                padding=Spacing.XL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    # Thiết lập cấu hình trang
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_quiz_management

    # Hiển thị
    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

# --- Thêm hàm sau vào cuối file instructor_admin_views.py ---

def show_question_management(quiz):
    """Hiển thị trang quản lý câu hỏi chi tiết với nhiều loại câu hỏi"""
    app_state.current_page.clean()
    
    sidebar = create_sidebar(app_state.current_user['role'], "questions") # "questions" không phải trang chính, nhưng để active item
    
    def handle_delete_question(quiz, question_to_delete):
        def on_delete(e):
            if quiz['id'] in mock_data.mock_questions:
                # Xóa câu hỏi
                mock_data.mock_questions[quiz['id']] = [q for q in mock_data.mock_questions[quiz['id']] if q['id'] != question_to_delete['id']]
                
                # Cập nhật số lượng câu hỏi trong quiz
                for q_quiz in mock_data.mock_quizzes:
                    if q_quiz['id'] == quiz['id']:
                        q_quiz['questions_count'] = len(mock_data.mock_questions[quiz['id']])
                        break
            show_question_management(quiz) # Tải lại trang
        return on_delete

    # Các trường trong form tạo câu hỏi
    question_text_field = create_text_input("Question Text", width=500, multiline=True, min_lines=2)
    question_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    # Bộ chọn loại câu hỏi
    question_type_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="multiple_choice", label="Multiple Choice (A, B, C, D)"),
            ft.Radio(value="true_false", label="True/False"),
            ft.Radio(value="fill_in_blank", label="Fill in the Blank"),
            ft.Radio(value="multiple_select", label="Multiple Select (Check all that apply)"),
            ft.Radio(value="short_answer", label="Short Answer"),
        ], spacing=Spacing.SM)
    )
    question_type_group.value = "multiple_choice"
    
    # Bộ chọn độ khó
    difficulty_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Easy", label="Easy"),
            ft.Radio(value="Medium", label="Medium"),
            ft.Radio(value="Hard", label="Hard"),
        ], spacing=Spacing.LG)
    )
    difficulty_group.value = "Easy"

    # Container cho form động
    dynamic_form_container = ft.Container()
    
    def update_dynamic_form(question_type):
        """Cập nhật form dựa trên loại câu hỏi được chọn"""
        if question_type == "multiple_choice":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Answer Options:"), ft.Container(height=Spacing.SM),
                create_text_input("Option A", width=400), ft.Container(height=Spacing.SM),
                create_text_input("Option B", width=400), ft.Container(height=Spacing.SM),
                create_text_input("Option C", width=400), ft.Container(height=Spacing.SM),
                create_text_input("Option D", width=400), ft.Container(height=Spacing.LG),
                create_subtitle("Correct Answer:"), ft.Container(height=Spacing.SM),
                ft.RadioGroup(
                    content=ft.Column([
                        ft.Radio(value="A", label="Option A is correct"),
                        ft.Radio(value="B", label="Option B is correct"),
                        ft.Radio(value="C", label="Option C is correct"),
                        ft.Radio(value="D", label="Option D is correct"),
                    ])
                )
            ])
        elif question_type == "true_false":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Correct Answer:"), ft.Container(height=Spacing.SM),
                ft.RadioGroup(
                    content=ft.Column([
                        ft.Radio(value="true", label="True"),
                        ft.Radio(value="false", label="False"),
                    ])
                )
            ])
        elif question_type == "fill_in_blank":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Correct Answer:"), ft.Container(height=Spacing.SM),
                create_text_input("Correct answer", width=400), ft.Container(height=Spacing.SM),
                ft.Text("Tip: Use _______ in your question text to indicate where the blank should be.", 
                       size=Typography.SIZE_XS, color=Colors.TEXT_MUTED)
            ])
        elif question_type == "multiple_select":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Answer Options (Check all correct answers):"), ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option A", width=300), ft.Checkbox(label="Correct")]), ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option B", width=300), ft.Checkbox(label="Correct")]), ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option C", width=300), ft.Checkbox(label="Correct")]), ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option D", width=300), ft.Checkbox(label="Correct")]),
            ])
        elif question_type == "short_answer":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Sample Answer (for reference):"), ft.Container(height=Spacing.SM),
                create_text_input("Sample answer", width=500, multiline=True, min_lines=3), ft.Container(height=Spacing.SM),
                ft.Text("Note: Short answer questions require manual grading.", 
                       size=Typography.SIZE_XS, color=Colors.TEXT_MUTED)
            ])
        
        app_state.current_page.update()
    
    def on_question_type_change(e):
        update_dynamic_form(question_type_group.value)
    
    question_type_group.on_change = on_question_type_change
    
    def show_question_form(e):
        question_form_container.visible = True
        question_text_field.value = ""
        difficulty_group.value = "Easy"
        question_type_group.value = "multiple_choice"
        update_dynamic_form("multiple_choice")
        question_error_text.value = ""
        app_state.current_page.update()
    
    def hide_question_form(e):
        question_form_container.visible = False
        app_state.current_page.update()
    
    def handle_create_question(e):
        question_text = question_text_field.value or ""
        question_type = question_type_group.value
        difficulty = difficulty_group.value
        
        if not question_text.strip():
            question_error_text.value = "Question text is required"
            app_state.current_page.update()
            return
        
        new_question = {
            'id': (max(q['id'] for q in mock_data.mock_questions[quiz['id']]) + 1) if quiz['id'] in mock_data.mock_questions and mock_data.mock_questions[quiz['id']] else 1,
            'question_type': question_type,
            'question_text': question_text.strip(),
            'difficulty': difficulty,
        }
        
        if question_type == "multiple_choice":
            form_controls = dynamic_form_container.content.controls
            option_texts = [form_controls[2].value or "", form_controls[4].value or "", form_controls[6].value or "", form_controls[8].value or ""]
            
            if not all(opt.strip() for opt in option_texts):
                question_error_text.value = "All options are required for multiple choice questions"
                app_state.current_page.update()
                return
            
            correct_group = form_controls[-1]
            if not correct_group.value:
                question_error_text.value = "Please select the correct answer"
                app_state.current_page.update()
                return
            
            new_question['options'] = [
                {'option_text': option_texts[0], 'is_correct': correct_group.value == 'A'},
                {'option_text': option_texts[1], 'is_correct': correct_group.value == 'B'},
                {'option_text': option_texts[2], 'is_correct': correct_group.value == 'C'},
                {'option_text': option_texts[3], 'is_correct': correct_group.value == 'D'}
            ]
        # ... (các khối elif khác tương tự)
        elif question_type == "true_false":
            correct_group = dynamic_form_container.content.controls[2]
            if not hasattr(correct_group, 'value') or not correct_group.value:
                question_error_text.value = "Please select True or False"
                app_state.current_page.update()
                return
            new_question['correct_answer'] = correct_group.value == "true"
        elif question_type == "fill_in_blank":
            answer_field = dynamic_form_container.content.controls[2]
            if not hasattr(answer_field, 'value') or not answer_field.value:
                question_error_text.value = "Please provide the correct answer"
                app_state.current_page.update()
                return
            new_question['correct_answer'] = answer_field.value
            new_question['answer_variations'] = [answer_field.value.lower()]
        elif question_type == "short_answer":
            sample_field = dynamic_form_container.content.controls[2]
            new_question['sample_answer'] = getattr(sample_field, 'value', '') or ''
        elif question_type == "multiple_select":
            options_container = dynamic_form_container.content.controls[2:]
            options = []
            has_empty_option = False
            for i in range(4):
                row = options_container[i*2]
                option_field = row.controls[0]
                checkbox = row.controls[1]
                
                option_text = option_field.value or ""
                if not option_text.strip():
                    has_empty_option = True
                    break
                
                options.append({'option_text': option_text, 'is_correct': checkbox.value})
            if has_empty_option:
                question_error_text.value = "All option texts are required for multiple select questions"
                app_state.current_page.update()
                return
            new_question['options'] = options

        if quiz['id'] not in mock_data.mock_questions:
            mock_data.mock_questions[quiz['id']] = []
        mock_data.mock_questions[quiz['id']].append(new_question)
        
        for q in mock_data.mock_quizzes:
            if q['id'] == quiz['id']:
                q['questions_count'] = len(mock_data.mock_questions[quiz['id']])
                break
        
        question_error_text.value = ""
        hide_question_form(e)
        show_question_management(quiz)
    
    def back_to_quizzes(e):
        show_quiz_management()
    
    update_dynamic_form("multiple_choice")
    
    question_form_container = create_card(
        content=ft.Column([
            create_section_title("Add New Question"), ft.Container(height=Spacing.LG),
            create_subtitle("Question Type:"), ft.Container(height=Spacing.MD), question_type_group, ft.Container(height=Spacing.XL),
            create_subtitle("Question Text:"), ft.Container(height=Spacing.MD), question_text_field, ft.Container(height=Spacing.XL),
            create_subtitle("Difficulty:"), ft.Container(height=Spacing.MD), difficulty_group, ft.Container(height=Spacing.XL),
            dynamic_form_container, ft.Container(height=Spacing.MD),
            question_error_text, ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Add Question", on_click=handle_create_question, width=130),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Cancel", on_click=hide_question_form, width=100)
            ])
        ]),
        padding=Spacing.LG
    )
    question_form_container.visible = False
    
    quiz_questions = mock_data.mock_questions.get(quiz['id'], [])
    question_cards = []
    
    for i, question in enumerate(quiz_questions, 1):
        question_type = question.get('question_type', 'multiple_choice')
        difficulty = question.get('difficulty', 'Medium')
        difficulty_color_map = {'Easy': Colors.SUCCESS, 'Medium': Colors.WARNING, 'Hard': Colors.ERROR}
        
        preview_content = ft.Text("Preview not available", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
        if question_type == "multiple_choice":
            correct_option = next((opt['option_text'] for opt in question.get('options', []) if opt['is_correct']), "")
            preview_content = ft.Column([
                ft.Column([ft.Text(f"A) {opt['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY) for opt in question.get('options', [])], spacing=Spacing.XS),
                ft.Container(height=Spacing.SM),
                ft.Row([ft.Text("Correct Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED), ft.Text(correct_option, size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)])
            ])
        elif question_type == "true_false":
            preview_content = ft.Row([ft.Text("Correct Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED), ft.Text(str(question.get('correct_answer', '')), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)])
        elif question_type == "fill_in_blank":
            preview_content = ft.Row([ft.Text("Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED), ft.Text(question.get('correct_answer', ''), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)])
        elif question_type == "short_answer":
            preview_content = ft.Text("Sample: " + (question.get('sample_answer', 'No sample provided')[:50] + "..."), size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
        elif question_type == "multiple_select":
            correct_options = [opt['option_text'] for opt in question.get('options', []) if opt['is_correct']]
            preview_content = ft.Column([
                ft.Column([ft.Text(f"- {opt['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY) for opt in question.get('options', [])], spacing=Spacing.XS),
                ft.Container(height=Spacing.SM),
                ft.Row([ft.Text("Correct Answers:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED), ft.Text(", ".join(correct_options), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)])
            ])

        question_card = create_card(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Question {i}", size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.PRIMARY),
                    create_badge(question_type.replace('_', ' ').title(), color=Colors.PRIMARY_LIGHT),
                    create_badge(difficulty, color=difficulty_color_map.get(difficulty, Colors.GRAY_400)),
                    ft.Container(expand=True),
                    create_secondary_button("Delete", on_click=handle_delete_question(quiz, question), width=80)
                ]),
                ft.Container(height=Spacing.SM),
                ft.Text(question['question_text'], size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY),
                ft.Container(height=Spacing.SM),
                preview_content
            ]),
            padding=Spacing.LG
        )
        question_cards.append(question_card)
    
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Row([create_secondary_button("← Back to Quizzes", on_click=back_to_quizzes, width=150), ft.Container(expand=True)]),
                        ft.Container(height=Spacing.LG),
                        create_card(
                            content=ft.Column([
                                ft.Row([
                                    ft.Column([
                                        ft.Text(quiz['title'], size=Typography.SIZE_2XL, weight=ft.FontWeight.W_700),
                                        ft.Text(quiz['description'] or "No description", size=Typography.SIZE_BASE, color=Colors.TEXT_SECONDARY)
                                    ], expand=True),
                                    create_badge(f"{len(quiz_questions)} Questions")
                                ])
                            ]),
                            padding=Spacing.LG
                        ),
                        ft.Container(height=Spacing.LG),
                        ft.Row([
                            create_section_title("Questions"), ft.Container(expand=True),
                            create_secondary_button("Preview Quiz", on_click=lambda e: show_quiz_preview(quiz), width=120),
                            create_primary_button("Add Question", on_click=show_question_form, width=120),
                        ]),
                        ft.Container(height=Spacing.LG),
                        question_form_container, ft.Container(height=Spacing.LG),
                        ft.Column(question_cards, spacing=Spacing.LG) if question_cards else create_card(
                            content=ft.Column([
                                ft.Icon(ft.Icons.HELP_OUTLINE, size=48, color=Colors.GRAY_400),
                                ft.Text("No questions added yet", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                                ft.Text("Add your first question to get started!", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=Spacing.XXXXL
                        )
                    ]),
                padding=Spacing.XL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )
    
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = lambda e=None: show_question_management(quiz)

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

# --- Thêm hàm sau vào cuối file instructor_admin_views.py ---

def show_quiz_preview(quiz_basic_info):
    """Hiển thị bài thi ở chế độ xem trước cho giảng viên."""
    app_state.current_page.clean()
    app_state.current_question_index = 0

    app_state.quiz_questions = mock_data.mock_questions.get(quiz_basic_info['id'], [])

    if quiz_basic_info.get('shuffle_questions', False):
        random.shuffle(app_state.quiz_questions)

    if not app_state.quiz_questions:
        show_quiz_management() # Quay lại nếu không có câu hỏi
        return

    # UI Components
    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_component_container = ft.Container(content=ft.Column([]))

    def update_preview_display():
        if app_state.current_question_index >= len(app_state.quiz_questions):
            return

        question = app_state.quiz_questions[app_state.current_question_index]
        question_counter_text.value = f"Question {app_state.current_question_index + 1} of {len(app_state.quiz_questions)}"

        def dummy_answer_handler(q_id, answer):
            pass

        shuffle_answers = quiz_basic_info.get('shuffle_answers', False)
        question_component = create_question_by_type(question, dummy_answer_handler, shuffle_answers)
        question_component_container.content = question_component

        prev_button.disabled = (app_state.current_question_index == 0)
        next_button.disabled = (app_state.current_question_index == len(app_state.quiz_questions) - 1)
        app_state.current_page.update()

    def handle_previous(e):
        if app_state.current_question_index > 0:
            app_state.current_question_index -= 1
            update_preview_display()

    def handle_next(e):
        if app_state.current_question_index < len(app_state.quiz_questions) - 1:
            app_state.current_question_index += 1
            update_preview_display()

    def exit_preview(e):
        show_question_management(quiz_basic_info)

    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120)

    # Giao diện xem trước
    preview_content = ft.Container(
        content=ft.Column([
            create_card(content=ft.Row([
                ft.Icon(ft.Icons.VISIBILITY, color=Colors.PRIMARY),
                ft.Text("Quiz Preview Mode", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                create_secondary_button("Exit Preview", on_click=exit_preview, width=120)
            ]), padding=Spacing.LG),
            ft.Container(height=Spacing.LG),
            create_card(content=question_component_container, padding=Spacing.XXXXL),
            ft.Container(height=Spacing.XL),
            ft.Row([prev_button, ft.Container(expand=True), next_button])
        ]), padding=Spacing.XXXXL, expand=True, alignment=ft.alignment.top_center)

    update_preview_display()
    app_state.current_page.add(preview_content)
    app_state.current_view_handler = None # Tắt responsive cho trang này
    app_state.current_page.update()

# --- Thêm các hàm sau vào cuối file instructor_admin_views.py ---

def show_results_overview():
    """Hiển thị trang tổng quan kết quả (điều hướng dựa trên vai trò)"""
    if app_state.current_user['role'] == 'instructor':
        show_instructor_results_page()
    elif app_state.current_user['role'] == 'admin':
        # Có thể thêm trang kết quả riêng cho admin sau này
        pass

def show_instructor_results_page():
    """Hiển thị trang kết quả chi tiết cho giảng viên, có thể lọc theo lớp và bài thi."""
    app_state.current_page.clean()

    sidebar = create_sidebar(app_state.current_user['role'], "results")
    results_container = ft.Column()

    def update_results_display(selected_class_id=None, selected_quiz_id=None):
        results_container.controls.clear()

        if not selected_class_id or not selected_quiz_id:
            results_container.controls.append(
                create_card(ft.Column([
                    ft.Icon(ft.Icons.FILTER_LIST, size=48, color=Colors.GRAY_400),
                    ft.Text("Select a Class and Quiz", size=Typography.SIZE_LG, color=Colors.TEXT_MUTED),
                    ft.Text("Choose from the dropdowns above to view results.", color=Colors.TEXT_MUTED),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=Spacing.XXXXL)
            )
            app_state.current_page.update()
            return

        students_in_class = [u for u in mock_data.mock_users.values() if u.get('class_id') == int(selected_class_id)]
        attempts_for_quiz = [a for a in mock_data.mock_attempts if a['quiz_id'] == int(selected_quiz_id)]

        student_results = []
        for student in students_in_class:
            student_attempts = [a for a in attempts_for_quiz if a['user_id'] == student['id']]
            if student_attempts:
                latest_attempt = max(student_attempts, key=lambda x: x['completed_at'])
                student_results.append({'student': student, 'attempt': latest_attempt})

        total_students = len(students_in_class)
        completed_count = len(student_results)
        completion_rate = (completed_count / total_students * 100) if total_students > 0 else 0
        
        scores_10 = [res['attempt']['percentage'] / 10.0 for res in student_results]
        avg_score_10 = sum(scores_10) / len(scores_10) if scores_10 else 0
        highest_score_10 = max(scores_10) if scores_10 else 0

        bar_groups = [
            ft.BarChartGroup(x=i, bar_rods=[
                ft.BarChartRod(from_y=0, to_y=res['attempt']['percentage'] / 10.0, width=15, color=Colors.PRIMARY, tooltip=f"{res['student']['username']}: {res['attempt']['percentage'] / 10.0:.1f}", border_radius=BorderRadius.SM)
            ]) for i, res in enumerate(student_results)
        ]
        
        chart = ft.BarChart(
            bar_groups=bar_groups,
            left_axis=ft.ChartAxis(labels=[ft.ChartAxisLabel(value=v, label=ft.Text(str(v))) for v in range(0, 11, 2)], labels_size=40),
            bottom_axis=ft.ChartAxis(labels=[ft.ChartAxisLabel(value=i, label=ft.Text(res['student']['username'], size=10, rotate=45)) for i, res in enumerate(student_results)], labels_size=50),
            horizontal_grid_lines=ft.ChartGridLines(interval=2, color=Colors.GRAY_200, width=1),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, Colors.GRAY_800), max_y=10, interactive=True, expand=True
        )

        table_rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(res['student']['username'])),
                ft.DataCell(ft.Text(res['attempt']['score'])),
                ft.DataCell(ft.Text(f"{res['attempt']['percentage']:.1f}%")),
                ft.DataCell(ft.Text(res['attempt']['time_taken'])),
                ft.DataCell(ft.Text(datetime.datetime.strptime(res['attempt']['completed_at'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M'))),
            ]) for res in student_results
        ]

        results_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Student")), ft.DataColumn(ft.Text("Score")), ft.DataColumn(ft.Text("Percentage")),
                ft.DataColumn(ft.Text("Time Taken")), ft.DataColumn(ft.Text("Completed At")),
            ],
            rows=table_rows, heading_row_color=Colors.GRAY_100, border=ft.border.all(1, Colors.GRAY_200), border_radius=BorderRadius.MD
        )

        results_container.controls.extend([
            ft.Row([
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.STAR_HALF, color=Colors.PRIMARY), ft.Text("Điểm trung bình")]), ft.Text(f"{avg_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color=Colors.WARNING), ft.Text("Điểm cao nhất")]), ft.Text(f"{highest_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.PIE_CHART, color=Colors.SUCCESS), ft.Text("Tỷ lệ hoàn thành")]), ft.Text(f"{completion_rate:.1f}%", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Container(height=Spacing.XXL),
            create_card(ft.Column([create_section_title("Biểu đồ điểm sinh viên (Thang 10)"), ft.Container(chart, height=300, padding=Spacing.LG)]), padding=Spacing.XL),
            ft.Container(height=Spacing.XXL),
            create_card(ft.Column([create_section_title("Kết quả chi tiết"), results_table]), padding=Spacing.XL),
        ])
        app_state.current_page.update()

    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_dd = ft.Dropdown(label="Chọn Lớp học", width=250, options=[ft.dropdown.Option(key=c['id'], text=c['name']) for c in instructor_classes])
    quiz_dd = ft.Dropdown(label="Chọn Bài thi", width=300, disabled=True)

    def on_class_change(e):
        selected_class_id = int(e.control.value)
        quizzes_in_class = [q for q in mock_data.mock_quizzes if q.get('class_id') == selected_class_id]
        quiz_dd.options = [ft.dropdown.Option(key=q['id'], text=q['title']) for q in quizzes_in_class]
        quiz_dd.value = None
        quiz_dd.disabled = False
        update_results_display()
        app_state.current_page.update()

    def on_quiz_change(e):
        update_results_display(class_dd.value, quiz_dd.value)

    class_dd.on_change = on_class_change
    quiz_dd.on_change = on_quiz_change

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Row([
                        ft.Column([
                            create_page_title("Quiz Results"),
                            create_subtitle("Review attempts and results for your quizzes.")
                        ], expand=True),
                        class_dd,
                        quiz_dd,
                    ]),
                    ft.Container(height=Spacing.XXL),
                    results_container,
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    update_results_display()

    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_instructor_results_page

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

# --- Thêm các hàm cuối cùng vào file instructor_admin_views.py ---

def show_settings_page():
    """Hiển thị trang cài đặt cho giảng viên và admin."""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "settings")

    current_password_field = create_text_input("Mật khẩu hiện tại", password=True, can_reveal=True)
    new_password_field = create_text_input("Mật khẩu mới", password=True, can_reveal=True)
    confirm_password_field = create_text_input("Xác nhận mật khẩu mới", password=True, can_reveal=True)
    password_message_text = ft.Text("", size=Typography.SIZE_SM)

    def handle_save_password(e):
        current_pass = current_password_field.value
        new_pass = new_password_field.value
        confirm_pass = confirm_password_field.value

        if not all([current_pass, new_pass, confirm_pass]):
            password_message_text.value = "Vui lòng điền đầy đủ các trường."
            password_message_text.color = Colors.ERROR
        elif current_pass != app_state.current_user['password']:
            password_message_text.value = "Mật khẩu hiện tại không đúng."
            password_message_text.color = Colors.ERROR
            current_password_field.value = ""
        elif new_pass != confirm_pass:
            password_message_text.value = "Mật khẩu mới không khớp."
            password_message_text.color = Colors.ERROR
            new_password_field.value = ""
            confirm_password_field.value = ""
        else:
            mock_data.mock_users[app_state.current_user['username']]['password'] = new_pass
            app_state.current_user['password'] = new_pass
            password_message_text.value = "Đổi mật khẩu thành công!"
            password_message_text.color = Colors.SUCCESS
            current_password_field.value = ""
            new_password_field.value = ""
            confirm_password_field.value = ""
        app_state.current_page.update()

    info_details = [
        ft.Row([ft.Text("Username:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['username'])]),
        ft.Divider(),
        ft.Row([ft.Text("Vai trò:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['role'].title())]),
    ]

    if app_state.current_user['role'] == 'instructor':
        assigned_classes = [c['name'] for c in mock_data.mock_classes if c.get('instructor_id') == app_state.current_user['id']]
        if assigned_classes:
            info_details.extend([ft.Divider(), ft.Row([ft.Text("Các lớp phụ trách:", weight=ft.FontWeight.W_600), ft.Text(", ".join(assigned_classes))])])

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title("Account Settings"),
                            create_subtitle("Manage your personal information and account settings.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    ft.Row([
                        create_card(content=ft.Column([create_section_title("Thông tin tài khoản"), ft.Container(height=Spacing.LG), *info_details]), padding=Spacing.XL),
                        create_card(content=ft.Column([
                            create_section_title("Đổi mật khẩu"), ft.Container(height=Spacing.LG),
                            current_password_field, new_password_field, confirm_password_field,
                            ft.Container(height=Spacing.SM), password_message_text, ft.Container(height=Spacing.LG),
                            create_primary_button("Lưu thay đổi", on_click=handle_save_password)
                        ]), padding=Spacing.XL),
                    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_settings_page

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

def show_class_management():
    """Hiển thị trang quản lý lớp học cho admin."""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "classes")
    search_field = create_text_input("Search by class name...", width=300, icon=ft.Icons.SEARCH)
    class_list_view = ft.Column(spacing=Spacing.LG)

    def update_class_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        filtered_classes = [c for c in mock_data.mock_classes if search_term in c['name'].lower()]
        class_list_view.controls.clear()
        if filtered_classes:
            for cls in filtered_classes:
                class_list_view.controls.append(create_class_card(cls))
        else:
            class_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=Colors.GRAY_400),
                    ft.Text("No classes found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        app_state.current_page.update()

    search_field.on_change = update_class_list

    def handle_delete_class(class_id_to_delete):
        def on_delete(e):
            mock_data.mock_classes = [c for c in mock_data.mock_classes if c['id'] != class_id_to_delete]
            show_class_management()
        return on_delete

    class_name_field = create_text_input("Tên lớp học", width=400)
    instructors = [user for user in mock_data.mock_users.values() if user['role'] == 'instructor']
    instructor_dropdown = ft.Dropdown(
        label="Chọn giảng viên", width=400,
        options=[ft.dropdown.Option(key=ins['id'], text=ins['username']) for ins in instructors]
    )
    class_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    class_form_container = ft.Container() # Placeholder

    def show_create_form(e):
        class_form_container.visible = True
        class_name_field.value = ""
        instructor_dropdown.value = None
        class_error_text.value = ""
        app_state.current_page.update()

    def hide_create_form(e):
        class_form_container.visible = False
        app_state.current_page.update()

    def handle_create_class(e):
        class_name = class_name_field.value or ""
        instructor_id = instructor_dropdown.value
        if not class_name.strip() or not instructor_id:
            class_error_text.value = "Tên lớp và giảng viên là bắt buộc."
            app_state.current_page.update()
            return

        new_id = max(c['id'] for c in mock_data.mock_classes) + 1 if mock_data.mock_classes else 1
        new_class = {'id': new_id, 'name': class_name.strip(), 'instructor_id': int(instructor_id)}
        mock_data.mock_classes.append(new_class)
        class_error_text.value = ""
        hide_create_form(e)
        show_class_management()

    class_form_container_content = create_card(
        content=ft.Column([
            create_section_title("Tạo Lớp học mới"), ft.Container(height=Spacing.LG),
            class_name_field, ft.Container(height=Spacing.LG), instructor_dropdown, ft.Container(height=Spacing.MD),
            class_error_text, ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Tạo Lớp", on_click=handle_create_class, width=120),
                create_secondary_button("Hủy", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    class_form_container.content = class_form_container_content
    class_form_container.visible = False

    def create_class_card(cls):
        instructor_name = next((user['username'] for user in mock_data.mock_users.values() if user['id'] == cls['instructor_id']), "N/A")
        return create_card(
            content=ft.Row([
                ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=Colors.PRIMARY, size=32), ft.Container(width=Spacing.LG),
                ft.Column([
                    ft.Text(cls['name'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                    ft.Text(f"Giảng viên: {instructor_name}", color=Colors.TEXT_SECONDARY),
                ], expand=True),
                create_secondary_button("Xóa", width=80, on_click=handle_delete_class(cls['id'])),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=Spacing.LG
        )

    update_class_list()
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Row([
                        ft.Column([
                            create_page_title("Quản lý Lớp học"),
                            create_subtitle("Tạo và quản lý các lớp học trong hệ thống.")
                        ], expand=True, spacing=Spacing.XS),
                        search_field,
                        create_primary_button("Tạo Lớp mới", on_click=show_create_form, width=150)
                    ]),
                    ft.Container(height=Spacing.XXL), class_form_container, ft.Container(height=Spacing.XL),
                    create_section_title("Danh sách Lớp học"), ft.Container(height=Spacing.LG),
                    class_list_view if class_list_view.controls else ft.Text("Chưa có lớp học nào.")
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )
    
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_class_management

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()


def show_user_management():
    """Hiển thị trang quản lý người dùng cho admin."""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "users")
    search_field = create_text_input("Search by username...", width=300, icon=ft.Icons.SEARCH)
    role_filter_dropdown = ft.Dropdown(
        label="Filter by Role", width=200, value="all",
        options=[
            ft.dropdown.Option(key="all", text="All Roles"),
            ft.dropdown.Option(key='instructor', text='Instructor'),
            ft.dropdown.Option(key='admin', text='Admin'),
            ft.dropdown.Option(key='examinee', text='Examinee'),
        ]
    )
    user_list_view = ft.Column(spacing=Spacing.LG)

    def update_user_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        selected_role = role_filter_dropdown.value
        filtered_users = mock_data.mock_users.items()
        if search_term:
            filtered_users = [(u, d) for u, d in filtered_users if search_term in d['username'].lower()]
        if selected_role != "all":
            filtered_users = [(u, d) for u, d in filtered_users if d['role'] == selected_role]

        user_list_view.controls.clear()
        if filtered_users:
            for username, user_data in filtered_users:
                user_list_view.controls.append(create_user_card(username, user_data))
        else:
            user_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON_SEARCH, size=48, color=Colors.GRAY_400),
                    ft.Text("No users found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        app_state.current_page.update()

    search_field.on_change = update_user_list
    role_filter_dropdown.on_change = update_user_list

    def open_edit_dialog(user_to_edit):
        """Mở dialog để chỉnh sửa thông tin người dùng."""
        username = user_to_edit['username']
        edit_password_field = create_text_input("New Password (leave blank to keep unchanged)", password=True, width=400)
        edit_role_dropdown = ft.Dropdown(
            label="Select Role", width=400, value=user_to_edit['role'],
            options=[
                ft.dropdown.Option(key='instructor', text='Instructor'),
                ft.dropdown.Option(key='admin', text='Admin'),
                ft.dropdown.Option(key='examinee', text='Examinee (Student)'),
            ]
        )
        edit_class_assignment_dropdown = ft.Dropdown(
            label="Gán vào lớp học (tùy chọn)", width=400, value=user_to_edit.get('class_id'),
            options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in mock_data.mock_classes],
            visible=(user_to_edit['role'] == 'examinee')
        )

        def on_edit_role_change(e):
            edit_class_assignment_dropdown.visible = (e.control.value == 'examinee')
            edit_dialog.content.update()
        edit_role_dropdown.on_change = on_edit_role_change

        def save_changes(e):
            new_password = edit_password_field.value.strip()
            if new_password:
                mock_data.mock_users[username]['password'] = new_password
            mock_data.mock_users[username]['role'] = edit_role_dropdown.value
            mock_data.mock_users[username]['class_id'] = int(edit_class_assignment_dropdown.value) if edit_role_dropdown.value == 'examinee' and edit_class_assignment_dropdown.value else None
            edit_dialog.open = False
            app_state.current_page.update()
            show_user_management()

        def close_dialog(e):
            edit_dialog.open = False
            app_state.current_page.update()

        edit_dialog = ft.AlertDialog(
            modal=True, title=ft.Text(f"Edit User: {username}"),
            content=ft.Column([edit_password_field, edit_role_dropdown, edit_class_assignment_dropdown], tight=True),
            actions=[create_secondary_button("Cancel", on_click=close_dialog), create_primary_button("Save Changes", on_click=save_changes)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        app_state.current_page.dialog = edit_dialog
        edit_dialog.open = True
        app_state.current_page.update()

    username_field = create_text_input("Username", width=400)
    password_field = create_text_input("Password", password=True, width=400)
    role_dropdown = ft.Dropdown(
        label="Select Role", width=400,
        options=[
            ft.dropdown.Option(key='instructor', text='Instructor'),
            ft.dropdown.Option(key='admin', text='Admin'),
            ft.dropdown.Option(key='examinee', text='Examinee (Student)'),
        ]
    )
    class_assignment_dropdown = ft.Dropdown(
        label="Gán vào lớp học (tùy chọn)", width=400,
        options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in mock_data.mock_classes],
        visible=False
    )
    user_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    user_form_container = ft.Container()

    def show_create_form(e):
        user_form_container.visible = True
        username_field.value = ""
        password_field.value = ""
        role_dropdown.value = None
        class_assignment_dropdown.value = None
        class_assignment_dropdown.visible = False
        user_error_text.value = ""
        app_state.current_page.update()

    def hide_create_form(e):
        user_form_container.visible = False
        app_state.current_page.update()
    
    def on_role_change(e):
        class_assignment_dropdown.visible = role_dropdown.value == 'examinee'
        app_state.current_page.update()
    role_dropdown.on_change = on_role_change

    def handle_create_user(e):
        username = username_field.value or ""
        password = password_field.value or ""
        role = role_dropdown.value
        if not username.strip() or not password.strip() or not role:
            user_error_text.value = "Username, password, and role are required."
        elif username.strip() in mock_data.mock_users:
            user_error_text.value = f"Username '{username.strip()}' already exists."
        else:
            new_id = max(user['id'] for user in mock_data.mock_users.values()) + 1 if mock_data.mock_users else 1
            new_user = {
                'id': new_id, 'username': username.strip(), 'password': password.strip(), 'role': role,
                'class_id': int(class_assignment_dropdown.value) if role == 'examinee' and class_assignment_dropdown.value else None
            }
            mock_data.mock_users[username.strip()] = new_user
            user_error_text.value = ""
            hide_create_form(e)
            show_user_management()
            return
        app_state.current_page.update()


    def handle_delete_user(username_to_delete):
        def on_delete(e):
            if username_to_delete in mock_data.mock_users:
                del mock_data.mock_users[username_to_delete]
            show_user_management()
        return on_delete

    user_form_container_content = create_card(
        content=ft.Column([
            create_section_title("Create New User"), ft.Container(height=Spacing.LG),
            username_field, ft.Container(height=Spacing.LG), password_field, ft.Container(height=Spacing.LG),
            role_dropdown, ft.Container(height=Spacing.LG), class_assignment_dropdown, ft.Container(height=Spacing.MD),
            user_error_text, ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Create User", on_click=handle_create_user, width=120),
                create_secondary_button("Cancel", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    user_form_container.content = user_form_container_content
    user_form_container.visible = False

    def create_user_card(username, user_data):
        details_column = [
            ft.Text(user_data['username'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
            ft.Text(f"Role: {user_data['role'].title()}", color=Colors.TEXT_SECONDARY),
        ]
        if user_data['role'] == 'examinee' and user_data.get('class_id'):
            class_name = next((c['name'] for c in mock_data.mock_classes if c['id'] == user_data['class_id']), "Chưa gán lớp")
            details_column.append(ft.Text(f"Lớp: {class_name}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM))

        return create_card(
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON_OUTLINE, color=Colors.PRIMARY, size=32), ft.Container(width=Spacing.LG),
                ft.Column(details_column, expand=True, spacing=2),
                create_primary_button("Edit", width=80, on_click=lambda e, u=user_data: open_edit_dialog(u)),
                ft.Container(width=Spacing.SM),
                create_secondary_button("Delete", width=80, on_click=handle_delete_user(username)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=Spacing.LG
        )

    # --- Thống kê và tạo biểu đồ tròn với chú thích ---
    all_users = list(mock_data.mock_users.values())
    total_users = len(all_users)
    role_counts = {
        'admin': sum(1 for u in all_users if u['role'] == 'admin'),
        'instructor': sum(1 for u in all_users if u['role'] == 'instructor'),
        'examinee': sum(1 for u in all_users if u['role'] == 'examinee'),
    }
    role_colors = {
        'admin': Colors.WARNING,
        'instructor': Colors.PRIMARY,
        'examinee': Colors.SUCCESS
    }

    def create_pie_section(count, color):
        percentage = (count / total_users * 100) if total_users > 0 else 0
        return ft.PieChartSection(
            percentage,
            title=f"{percentage:.1f}%",
            title_style=ft.TextStyle(size=Typography.SIZE_XS, color=Colors.WHITE, weight=ft.FontWeight.W_600),
            color=color,
            radius=60,
        )

    def create_legend_item(role, count, color):
        percentage = (count / total_users * 100) if total_users > 0 else 0
        return ft.Row(
            controls=[
                ft.Container(width=16, height=16, bgcolor=color, border_radius=BorderRadius.SM),
                ft.Text(role.title(), weight=ft.FontWeight.W_600, size=Typography.SIZE_SM, expand=True),
                ft.Text(f"{count} ({percentage:.1f}%)", color=Colors.TEXT_SECONDARY, text_align=ft.TextAlign.RIGHT)
            ],
            spacing=Spacing.MD, vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    pie_chart = ft.PieChart(
        sections=[
            create_pie_section(role_counts['admin'], role_colors['admin']),
            create_pie_section(role_counts['instructor'], role_colors['instructor']),
            create_pie_section(role_counts['examinee'], role_colors['examinee']),
        ],
        sections_space=2,
        center_space_radius=30,
    )

    legend = ft.Column([create_legend_item(role, count, role_colors[role]) for role, count in role_counts.items()])

    stats_card = create_card(
        content=ft.Column([
            create_section_title("Thống kê vai trò"),
            ft.Container(height=Spacing.LG),
            ft.Row([ft.Container(pie_chart, expand=1), ft.Container(legend, expand=1)], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ]), padding=Spacing.XL)

    update_user_list()
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Column([
                        ft.Column([
                            create_page_title("User Management"),
                            create_subtitle("Create and manage system users.")
                        ], spacing=Spacing.XS),
                        ft.Container(height=Spacing.LG),
                        ft.Row([
                            search_field, role_filter_dropdown,
                            create_primary_button("Add New User", on_click=show_create_form, width=150)
                        ], spacing=Spacing.MD)
                    ]),
                    ft.Container(height=Spacing.XXL), user_form_container, ft.Container(height=Spacing.XL),
                    ft.Row([
                        ft.Column([
                            create_section_title("All Users"),
                            ft.Container(height=Spacing.LG),
                            user_list_view if user_list_view.controls else ft.Text("No users found.")
                        ], expand=3),
                        ft.Column([stats_card], expand=2)
                    ], vertical_alignment=ft.CrossAxisAlignment.START)
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )
    
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_user_management

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()
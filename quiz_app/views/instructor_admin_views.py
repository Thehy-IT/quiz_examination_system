# QUIZ_EXAMINATION_SYSTEM/quiz_app/views/instructor_admin_views.py

import flet as ft
import datetime
import random

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
import copy
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
    # "Dọn dẹp" trang cũ trước khi vẽ trang mới, một pattern phổ biến trong Flet
    # để đảm bảo không có control rác nào còn sót lại.
    app_state.current_page.clean()
    
    sidebar = create_sidebar(app_state.current_user['role'], "dashboard")
    
    # Hàm tạo mục lịch sử hoạt động
    def create_activity_item(log):
        # Dùng dictionary (map) để ánh xạ một chuỗi hành động sang một cặp (icon, màu sắc).
        # Cách này giúp code dễ đọc và dễ mở rộng hơn là dùng một chuỗi if-elif dài.
        icon_map = {
            'created a new quiz': (ft.Icons.QUIZ, Colors.PRIMARY),
            'completed the quiz': (ft.Icons.CHECK_CIRCLE, Colors.SUCCESS),
            'created a new user': (ft.Icons.PERSON_ADD, Colors.WARNING),
            'created a new class': (ft.Icons.SCHOOL, Colors.PRIMARY_LIGHT),
        }
        # Normalize action key
        action_key = log['action'].replace('đã tạo một bài thi mới', 'created a new quiz') \
                                  .replace('đã hoàn thành bài thi', 'completed the quiz') \
                                  .replace('đã tạo người dùng mới', 'created a new user') \
                                  .replace('đã tạo một lớp học mới', 'created a new class')
        icon, color = icon_map.get(action_key, (ft.Icons.INFO, Colors.GRAY_400))

        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Container(width=Spacing.LG),
                ft.Column([
                    ft.Row([
                        ft.Text(log['user'], weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY),
                        ft.Text(log['action'], color=Colors.TEXT_SECONDARY),
                        ft.Text(f"'{log['details']}'", weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY) if log['details'] else ft.Text(""),
                    ], spacing=Spacing.XS),
                    ft.Text(
                        f"Time: {log['timestamp']}",
                        size=Typography.SIZE_XS,
                        color=Colors.TEXT_MUTED
                    )
                ], spacing=2)
            ]),
            padding=ft.padding.symmetric(vertical=Spacing.MD),
            border=ft.border.only(bottom=ft.BorderSide(1, Colors.GRAY_200))
        )

    stats_cards_list = []
    # Logic phân quyền ngay trên giao diện: Dựa vào vai trò của người dùng đang đăng nhập
    # để quyết định hiển thị các thẻ thống kê nào cho phù hợp.
    # Tạo các thẻ thống kê dựa trên vai trò người dùng
    if app_state.current_user['role'] == 'admin':
        stats_cards_list.extend([
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SCHOOL, color=Colors.PRIMARY), ft.Text("Total Classes", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_data.mock_classes)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.PEOPLE_OUTLINE, color=Colors.SUCCESS), ft.Text("Total Users", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_data.mock_users)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.FACE, color=Colors.WARNING), ft.Text("Total Students", color=Colors.TEXT_SECONDARY)]),
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
    # Tạo nội dung chính của trang tổng quan
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title(f"Welcome back, {app_state.current_user['username']}!"),
                            create_subtitle("Here's an overview of the system's activities.") if app_state.current_user['role'] == 'admin' else create_subtitle("Here's what's happening with your quizzes today.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    stats_cards,
                    ft.Container(height=Spacing.XXXXL),
                    ft.Column([
                        ft.Column([
                            create_section_title("Activity History"),
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
                            create_section_title("Assigned Classes"),
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
                                content=ft.Text("You are not assigned to any classes yet.", color=Colors.TEXT_MUTED),
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
    
    # Cấu hình trang
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    # Gán drawer và appbar vào page. Các control này sẽ được Flet tự động quản lý
    # khi kích thước cửa sổ thay đổi.
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_instructor_dashboard
    
    # Responsive layout
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

    # DatePicker và TimePicker là các control "overlay", chúng không nằm trực tiếp trên trang
    # mà sẽ hiển thị đè lên trên khi được gọi. Cần thêm chúng vào `page.overlay`.
    # 1. Định nghĩa các DatePicker và TimePicker (bang thoi gian)
    def on_start_date_change(e):
        current_val = quiz_start_time_field.value or " "
        time_part = current_val.split(" ")[1] if " " in current_val and len(current_val.split(" ")) > 1 else "00:00"
        quiz_start_time_field.value = f"{start_date_picker.value.strftime('%Y-%m-%d')} {time_part}"
        quiz_start_time_field.update()

    def on_start_time_change(e):
        current_val = quiz_start_time_field.value or " "
        date_part = current_val.split(" ")[0] if " " in current_val else datetime.date.today().strftime('%Y-%m-%d')
        quiz_start_time_field.value = f"{date_part} {start_time_picker.value.strftime('%H:%M')}"
        quiz_start_time_field.update()

    def on_end_date_change(e):
        current_val = quiz_end_time_field.value or " "
        time_part = current_val.split(" ")[1] if " " in current_val and len(current_val.split(" ")) > 1 else "23:59"
        quiz_end_time_field.value = f"{end_date_picker.value.strftime('%Y-%m-%d')} {time_part}"
        quiz_end_time_field.update()

    def on_end_time_change(e):
        current_val = quiz_end_time_field.value or " "
        date_part = current_val.split(" ")[0] if " " in current_val else datetime.date.today().strftime('%Y-%m-%d')
        quiz_end_time_field.value = f"{date_part} {end_time_picker.value.strftime('%H:%M')}"
        quiz_end_time_field.update()

    start_date_picker = ft.DatePicker(on_change=on_start_date_change)
    start_time_picker = ft.TimePicker(on_change=on_start_time_change)
    end_date_picker = ft.DatePicker(on_change=on_end_date_change)
    end_time_picker = ft.TimePicker(on_change=on_end_time_change)

    # Thêm các picker vào overlay của trang để chúng có thể hiển thị
    # Và xóa overlay cũ và thêm các picker vào overlay của trang để chúng có thể hiển thị
    app_state.current_page.overlay.clear()
    app_state.current_page.overlay.extend([start_date_picker, start_time_picker, end_date_picker, end_time_picker])

    #Lọc, khởi tạo các tuỳ chọn lọc, tạo các dropdown lọc
    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_filter_options = [ft.dropdown.Option(key="all", text="All Classes")]
    class_filter_options.extend([ft.dropdown.Option(key=str(cls['id']), text=cls['name']) for cls in instructor_classes])
    
    class_filter_dropdown = ft.Dropdown(label="Filter by Class", width=220, value="all", options=class_filter_options)
    status_filter_dropdown = ft.Dropdown(label="Filter by Status", width=180, value="all", options=[
        ft.dropdown.Option(key="all", text="All Statuses"),
        ft.dropdown.Option(key="active", text="Active"),
        ft.dropdown.Option(key="disabled", text="Disabled"),
    ])
    shuffle_filter_dropdown = ft.Dropdown(label="Filter by Shuffle", width=200, value="all", options=[
        ft.dropdown.Option(key="all", text="All (Shuffle)"),
        ft.dropdown.Option(key="questions", text="Shuffle Questions Only"),
        ft.dropdown.Option(key="answers", text="Shuffle Answers Only"),
        ft.dropdown.Option(key="both", text="Shuffle Both"),
        ft.dropdown.Option(key="none", text="No Shuffle"),
    ])

    # Tạo một cột để chứa danh sách các bài thi đã được lọc và hiển thị.
    quiz_list_view = ft.Column(spacing=Spacing.LG)

    # Hàm xóa bài thi
    def handle_delete_quiz(quiz_to_delete):
        # Dùng closure để "bắt" lấy `quiz_to_delete`. Mỗi nút xóa sẽ có một hàm
        # on_delete riêng biệt với đúng đối tượng quiz cần xóa.
        def on_delete(e):
            mock_data.mock_quizzes = [q for q in mock_data.mock_quizzes if q['id'] != quiz_to_delete['id']]
            if quiz_to_delete['id'] in mock_data.mock_questions:
                del mock_data.mock_questions[quiz_to_delete['id']]
            show_quiz_management()
        return on_delete

    # Hàm cập nhật danh sách bài thi dựa trên các bộ lọc và tìm kiếm
    def update_quiz_list(e=None):
        # Logic lọc đa điều kiện: kết hợp cả tìm kiếm, lọc theo lớp, trạng thái, và kiểu xáo trộn.
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
        # Hiển thị "empty state" nếu không có kết quả, giúp cải thiện UX.
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

    # Gán các hàm xử lý sự kiện cho các control lọc.
    # Kết nối các sự kiện thay đổi để cập nhật danh sách bài thi khi người dùng tương tác.
    search_field.on_change = update_quiz_list
    class_filter_dropdown.on_change = update_quiz_list
    status_filter_dropdown.on_change = update_quiz_list
    shuffle_filter_dropdown.on_change = update_quiz_list

    # Biểu mẫu tạo bài thi mới
    quiz_title_field = create_text_input("Quiz Title", width=400)
    quiz_description_field = create_text_input("Description", width=400, multiline=True, min_lines=3)
    quiz_start_time_field = create_text_input("Start Time (YYYY-MM-DD HH:MM)", width=250, icon=ft.Icons.CALENDAR_MONTH)
    quiz_end_time_field = create_text_input("YYYY-MM-DD HH:MM", width=250, icon=ft.Icons.CALENDAR_MONTH) # thêm trường end_time: hạn của quiz
    quiz_duration_field = create_text_input("Duration (minutes)", width=140, icon=ft.Icons.TIMER)
    quiz_password_field = create_text_input("Quiz Password (optional)", password=True, width=400, icon=ft.Icons.LOCK, can_reveal=True)
    shuffle_questions_switch = ft.Switch(label="Questions shuffle", value=False)
    shuffle_answers_switch = ft.Switch(label="Answers shuffle", value=True)
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
        # Reset các trường về giá trị mặc định mỗi khi mở form để tránh
        # hiển thị lại dữ liệu của lần nhập trước.
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
        # Thu thập dữ liệu từ các trường nhập liệu.
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

        # Validation: Kiểm tra các trường bắt buộc và định dạng dữ liệu.
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

        # Tạo một object quiz mới và thêm vào mock_data.
        new_id = max(q['id'] for q in mock_data.mock_quizzes) + 1 if mock_data.mock_quizzes else 1
        new_quiz = {
            'id': new_id, 'title': title.strip(), 'description': description.strip(),
            'created_by': app_state.current_user['id'], 'created_at': datetime.datetime.now().strftime('%Y-%m-%d'),
            'creator': app_state.current_user['username'], 'questions_count': 0,
            'start_time': start_time_str.strip(), 'duration_minutes': duration_minutes,
            'end_time': end_time_str.strip() if end_time_str else None, # luu End Time
            'class_id': int(class_id), 'password': password.strip() if password else None,
            'is_active': True, 'shuffle_questions': shuffle_questions,
            'shuffle_answers': shuffle_answers, 'show_answers_after_quiz': show_answers_after_quiz
        }
        mock_data.mock_quizzes.append(new_quiz)
        
        quiz_error_text.value = ""
        # Sau khi tạo thành công, ẩn form và tải lại toàn bộ view.
        hide_create_form(e)
        show_quiz_management()

    # Container cho form tạo bài thi mới
    quiz_form_container = create_card(
        content=ft.Column([
            create_section_title("Create New Quiz"), ft.Container(height=Spacing.LG),
            quiz_title_field, ft.Container(height=Spacing.LG),
            quiz_description_field, ft.Container(height=Spacing.LG),
            class_dropdown, ft.Container(height=Spacing.LG),

            # 2. Bố cục cài đặt thời gian theo chiều dọc
            # ft.Text("Start Time", color=Colors.TEXT_SECONDARY), # The field has a label now
            ft.Row([
                quiz_start_time_field,
                ft.IconButton(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, on_click=lambda _: app_state.current_page.open(start_date_picker), tooltip="Pick Start Date"),
                ft.IconButton(icon=ft.Icons.ACCESS_TIME_OUTLINED, on_click=lambda _: app_state.current_page.open(start_time_picker), tooltip="Pick Start Time"),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=Spacing.SM),

            ft.Text("End Time (Optional)", color=Colors.TEXT_SECONDARY),
            ft.Row([
                quiz_end_time_field,
                ft.IconButton(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, on_click=lambda _: app_state.current_page.open(end_date_picker), tooltip="Pick End Date"),
                ft.IconButton(icon=ft.Icons.ACCESS_TIME_OUTLINED, on_click=lambda _: app_state.current_page.open(end_time_picker), tooltip="Pick End Time"),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=Spacing.SM),

            ft.Text("Duration", color=Colors.TEXT_SECONDARY),
            quiz_duration_field,

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
        shuffle_info_en = []
        if quiz.get('shuffle_questions'): shuffle_info_en.append("Questions")
        if quiz.get('shuffle_answers'): shuffle_info_en.append("Answers")

        def toggle_active_state(e):
            # Cập nhật trạng thái `is_active` trực tiếp trong mock_data và tải lại view.
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
                        create_badge(f"Shuffle: {', '.join(shuffle_info_en) if shuffle_info_en else 'None'}", color=Colors.PRIMARY_LIGHT),
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
                    ]),
                    ft.Container(height=Spacing.LG),
                    ft.Row([
                        search_field,
                        ft.Container(expand=True),
                        # THAY ĐỔI CÁC NÚT TẠO QUIZ
                        create_secondary_button("Create from Bank", on_click=lambda e: show_create_quiz_from_bank(), width=160),                        create_primary_button("Create New Quiz", on_click=show_create_form, width=150)
                    ], spacing=Spacing.MD),
                    ft.Container(height=Spacing.MD),
                    ft.Row([
                        ft.Container(expand=True),
                        status_filter_dropdown, shuffle_filter_dropdown, class_filter_dropdown
                    ], spacing=Spacing.MD),

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

def show_create_quiz_from_bank():
    """Hiển thị giao diện tạo quiz bằng cách chọn câu hỏi từ ngân hàng (dùng mock_data)."""
    # Đây là một màn hình phức tạp hơn, có state riêng (`selected_questions`).
    # Nó cho phép người dùng chọn câu hỏi từ một "ngân hàng" chung.
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "quizzes")

    # State cho giao diện này
    selected_questions = {}  # Dùng dictionary để tránh trùng lặp: {question_id: question_data}

    # --- Các controls cho form thông tin quiz ---
    quiz_title_field = create_text_input("Quiz Title", width=400)
    quiz_description_field = create_text_input("Description", width=400, multiline=True, min_lines=2)
    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_dropdown = ft.Dropdown(
        label="Select Class for this Quiz", width=400,
        options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in instructor_classes]
    )
    error_text = ft.Text("", color=Colors.ERROR)

    # --- Các controls cho phần ngân hàng câu hỏi ---
    bank_search_field = create_text_input("Search questions...", width=300, icon=ft.Icons.SEARCH)
    difficulty_filter = ft.Dropdown(label="Difficulty", width=150, value="all", options=[
        ft.dropdown.Option("all", "All Difficulties"),
        ft.dropdown.Option("Easy", "Easy"),
        ft.dropdown.Option("Medium", "Medium"),
        ft.dropdown.Option("Hard", "Hard"),
    ])
    question_bank_list_view = ft.ListView(expand=True, spacing=Spacing.MD)
    selected_questions_list_view = ft.ListView(expand=True, spacing=Spacing.MD)
    selected_counter_text = create_section_title(f"Selected Questions (0)")

    def get_all_questions_from_mock_bank(search_term="", difficulty_filter="all"):
        """Lấy và lọc tất cả câu hỏi từ mock_data để làm ngân hàng câu hỏi."""
        # Logic này khá hay: nó duyệt qua tất cả các bài thi trong mock_data để
        # tổng hợp thành một ngân hàng câu hỏi duy nhất cho giảng viên lựa chọn.
        all_questions = []
        # Dùng set để đảm bảo ID câu hỏi là duy nhất, tránh trùng lặp
        unique_question_ids = set()
        
        # Tổng hợp câu hỏi từ tất cả các bài thi trong mock_data
        for quiz_id in mock_data.mock_questions:
            for question in mock_data.mock_questions[quiz_id]:
                # Tạo một ID duy nhất tạm thời cho mỗi câu hỏi để xử lý
                temp_unique_id = f"{quiz_id}-{question['id']}"
                if temp_unique_id not in unique_question_ids:
                    # Lọc theo từ khóa tìm kiếm
                    matches_search = search_term.lower() in question['question_text'].lower()
                    # Lọc theo độ khó
                    matches_difficulty = (difficulty_filter == "all" or question.get('difficulty') == difficulty_filter)
                    
                    if matches_search and matches_difficulty:
                        # Thêm ID tạm thời vào câu hỏi để xử lý trong UI
                        question_with_temp_id = question.copy()
                        question_with_temp_id['temp_id'] = temp_unique_id
                        all_questions.append(question_with_temp_id)
                        unique_question_ids.add(temp_unique_id)
        return all_questions

    def update_question_views():
        """Cập nhật cả hai danh sách câu hỏi (ngân hàng và đã chọn)."""
        # Hàm này chịu trách nhiệm đồng bộ hóa giao diện của 2 cột:
        # cột ngân hàng câu hỏi và cột câu hỏi đã chọn.
        # Cập nhật danh sách câu hỏi từ ngân hàng
        all_db_questions = get_all_questions_from_mock_bank(
            search_term=bank_search_field.value or "",
            difficulty_filter=difficulty_filter.value or "all"
        )
        question_bank_list_view.controls.clear()
        for q in all_db_questions:
            # Chỉ hiển thị câu hỏi chưa được chọn
            if q['temp_id'] not in selected_questions:
                question_bank_list_view.controls.append(
                    create_card(ft.Row([
                        ft.Column([
                            ft.Text(q['question_text'], weight=ft.FontWeight.W_600),
                            ft.Text(f"Type: {q['question_type']} | Difficulty: {q['difficulty']}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM)
                        ], expand=True),
                        create_primary_button("Add", on_click=lambda e, q_id=q['temp_id'], q_data=q: add_question(q_id, q_data), width=80)
                    ]), padding=Spacing.MD)
                )

        # Cập nhật danh sách câu hỏi đã chọn
        selected_questions_list_view.controls.clear()
        for q_id, q_data in selected_questions.items():
            selected_questions_list_view.controls.append(
                create_card(ft.Row([
                    ft.Column([
                        ft.Text(q_data['question_text'], weight=ft.FontWeight.W_600),
                        ft.Text(f"Type: {q_data['question_type']} | Difficulty: {q_data['difficulty']}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM)
                    ], expand=True),
                    create_secondary_button("Remove", on_click=lambda e, q_id_to_remove=q_id: remove_question(q_id_to_remove), width=80)
                ]), padding=Spacing.MD)
            )
        selected_counter_text.value = f"Selected Questions ({len(selected_questions)})"
        app_state.current_page.update()
    
    def add_question(question_id, question_data):
        selected_questions[question_id] = question_data
        update_question_views()

    def remove_question(question_id):
        if question_id in selected_questions:
            del selected_questions[question_id]
        update_question_views()
    
    def handle_final_create_quiz(e):
        # Validation cuối cùng trước khi tạo quiz.
        if not quiz_title_field.value or not class_dropdown.value or not selected_questions:
            error_text.value = "Quiz Title, Class, and at least one question are required."
            app_state.current_page.update()
            return
        
        new_quiz_id = max(q['id'] for q in mock_data.mock_quizzes) + 1 if mock_data.mock_quizzes else 1
        new_quiz = {
            'id': new_quiz_id, 'title': quiz_title_field.value.strip(), 'description': quiz_description_field.value.strip(),
            'created_by': app_state.current_user['id'], 'created_at': datetime.datetime.now().strftime('%Y-%m-%d'),
            'creator': app_state.current_user['username'], 'questions_count': len(selected_questions),
            'start_time': None, 'duration_minutes': 60, 'end_time': None,
            'class_id': int(class_dropdown.value), 'password': None, 'is_active': True,
            'shuffle_questions': False, 'shuffle_answers': True, 'show_answers_after_quiz': False
        }
        mock_data.mock_quizzes.append(new_quiz)

        # Tạo một danh sách câu hỏi mới cho quiz này.
        # Dùng `copy.deepcopy` để đảm bảo không ảnh hưởng đến dữ liệu gốc trong mock_data.
        new_questions_list = []
        for i, original_question in enumerate(selected_questions.values(), 1):
            new_q = copy.deepcopy(original_question)
            new_q['id'] = i # Gán lại ID mới cho câu hỏi trong bài thi mới
            if 'temp_id' in new_q:
                del new_q['temp_id'] # Xóa ID tạm thời
            new_questions_list.append(new_q)
        
        mock_data.mock_questions[new_quiz_id] = new_questions_list
        
        show_quiz_management()

    bank_search_field.on_change = lambda e: update_question_views()
    difficulty_filter.on_change = lambda e: update_question_views()

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column([
                    ft.Row([create_secondary_button("← Back to Quizzes", on_click=lambda e: show_quiz_management(), width=180)]),
                    ft.Container(height=Spacing.LG),
                    create_page_title("Create Quiz from Question Bank"),
                    ft.Row([
                        ft.Column([
                            create_section_title("Question Bank"), ft.Row([bank_search_field, difficulty_filter]), ft.Divider(),
                            question_bank_list_view,
                        ], expand=3),
                        ft.VerticalDivider(width=Spacing.XXL),
                        ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                            selected_counter_text, ft.Divider(), selected_questions_list_view, ft.Divider(),
                            create_section_title("Quiz Details"), quiz_title_field, quiz_description_field, class_dropdown,
                            error_text, ft.Container(height=Spacing.LG),
                            create_primary_button("Create Quiz", on_click=handle_final_create_quiz, icon=ft.Icons.ADD_CIRCLE)
                        ], expand=2),
                    ], expand=True)
                ]), padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]), expand=True
    )

    update_question_views()

    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_create_quiz_from_bank

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

def show_question_management(quiz):
    """Hiển thị trang quản lý câu hỏi chi tiết với nhiều loại câu hỏi"""
    # Đây là màn hình "trái tim" của việc tạo quiz, nơi giảng viên thêm/sửa/xóa
    # từng câu hỏi cho một bài thi cụ thể.
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
        # Đây là một kỹ thuật rất mạnh: tạo giao diện động (dynamic UI).
        # Tùy thuộc vào loại câu hỏi được chọn, nội dung của `dynamic_form_container` sẽ được thay thế hoàn toàn.
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
    
    # Hàm hiển thị/ẩn form tạo câu hỏi
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
    
    # Hàm xử lý tạo câu hỏi mới
    def handle_create_question(e):
        # Logic này khá phức tạp vì nó phải "đọc" dữ liệu từ các control
        # trong `dynamic_form_container`, mà cấu trúc của container này lại thay đổi liên tục.
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
            # Truy cập vào các control con của form động để lấy giá trị.
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
        
        # Tải lại toàn bộ trang để hiển thị câu hỏi mới.
        question_error_text.value = ""
        hide_question_form(e)
        show_question_management(quiz)
    
    def back_to_quizzes(e):
        show_quiz_management()
    
    update_dynamic_form("multiple_choice")
    
    # Container cho form tạo câu hỏi mới
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
    
    # Tạo card cho từng câu hỏi
    for i, question in enumerate(quiz_questions, 1):
        # Tạo một "bản xem trước" (preview) nhỏ cho mỗi câu hỏi ngay trên card,
        # giúp giảng viên có cái nhìn tổng quan nhanh chóng.
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
    
    # Layout chính
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
    # Chức năng này cho phép giảng viên "nhìn" bài thi dưới góc độ của sinh viên.
    # Nó tái sử dụng rất nhiều code từ `examinee_views.py`.
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
            # Vì đây là chế độ xem trước, không cần xử lý câu trả lời.
            # Ta truyền vào một hàm rỗng (dummy function).
            pass

        shuffle_answers = quiz_basic_info.get('shuffle_answers', False)
        question_component = create_question_by_type(question, dummy_answer_handler, shuffle_answers, is_review=False)
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
    # Màn hình này tổng hợp và trực quan hóa dữ liệu kết quả thi,
    # là một công cụ rất mạnh cho giảng viên.
    app_state.current_page.clean()

    sidebar = create_sidebar(app_state.current_user['role'], "results")
    results_container = ft.Column()

    def update_results_display(selected_class_id=None, selected_quiz_id=None):
        results_container.controls.clear()
        # Nếu chưa chọn lớp hoặc bài thi, hiển thị hướng dẫn.
        if not selected_class_id or not selected_quiz_id:
            results_container.controls.append(
                create_card(ft.Column([
                    ft.Icon(ft.Icons.FILTER_LIST, size=48, color=Colors.GRAY_400),
                    ft.Text("Select a Class and a Quiz", size=Typography.SIZE_LG, color=Colors.TEXT_MUTED),
                    ft.Text("Choose from the dropdowns above to view the results.", color=Colors.TEXT_MUTED),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=Spacing.XXXXL)
            )
            app_state.current_page.update()
            return

        # Logic tổng hợp dữ liệu:
        # 1. Lấy danh sách sinh viên trong lớp đã chọn.
        students_in_class = [u for u in mock_data.mock_users.values() if u.get('class_id') == int(selected_class_id)]
        attempts_for_quiz = [a for a in mock_data.mock_attempts if a['quiz_id'] == int(selected_quiz_id)]

        student_results = []
        for student in students_in_class:
            student_attempts = [a for a in attempts_for_quiz if a['user_id'] == student['id']]
            if student_attempts:
                latest_attempt = max(student_attempts, key=lambda x: x['completed_at'])
                student_results.append({'student': student, 'attempt': latest_attempt})

        # Tính toán các chỉ số thống kê.
        total_students = len(students_in_class)
        completed_count = len(student_results)
        completion_rate = (completed_count / total_students * 100) if total_students > 0 else 0
        
        scores_10 = [res['attempt']['percentage'] / 10.0 for res in student_results]
        avg_score_10 = sum(scores_10) / len(scores_10) if scores_10 else 0
        highest_score_10 = max(scores_10) if scores_10 else 0

        bar_groups = [
            # Chuẩn bị dữ liệu cho biểu đồ cột.
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

        # Chuẩn bị dữ liệu cho bảng chi tiết.
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

        # Thêm các component đã xử lý vào view.
        results_container.controls.extend([
            ft.Row([
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.STAR_HALF, color=Colors.PRIMARY), ft.Text("Average Score")]), ft.Text(f"{avg_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color=Colors.WARNING), ft.Text("Highest Score")]), ft.Text(f"{highest_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.PIE_CHART, color=Colors.SUCCESS), ft.Text("Completion Rate")]), ft.Text(f"{completion_rate:.1f}%", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Container(height=Spacing.XXL),
            create_card(ft.Column([create_section_title("Student Score Distribution (Scale of 10)"), ft.Container(chart, height=300, padding=Spacing.LG)]), padding=Spacing.XL),
            ft.Container(height=Spacing.XXL),
            create_card(ft.Column([create_section_title("Detailed Results"), results_table]), padding=Spacing.XL),
        ])
        app_state.current_page.update()

    instructor_classes = [c for c in mock_data.mock_classes if c['instructor_id'] == app_state.current_user['id']]
    class_dd = ft.Dropdown(label="Select Class", width=250, options=[ft.dropdown.Option(key=c['id'], text=c['name']) for c in instructor_classes])
    quiz_dd = ft.Dropdown(label="Select Quiz", width=300, disabled=True)

    def on_class_change(e):
        # Đây là logic cho "dependent dropdowns" (dropdown phụ thuộc).
        # Khi chọn một lớp, danh sách các bài thi trong dropdown thứ hai sẽ được cập nhật tương ứng.
        selected_class_id = int(e.control.value)
        quizzes_in_class = [q for q in mock_data.mock_quizzes if q.get('class_id') == selected_class_id]
        quiz_dd.options = [ft.dropdown.Option(key=q['id'], text=q['title']) for q in quizzes_in_class]
        # Reset lựa chọn của dropdown quiz.
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
    # Một trang CRUD (Create, Read, Update, Delete) đơn giản cho thông tin cá nhân.
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "settings")

    current_password_field = create_text_input("Current Password", password=True, can_reveal=True)
    new_password_field = create_text_input("New Password", password=True, can_reveal=True)
    confirm_password_field = create_text_input("Confirm New Password", password=True, can_reveal=True)
    password_message_text = ft.Text("", size=Typography.SIZE_SM)

    # Hàm xử lý lưu mật khẩu mới
    # Bao gồm các bước validation cơ bản.
    def handle_save_password(e):
        current_pass = current_password_field.value
        new_pass = new_password_field.value
        confirm_pass = confirm_password_field.value

        if not all([current_pass, new_pass, confirm_pass]):
            password_message_text.value = "Please fill in all fields."
            password_message_text.color = Colors.ERROR
        elif current_pass != app_state.current_user['password']:
            password_message_text.value = "Incorrect current password."
            password_message_text.color = Colors.ERROR
            current_password_field.value = ""
        elif new_pass != confirm_pass:
            password_message_text.value = "New passwords do not match."
            password_message_text.color = Colors.ERROR
            new_password_field.value = ""
            confirm_password_field.value = ""
        else:
            mock_data.mock_users[app_state.current_user['username']]['password'] = new_pass
            app_state.current_user['password'] = new_pass
            password_message_text.value = "Password changed successfully!"
            password_message_text.color = Colors.SUCCESS
            current_password_field.value = ""
            new_password_field.value = ""
            confirm_password_field.value = ""
        app_state.current_page.update()

    info_details = [
        ft.Row([ft.Text("Username:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['username'])]),
        ft.Divider(),
        ft.Row([ft.Text("Role:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['role'].title())]),
    ]

    # Thêm thông tin lớp học nếu là giảng viên
    if app_state.current_user['role'] == 'instructor':
        assigned_classes = [c['name'] for c in mock_data.mock_classes if c.get('instructor_id') == app_state.current_user['id']]
        if assigned_classes:
            info_details.extend([ft.Divider(), ft.Row([ft.Text("Assigned Classes:", weight=ft.FontWeight.W_600), ft.Text(", ".join(assigned_classes))])])

    # Giao diện chính
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
                        create_card(content=ft.Column([create_section_title("Account Information"), ft.Container(height=Spacing.LG), *info_details]), padding=Spacing.XL),
                        create_card(content=ft.Column([
                            create_section_title("Change Password"), ft.Container(height=Spacing.LG),
                            current_password_field, new_password_field, confirm_password_field,
                            ft.Container(height=Spacing.SM), password_message_text, ft.Container(height=Spacing.LG),
                            create_primary_button("Save Changes", on_click=handle_save_password)
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
    # Một trang CRUD điển hình cho việc quản lý lớp học.
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

    class_name_field = create_text_input("Class Name", width=400)
    instructors = [user for user in mock_data.mock_users.values() if user['role'] == 'instructor']
    instructor_dropdown = ft.Dropdown(
        label="Select Instructor", width=400,
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
            class_error_text.value = "Class name and instructor are required."
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
            create_section_title("Create New Class"), ft.Container(height=Spacing.LG),
            class_name_field, ft.Container(height=Spacing.LG), instructor_dropdown, ft.Container(height=Spacing.MD),
            class_error_text, ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Create Class", on_click=handle_create_class, width=120),
                create_secondary_button("Cancel", on_click=hide_create_form, width=100)
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
                    ft.Text(f"Instructor: {instructor_name}", color=Colors.TEXT_SECONDARY),
                ], expand=True),
                create_secondary_button("Delete", width=80, on_click=handle_delete_class(cls['id'])),
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
                            create_page_title("Class Management"),
                            create_subtitle("Create and manage classes in the system.")
                        ], expand=True, spacing=Spacing.XS),
                        search_field,
                        create_primary_button("Create New Class", on_click=show_create_form, width=150)
                    ]),
                    ft.Container(height=Spacing.XXL), class_form_container, ft.Container(height=Spacing.XL),
                    create_section_title("Class List"), ft.Container(height=Spacing.LG),
                    class_list_view if class_list_view.controls else ft.Text("No classes have been created yet.")
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
    # Một trang CRUD khác, nhưng phức tạp hơn một chút với việc sử dụng Dialog để chỉnh sửa.
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
        # Sử dụng `AlertDialog` là một cách hay để thực hiện các hành động chỉnh sửa
        # mà không cần chuyển sang một trang hoàn toàn mới.
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
            label="Assign to Class (optional)", width=400, value=user_to_edit.get('class_id'),
            options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in mock_data.mock_classes],
            visible=(user_to_edit['role'] == 'examinee')
        )

        def on_edit_role_change(e):
            # Dropdown chọn lớp chỉ hiển thị khi vai trò là 'examinee'.
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
            ft.dropdown.Option(key='examinee', text='Examinee'),
        ]
    )
    class_assignment_dropdown = ft.Dropdown(
        label="Assign to Class (optional)", width=400,
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
        if user_data['role'] == 'examinee' and user_data.get('class_id') is not None:
            class_name = next((c['name'] for c in mock_data.mock_classes if c['id'] == user_data['class_id']), "Unassigned")
            details_column.append(ft.Text(f"Class: {class_name}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM))

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
            create_section_title("Role Statistics"),
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
                            user_list_view if user_list_view.controls else create_card(ft.Text("No users found.", text_align=ft.TextAlign.CENTER), padding=Spacing.XL)
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
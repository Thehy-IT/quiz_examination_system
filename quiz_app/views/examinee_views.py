import flet as ft
import time
import threading
from datetime import datetime, timedelta
from ..components.navigation import create_app_bar

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
from ..components.ui_helpers import (
    create_primary_button, 
    create_secondary_button,
    create_card, 
    create_section_title, 
    create_page_title, 
    create_subtitle,
    create_badge
)
from ..components.question_widgets import create_question_by_type
from ..components.navigation import create_app_header, create_sidebar
from ..utils.constants import Colors, Spacing, Typography, BorderRadius


# =============================================================================
# EXAMINEE DASHBOARD VIEW ..
# =============================================================================

def show_examinee_dashboard():
    """Hiển thị giao diện Dashboard cho Examinee"""
    
    # 1. Làm sạch trang hiện tại và thiết lập layout chính
    app_state.current_page.clean()
    app_state.current_page.title = "Examinee Dashboard"
    app_state.current_view_handler = show_examinee_dashboard
    
    sidebar = create_sidebar(app_state.current_user['role'], active_page="home")
    header = create_app_header()
    quiz_list_view = ft.ListView(expand=1, spacing=Spacing.LG, padding=ft.padding.symmetric(horizontal=Spacing.XXXL, vertical=Spacing.LG))
    

    # Bố cục trang chính
    main_content = ft.Column([
        header,
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=Colors.GRAY_200),

            ft.Container(
                content=ft.Column([
                    create_page_title("Available Quizzes"),
                    create_subtitle("Select a quiz to start your exam."),
                    ft.Container(height=Spacing.LG),
                    quiz_list_view
                ], expand=True, spacing=Spacing.SM),
                padding=ft.padding.symmetric(vertical=Spacing.LG),
                expand=True
            )
        ], expand=True)
    ], expand=True)
    
    app_state.current_page.add(main_content)

    # 2. Hàm cập nhật danh sách bài quiz
    def update_quiz_list(e=None):
        quiz_list_view.controls.clear()
        for quiz in mock_data.mock_quizzes:
            quiz_card = create_quiz_card(quiz)
            quiz_list_view.controls.append(quiz_card)
        app_state.current_page.update()

    # 3. Hàm xử lý khi học sinh bấm vào "Start Quiz"
    def handle_start_quiz(quiz):
        def start_action(e):
            """Hàm được gọi khi nhấn nút. Nó sẽ tạo và hiển thị dialog nhập mật khẩu."""
            
            # Tạo ô nhập mật khẩu
            password_field = ft.TextField(
                label="Quiz Password",
                password=True, 
                can_reveal_password=True,
                border_color=Colors.GRAY_300,
                focused_border_color=Colors.PRIMARY
            )
            error_message = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

            # Hàm kiểm tra mật khẩu
            def check_password(e_dialog):
                correct_password = str(quiz.get('password') or "")
                entered_password = str(password_field.value or "").strip()
                if correct_password and entered_password == correct_password:
                    dialog.open = False
                    app_state.current_page.dialog = None
                    app_state.current_page.update()
                    show_quiz_taking(quiz)
                else:
                    error_message.value = "Incorrect password. Please try again."
                    dialog.update()
            
            # Hàm đóng dialog
            def close_dialog(e_dialog):
                dialog.open = False
                if dialog in app_state.current_page.overlay:
                    app_state.current_page.overlay.remove(dialog)
                app_state.current_page.dialog = None  # Reset trạng thái dialog
                app_state.current_page.update()

            # Tạo dialog
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Password required for '{quiz['title']}'", weight=ft.FontWeight.W_600),
                content=ft.Column([
                    ft.Text("This quiz requires a password to start."),
                    password_field, 
                    error_message
                ], tight=True, spacing=Spacing.LG),
                actions=[
                    create_secondary_button("Cancel", on_click=close_dialog),
                    create_primary_button("Start Quiz", on_click=check_password, icon=ft.Icons.LOGIN),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.LG)
            )

            # Hiển thị dialog
            app_state.current_page.overlay.append(dialog)
            dialog.open = True
            app_state.current_page.update()

        return start_action

    # 4. Tạo card cho mỗi bài quiz
    def create_quiz_card(quiz):
        return create_card(
            ft.Column([
                ft.Row([
                    ft.Text(quiz["title"], size=Typography.SIZE_XL, weight=ft.FontWeight.W_600, expand=True),
                    create_badge(f"{quiz['questions_count']} Qs", color=Colors.PRIMARY_LIGHT),
                    ft.Container(width=Spacing.SM),
                    create_badge(f"{quiz['duration_minutes']} min", color=Colors.WARNING)
                ]),
                ft.Text(quiz["description"], size=Typography.SIZE_BASE, color=Colors.TEXT_SECONDARY),
                ft.Divider(height=Spacing.LG, color="transparent"),
                ft.Row([
                    ft.Icon(ft.Icons.PERSON_OUTLINED, color=Colors.TEXT_MUTED, size=16),
                    ft.Text(f"Created by: {quiz['creator']}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM),
                    ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, color=Colors.TEXT_MUTED, size=16),
                    ft.Text(f"Start: {quiz['start_time']}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM),
                ], spacing=Spacing.SM),
                ft.Divider(),
                ft.Row([
                    ft.Container(expand=True),
                    create_primary_button("Start Quiz", on_click=handle_start_quiz(quiz), icon=ft.Icons.PLAY_ARROW_ROUNDED)
                ])
            ])
        )

    # Khởi tạo và cập nhật danh sách
    update_quiz_list()
    app_state.current_page.update()

# =============================================================================
# QUIZ TAKING VIEW
# =============================================================================

def show_quiz_taking(quiz_basic_info):
    """Hiển thị giao diện làm bài thi"""
    app_state.current_page.clean()
    app_state.current_page.title = f"Taking Quiz: {quiz_basic_info['title']}"
    app_state.current_view_handler = None # Không cho phép resize khi đang làm bài

    # Khởi tạo trạng thái làm bài
    app_state.current_question_index = 0
    app_state.user_answers = {}
    app_state.quiz_questions = mock_data.mock_questions.get(quiz_basic_info['id'], [])


    app_state.quiz_start_time = datetime.now()

    
    # Giao diện câu hỏi và điều hướng
    question_container = ft.Column(expand=True)
    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text("0/0")
    timer_text = ft.Text("00:00")

    def update_question_display():
        """Cập nhật giao diện để hiển thị câu hỏi hiện tại"""
        if not app_state.quiz_questions:
            question_container.controls = [ft.Text("This quiz has no questions.")]
            return
            
        current_question = app_state.quiz_questions[app_state.current_question_index]
        user_answer = app_state.user_answers.get(current_question['id'])
        

        question_widget = create_question_by_type(
            question=current_question,
            on_answer_change=handle_answer_change,
            user_answer=user_answer,
            shuffle_answers=True, # Xáo trộn câu trả lời khi làm bài
        )

        
        question_container.controls = [create_card(question_widget, elevation=4)]
        update_progress()
        app_state.current_page.update()

    def handle_answer_change(question_id, answer):
        """Lưu câu trả lời của người dùng"""
        app_state.user_answers[question_id] = answer

    def handle_previous(e):
        """Chuyển đến câu hỏi trước đó"""
        if app_state.current_question_index > 0:
            app_state.current_question_index -= 1
            update_question_display()

    def handle_next(e):
        """Chuyển đến câu hỏi tiếp theo"""
        if app_state.current_question_index < len(app_state.quiz_questions) - 1:
            app_state.current_question_index += 1
            update_question_display()

    def handle_submit(e):
        """Xử lý nộp bài"""
        if app_state.quiz_timer_thread:
            app_state.quiz_timer_thread.do_run = False

        show_quiz_results(quiz_basic_info, app_state.user_answers, app_state.quiz_start_time)

    def exit_quiz(e):
        """Thoát khỏi chế độ làm bài (có thể thêm cảnh báo)"""
        if app_state.quiz_timer_thread:
            app_state.quiz_timer_thread.do_run = False
        show_examinee_dashboard()
    
    def update_progress():
        """Cập nhật thanh tiến trình"""
        total_questions = len(app_state.quiz_questions)
        current_num = app_state.current_question_index + 1
        progress_bar.value = current_num / total_questions if total_questions > 0 else 0
        progress_text.value = f"{current_num}/{total_questions}"

    def run_timer():
        """Chạy đồng hồ đếm giờ"""
        t = threading.current_thread()
        duration = timedelta(minutes=quiz_basic_info.get('duration_minutes', 10))
        end_time = datetime.now() + duration
        
        while getattr(t, "do_run", True) and datetime.now() < end_time:
            remaining = end_time - datetime.now()
            timer_text.value = str(remaining).split('.')[0][2:] # Format MM:SS
            app_state.current_page.update()
            time.sleep(1)
        
        if getattr(t, "do_run", True): # Nếu timer hết giờ tự nhiên
            handle_submit(None)

    # Chạy timer trong một thread riêng
    app_state.quiz_timer_thread = threading.Thread(target=run_timer)
    app_state.quiz_timer_thread.start()


    # Bố cục giao diện làm bài
    quiz_layout = ft.Column([
        ft.Row([
            create_secondary_button("Exit Quiz", on_click=exit_quiz),  # Xóa icon ở đây
            ft.Container(expand=True),

            ft.Row([
                ft.Icon(ft.Icons.TIMER_OUTLINED, color=Colors.PRIMARY),
                timer_text
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(expand=True)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        question_container,
        ft.Container(height=Spacing.XL),
        ft.Row([
            create_secondary_button("Previous", on_click=handle_previous),  # Xóa icon nếu có
            ft.Column([progress_text, progress_bar], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            create_secondary_button("Next", on_click=handle_next),  # Xóa icon nếu có
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Container(height=Spacing.LG),
        create_primary_button("Submit Quiz", on_click=handle_submit, width=9999, icon=ft.Icons.DONE_ALL_ROUNDED)
    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)

    app_state.current_page.add(
        ft.Container(
            content=quiz_layout, 
            padding=Spacing.XXXXL, 
            alignment=ft.alignment.center
        )
    )
    update_question_display()

# Các hàm còn lại (show_quiz_results, show_my_attempts, ...) giữ nguyên
def show_quiz_results(quiz_data, user_answers, start_time):
    """Hiển thị kết quả bài thi"""
    app_state.current_page.clean()
    app_state.current_page.title = f"Results for {quiz_data['title']}"
    app_state.current_view_handler = show_examinee_dashboard # Để có thể resize

    questions = mock_data.mock_questions.get(quiz_data['id'], [])
    total_questions = len(questions)
    correct_answers = 0

    for q in questions:
        user_ans = user_answers.get(q['id'])
        if q['question_type'] == 'multiple_choice':
            correct_option = next((opt['option_text'] for opt in q['options'] if opt['is_correct']), None)
            if user_ans == correct_option:
                correct_answers += 1
        elif q['question_type'] == 'true_false':
            if user_ans == q['correct_answer']:
                correct_answers += 1
        # Thêm các logic chấm điểm khác ở đây

    score_text = f"{correct_answers}/{total_questions}"
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    time_taken = datetime.now() - start_time

    results_content = ft.Column([
        create_page_title("Quiz Results"),
        create_card(
            ft.Column([
                ft.Row([
                    ft.Column([
                        create_section_title("Score"),
                        ft.Text(score_text, size=Typography.SIZE_3XL, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
                    ]),
                    ft.Column([
                        create_section_title("Percentage"),
                        ft.Text(f"{percentage:.2f}%", size=Typography.SIZE_3XL, weight=ft.FontWeight.BOLD, color=Colors.SUCCESS),
                    ]),
                    ft.Column([
                        create_section_title("Time Taken"),
                        ft.Text(str(time_taken).split('.')[0], size=Typography.SIZE_3XL, weight=ft.FontWeight.BOLD),
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Divider(),
                create_primary_button("Back to Dashboard", on_click=lambda e: show_examinee_dashboard(), icon=ft.Icons.HOME)
            ], spacing=Spacing.XL)
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    app_state.current_page.add(
        ft.Container(
            content=results_content,
            expand=True,
            alignment=ft.alignment.center,
            padding=Spacing.XXXL
        )
    )
    app_state.current_page.update()

def show_student_results_overview():
    """Hiển thị tổng quan kết quả của sinh viên với biểu đồ"""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "results")

    user_attempts = [attempt for attempt in mock_data.mock_attempts if attempt['user_id'] == app_state.current_user['id']]
    user_attempts.sort(key=lambda x: x['completed_at'])

    bar_groups = []
    total_score_10 = 0
    highest_score_10 = 0

    if user_attempts:
        for i, attempt in enumerate(user_attempts):
            quiz_info = next((q for q in mock_data.mock_quizzes if q['id'] == attempt['quiz_id']), None)
            quiz_title = quiz_info['title'] if quiz_info else f"Quiz {attempt['quiz_id']}"
            
            score_10 = attempt['percentage'] / 10.0
            total_score_10 += score_10
            if score_10 > highest_score_10:
                highest_score_10 = score_10

            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=score_10,
                            width=20,
                            color=Colors.PRIMARY,
                            tooltip=f"{quiz_title}\nĐiểm: {score_10:.1f}",
                            border_radius=BorderRadius.SM,
                        ),
                    ],
                )
            )

    avg_score_10 = (total_score_10 / len(user_attempts)) if user_attempts else 0

    chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, Colors.GRAY_300),
        left_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=v, label=ft.Text(str(v))) for v in range(0, 11, 2)],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=i, label=ft.Text(f"Lần {i+1}", size=Typography.SIZE_XS)) for i in range(len(user_attempts))],
            labels_size=30,
        ),
        horizontal_grid_lines=ft.ChartGridLines(interval=2, color=Colors.GRAY_200, width=1),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, Colors.GRAY_800),
        max_y=10,
        interactive=True,
        expand=True,
    )

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Results Overview"),
                            create_subtitle("A visual summary of your performance across all quizzes.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    ft.Row([
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.STAR_HALF, color=Colors.PRIMARY), ft.Text("Điểm trung bình")]), ft.Text(f"{avg_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color=Colors.WARNING), ft.Text("Điểm cao nhất")]), ft.Text(f"{highest_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.QUIZ, color=Colors.SUCCESS), ft.Text("Tổng số bài đã làm")]), ft.Text(str(len(user_attempts)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Container(height=Spacing.XXXXL),
                    create_card(
                        content=ft.Column([
                            create_section_title("Biểu đồ tiến độ (Thang điểm 10)"),
                            ft.Container(height=Spacing.LG),
                            ft.Container(
                                content=chart if user_attempts else ft.Column([
                                    ft.Icon(ft.Icons.CHART, size=48, color=Colors.GRAY_400),
                                    ft.Text("No data to display", size=Typography.SIZE_LG, color=Colors.TEXT_MUTED),
                                    ft.Text("Complete a quiz to see your progress here.", color=Colors.TEXT_MUTED)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                                height=400,
                                padding=Spacing.LG
                            )
                        ]),
                        padding=Spacing.XL
                    )
                ]),
                padding=Spacing.XXXXL,
                expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_student_results_overview

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

def show_attempt_review(attempt):
    """Hiển thị giao diện xem lại chi tiết một lần làm bài"""
    quiz_id = attempt['quiz_id']
    quiz_info = next((q for q in mock_data.mock_quizzes if q['id'] == quiz_id), {})

    if not quiz_info.get('show_answers_after_quiz', False):
        # Hiển thị thông báo và quay về trang My Attempts
        app_state.current_page.clean()
        app_state.current_page.title = "Review Not Allowed"
        app_state.current_page.add(
            create_card(
                ft.Column([
                    ft.Text("Bạn không được phép xem lại đáp án bài thi này.", color=Colors.ERROR, size=Typography.SIZE_XL),
                    ft.Container(height=Spacing.LG),
                    create_primary_button("Return", on_click=lambda e: show_my_attempts())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.XL)
            )
        )
        app_state.current_page.update()
        return
    app_state.current_page.clean()
    app_state.current_page.title = f"Reviewing: {quiz_info.get('title', 'Quiz')}"
    app_state.current_view_handler = None

    # Khởi tạo trạng thái review
    questions = mock_data.mock_questions.get(quiz_id, [])
    current_question_index = 0
    question_container = ft.Column(expand=True)

    def update_review_display():
        current_question = questions[current_question_index]
        user_answer = attempt['user_answers'].get(current_question['id'])
        
        question_widget = create_question_by_type(
            question=current_question,
            is_review=True,
            user_answer=user_answer,
            on_answer_change=lambda q_id, ans: None,
        )
        question_container.controls = [create_card(question_widget, elevation=2)]
        app_state.current_page.update()

    def handle_previous(e):
        nonlocal current_question_index
        if current_question_index > 0:
            current_question_index -= 1
            update_review_display()

    def handle_next(e):
        nonlocal current_question_index
        if current_question_index < len(questions) - 1:
            current_question_index += 1
            update_review_display()
    
    def exit_review(e):
        show_my_attempts()

    review_layout = ft.Column([
        ft.Row([
            create_secondary_button("Back to Attempts", on_click=exit_review),
            ft.Container(expand=True),
            create_page_title(f"Question {current_question_index + 1}/{len(questions)}")
        ]),
        ft.Divider(),
        question_container,
        ft.Row([
            create_secondary_button("Previous", on_click=handle_previous),
            ft.Container(expand=True),
            create_secondary_button("Next", on_click=handle_next),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ], expand=True)
    
    app_state.current_page.add(ft.Container(content=review_layout, padding=Spacing.XXXXL))
    update_review_display()

def show_my_attempts():
    """Hiển thị lịch sử các lần làm bài của sinh viên"""
    app_state.current_page.clean()
    app_state.current_page.title = "My Attempts"
    app_state.current_view_handler = show_my_attempts

    sidebar = create_sidebar(app_state.current_user['role'], active_page="attempts")
    header = create_app_header()
    
    attempts_list = ft.ListView(expand=True, spacing=Spacing.LG)
    user_id = app_state.current_user['id']
    user_attempts = [atm for atm in mock_data.mock_attempts if atm['user_id'] == user_id]

    for attempt in user_attempts:
        quiz_info = next((q for q in mock_data.mock_quizzes if q['id'] == attempt['quiz_id']), {})
        
        def create_review_handler(atm):
            return lambda e: show_attempt_review(atm)

        attempts_list.controls.append(
            create_card(ft.Column([
                ft.Row([
                    ft.Text(quiz_info.get('title', 'Unknown Quiz'), weight=ft.FontWeight.W_600, size=Typography.SIZE_LG, expand=True),
                    create_badge(f"Score: {attempt['score']}", Colors.PRIMARY),
                    ft.Container(width=Spacing.SM),
                    create_badge(f"{attempt['percentage']}%", Colors.SUCCESS)
                ]),
                ft.Text(f"Completed on: {attempt['completed_at']}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM),
                ft.Row([
                    ft.Container(expand=True),
                    create_primary_button("Review", on_click=create_review_handler(attempt), icon=ft.Icons.PAGEVIEW)
                ])
            ]))
        )
    
    main_content = ft.Column([
        header,
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=Colors.GRAY_200),
            ft.Container(
                content=ft.Column([
                    create_page_title("My Attempts"),
                    ft.Container(height=Spacing.LG),
                    attempts_list if user_attempts else ft.Text("You have not made any attempts yet."),
                ]),
                padding=ft.padding.symmetric(horizontal=Spacing.XXXL, vertical=Spacing.LG),
                expand=True
            )
        ], expand=True)
    ], expand=True)

    app_state.current_page.add(main_content)
    app_state.current_page.update()

def show_profile_page():
    """Hiển thị trang thông tin cá nhân và đổi mật khẩu cho sinh viên."""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "profile")

    current_password_field = ft.TextField(label="Mật khẩu hiện tại", password=True, can_reveal_password=True)
    new_password_field = ft.TextField(label="Mật khẩu mới", password=True, can_reveal_password=True)
    confirm_password_field = ft.TextField(label="Xác nhận mật khẩu mới", password=True, can_reveal_password=True)
    password_message_text = ft.Text("", size=Typography.SIZE_SM)

    def handle_save_password(e):
        current_pass = current_password_field.value
        new_pass = new_password_field.value
        confirm_pass = confirm_password_field.value

        if not all([current_pass, new_pass, confirm_pass]):
            password_message_text.value = "Vui lòng điền đầy đủ các trường."
            password_message_text.color = Colors.ERROR
            app_state.current_page.update()
            return

        if current_pass != app_state.current_user['password']:
            password_message_text.value = "Mật khẩu hiện tại không đúng."
            password_message_text.color = Colors.ERROR
            current_password_field.value = ""
            app_state.current_page.update()
            return

        if new_pass != confirm_pass:
            password_message_text.value = "Mật khẩu mới không khớp."
            password_message_text.color = Colors.ERROR
            new_password_field.value = ""
            confirm_password_field.value = ""
            app_state.current_page.update()
            return

        mock_data.mock_users[app_state.current_user['username']]['password'] = new_pass
        app_state.current_user['password'] = new_pass

        password_message_text.value = "Đổi mật khẩu thành công!"
        password_message_text.color = Colors.SUCCESS
        current_password_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        app_state.current_page.update()

    class_name = "N/A"
    if app_state.current_user.get('class_id'):
        class_info = next((c for c in mock_data.mock_classes if c['id'] == app_state.current_user['class_id']), None)
        if class_info:
            class_name = class_info['name']

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Profile"),
                            create_subtitle("View your personal information and manage your account.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    ft.Row([
                        create_card(
                            content=ft.Column([
                                create_section_title("Thông tin tài khoản"),
                                ft.Container(height=Spacing.LG),
                                ft.Row([ft.Text("Username:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['username'])]),
                                ft.Divider(),
                                ft.Row([ft.Text("Vai trò:", weight=ft.FontWeight.W_600), ft.Text(app_state.current_user['role'].title())]),
                                ft.Divider(),
                                ft.Row([ft.Text("Lớp học:", weight=ft.FontWeight.W_600), ft.Text(class_name)]),
                            ]),
                            padding=Spacing.XL
                        ),
                        create_card(
                            content=ft.Column([
                                create_section_title("Đổi mật khẩu"),
                                ft.Container(height=Spacing.LG),
                                current_password_field,
                                new_password_field,
                                confirm_password_field,
                                ft.Container(height=Spacing.SM),
                                password_message_text,
                                ft.Container(height=Spacing.LG),
                                create_primary_button("Lưu thay đổi", on_click=handle_save_password)
                            ]),
                            padding=Spacing.XL
                        ),
                    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
                ]),
                padding=Spacing.XXXXL,
                expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_profile_page

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()
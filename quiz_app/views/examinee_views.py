import flet as ft
import time
import threading
from datetime import datetime, timedelta

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
# EXAMINEE DASHBOARD VIEW
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
    """Giao diện xem tổng quan kết quả các bài thi của sinh viên"""
    app_state.current_page.clean()
    app_state.current_page.title = "My Results"
    app_state.current_view_handler = show_student_results_overview

    sidebar = create_sidebar(app_state.current_user['role'], active_page="results")
    header = create_app_header()
    
    main_content = ft.Column([
        header,
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=Colors.GRAY_200),
            ft.Container(
                content=ft.Text("Student Results Overview - In Progress", size=24),
                padding=Spacing.LG,
                expand=True,
                alignment=ft.alignment.center
            )
        ], expand=True)
    ], expand=True)
    
    app_state.current_page.add(main_content)
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
    """Hiển thị trang thông tin cá nhân của người dùng"""
    app_state.current_page.clean()
    app_state.current_page.title = "My Profile"
    app_state.current_view_handler = show_profile_page

    sidebar = create_sidebar(app_state.current_user['role'], active_page="profile")
    header = create_app_header()

    def handle_save_password(e):
        # Logic lưu mật khẩu mới
        print("Password saved!")

    main_content = ft.Column([
        header,
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=Colors.GRAY_200),
            ft.Container(
                content=ft.Text("Profile Page - In Progress", size=24),
                padding=Spacing.LG,
                expand=True,
                alignment=ft.alignment.center
            )
        ], expand=True)
    ], expand=True)
    
    app_state.current_page.add(main_content)
    app_state.current_page.update()
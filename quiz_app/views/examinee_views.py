# QUIZ_EXAMINATION_SYSTEM/quiz_app/views/examinee_views.py

import flet as ft
import datetime
import time
import threading

# Import các module cần thiết
from .. import app_state
from ..data import mock_data
from ..utils.constants import Colors, Spacing, Typography, BorderRadius

# Import các hàm trợ giúp và component
from ..components.ui_helpers import (
    create_text_input, create_card, create_page_title, create_subtitle,
    create_primary_button, create_secondary_button, create_section_title
)
from ..components.navigation import create_sidebar, create_app_bar, create_app_header
from ..components.question_widgets import create_question_by_type


def show_examinee_dashboard():
    """Hiển thị trang tổng quan cho sinh viên"""
    app_state.current_page.clean()
    
    sidebar = create_sidebar(app_state.current_user['role'], "home")
    
    # Logic tìm kiếm và lọc
    search_field = create_text_input("Search by quiz title...", width=300, icon=ft.Icons.SEARCH)
    quiz_list_view = ft.Column(spacing=Spacing.LG)

    def update_quiz_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        student_class_id = app_state.current_user.get('class_id')
        
        available_quizzes = []
        if student_class_id is not None:
            available_quizzes = [
                q for q in mock_data.mock_quizzes 
                if q.get('is_active', False) and q.get('class_id') == student_class_id
            ]
        filtered_quizzes = [
            q for q in available_quizzes if search_term in q['title'].lower()
        ]

        quiz_list_view.controls.clear()
        if filtered_quizzes:
            for quiz in filtered_quizzes:
                quiz_list_view.controls.append(create_quiz_card(quiz))
        else:
            quiz_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=Colors.GRAY_400),
                    ft.Container(height=Spacing.SM),
                    ft.Text("No quizzes found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                    ft.Text(
                        "There are no available quizzes for your class at the moment." if not search_field.value else f"Your search for '{search_field.value}' did not match any quizzes in your class.",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        
        app_state.current_page.update()

    search_field.on_change = update_quiz_list

    def handle_start_quiz(quiz):
        def start_action(e):
            if quiz.get('password') is not None:
                password_field = create_text_input("Quiz Password", password=True, can_reveal=True)
                error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

                def check_password(e_dialog):
                    if password_field.value == quiz['password']:
                        password_dialog.open = False
                        app_state.current_page.update()
                        show_quiz_taking(quiz)
                    else:
                        error_text.value = "Incorrect password. Please try again."
                        password_field.value = ""
                        app_state.current_page.update()

                def close_dialog(e_dialog):
                    password_dialog.open = False
                    app_state.current_page.update()

                password_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Password Required"),
                    content=ft.Column([
                        ft.Text(f"This quiz '{quiz['title']}' is password protected."),
                        password_field,
                        error_text
                    ]),
                    actions=[
                        create_secondary_button("Cancel", on_click=close_dialog),
                        create_primary_button("Enter", on_click=check_password),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                app_state.current_page.dialog = password_dialog
                password_dialog.open = True
                app_state.current_page.update()
            else:
                show_quiz_taking(quiz)
        return start_action

    def create_quiz_card(quiz):
        quiz_card = create_card(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(
                            quiz['title'],
                            size=Typography.SIZE_LG,
                            weight=ft.FontWeight.W_600,
                            color=Colors.TEXT_PRIMARY
                        ),
                        ft.Text(
                            quiz['description'],
                            size=Typography.SIZE_SM,
                            color=Colors.TEXT_SECONDARY
                        )
                    ], expand=True),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCK, color=Colors.WARNING, size=16) if quiz.get('password') else ft.Container(),
                        ft.Container(width=Spacing.SM) if quiz.get('password') else ft.Container(),
                    ], alignment=ft.MainAxisAlignment.START)
                    
                ]),
                ft.Container(height=Spacing.SM),
                ft.Row([
                    ft.Text(
                        f"{quiz['questions_count']} questions",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Text(
                        f"Created by {quiz['creator']}",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Text(f"| Starts: {quiz.get('start_time', 'N/A')}", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(f"| {quiz.get('duration_minutes', 'N/A')} min", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Container(expand=True),
                    create_primary_button(
                        "Start Quiz", on_click=handle_start_quiz(quiz), width=120,
                        disabled=datetime.datetime.now() < datetime.datetime.strptime(quiz.get('start_time', '1970-01-01 00:00'), '%Y-%m-%d %H:%M')
                    )
                ])
            ]),
            padding=Spacing.XL
        )
        return quiz_card

    update_quiz_list()
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title(f"Welcome, {app_state.current_user['username']}!"),
                            create_subtitle("Choose a quiz to test your knowledge."),
                        ], spacing=Spacing.XS),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    ft.Row([create_section_title("Available Quizzes"), ft.Container(expand=True), search_field]),
                    ft.Container(height=Spacing.LG),
                    quiz_list_view
                ]),
                padding=Spacing.XXXXL,
                expand=True, bgcolor=Colors.GRAY_50)
        ]),
        expand=True
    )
    
    app_state.sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    app_state.current_page.drawer = app_state.sidebar_drawer
    app_state.current_page.appbar = create_app_bar()
    app_state.current_view_handler = show_examinee_dashboard

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True

    app_state.current_page.update()


def show_quiz_taking(quiz_basic_info):
    """Hiển thị giao diện làm bài thi"""
    app_state.current_page.clean()
    app_state.current_question_index = 0
    app_state.user_answers = {}
    app_state.quiz_start_time = datetime.datetime.now()
    app_state.quiz_timer_thread = None
    
    app_state.quiz_questions = mock_data.mock_questions.get(quiz_basic_info['id'], [])

    if quiz_basic_info.get('shuffle_questions', False):
        import random
        random.shuffle(app_state.quiz_questions)

    if not app_state.quiz_questions:
        show_examinee_dashboard()
        return
    
    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_text_display = ft.Text("", size=Typography.SIZE_XL, weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY)
    timer_text = ft.Text("", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.ERROR)
    
    def update_question_display():
        if app_state.current_question_index >= len(app_state.quiz_questions):
            return
        
        question = app_state.quiz_questions[app_state.current_question_index]
        question_counter_text.value = f"Question {app_state.current_question_index + 1} of {len(app_state.quiz_questions)}"
        question_text_display.value = question['question_text']
        
        shuffle_answers = quiz_basic_info.get('shuffle_answers', False)
        question_component = create_question_by_type(question, handle_answer_change, shuffle_answers)
        question_component_container.content = question_component # Gán trực tiếp vào container bên dưới
        
        prev_button.disabled = (app_state.current_question_index == 0)
        has_answer = question['id'] in app_state.user_answers
        next_button.disabled = not has_answer
        submit_button.visible = (app_state.current_question_index == len(app_state.quiz_questions) - 1 and has_answer)
        
        app_state.current_page.update()
    
    def handle_answer_change(question_id, answer):
        app_state.user_answers[question_id] = answer
        has_answer = answer is not None and answer != "" and answer != []
        next_button.disabled = not has_answer
        submit_button.visible = (app_state.current_question_index == len(app_state.quiz_questions) - 1 and has_answer)
        app_state.current_page.update()
    
    def handle_previous(e):
        if app_state.current_question_index > 0:
            app_state.current_question_index -= 1
            update_question_display()
    
    def handle_next(e):
        if app_state.current_question_index < len(app_state.quiz_questions) - 1:
            app_state.current_question_index += 1
            update_question_display()
    
    def handle_submit(e):
        if app_state.quiz_timer_thread:
            app_state.quiz_timer_thread.do_run = False
            app_state.quiz_timer_thread = None
        show_quiz_results(quiz_basic_info, app_state.user_answers, app_state.quiz_start_time)
    
    def exit_quiz(e):
        show_examinee_dashboard()
    
    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120, disabled=True)
    submit_button = create_primary_button("Submit Quiz", on_click=handle_submit, width=130)
    submit_button.visible = False
    
    progress_bar = ft.ProgressBar(
        width=400,
        color=Colors.PRIMARY,
        bgcolor=Colors.GRAY_200,
        value=0
    )
    
    def update_progress():
        progress = (app_state.current_question_index + 1) / len(app_state.quiz_questions)
        progress_bar.value = progress
        app_state.current_page.update()
    
    def run_timer():
        duration_minutes = quiz_basic_info.get('duration_minutes', 10)
        end_time = app_state.quiz_start_time + datetime.timedelta(minutes=duration_minutes)
        
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            remaining = end_time - datetime.datetime.now()
            if remaining.total_seconds() <= 0:
                timer_text.value = "00:00"
                app_state.current_page.update()
                app_state.current_page.run(handle_submit(None))
                break

            minutes, seconds = divmod(int(remaining.total_seconds()), 60)
            timer_text.value = f"{minutes:02d}:{seconds:02d}"
            app_state.current_page.update()
            time.sleep(1)

    app_state.quiz_timer_thread = threading.Thread(target=run_timer, daemon=True)
    app_state.quiz_timer_thread.start()

    question_component_container = ft.Container(content=ft.Column([]))

    quiz_content = ft.Container(
        content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            create_card(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(
                                quiz_basic_info['title'],
                                size=Typography.SIZE_2XL,
                                weight=ft.FontWeight.W_700,
                                color=Colors.TEXT_PRIMARY
                            ),
                            question_counter_text
                        ], expand=True, spacing=Spacing.XS),
                        ft.Icon(ft.Icons.TIMER, color=Colors.ERROR),
                        timer_text,
                        ft.Container(width=Spacing.XL),
                        create_secondary_button("Exit Quiz", on_click=exit_quiz, width=100)
                    ]),
                    ft.Container(height=Spacing.LG),
                    progress_bar
                ]),
                padding=Spacing.XL
            ),
            ft.Container(height=Spacing.XXL),
            create_card(
                content=ft.Column([
                    question_component_container
                ]),
                padding=Spacing.XXXXL
            ),
            ft.Container(height=Spacing.XXL),
            ft.Row([
                prev_button,
                ft.Container(expand=True),
                next_button,
                submit_button
            ])
        ]),
        padding=Spacing.XXXXL,
        expand=True,
        alignment=ft.alignment.top_center
    )
    
    update_question_display()
    update_progress()
    
    app_state.current_page.add(quiz_content)
    app_state.current_view_handler = None
    app_state.current_page.update()


def show_quiz_results(quiz_data, user_answers, start_time):
    """Hiển thị kết quả sau khi làm bài thi"""
    app_state.current_page.clean()
    
    quiz_questions = mock_data.mock_questions.get(quiz_data['id'], [])
    correct_count = 0
    total_questions = len(quiz_questions)
    
    for question in quiz_questions:
        question_id = question['id']
        if question_id in user_answers:
            user_answer = user_answers[question_id]
            question_type = question.get('question_type', 'multiple_choice')
            
            if question_type == 'multiple_choice':
                correct_option_text = next((opt['option_text'] for opt in question['options'] if opt['is_correct']), None)
                if correct_option_text and user_answer == correct_option_text:
                    correct_count += 1
            elif question_type == 'true_false':
                if user_answer == question.get('correct_answer'):
                    correct_count += 1
            elif question_type == 'fill_in_blank':
                correct_answer = question.get('correct_answer', '').lower().strip()
                answer_variations = question.get('answer_variations', [])
                user_answer_clean = str(user_answer).lower().strip()
                if user_answer_clean == correct_answer or user_answer_clean in answer_variations:
                    correct_count += 1
            elif question_type == 'multiple_select':
                if isinstance(user_answer, list):
                    correct_options_texts = {opt['option_text'] for opt in question['options'] if opt['is_correct']}
                    user_answers_texts = set(user_answer)
                    if user_answers_texts == correct_options_texts:
                        correct_count += 1
            elif question_type == 'short_answer':
                if user_answer and str(user_answer).strip():
                    correct_count += 0.5
    
    percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    end_time = datetime.datetime.now()
    time_taken = end_time - start_time
    time_minutes = int(time_taken.total_seconds() / 60)
    time_seconds = int(time_taken.total_seconds() % 60)
    
    if mock_data.mock_attempts:
        new_attempt_id = max(a['attempt_id'] for a in mock_data.mock_attempts) + 1
    else:
        new_attempt_id = 1

    new_attempt = {
        'attempt_id': new_attempt_id,
        'user_id': app_state.current_user['id'],
        'quiz_id': quiz_data['id'],
        'score': f"{correct_count}/{total_questions}",
        'percentage': percentage,
        'time_taken': f"{time_minutes:02d}:{time_seconds:02d}",
        'completed_at': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_answers': user_answers
    }
    mock_data.mock_attempts.append(new_attempt)

    results_content = ft.Container(
        content=ft.Column([
            create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.EMOJI_EVENTS, size=64, color=Colors.SUCCESS if percentage >= 70 else Colors.WARNING),
                    ft.Container(height=Spacing.LG),
                    ft.Text(
                        "Quiz Completed!",
                        size=Typography.SIZE_3XL,
                        weight=ft.FontWeight.W_700,
                        color=Colors.TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        quiz_data['title'],
                        size=Typography.SIZE_LG,
                        color=Colors.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ),
            ft.Container(height=Spacing.XXL),
            ft.Row([
                create_card(
                    content=ft.Column([
                        ft.Text("Score", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Text(
                            f"{correct_count}/{total_questions}",
                            size=Typography.SIZE_3XL,
                            weight=ft.FontWeight.W_700,
                            color=Colors.TEXT_PRIMARY
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=Spacing.XL
                ),
                create_card(
                    content=ft.Column([
                        ft.Text("Percentage", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Text(
                            f"{percentage:.1f}%",
                            size=Typography.SIZE_3XL,
                            weight=ft.FontWeight.W_700,
                            color=Colors.SUCCESS if percentage >= 70 else Colors.WARNING
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=Spacing.XL
                ),
                create_card(
                    content=ft.Column([
                        ft.Text("Time Taken", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Text(
                            f"{time_minutes:02d}:{time_seconds:02d}",
                            size=Typography.SIZE_3XL,
                            weight=ft.FontWeight.W_700,
                            color=Colors.TEXT_PRIMARY
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=Spacing.XL
                )
            ], spacing=Spacing.XL),
            ft.Container(height=Spacing.XXXXL),
            ft.Row([
                ft.Container(expand=True),
                create_secondary_button("Review Answers", on_click=lambda e, a=new_attempt: show_attempt_review(a), width=140),
                ft.Container(width=Spacing.LG),
                create_primary_button("Back to Dashboard", on_click=lambda e: show_examinee_dashboard(), width=160),
                ft.Container(expand=True)
            ])
        ]),
        padding=Spacing.XXXXL,
        expand=True,
        alignment=ft.alignment.top_center
    )
    
    app_state.current_page.add(results_content)
    app_state.current_view_handler = None
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
    """Hiển thị lại bài làm chi tiết của một lần thi"""
    app_state.current_page.clean()
    app_state.current_question_index = 0

    quiz_info = next((q for q in mock_data.mock_quizzes if q['id'] == attempt['quiz_id']), None)
    if not quiz_info:
        show_my_attempts()
        return

    app_state.quiz_questions = mock_data.mock_questions.get(quiz_info['id'], [])
    user_answers = attempt.get('user_answers', {})

    if not app_state.quiz_questions:
        show_my_attempts()
        return

    show_correct_answers = quiz_info.get('show_answers_after_quiz', False)

    if not show_correct_answers:
        notice_content = ft.Container(
            content=ft.Column([
                create_card(content=ft.Row([
                    ft.Icon(ft.Icons.LOCK, color=Colors.ERROR),
                    ft.Text("Bạn không được phép xem đáp án của bài quiz này.", size=Typography.SIZE_LG, color=Colors.ERROR, weight=ft.FontWeight.W_600),
                    ft.Container(expand=True),
                    create_secondary_button("Back to Attempts", on_click=lambda e: show_my_attempts(), width=150)
                ]), padding=Spacing.XXXXL)
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=Spacing.XXXXL,
            expand=True
        )
        app_state.current_page.add(notice_content)
        app_state.current_view_handler = None
        app_state.current_page.update()
        return

    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_component_container = ft.Container(content=ft.Column([]))

    def update_review_display():
        if app_state.current_question_index >= len(app_state.quiz_questions):
            return
        question = app_state.quiz_questions[app_state.current_question_index]
        user_answer = user_answers.get(question['id'])
        question_counter_text.value = f"Question {app_state.current_question_index + 1} of {len(app_state.quiz_questions)}"

        question_component = create_question_by_type(
            question, on_answer_change=None, is_review=True,
            user_answer=user_answer, show_correct_answers=True
        )
        question_component_container.content = question_component

        prev_button.disabled = (app_state.current_question_index == 0)
        next_button.disabled = (app_state.current_question_index == len(app_state.quiz_questions) - 1)
        app_state.current_page.update()

    def handle_previous(e):
        if app_state.current_question_index > 0:
            app_state.current_question_index -= 1
            update_review_display()

    def handle_next(e):
        if app_state.current_question_index < len(app_state.quiz_questions) - 1:
            app_state.current_question_index += 1
            update_review_display()

    def exit_review(e):
        show_my_attempts()

    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120)

    review_content = ft.Container(
        content=ft.Column([
            create_card(content=ft.Row([
                ft.Icon(ft.Icons.RATE_REVIEW, color=Colors.PRIMARY),
                ft.Text(f"Reviewing: {quiz_info['title']}", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                create_secondary_button("Back to Attempts", on_click=exit_review, width=150)
            ]), padding=Spacing.LG),
            ft.Container(height=Spacing.LG),
            create_card(content=question_component_container, padding=Spacing.XXXXL),
            ft.Container(height=Spacing.XL),
            ft.Row([prev_button, ft.Container(expand=True), question_counter_text, ft.Container(expand=True), next_button])
        ]), padding=Spacing.XXXXL, expand=True, alignment=ft.alignment.top_center)

    update_review_display()
    app_state.current_page.add(review_content)
    app_state.current_view_handler = None
    app_state.current_page.update()

def show_my_attempts():
    """Hiển thị lịch sử các lần làm bài của sinh viên"""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "attempts")

    user_attempts = [attempt for attempt in mock_data.mock_attempts if attempt['user_id'] == app_state.current_user['id']]
    user_attempts.sort(key=lambda x: x['completed_at'], reverse=True)

    attempt_cards = []
    if user_attempts:
        for attempt in user_attempts:
            quiz_info = next((q for q in mock_data.mock_quizzes if q['id'] == attempt['quiz_id']), None)
            if not quiz_info: continue

            percentage = attempt['percentage']
            score_color = Colors.SUCCESS if percentage >= 70 else (Colors.WARNING if percentage >= 40 else Colors.ERROR)

            attempt_card = create_card(
                content=ft.Row([
                    ft.Column([
                        ft.Text(quiz_info['title'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                        ft.Text(f"Completed on: {datetime.datetime.strptime(attempt['completed_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')}",
                                size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Container(height=Spacing.SM),
                        ft.Row([
                            ft.Icon(ft.Icons.TIMER, size=16, color=Colors.TEXT_MUTED),
                            ft.Text(f"Time: {attempt['time_taken']}", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                        ], spacing=Spacing.SM)
                    ], expand=True),
                    ft.VerticalDivider(color=Colors.GRAY_200),
                    ft.Container(width=Spacing.LG),
                    ft.Column([
                        ft.Text("Score", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Text(attempt['score'], size=Typography.SIZE_XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(width=Spacing.LG),
                    ft.Column([
                        ft.Text("Percentage", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                        ft.Text(f"{attempt['percentage']:.1f}%", size=Typography.SIZE_XL, weight=ft.FontWeight.W_700, color=score_color),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(width=Spacing.LG),
                    create_primary_button("Review", on_click=lambda e, a=attempt: show_attempt_review(a), width=100)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=Spacing.LG
            )
            attempt_cards.append(attempt_card)
    else:
        attempt_cards.append(create_card(
            content=ft.Column([
                ft.Icon(ft.Icons.HISTORY_EDU, size=48, color=Colors.GRAY_400),
                ft.Container(height=Spacing.SM),
                ft.Text("No Attempts Yet", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                ft.Text("Your completed quizzes will appear here.", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=Spacing.XXXXL
        ))

    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Attempts"),
                            create_subtitle("Here is a history of all the quizzes you have completed.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    ft.Column(attempt_cards, spacing=Spacing.LG)
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
    app_state.current_view_handler = show_my_attempts

    if app_state.current_page.width >= 1000:
        app_state.current_page.add(ft.Row([sidebar, main_content], expand=True))
        app_state.current_page.appbar.visible = False
    else:
        app_state.current_page.add(main_content)
        app_state.current_page.appbar.visible = True
    app_state.current_page.update()

def show_profile_page():
    """Hiển thị trang thông tin cá nhân và đổi mật khẩu cho sinh viên."""
    app_state.current_page.clean()
    sidebar = create_sidebar(app_state.current_user['role'], "profile")

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
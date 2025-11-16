# Modern Quiz App - Clean Light Theme UI
# Beautiful, modern design with clean components and navigation

import random
import flet as ft # Nạp thư viện Flet để xây dựng giao diện người dùng
import datetime
import time
import threading

# =============================================================================
# DESIGN SYSTEM CONSTANTS
# =============================================================================

# Colors - Light Theme Only
class Colors:
    # Primary blue palette màu chủ đạo
    PRIMARY = "#2563eb"
    PRIMARY_LIGHT = "#3b82f6" 
    PRIMARY_LIGHTER = "#60a5fa"
    PRIMARY_LIGHTEST = "#eff6ff"
    
    # Gray scale colors: màu xám dùng làm nền và viền
    WHITE = "#ffffff"
    GRAY_50 = "#f8fafc"
    GRAY_100 = "#f1f5f9"
    GRAY_200 = "#e2e8f0"
    GRAY_300 = "#cbd5e1"
    GRAY_400 = "#94a3b8"
    GRAY_500 = "#64748b"
    GRAY_600 = "#475569"
    GRAY_700 = "#334155"
    GRAY_800 = "#1e293b"
    GRAY_900 = "#0f172a"
    
    # Accent colors màu nhấn nếu báo lỗi hoặc thành công
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    # Màu chữ
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_MUTED = "#94a3b8"

# Spacing scale (4px base): khoảng cách giữa các thành phần
class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32
    XXXXL = 48
    XXXXXL = 64

# Typography: kích thước chữ
class Typography:
    SIZE_XS = 12
    SIZE_SM = 14
    SIZE_BASE = 16
    SIZE_LG = 18
    SIZE_XL = 20
    SIZE_2XL = 24
    SIZE_3XL = 32
    SIZE_4XL = 48

# Border radius scale: bo góc các thành phần
class BorderRadius:
    SM = 4
    MD = 8
    LG = 12
    XL = 16
    XXL = 24 # New larger radius for prominent elements

# =============================================================================
# GLOBAL STATE
# =============================================================================
# khởi tạo biến toàn cục để theo dõi trạng thái ứng dụng
current_view_handler = None # NEW: Stores the function to call to redraw the current view
current_user = None
current_page = None
sidebar_drawer = None

# Quiz taking state: trạng thái khi làm bài thi
current_question_index = 0
user_answers = {}
quiz_questions = []
quiz_start_time = None
quiz_timer_thread = None

# =============================================================================
# MOCK DATA
# =============================================================================

# mock_users: Từ điển chứa thông tin tài khoản người dùng mẫu
# Key là username (tên đăng nhập), chứa các thuộc tính:
# - id: ID duy nhất của user
# - username: tên đăng nhập
# - password: mật khẩu (trong thực tế sẽ được hash)
# - role: vai trò ('instructor', 'admin', 'examinee')
# Mục đích: Để test chức năng đăng nhập và phân quyền
mock_users = {
    'instructor': {'id': 1, 'username': 'instructor', 'password': 'instructor', 'role': 'instructor'},
    'admin': {'id': 2, 'username': 'admin', 'password': 'admin', 'role': 'admin'},
    'student': {'id': 3, 'username': 'student', 'password': 'student', 'role': 'examinee', 'class_id': 1},
    # dùng tải khoản sau để test nhiều người thi
    'THEHY': {'id': 4, 'username': 'THEHY', 'password': 'THEHY', 'role': 'examinee', 'class_id': 1},
    'TAI': {'id': 5, 'username': 'TAI', 'password': 'TAI', 'role': 'examinee', 'class_id': 2},
    'HUNG': {'id': 6, 'username': 'HUNG', 'password': 'HUNG', 'role': 'examinee', 'class_id': 2},
    'HUY': {'id': 7, 'username': 'HUY', 'password': 'HUY', 'role': 'examinee', 'class_id': None},
}

# mock_quizzes: List chứa các bài quiz mẫu
# Mỗi quiz sẽ chưa các thông tin (attribute):
# - id: ID duy nhất của quiz
# - title: tiêu đề quiz
# - description: mô tả quiz
# - created_by: ID của người tạo (liên kết với mock_users)
# - created_at: ngày tạo (string) 
# - creator: tên người tạo
# - questions_count: số câu hỏi trong quiz
# - start_time: thời gian bắt đầu (YYYY-MM-DD HH:MM)
# - duration_minutes: thời gian làm bài (phút)
# Mục đích: Để hiển thị danh sách quiz và quản lý quiz
mock_quizzes = [
    {'id': 1, 'title': 'Python Basics', 'description': 'Learn Python fundamentals', 'created_by': 1, 'created_at': '2024-01-15', 'creator': 'instructor', 'questions_count': 5, 'start_time': '2025-01-15 14:20', 'duration_minutes': 10, 'class_id': 1, 'password': '123', 'is_active': True, 'shuffle_questions': True, 'shuffle_answers': True},
    {'id': 2, 'title': 'Web Development', 'description': 'HTML, CSS, JavaScript basics', 'created_by': 1, 'created_at': '2024-01-14', 'creator': 'instructor', 'questions_count': 8, 'start_time': '2024-01-20 10:00', 'duration_minutes': 20, 'class_id': 2, 'password': None, 'is_active': True, 'shuffle_questions': False, 'shuffle_answers': True},
    {'id': 3, 'title': 'Data Structures', 'description': 'Arrays, Lists, Trees, Algorithms', 'created_by': 2, 'created_at': '2024-01-13', 'creator': 'admin', 'questions_count': 12, 'start_time': '2024-01-22 14:00', 'duration_minutes': 30, 'class_id': 1, 'password': 'dsa', 'is_active': False, 'shuffle_questions': True, 'shuffle_answers': False}
]

# mock_classes: List chứa thông tin các lớp học mẫu
# Mỗi class sẽ chứa :
# - id: ID duy nhất của lớp
# - name: tên lớp
# - instructor_id: ID của giảng viên dạy lớp (liên kết với mock_users)
# Mục đích: Để quản lý lớp học (tính năng admin)
mock_classes = [
    {'id': 1, 'name': 'Lớp K22', 'instructor_id': 1},
    {'id': 2, 'name': 'Lớp SE K23', 'instructor_id': 1},
]

# mock_questions: Từ điển chứa câu hỏi cho từng quiz
# Key là quiz_id (liên kết với mock_quizzes)
# Mỗi câu hỏi sẽ có các thuộc tính như:
# - id: ID duy nhất của câu hỏi
# - question_type: loại câu hỏi ('multiple_choice', 'true_false', 'fill_in_blank', 'multiple_select', 'short_answer')
# - question_text: nội dung câu hỏi
# - options: list các lựa chọn (cho multiple_choice và multiple_select)
# - correct_answer: đáp án đúng (cho true_false, fill_in_blank)
# - answer_variations: các biến thể đáp án (cho fill_in_blank)
# - sample_answer: mẫu đáp án (cho short_answer)
# Mục đích: Để lưu trữ và hiển thị câu hỏi trong quiz
mock_questions = {
    1: [  # Quiz ID 1 có 5 câu hỏi mẫu
        {
            'id': 1,
            'question_type': 'multiple_choice',  # Câu hỏi trắc nghiệm 4 lựa chọn
            'question_text': 'What is Python?',
            'difficulty': 'Easy',
            'options': [  # 4 lựa chọn, mỗi cái có text và is_correct
                {'option_text': 'A snake', 'is_correct': False},
                {'option_text': 'A programming language', 'is_correct': True},
                {'option_text': 'A movie', 'is_correct': False},
                {'option_text': 'A game', 'is_correct': False}
            ]
        },
        {
            'id': 2,
            'question_type': 'true_false', 
            'question_text': 'Python is an interpreted programming language.',
            'difficulty': 'Easy',
            'correct_answer': True  
        },
        {
            'id': 3,
            'question_type': 'fill_in_blank', 
            'question_text': 'Python was created by _______ in 1991.',
            'difficulty': 'Medium',
            'correct_answer': 'Guido van Rossum',  
            'answer_variations': ['guido van rossum', 'guido', 'van rossum']  
        },
        {
            'id': 4,
            'question_type': 'multiple_select',  
            'question_text': 'Which of the following are Python web frameworks? (Select all that apply)',
            'difficulty': 'Medium',
            'options': [
                {'option_text': 'Django', 'is_correct': True},
                {'option_text': 'Flask', 'is_correct': True},
                {'option_text': 'React', 'is_correct': False},  
                {'option_text': 'FastAPI', 'is_correct': True}
            ]
        },
        {
            'id': 5,
            'question_type': 'short_answer',  
            'question_text': 'Explain the difference between a list and a tuple in Python.',
            'difficulty': 'Hard',
            'sample_answer': 'Lists are mutable and use square brackets, while tuples are immutable and use parentheses.'  # Mẫu đáp án để tham khảo
        }
    ]
}

# mock_notifications: Từ điển chứa thông báo cho từng role
# Key là role ('instructor', 'admin', 'examinee')
# Mỗi thông báo sẽ có:
# - id: ID thông báo
# - text: nội dung thông báo
# - read: đã đọc hay chưa (boolean)
# - timestamp: thời gian (string)
# Mục đích: Để hiển thị thông báo trong header của app
mock_notifications = {
    'instructor': [
        {'id': 1, 'text': 'Student "THEHY" has completed the "Python Basics" quiz.', 'read': False, 'timestamp': '2 hours ago'},
        {'id': 2, 'text': 'A new version of the app is available.', 'read': True, 'timestamp': '1 day ago'},
    ],
    'admin': [
        {'id': 5, 'text': 'Instructor "instructor" created a new quiz "Web Development".', 'read': False, 'timestamp': '1 day ago'},
    ],
    'examinee': [
        {'id': 3, 'text': 'Your results for "Python Basics" are ready.', 'read': False, 'timestamp': '30 minutes ago'},
        {'id': 4, 'text': 'New quiz "Data Structures" has been added.', 'read': False, 'timestamp': '5 hours ago'},
    ],
}

# mock_activity_log: List chứa lịch sử hoạt động trên hệ thống
# Mục đích: Để admin theo dõi các sự kiện quan trọng
mock_activity_log = [
    {'timestamp': '2025-07-21 10:05', 'user': 'instructor', 'action': 'đã tạo một bài thi mới', 'details': 'Web Development'},
    {'timestamp': '2025-07-21 09:30', 'user': 'THEHY', 'action': 'đã hoàn thành bài thi', 'details': 'Python Basics'},
    {'timestamp': '2025-07-20 15:00', 'user': 'admin', 'action': 'đã tạo người dùng mới', 'details': 'HUNG'},
    {'timestamp': '2025-07-20 14:00', 'user': 'admin', 'action': 'đã tạo một lớp học mới', 'details': 'Lớp Phát triển Web K12'},
]

# mock_attempts: List chứa lịch sử làm bài của sinh viên
# Mục đích: Để sinh viên xem lại các lần làm bài của mình
mock_attempts = [
    {'attempt_id': 1, 'user_id': 3, 'quiz_id': 1, 'score': '4/5', 'percentage': 80.0, 'time_taken': '00:05:30', 'completed_at': '2025-07-21 11:00:00', 'user_answers': {1: 'A programming language', 2: True, 3: 'Guido van Rossum', 4: ['Django', 'Flask'], 5: 'Lists are mutable'}},
    {'attempt_id': 2, 'user_id': 4, 'quiz_id': 1, 'score': '3.5/5', 'percentage': 70.0, 'time_taken': '00:08:15', 'completed_at': '2025-07-21 11:05:00', 'user_answers': {1: 'A snake', 2: True, 3: 'guido', 4: ['Django', 'Flask', 'FastAPI'], 5: 'Lists are mutable and use square brackets, while tuples are immutable and use parentheses.'}},
    {'attempt_id': 3, 'user_id': 4, 'quiz_id': 2, 'score': '7/8', 'percentage': 87.5, 'time_taken': '00:15:45', 'completed_at': '2025-07-22 14:30:00', 'user_answers': {}},
]

# =============================================================================
# COMPONENT HELPER FUNCTIONS
# =============================================================================

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
        current_page.update()

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

def create_app_header():
    """Create the main application header with user info"""
    if not current_user:
        return ft.Container()

    user_role = current_user.get('role')
    notifications = mock_notifications.get(user_role, [])
    unread_count = sum(1 for n in notifications if not n['read'])

    def mark_as_read(notification):
        def on_click(e):
            notification['read'] = True
            # In a real app, you would update the backend here
            # For this demo, we just need to refresh the header state
            current_page.controls[0].content.controls[0].controls[0] = create_app_header()
            current_page.update()
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
            # Left side can have breadcrumbs or search in the future
            ft.Container(expand=True),

            # Right side with user info
            ft.Row([
                notification_button,
                ft.VerticalDivider(width=1, color=Colors.GRAY_200),
                ft.Column([
                    ft.Text(
                        current_user.get('username', "User"),
                        size=Typography.SIZE_SM,
                        weight=ft.FontWeight.W_600,
                        color=Colors.TEXT_PRIMARY
                    ),
                    ft.Text(
                        current_user.get('role', "Role").title(),
                        size=Typography.SIZE_XS,
                        color=Colors.TEXT_SECONDARY
                    )
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(width=Spacing.MD),
                ft.CircleAvatar(
                    content=ft.Text(current_user['username'][0].upper(), color=Colors.WHITE, weight=ft.FontWeight.W_600),
                    bgcolor=Colors.PRIMARY,
                    radius=20
                ),
            ], spacing=Spacing.MD)
        ]),
        padding=ft.padding.symmetric(horizontal=Spacing.XXL, vertical=Spacing.MD),
        border=ft.border.only(bottom=ft.BorderSide(width=1, color=Colors.GRAY_200))
    )
# =============================================================================
# QUESTION TYPE COMPONENTS
# =============================================================================

def create_multiple_choice_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None):
    """Create a multiple choice question component"""
    options_group = ft.RadioGroup(content=ft.Column([]))
    
    options_data = question.get('options', [])
    
    # Xáo trộn đáp án nếu được yêu cầu
    if shuffle_answers:
        random.shuffle(options_data)

    # Create radio options
    options = []
    for i, option in enumerate(options_data):
        # Lưu trữ ID gốc của option (hoặc text) để xác định câu trả lời đúng
        # Ở đây ta dùng chính text của option
        option_text = option['option_text']
        is_correct = option['is_correct']
        
        radio = ft.Radio(
            value=option_text,
            label=option_text,
            label_style=ft.TextStyle(size=Typography.SIZE_BASE)
        )

        if is_review:
            radio.disabled = True
            radio.value = user_answer

            # Hiển thị icon và màu sắc cho chế độ review
            review_indicator = ft.Container(width=24) # Placeholder
            if is_correct:
                # Đây là đáp án đúng
                radio.label_style.color = Colors.SUCCESS
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CHECK_CIRCLE, color=Colors.SUCCESS, size=20)
            elif option_text == user_answer:
                # Đây là đáp án sai mà người dùng đã chọn
                radio.label_style.color = Colors.ERROR
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CANCEL, color=Colors.ERROR, size=20)
            
            options.append(ft.Row([review_indicator, radio], spacing=Spacing.SM))
        else:
            options.append(radio)

    options_group.content = ft.Column(options, spacing=Spacing.MD)

    if not is_review:
        options_group.on_change = lambda e: on_answer_change(e, e.control.value)
    else:
        options_group.value = user_answer

    # Thêm phần giải thích nếu có (cho chế độ review)
    explanation_content = []
    if is_review and question.get('explanation'):
        explanation_content.append(ft.Container(height=Spacing.LG))
        explanation_content.append(create_card(content=ft.Text(f"Explanation: {question['explanation']}", color=Colors.TEXT_SECONDARY), elevation=0, padding=Spacing.LG))

    return ft.Column([
        ft.Text(
            question['question_text'],
            size=Typography.SIZE_XL,
            weight=ft.FontWeight.W_600,
            color=Colors.TEXT_PRIMARY
        ),
        ft.Container(height=Spacing.XL),
        options_group,
        *explanation_content
    ])

def create_true_false_question(question, on_answer_change, is_review=False, user_answer=None):
    """Create a true/false question component"""
    true_false_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="true", label="True", label_style=ft.TextStyle(size=Typography.SIZE_BASE)),
            ft.Radio(value="false", label="False", label_style=ft.TextStyle(size=Typography.SIZE_BASE))
        ], spacing=Spacing.MD)
    )

    if is_review:
        true_false_group.disabled = True
        true_false_group.value = str(user_answer).lower()
        correct_answer = question.get('correct_answer')

        for radio in true_false_group.content.controls:
            is_this_option_correct = (radio.value == "true") == correct_answer
            is_this_option_selected = (radio.value == "true") == user_answer

            review_indicator = ft.Container(width=24)
            if is_this_option_correct:
                radio.label_style.color = Colors.SUCCESS
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CHECK_CIRCLE, color=Colors.SUCCESS, size=20)
            elif is_this_option_selected:
                radio.label_style.color = Colors.ERROR
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CANCEL, color=Colors.ERROR, size=20)
            
            # Wrap in a Row to show indicator
            radio.label = ft.Row([review_indicator, ft.Text(radio.label)], spacing=Spacing.SM)

    else:
        true_false_group.on_change = lambda e: on_answer_change(e, e.control.value == "true")
    
    explanation_content = []
    if is_review and question.get('explanation'):
        explanation_content.append(ft.Container(height=Spacing.LG))
        explanation_content.append(create_card(content=ft.Text(f"Explanation: {question['explanation']}", color=Colors.TEXT_SECONDARY), elevation=0, padding=Spacing.LG))

    return ft.Column([
        ft.Text(
            question['question_text'],
            size=Typography.SIZE_XL,
            weight=ft.FontWeight.W_600,
            color=Colors.TEXT_PRIMARY
        ),
        ft.Container(height=Spacing.XL),
        true_false_group,
        *explanation_content
    ])

def create_fill_in_blank_question(question, on_answer_change, is_review=False, user_answer=None):
    """Create a fill-in-the-blank question component"""
    answer_field = create_text_input("Your answer", width=400)
    
    review_content = []
    if is_review:
        answer_field.value = user_answer
        answer_field.disabled = True
        
        correct_answer = question.get('correct_answer', '').lower().strip()
        answer_variations = question.get('answer_variations', [])
        user_answer_clean = str(user_answer).lower().strip()
        is_correct = user_answer_clean == correct_answer or user_answer_clean in answer_variations

        answer_field.border_color = Colors.SUCCESS if is_correct else Colors.ERROR
        review_content.append(ft.Container(height=Spacing.SM))
        review_content.append(
            ft.Text(f"Correct Answer: {question.get('correct_answer')}", color=Colors.SUCCESS, weight=ft.FontWeight.W_600)
        )

    else:
        answer_field.on_change = lambda e: on_answer_change(e, e.control.value)
    

    return ft.Column([
        ft.Text(
            question['question_text'],
            size=Typography.SIZE_XL,
            weight=ft.FontWeight.W_600,
            color=Colors.TEXT_PRIMARY
        ),
        ft.Container(height=Spacing.XL),
        answer_field,
        *review_content
    ])

def create_multiple_select_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None):
    """Create a multiple select question component"""
    checkboxes = []
    options_data = question.get('options', [])

    # Xáo trộn đáp án nếu được yêu cầu
    if shuffle_answers:
        random.shuffle(options_data)
    
    for i, option in enumerate(options_data):
        option_text = option['option_text']
        is_correct = option['is_correct']

        checkbox = ft.Checkbox(
            label=option_text,
            data=option_text,
            value=False,
            label_style=ft.TextStyle(size=Typography.SIZE_BASE),
        )

        if is_review:
            checkbox.disabled = True
            user_answer_set = set(user_answer or [])
            checkbox.value = option_text in user_answer_set

            review_indicator = ft.Container(width=24)
            if is_correct:
                checkbox.label_style.color = Colors.SUCCESS
                checkbox.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=Colors.SUCCESS, size=20)
            elif option_text in user_answer_set: # Incorrectly selected
                checkbox.label_style.color = Colors.ERROR
                review_indicator = ft.Icon(ft.Icons.CANCEL_OUTLINED, color=Colors.ERROR, size=20)

            checkboxes.append(ft.Row([review_indicator, checkbox], spacing=Spacing.SM))
        else:
            checkboxes.append(checkbox)

    if not is_review:
        def on_checkbox_change(e):
            selected = [cb.data for cb in checkboxes if cb.value]
            on_answer_change(e, selected)
        
        for cb in checkboxes:
            cb.on_change = on_checkbox_change

    explanation_content = []
    if is_review:
        correct_options_texts = {opt['option_text'] for opt in question['options'] if opt['is_correct']}
        explanation_content.append(ft.Container(height=Spacing.LG))
        explanation_content.append(
            ft.Text(f"Correct Answer(s): {', '.join(correct_options_texts)}", color=Colors.SUCCESS, weight=ft.FontWeight.W_600)
        )
        if question.get('explanation'):
            explanation_content.append(ft.Container(height=Spacing.SM))
            explanation_content.append(
                create_card(content=ft.Text(f"Explanation: {question['explanation']}", color=Colors.TEXT_SECONDARY), elevation=0, padding=Spacing.LG)
            )


    return ft.Column([
        ft.Text(
            question['question_text'],
            size=Typography.SIZE_XL,
            weight=ft.FontWeight.W_600,
            color=Colors.TEXT_PRIMARY
        ),
        ft.Container(height=Spacing.XL),
        ft.Column(checkboxes, spacing=Spacing.MD),
        *explanation_content
    ])

def create_short_answer_question(question, on_answer_change, is_review=False, user_answer=None):
    """Create a short answer question component"""
    answer_field = create_text_input("Your answer", width=500, multiline=True, min_lines=4)
    
    review_content = []
    if is_review:
        answer_field.value = user_answer
        answer_field.disabled = True
        answer_field.label = "Your Answer"

        # Short answer questions are manually graded, so we just show the sample answer
        if question.get('sample_answer'):
            review_content.append(ft.Container(height=Spacing.LG))
            review_content.append(
                create_card(
                    content=ft.Column([
                        ft.Text("Sample Answer for Grading", weight=ft.FontWeight.W_600, color=Colors.PRIMARY),
                        ft.Text(question['sample_answer'], color=Colors.TEXT_SECONDARY)
                    ]), elevation=0, padding=Spacing.LG)
            )
    else:
        answer_field.on_change = lambda e: on_answer_change(e, e.control.value)

    return ft.Column([
        ft.Text(
            question['question_text'],
            size=Typography.SIZE_XL,
            weight=ft.FontWeight.W_600,
            color=Colors.TEXT_PRIMARY
        ),
        ft.Container(height=Spacing.XL),
        answer_field,
        *review_content
    ])

def create_question_by_type(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None):
    """Create question component based on question type"""
    question_type = question.get('question_type', 'multiple_choice')
    
    # In review mode, on_answer_change is a dummy function
    answer_handler = (lambda e, answer_value: on_answer_change(question['id'], answer_value)) if not is_review else (lambda e, v: None)

    # Chỉ truyền cờ shuffle_answers cho các loại câu hỏi có lựa chọn
    if question_type == 'multiple_choice':
        return create_multiple_choice_question(question, answer_handler, shuffle_answers, is_review, user_answer)
    elif question_type == 'true_false':
        return create_true_false_question(question, answer_handler, is_review, user_answer)
    elif question_type == 'fill_in_blank':
        return create_fill_in_blank_question(question, answer_handler, is_review, user_answer)
    elif question_type == 'multiple_select':
        return create_multiple_select_question(question, answer_handler, shuffle_answers, is_review, user_answer)
    elif question_type == 'short_answer':
        return create_short_answer_question(question, answer_handler, is_review, user_answer)
    else:
        return create_multiple_choice_question(question, answer_handler, shuffle_answers, is_review, user_answer)

# =============================================================================
# NAVIGATION COMPONENTS
# =============================================================================

def create_sidebar_item(icon, text, is_active=False, on_click=None):
    """Create a sidebar navigation item"""
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
    """Create the sidebar navigation"""
    sidebar_items = []
    
    if user_role in ['instructor', 'admin']:
        sidebar_items.append(create_sidebar_item(ft.Icons.HOME, "Home", active_page == "dashboard", on_click=lambda e: show_instructor_dashboard()))
        
        if user_role == 'instructor':
            sidebar_items.append(create_sidebar_item(ft.Icons.QUIZ, "Quiz Management", active_page == "quizzes", on_click=lambda e: show_quiz_management()))
            sidebar_items.append(create_sidebar_item(ft.Icons.EMOJI_EVENTS, "View Results", active_page == "results", on_click=lambda e: show_results_overview()))

        if user_role == 'admin':
            sidebar_items.append(create_sidebar_item(ft.Icons.SCHOOL, "Classes Management", active_page == "classes", on_click=lambda e: show_class_management()))
            sidebar_items.append(create_sidebar_item(ft.Icons.PEOPLE, "User Management", active_page == "users", on_click=lambda e: show_user_management()))
        sidebar_items.extend([
            create_sidebar_item(ft.Icons.SETTINGS, "Settings", active_page == "settings", on_click=lambda e: show_settings_page()),
        ])
    else:  # examinee
        sidebar_items = [
            create_sidebar_item(ft.Icons.HOME, "Home", active_page == "home", on_click=lambda e: show_examinee_dashboard()),
            create_sidebar_item(ft.Icons.LIBRARY_BOOKS, "My Attempts", active_page == "attempts", on_click=lambda e: show_my_attempts()),
            create_sidebar_item(ft.Icons.EMOJI_EVENTS, "Results", active_page == "results", on_click=lambda e: show_student_results_overview()),
            create_sidebar_item(ft.Icons.PERSON, "Profile", active_page == "profile", on_click=lambda e: show_profile_page()),
        ]
    
    # Add logout item
    sidebar_items.append(ft.Divider(color=Colors.GRAY_200))
    sidebar_items.append(
        create_sidebar_item(ft.Icons.LOGOUT, "Logout", on_click=handle_logout)
    )
    
    return ft.Container(
        content=ft.Column([
            # Logo/Brand section
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
            
            # Navigation items
            ft.Container(
                content=ft.Column(sidebar_items, spacing=Spacing.XS),
                expand=True,
                padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.LG)
            ),
            
            # Support info section
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUPPORT_AGENT, color=Colors.TEXT_SECONDARY, size=24),
                    ft.Column([
                        ft.Text(
                            "Hỗ trợ kỹ thuật",
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
        # --- Thêm hiệu ứng đổ bóng cho sidebar ---
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(4, 0),
        ),
        clip_behavior=ft.ClipBehavior.NONE # Cho phép bóng hiển thị bên ngoài container
    )

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def handle_logout(e=None):
    """Handle user logout"""
    global current_user
    current_user = None
    show_login()

def open_drawer(e):
    """Open the navigation drawer"""
    if sidebar_drawer:
        sidebar_drawer.open = True
        sidebar_drawer.update()

def create_app_bar():
    """Create a responsive app bar with a menu button"""
    return ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer, tooltip="Menu"),
        leading_width=40
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

# =============================================================================
# PAGE FUNCTIONS
# =============================================================================

def show_login():
    """Show the modern login page"""
    global current_page
    global current_view_handler
    current_page.clean()
    current_page.appbar = None
    
    # Form fields
    username_field = create_text_input("Username", width=400, icon=ft.Icons.PERSON)
    password_field = create_text_input("Password", password=True, width=400, icon=ft.Icons.PASSWORD)
    error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    def handle_login_click(e):
        global current_user
        
        username = username_field.value or ""
        password = password_field.value or ""
        
        # Validation
        if not username.strip() or not password.strip():
            error_text.value = "Please enter both username and password"
            current_page.update()
            return
        
        # Check credentials
        user = mock_users.get(username.strip())
        if not user or user['password'] != password:
            error_text.value = "Invalid username or password"
            password_field.value = ""
            current_page.update()
            return
        
        # Login successful
        current_user = user
        error_text.value = ""
        
        # Route to appropriate dashboard
        if user['role'] in ['instructor', 'admin']:
            show_instructor_dashboard()
        else:
            show_examinee_dashboard()
    
    # Login form
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
                    # on_click=... # Sẽ thêm hành động xử lý sau
                ),
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(top=Spacing.SM),
                width=400, # Đảm bảo chiều rộng bằng với ô nhập liệu
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
    login_form.width = 900  # Điều chỉnh chiều rộng của form
    login_form.color = ft.Colors.TRANSPARENT  # Make the card background transparent
    login_form.elevation = 20
    login_form.height = 660 # Điều chỉnh chiều cao của form
    login_form.shape = ft.RoundedRectangleBorder(radius=BorderRadius.XXL) # Tăng độ bo góc cho Card

    # --- Tạo hiệu ứng nền kính trong suốt (Glassmorphism) ---
    # 1. Đặt gradient cho nền, đảo ngược so với nền chính và áp dụng độ mờ
    login_form.content.gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[
            ft.Colors.with_opacity(0.5, Colors.PRIMARY_LIGHTER),
            ft.Colors.with_opacity(0.6, Colors.GRAY_100),
            ft.Colors.with_opacity(0.7, Colors.PRIMARY_LIGHTEST),
        ]
    )
    # Xóa bgcolor để gradient có hiệu lực
    login_form.content.bgcolor = None
    # 2. Thêm hiệu ứng làm mờ (blur)
    login_form.content.blur = ft.Blur(20, 20, ft.BlurTileMode.MIRROR) # Điều chỉnh giá trị blur hợp lý
    # 3. Thêm viền mỏng để tạo cảm giác "kính"
    login_form.content.border = ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.WHITE)) # Giữ nguyên viền
    login_form.content.border_radius = BorderRadius.XXL # Đồng bộ độ bo góc của content với Card

    # The main content for the login page
    login_content = ft.Column(
        [login_form],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Wrap the content with the new background
    login_container = create_app_background(login_content)
    current_page.add(login_container)
    current_view_handler = show_login # Set the current view handler
    current_page.update()

def show_instructor_dashboard():
    """Show the instructor/admin dashboard"""
    global current_page
    global sidebar_drawer
    global current_view_handler
    current_page.clean()
    
    # Create main layout with sidebar
    sidebar = create_sidebar(current_user['role'], "dashboard")
    
    # --- Helper function to create an activity log item ---
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


    # --- Dashboard content based on user role ---
    stats_cards_list = []
    if current_user['role'] == 'admin':
        # Admin stats: Total classes, total users, total students
        stats_cards_list.extend([
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SCHOOL, color=Colors.PRIMARY), ft.Text("Tổng số lớp học", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_classes)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.PEOPLE_OUTLINE, color=Colors.SUCCESS), ft.Text("Tổng số người dùng", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len(mock_users)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            ),
            create_card(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.FACE, color=Colors.WARNING), ft.Text("Tổng số sinh viên", color=Colors.TEXT_SECONDARY)]),
                    ft.Text(str(len([u for u in mock_users.values() if u['role'] == 'examinee'])), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700, color=Colors.TEXT_PRIMARY)
                ], spacing=Spacing.SM),
                padding=Spacing.XL
            )
        ])
    else: # instructor
        # Instructor stats: Total quizzes, total questions, active students
        stats_cards_list.extend([
            create_card(
                content=ft.Column([
                    ft.Row([
                        ft.Image(src="assets/logo.png", width=24, height=24),
                        ft.Text("Total Quizzes", color=Colors.TEXT_SECONDARY)
                    ]),
                    ft.Text(
                        str(len([q for q in mock_quizzes if q['created_by'] == current_user['id']])),
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
                        str(sum(len(mock_questions.get(q['id'], [])) for q in mock_quizzes if q['created_by'] == current_user['id'])),
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
    
    # Main content
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Container(
                        content=ft.Column([
                            create_page_title(f"Chào mừng trở lại, {current_user['username']}!"),
                            create_subtitle("Đây là tổng quan về các hoạt động trên hệ thống.") if current_user['role'] == 'admin' else create_subtitle("Here's what's happening with your quizzes today.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    
                    # Stats cards
                    stats_cards,
                    ft.Container(height=Spacing.XXXXL),
                    
                    # --- Role-specific content ---
                    ft.Column([
                        # --- ADMIN: Activity History ---
                        ft.Column([
                            create_section_title("Lịch sử hoạt động"),
                            ft.Container(height=Spacing.LG),
                            create_card(
                                content=ft.Column([create_activity_item(log) for log in mock_activity_log]),
                                padding=ft.padding.symmetric(horizontal=Spacing.XL)
                            )
                        ]) if current_user['role'] == 'admin' else
                        
                        # --- INSTRUCTOR: Recent Quizzes ---
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
                                    ) for quiz in [q for q in mock_quizzes if q['created_by'] == current_user['id']][:3]
                                ],
                                spacing=Spacing.LG
                            ) if any(q for q in mock_quizzes if q['created_by'] == current_user['id']) else ft.Container(
                                content=ft.Text("No quizzes created yet. Create your first quiz to get started!", color=Colors.TEXT_MUTED),
                                padding=Spacing.XL
                            ),
                            ft.Container(height=Spacing.XL),
                            
                            # --- INSTRUCTOR: My Assigned Classes ---
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
                                    ) for cls in [c for c in mock_classes if c['instructor_id'] == current_user['id']]
                                ],
                                spacing=Spacing.LG
                            ) if any(c for c in mock_classes if c['instructor_id'] == current_user['id']) else ft.Container(
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
    
    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_instructor_dashboard # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_quiz_management():
    """Show the quiz management page"""
    global current_page
    global sidebar_drawer
    global current_view_handler
    current_page.clean()
    
    sidebar = create_sidebar(current_user['role'], "quizzes")
    
    # --- Search and Filter Logic ---
    search_field = create_text_input("Search by quiz title...", width=300, icon=ft.Icons.SEARCH)

    # --- Bộ lọc theo Lớp học ---
    instructor_classes = [c for c in mock_classes if c['instructor_id'] == current_user['id']]
    class_filter_options = [ft.dropdown.Option(key="all", text="Tất cả các lớp")]
    class_filter_options.extend([ft.dropdown.Option(key=str(cls['id']), text=cls['name']) for cls in instructor_classes])
    
    class_filter_dropdown = ft.Dropdown(
        label="Lọc theo lớp",
        width=220,
        value="all",
        options=class_filter_options,
    )

    # --- Bộ lọc theo Trạng thái ---
    status_filter_dropdown = ft.Dropdown(
        label="Lọc theo trạng thái",
        width=180,
        value="all",
        options=[
            ft.dropdown.Option(key="all", text="Tất cả trạng thái"),
            ft.dropdown.Option(key="active", text="Active"),
            ft.dropdown.Option(key="disabled", text="Disabled"),
        ],
    )

    # --- Bộ lọc theo Xáo trộn ---
    shuffle_filter_dropdown = ft.Dropdown(
        label="Lọc theo xáo trộn",
        width=200,
        value="all",
        options=[
            ft.dropdown.Option(key="all", text="Tất cả (Xáo trộn)"),
            ft.dropdown.Option(key="questions", text="Chỉ xáo trộn câu hỏi"),
            ft.dropdown.Option(key="answers", text="Chỉ xáo trộn đáp án"),
            ft.dropdown.Option(key="both", text="Xáo trộn cả hai"),
            ft.dropdown.Option(key="none", text="Không xáo trộn"),
        ],
    )

    quiz_list_view = ft.Column(spacing=Spacing.LG)

    def handle_delete_quiz(quiz_to_delete):
        def on_delete(e):
            global mock_quizzes, mock_questions
            mock_quizzes = [q for q in mock_quizzes if q['id'] != quiz_to_delete['id']]
            if quiz_to_delete['id'] in mock_questions:
                del mock_questions[quiz_to_delete['id']]
            
            show_quiz_management()
        return on_delete

    def update_quiz_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        selected_class_id = class_filter_dropdown.value
        selected_status = status_filter_dropdown.value
        selected_shuffle = shuffle_filter_dropdown.value
        
        # Filter quizzes based on current user and search term
        user_quizzes = [q for q in mock_quizzes if q['created_by'] == current_user['id']]
        filtered_quizzes = [
            q for q in user_quizzes if search_term in q['title'].lower()
        ]

        # Apply class filter
        if selected_class_id and selected_class_id != "all":
            filtered_quizzes = [q for q in filtered_quizzes if str(q.get('class_id')) == selected_class_id]

        # Apply status filter
        if selected_status and selected_status != "all":
            is_active = (selected_status == "active")
            filtered_quizzes = [q for q in filtered_quizzes if q.get('is_active', False) == is_active]

        # Apply shuffle filter
        if selected_shuffle and selected_shuffle != "all":
            if selected_shuffle == "questions":
                filtered_quizzes = [q for q in filtered_quizzes if q.get('shuffle_questions') and not q.get('shuffle_answers')]
            elif selected_shuffle == "answers":
                filtered_quizzes = [q for q in filtered_quizzes if not q.get('shuffle_questions') and q.get('shuffle_answers')]
            elif selected_shuffle == "both":
                filtered_quizzes = [q for q in filtered_quizzes if q.get('shuffle_questions') and q.get('shuffle_answers')]
            elif selected_shuffle == "none":
                filtered_quizzes = [q for q in filtered_quizzes if not q.get('shuffle_questions') and not q.get('shuffle_answers')]



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
                    ft.Text(f"Your search for '{search_field.value}' did not match any quizzes.", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        
        current_page.update()

    search_field.on_change = update_quiz_list
    class_filter_dropdown.on_change = update_quiz_list
    status_filter_dropdown.on_change = update_quiz_list
    shuffle_filter_dropdown.on_change = update_quiz_list

    # Quiz creation form (initially hidden)
    quiz_title_field = create_text_input("Quiz Title", width=400)
    quiz_description_field = create_text_input("Description", width=400, multiline=True, min_lines=3)
    quiz_start_time_field = create_text_input("Start Time (YYYY-MM-DD HH:MM)", width=250, icon=ft.Icons.CALENDAR_MONTH)
    quiz_duration_field = create_text_input("Duration (minutes)", width=140, icon=ft.Icons.TIMER)
    quiz_password_field = create_text_input("Quiz Password (optional)", password=True, width=400, icon=ft.Icons.LOCK, can_reveal=True)
    
    shuffle_questions_switch = ft.Switch(label="Xáo trộn câu hỏi", value=False)
    shuffle_answers_switch = ft.Switch(label="Xáo trộn đáp án", value=True)

    # Lấy danh sách các lớp mà giảng viên hiện tại được phân công
    instructor_classes = [c for c in mock_classes if c['instructor_id'] == current_user['id']]
    class_dropdown = ft.Dropdown(
        label="Select Class for this Quiz",
        width=400,
        border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300,
        focused_border_color=Colors.PRIMARY,
        options=[
            ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in instructor_classes
        ]
    )

    quiz_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    def show_create_form(e):
        quiz_form_container.visible = True
        quiz_title_field.value = ""
        quiz_description_field.value = ""
        quiz_error_text.value = ""
        quiz_start_time_field.value = ""
        quiz_duration_field.value = ""
        quiz_password_field.value = ""
        class_dropdown.value = None
        shuffle_questions_switch.value = False
        shuffle_answers_switch.value = True
        current_page.update()
    
    def hide_create_form(e):
        quiz_form_container.visible = False
        current_page.update()
    
    def handle_create_quiz(e):
        title = quiz_title_field.value or ""
        description = quiz_description_field.value or ""
        start_time_str = quiz_start_time_field.value or ""
        duration_str = quiz_duration_field.value or ""
        password = quiz_password_field.value or None
        class_id = class_dropdown.value
        shuffle_questions = shuffle_questions_switch.value
        shuffle_answers = shuffle_answers_switch.value
        
        if not title.strip():
            quiz_error_text.value = "Quiz title is required"
            current_page.update()
            return
        
        if not class_id:
            quiz_error_text.value = "Please select a class for the quiz"
            current_page.update()
            return

        try:
            datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            quiz_error_text.value = "Invalid start time format. Use YYYY-MM-DD HH:MM"
            current_page.update()
            return

        if not duration_str.isdigit() or int(duration_str) <= 0:
            quiz_error_text.value = "Duration must be a positive number of minutes"
            current_page.update()
            return
        
        duration_minutes = int(duration_str)

        
        # Add to mock data
        if mock_quizzes:
            new_id = max(q['id'] for q in mock_quizzes) + 1
        else:
            new_id = 1
        new_quiz = {
            'id': new_id,
            'title': title.strip(),
            'description': description.strip(),
            'created_by': current_user['id'],
            'created_at': '2025-01-15',
            'creator': current_user['username'],
            'questions_count': 0,
            'start_time': start_time_str.strip(),
            'duration_minutes': duration_minutes,
            'class_id': int(class_id),
            'password': password.strip() if password else None,
            'is_active': True, # Bài thi mới tạo mặc định được kích hoạt
            'shuffle_questions': shuffle_questions,
            'shuffle_answers': shuffle_answers
        }
        mock_quizzes.append(new_quiz)
        
        quiz_error_text.value = ""
        hide_create_form(e)
        show_quiz_management()  # Refresh the page
    
    def edit_quiz(quiz):
        return lambda e: show_question_management(quiz)
    
    quiz_form_container = create_card( # Quiz creation form
        content=ft.Column([
            create_section_title("Create New Quiz"),
            ft.Container(height=Spacing.LG),
            quiz_title_field,
            ft.Container(height=Spacing.LG),
            quiz_description_field,
            ft.Container(height=Spacing.LG),
            class_dropdown,
            ft.Container(height=Spacing.LG),
            ft.Row([
                quiz_start_time_field,
                quiz_duration_field
            ], spacing=Spacing.MD),
            ft.Container(height=Spacing.LG),
            quiz_password_field,
            ft.Container(height=Spacing.LG),
            ft.Row([
                shuffle_questions_switch,
                shuffle_answers_switch
            ], spacing=Spacing.XL),
            ft.Container(height=Spacing.MD),
            quiz_error_text,
            ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Create Quiz", on_click=handle_create_quiz, width=120),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Cancel", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    quiz_form_container.visible = False
    
    # --- Function to create a single quiz card ---
    def create_quiz_card(quiz):
        class_name = next((c['name'] for c in mock_classes if c['id'] == quiz.get('class_id')), "Unassigned")

        shuffle_info = []
        if quiz.get('shuffle_questions'): shuffle_info.append("Câu hỏi")
        if quiz.get('shuffle_answers'): shuffle_info.append("Đáp án")

        def toggle_active_state(e):
            # Tìm bài thi trong mock_quizzes và cập nhật trạng thái
            for q in mock_quizzes:
                if q['id'] == quiz['id']:
                    q['is_active'] = e.control.value
                    break
            show_quiz_management() # Tải lại trang để cập nhật giao diện

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
                            quiz['description'] or "No description",
                            size=Typography.SIZE_SM,
                            color=Colors.TEXT_SECONDARY
                        )
                    ], expand=True, spacing=Spacing.XS),
                    ft.Column([
                        create_badge(
                            f"Xáo trộn: {', '.join(shuffle_info) if shuffle_info else 'Không'}", 
                            color=Colors.PRIMARY_LIGHT
                        ) if 'shuffle_questions' in quiz else ft.Container(),
                        ft.Row([
                            create_badge(
                                "Active" if quiz.get('is_active', False) else "Disabled",
                                color=Colors.SUCCESS if quiz.get('is_active', False) else Colors.GRAY_400
                            ),
                            create_badge(class_name, color=Colors.WARNING),
                        ], spacing=Spacing.SM),
                        ft.Container(height=Spacing.XS),
                        ft.Switch(
                            value=quiz.get('is_active', False), 
                            on_change=toggle_active_state, 
                            label="Active", 
                            label_position=ft.LabelPosition.LEFT
                        ),
                    ], alignment=ft.CrossAxisAlignment.END, spacing=Spacing.XS),
                ]),
                ft.Container(height=Spacing.SM),
                ft.Row([
                    ft.Text(
                        f"{quiz['questions_count']} questions",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Text(
                        f"Created: {quiz['created_at']}",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Text(
                        f"| Starts: {quiz.get('start_time', 'N/A')}",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Text(
                        f"| Duration: {quiz.get('duration_minutes', 'N/A')} min",
                        size=Typography.SIZE_SM,
                        color=Colors.TEXT_MUTED
                    ),
                    ft.Container(expand=True),
                    create_secondary_button("Preview", on_click=lambda e, q=quiz: show_quiz_preview(q), width=80),
                    ft.Container(width=Spacing.SM),
                    create_secondary_button("Delete", on_click=handle_delete_quiz(quiz), width=80),
                    ft.Container(width=Spacing.SM),
                    create_primary_button("Manage Questions", on_click=edit_quiz(quiz), width=150)
                ])
            ]),
            padding=Spacing.LG
        )
        return quiz_card

    # Initial population of the list
    update_quiz_list()
    # Main content
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Row([
                        ft.Column([
                            create_page_title("Quiz Management"),
                            create_subtitle("Create and manage your quizzes")
                        ], expand=True, spacing=Spacing.XS),
                        search_field,
                        status_filter_dropdown,
                        shuffle_filter_dropdown,
                        class_filter_dropdown,
                        create_primary_button("Create New Quiz", on_click=show_create_form, width=150)
                    ]),
                    
                    ft.Container(height=Spacing.XXL),
                    
                    # Create form (hidden by default)
                    quiz_form_container,
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Quizzes list
                    create_section_title("Your Quizzes"),
                    ft.Container(height=Spacing.LG),
                    quiz_list_view if quiz_list_view.controls else create_card(
                        content=ft.Column([
                            ft.Image(src="assets/logo.png", width=48, height=48),
                            ft.Container(height=Spacing.SM),
                            ft.Text(
                                "No quizzes created yet",
                                size=Typography.SIZE_LG,
                                weight=ft.FontWeight.W_600,
                                color=Colors.TEXT_SECONDARY
                            ),
                            ft.Text(
                                "Create your first quiz to get started!",
                                size=Typography.SIZE_SM,
                                color=Colors.TEXT_MUTED
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=Spacing.XXXXL
                    )
                ]),
                padding=Spacing.XL,
                expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )
    
    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_quiz_management # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_question_management(quiz):
    """Show the enhanced question management page with multiple question types"""
    global current_page
    global sidebar_drawer
    global current_view_handler
    current_page.clean()
    
    sidebar = create_sidebar(current_user['role'], "questions")
    
    def handle_delete_question(quiz, question_to_delete):
        def on_delete(e):
            global mock_questions, mock_quizzes
            if quiz['id'] in mock_questions:
                # Remove the question
                mock_questions[quiz['id']] = [q for q in mock_questions[quiz['id']] if q['id'] != question_to_delete['id']]
                
                # Update quiz questions count
                for q_quiz in mock_quizzes:
                    if q_quiz['id'] == quiz['id']:
                        q_quiz['questions_count'] = len(mock_questions[quiz['id']])
                        break
            show_question_management(quiz) # Refresh the page
        return on_delete

    # Question form fields
    question_text_field = create_text_input("Question Text", width=500, multiline=True, min_lines=2)
    question_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)
    
    # Question type selector
    question_type_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="multiple_choice", label="Multiple Choice (A, B, C, D)"),
            ft.Radio(value="true_false", label="True/False"),
            ft.Radio(value="fill_in_blank", label="Fill in the Blank"),
            ft.Radio(value="multiple_select", label="Multiple Select (Check all that apply)"),
            ft.Radio(value="short_answer", label="Short Answer"),
        ], spacing=Spacing.SM)
    )
    question_type_group.value = "multiple_choice"  # Default
    
    # Difficulty selector
    difficulty_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Easy", label="Easy"),
            ft.Radio(value="Medium", label="Medium"),
            ft.Radio(value="Hard", label="Hard"),
        ], spacing=Spacing.LG)
    )
    difficulty_group.value = "Easy" # Default


    # Dynamic form container
    dynamic_form_container = ft.Container()
    
    def update_dynamic_form(question_type):
        """Update the form based on selected question type"""
        if question_type == "multiple_choice":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Answer Options:"),
                ft.Container(height=Spacing.SM),
                create_text_input("Option A", width=400),
                ft.Container(height=Spacing.SM),
                create_text_input("Option B", width=400),
                ft.Container(height=Spacing.SM),
                create_text_input("Option C", width=400),
                ft.Container(height=Spacing.SM),
                create_text_input("Option D", width=400),
                ft.Container(height=Spacing.LG),
                create_subtitle("Correct Answer:"),
                ft.Container(height=Spacing.SM),
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
                create_subtitle("Correct Answer:"),
                ft.Container(height=Spacing.SM),
                ft.RadioGroup(
                    content=ft.Column([
                        ft.Radio(value="true", label="True"),
                        ft.Radio(value="false", label="False"),
                    ])
                )
            ])
        elif question_type == "fill_in_blank":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Correct Answer:"),
                ft.Container(height=Spacing.SM),
                create_text_input("Correct answer", width=400),
                ft.Container(height=Spacing.SM),
                ft.Text("Tip: Use _______ in your question text to indicate where the blank should be.", 
                       size=Typography.SIZE_XS, color=Colors.TEXT_MUTED)
            ])
        elif question_type == "multiple_select":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Answer Options (Check all correct answers):"),
                ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option A", width=300), ft.Checkbox(label="Correct")]),
                ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option B", width=300), ft.Checkbox(label="Correct")]),
                ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option C", width=300), ft.Checkbox(label="Correct")]),
                ft.Container(height=Spacing.SM),
                ft.Row([create_text_input("Option D", width=300), ft.Checkbox(label="Correct")]),
            ])
        elif question_type == "short_answer":
            dynamic_form_container.content = ft.Column([
                create_subtitle("Sample Answer (for reference):"),
                ft.Container(height=Spacing.SM),
                create_text_input("Sample answer", width=500, multiline=True, min_lines=3),
                ft.Container(height=Spacing.SM),
                ft.Text("Note: Short answer questions require manual grading.", 
                       size=Typography.SIZE_XS, color=Colors.TEXT_MUTED)
            ])
        
        current_page.update()
    
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
        current_page.update()
    
    def hide_question_form(e):
        question_form_container.visible = False
        current_page.update()
    
    def handle_create_question(e):
        question_text = question_text_field.value or ""
        question_type = question_type_group.value
        difficulty = difficulty_group.value
        
        # Basic validation
        if not question_text.strip():
            question_error_text.value = "Question text is required"
            current_page.update()
            return
        
        # Create question based on type
        new_question = {
            # Tìm ID lớn nhất trong danh sách câu hỏi của quiz này và +1
            'id': (max(q['id'] for q in mock_questions[quiz['id']]) + 1) if quiz['id'] in mock_questions and mock_questions[quiz['id']] else 1,
            'question_type': question_type,
            'question_text': question_text.strip(),
            'difficulty': difficulty,
        }
        
        # Type-specific data collection
        if question_type == "multiple_choice":
            form_controls = dynamic_form_container.content.controls
            option_texts = []
            # Lấy giá trị từ các ô nhập liệu (vị trí 2, 4, 6, 8)
            option_texts.append(form_controls[2].value or "")
            option_texts.append(form_controls[4].value or "")
            option_texts.append(form_controls[6].value or "")
            option_texts.append(form_controls[8].value or "")
            
            if not all(opt.strip() for opt in option_texts):
                question_error_text.value = "All options are required for multiple choice questions"
                current_page.update()
                return
            
            correct_group = form_controls[-1]  # RadioGroup là thành phần cuối cùng
            if not correct_group.value:
                question_error_text.value = "Please select the correct answer"
                current_page.update()
                return
            
            new_question['options'] = [
                {'option_text': option_texts[0], 'is_correct': correct_group.value == 'A'},
                {'option_text': option_texts[1], 'is_correct': correct_group.value == 'B'},
                {'option_text': option_texts[2], 'is_correct': correct_group.value == 'C'},
                {'option_text': option_texts[3], 'is_correct': correct_group.value == 'D'}
            ]
            
        elif question_type == "true_false":
            correct_group = dynamic_form_container.content.controls[2]
            if not hasattr(correct_group, 'value') or not correct_group.value:
                question_error_text.value = "Please select True or False"
                current_page.update()
                return
            new_question['correct_answer'] = correct_group.value == "true"
            
        elif question_type == "fill_in_blank":
            answer_field = dynamic_form_container.content.controls[2]
            if not hasattr(answer_field, 'value') or not answer_field.value:
                question_error_text.value = "Please provide the correct answer"
                current_page.update()
                return
            new_question['correct_answer'] = answer_field.value
            new_question['answer_variations'] = [answer_field.value.lower()]
            
        elif question_type == "short_answer":
            sample_field = dynamic_form_container.content.controls[2]
            new_question['sample_answer'] = getattr(sample_field, 'value', '') or ''
        
        elif question_type == "multiple_select":
            options_container = dynamic_form_container.content.controls[2:] # Bắt đầu từ Row đầu tiên
            options = []
            has_empty_option = False
            for i in range(4):
                row = options_container[i*2] # Bỏ qua các container khoảng cách
                option_field = row.controls[0]
                checkbox = row.controls[1]
                
                option_text = option_field.value or ""
                if not option_text.strip():
                    has_empty_option = True
                    break
                
                options.append({
                    'option_text': option_text,
                    'is_correct': checkbox.value
                })
            if has_empty_option:
                question_error_text.value = "All option texts are required for multiple select questions"
                current_page.update()
                return
            new_question['options'] = options

        # Add to mock data
        if quiz['id'] not in mock_questions:
            mock_questions[quiz['id']] = []
        mock_questions[quiz['id']].append(new_question)
        
        # Update quiz questions count
        for q in mock_quizzes:
            if q['id'] == quiz['id']:
                q['questions_count'] = len(mock_questions[quiz['id']])
                break
        
        question_error_text.value = ""
        hide_question_form(e)
        show_question_management(quiz)  # Refresh
    
    def back_to_quizzes(e):
        show_quiz_management()
    
    # Initialize dynamic form
    update_dynamic_form("multiple_choice")
    
    # Question form
    question_form_container = create_card(
        content=ft.Column([
            create_section_title("Add New Question"),
            ft.Container(height=Spacing.LG),
            
            # Question type selector
            create_subtitle("Question Type:"),
            ft.Container(height=Spacing.MD),
            question_type_group,
            ft.Container(height=Spacing.XL),
            
            # Question text
            create_subtitle("Question Text:"),
            ft.Container(height=Spacing.MD),
            question_text_field,
            ft.Container(height=Spacing.XL),

            # Difficulty selector
            create_subtitle("Difficulty:"),
            ft.Container(height=Spacing.MD),
            difficulty_group,
            ft.Container(height=Spacing.XL),
            
            # Dynamic form based on question type
            dynamic_form_container,
            
            ft.Container(height=Spacing.MD),
            question_error_text,
            ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Add Question", on_click=handle_create_question, width=130),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Cancel", on_click=hide_question_form, width=100)
            ])
        ]),
        padding=Spacing.LG
    )
    question_form_container.visible = False
    
    # Existing questions
    quiz_questions = mock_questions.get(quiz['id'], [])
    question_cards = []
    
    for i, question in enumerate(quiz_questions, 1):
        # Create type-specific preview
        question_type = question.get('question_type', 'multiple_choice')
        difficulty = question.get('difficulty', 'Medium')
        difficulty_color_map = {
            'Easy': Colors.SUCCESS,
            'Medium': Colors.WARNING,
            'Hard': Colors.ERROR
        }
        
        if question_type == "multiple_choice":
            correct_option = next((opt['option_text'] for opt in question.get('options', []) if opt['is_correct']), "")
            preview_content = ft.Column([
                ft.Column([
                    ft.Text(f"A) {question['options'][0]['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                    ft.Text(f"B) {question['options'][1]['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                    ft.Text(f"C) {question['options'][2]['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                    ft.Text(f"D) {question['options'][3]['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY),
                ], spacing=Spacing.XS),
                ft.Container(height=Spacing.SM),
                ft.Row([
                    ft.Text("Correct Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(correct_option, size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)
                ])
            ])
        elif question_type == "true_false":
            preview_content = ft.Row([
                ft.Text("Correct Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                ft.Text(str(question.get('correct_answer', '')), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)
            ])
        elif question_type == "fill_in_blank":
            preview_content = ft.Row([
                ft.Text("Answer:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                ft.Text(question.get('correct_answer', ''), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)
            ])
        elif question_type == "short_answer":
            preview_content = ft.Text("Sample: " + (question.get('sample_answer', 'No sample provided')[:50] + "..."), 
                                    size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
        elif question_type == "multiple_select":
            correct_options = [opt['option_text'] for opt in question.get('options', []) if opt['is_correct']]
            preview_content = ft.Column([
                ft.Column([
                    ft.Text(f"- {opt['option_text']}", size=Typography.SIZE_SM, color=Colors.TEXT_SECONDARY) for opt in question.get('options', [])
                ], spacing=Spacing.XS),
                ft.Container(height=Spacing.SM),
                ft.Row([
                    ft.Text("Correct Answers:", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED),
                    ft.Text(", ".join(correct_options), size=Typography.SIZE_SM, weight=ft.FontWeight.W_600, color=Colors.SUCCESS)
                ])
            ])

        else:
            preview_content = ft.Text("Preview not available", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
        
        question_card = create_card(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        f"Question {i}",
                        size=Typography.SIZE_SM,
                        weight=ft.FontWeight.W_600,
                        color=Colors.PRIMARY
                    ),
                    create_badge(question_type.replace('_', ' ').title(), color=Colors.PRIMARY_LIGHT),
                    create_badge(difficulty, color=difficulty_color_map.get(difficulty, Colors.GRAY_400)),
                    ft.Container(expand=True),
                    create_secondary_button("Delete", on_click=handle_delete_question(quiz, question), width=80)
                ]),
                ft.Container(height=Spacing.SM),
                ft.Text(
                    question['question_text'],
                    size=Typography.SIZE_BASE,
                    weight=ft.FontWeight.W_600,
                    color=Colors.TEXT_PRIMARY
                ),
                ft.Container(height=Spacing.SM),
                preview_content
            ]),
            padding=Spacing.LG
        )
        question_cards.append(question_card)
    
    # Main content with scrolling
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        # Header
                        ft.Row([
                            create_secondary_button("← Back to Quizzes", on_click=back_to_quizzes, width=150),
                            ft.Container(expand=True)
                        ]),
                        ft.Container(height=Spacing.LG),
                    
                    # Quiz info
                    create_card(
                        content=ft.Column([
                            ft.Row([
                                ft.Column([
                                    ft.Text(
                                        quiz['title'],
                                        size=Typography.SIZE_2XL,
                                        weight=ft.FontWeight.W_700,
                                        color=Colors.TEXT_PRIMARY
                                    ),
                                    ft.Text(
                                        quiz['description'] or "No description",
                                        size=Typography.SIZE_BASE,
                                        color=Colors.TEXT_SECONDARY
                                    )
                                ], expand=True),
                                create_badge(f"{len(quiz_questions)} Questions")
                            ])
                        ]),
                        padding=Spacing.LG
                    ),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Add question button
                    ft.Row([
                        create_section_title("Questions"),
                        ft.Container(expand=True),
                        create_secondary_button("Preview Quiz", on_click=lambda e: show_quiz_preview(quiz), width=120),
                        create_primary_button("Add Question", on_click=show_question_form, width=120),
                    ]),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Question form (hidden by default)
                    question_form_container,
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Questions list
                    ft.Column(question_cards, spacing=Spacing.LG) if question_cards else create_card(
                        content=ft.Column([
                            ft.Icon(ft.Icons.HELP_OUTLINE, size=48, color=Colors.GRAY_400),
                            ft.Container(height=Spacing.SM),
                            ft.Text("No questions added yet", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                            ft.Text("Add your first question to get started!", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=Spacing.XXXXL
                    )
                ]),
                padding=Spacing.XL,
                expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )
    
    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = lambda e=None: show_question_management(quiz) # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_examinee_dashboard():
    """Show the examinee dashboard"""
    global current_page
    global sidebar_drawer
    global current_view_handler
    current_page.clean()
    
    sidebar = create_sidebar(current_user['role'], "home")
    
    # --- Search and Filter Logic ---
    search_field = create_text_input("Search by quiz title...", width=300, icon=ft.Icons.SEARCH)
    quiz_list_view = ft.Column(spacing=Spacing.LG)

    def update_quiz_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        student_class_id = current_user.get('class_id')
        
        # Filter quizzes based on class assignment, active state, and search term
        available_quizzes = []
        if student_class_id is not None:
            available_quizzes = [
                q for q in mock_quizzes 
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
        
        current_page.update()

    search_field.on_change = update_quiz_list


    def handle_start_quiz(quiz):
        def start_action(e):
            if quiz.get('password'):
                password_field = create_text_input("Quiz Password", password=True, can_reveal=True)
                error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

                def check_password(e_dialog):
                    if password_field.value == quiz['password']:
                        password_dialog.open = False
                        current_page.update() # Đóng dialog trước khi chuyển trang
                        show_quiz_taking(quiz)
                    else:
                        error_text.value = "Incorrect password. Please try again."
                        password_field.value = ""
                        # Cập nhật trực tiếp nội dung của dialog để hiển thị lỗi
                        # Gọi page.update() thay vì content.update() để đảm bảo dialog được vẽ lại
                        current_page.update()

                def close_dialog(e_dialog):
                    password_dialog.open = False
                    current_page.update()

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

                current_page.dialog = password_dialog
                password_dialog.open = True
                current_page.update()
            else:
                # No password, start directly
                show_quiz_taking(quiz)
        return start_action

    # --- Function to create a single quiz card for examinee ---
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

    # Initial population of the list
    update_quiz_list()
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Container(
                        content=ft.Column([
                            create_page_title(f"Welcome, {current_user['username']}!"),
                            create_subtitle("Choose a quiz to test your knowledge."),
                        ], spacing=Spacing.XS),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),
                    
                    # Available quizzes
                    ft.Row([create_section_title("Available Quizzes"), ft.Container(expand=True), search_field]),
                    ft.Container(height=Spacing.LG),
                    quiz_list_view
                ]),
                padding=Spacing.XXXXL,
                expand=True, bgcolor=Colors.GRAY_50)
        ]),
        expand=True
    )
    
    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_examinee_dashboard # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True

    current_page.update()

def show_quiz_taking(quiz_basic_info):
    """Show the modern quiz taking interface with multiple question types"""
    global current_page, current_user, current_question_index, user_answers, quiz_questions, quiz_start_time, quiz_timer_thread
    global current_view_handler
    
    current_page.clean()
    current_question_index = 0
    user_answers = {}
    quiz_start_time = datetime.datetime.now()
    quiz_timer_thread = None
    
    # Load quiz questions
    quiz_questions = mock_questions.get(quiz_basic_info['id'], [])

    # Xáo trộn câu hỏi nếu được yêu cầu
    if quiz_basic_info.get('shuffle_questions', False):
        random.shuffle(quiz_questions)

    
    if not quiz_questions:
        show_examinee_dashboard()
        return
    
    # Quiz state
    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_text_display = ft.Text("", size=Typography.SIZE_XL, weight=ft.FontWeight.W_600, color=Colors.TEXT_PRIMARY)
    timer_text = ft.Text("", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.ERROR)
    question_component_container = ft.Container(content=ft.Column([]))
    
    def update_question_display():
        if current_question_index >= len(quiz_questions):
            return
        
        question = quiz_questions[current_question_index]
        
        # Update counter
        question_counter_text.value = f"Question {current_question_index + 1} of {len(quiz_questions)}"
        
        # Update question text
        question_text_display.value = question['question_text']
        
        # Create question component based on type
        shuffle_answers = quiz_basic_info.get('shuffle_answers', False)
        question_component = create_question_by_type(question, handle_answer_change, shuffle_answers)
        question_component_container.content = question_component
        
        # Update navigation buttons
        prev_button.disabled = (current_question_index == 0)
        has_answer = question['id'] in user_answers
        next_button.disabled = not has_answer
        submit_button.visible = (current_question_index == len(quiz_questions) - 1 and has_answer)
        
        current_page.update()
    
    def handle_answer_change(question_id, answer):
        """Handle answer changes for any question type"""
        user_answers[question_id] = answer
        has_answer = answer is not None and answer != "" and answer != []
        next_button.disabled = not has_answer
        submit_button.visible = (current_question_index == len(quiz_questions) - 1 and has_answer)
        current_page.update()
    
    def handle_previous(e):
        global current_question_index
        if current_question_index > 0:
            current_question_index -= 1
            update_question_display()
    
    def handle_next(e):
        global current_question_index
        if current_question_index < len(quiz_questions) - 1:
            current_question_index += 1
            update_question_display()
    
    def handle_submit(e):
        global quiz_timer_thread
        if quiz_timer_thread:
            quiz_timer_thread.do_run = False # Signal thread to stop
            quiz_timer_thread = None
        show_quiz_results(quiz_basic_info, user_answers, quiz_start_time)
    
    def exit_quiz(e):
        show_examinee_dashboard()
    
    # Navigation buttons
    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120, disabled=True)
    submit_button = create_primary_button("Submit Quiz", on_click=handle_submit, width=130)
    submit_button.visible = False
    
    # Answer handler is connected via create_question_by_type
    
    # Progress bar
    progress_bar = ft.ProgressBar(
        width=400,
        color=Colors.PRIMARY,
        bgcolor=Colors.GRAY_200,
        value=0
    )
    
    def update_progress():
        progress = (current_question_index + 1) / len(quiz_questions)
        progress_bar.value = progress
        current_page.update()
    
    def run_timer():
        """Background thread function to update the countdown timer."""
        duration_minutes = quiz_basic_info.get('duration_minutes', 10)
        end_time = quiz_start_time + datetime.timedelta(minutes=duration_minutes)
        
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            remaining = end_time - datetime.datetime.now()
            if remaining.total_seconds() <= 0:
                timer_text.value = "00:00"
                current_page.update()
                # Use page.run() to ensure thread-safe execution of UI-modifying code
                current_page.run(handle_submit(None))
                break

            minutes, seconds = divmod(int(remaining.total_seconds()), 60)
            timer_text.value = f"{minutes:02d}:{seconds:02d}"
            current_page.update()
            time.sleep(1)

    # Start the timer thread
    quiz_timer_thread = threading.Thread(target=run_timer, daemon=True)
    quiz_timer_thread.start()

    # Main quiz interface
    quiz_content = ft.Container(
        content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            # Header
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
            
            # Question area
            create_card(
                content=ft.Column([
                    question_text_display,
                    ft.Container(height=Spacing.XXL),
                    question_component_container
                ]),
                padding=Spacing.XXXXL
            ),
            
            ft.Container(height=Spacing.XXL),
            
            # Navigation
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
    
    # Initialize first question
    update_question_display()
    update_progress()
    
    current_page.add(quiz_content)
    current_view_handler = None # Disable resizing for this page
    current_page.update()

def show_quiz_preview(quiz_basic_info):
    """Show the quiz in a preview mode for instructors."""
    global current_page, current_question_index, quiz_questions

    current_page.clean()
    current_question_index = 0

    # Load quiz questions
    quiz_questions = mock_questions.get(quiz_basic_info['id'], [])

    # Xáo trộn câu hỏi nếu được yêu cầu
    if quiz_basic_info.get('shuffle_questions', False):
        random.shuffle(quiz_questions)

    if not quiz_questions:
        show_quiz_management() # Go back if no questions
        return

    # UI Components
    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_component_container = ft.Container(content=ft.Column([]))

    def update_preview_display():
        if current_question_index >= len(quiz_questions):
            return

        question = quiz_questions[current_question_index]
        question_counter_text.value = f"Question {current_question_index + 1} of {len(quiz_questions)}"

        # Use a dummy answer handler as we don't save answers in preview
        def dummy_answer_handler(q_id, answer):
            pass

        shuffle_answers = quiz_basic_info.get('shuffle_answers', False)
        question_component = create_question_by_type(question, dummy_answer_handler, shuffle_answers)
        question_component_container.content = question_component

        prev_button.disabled = (current_question_index == 0)
        next_button.disabled = (current_question_index == len(quiz_questions) - 1)
        current_page.update()

    def handle_previous(e):
        global current_question_index
        if current_question_index > 0:
            current_question_index -= 1
            update_preview_display()

    def handle_next(e):
        global current_question_index
        if current_question_index < len(quiz_questions) - 1:
            current_question_index += 1
            update_preview_display()

    def exit_preview(e):
        show_question_management(quiz_basic_info)

    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120)

    # Main preview interface
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
    current_page.add(preview_content)
    current_view_handler = None # Disable resizing for this page
    current_page.update()

def show_quiz_results(quiz_data, user_answers, start_time):
    """Show modern quiz results"""
    global current_page, current_user, mock_attempts
    global current_view_handler
    
    current_page.clean()
    
    # Calculate score for multiple question types
    quiz_questions = mock_questions.get(quiz_data['id'], [])
    correct_count = 0
    total_questions = len(quiz_questions)
    
    for question in quiz_questions:
        question_id = question['id']
        if question_id in user_answers:
            user_answer = user_answers[question_id]
            question_type = question.get('question_type', 'multiple_choice')
            
            if question_type == 'multiple_choice':
                # user_answer bây giờ là text của lựa chọn
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
                # user_answer bây giờ là list các text của lựa chọn
                if isinstance(user_answer, list):
                    correct_options_texts = {opt['option_text'] for opt in question['options'] if opt['is_correct']}
                    user_answers_texts = set(user_answer)
                    if user_answers_texts == correct_options_texts:
                        correct_count += 1
            elif question_type == 'short_answer':
                # For now, manual grading needed - give partial credit
                if user_answer and str(user_answer).strip():
                    correct_count += 0.5  # Partial credit for providing an answer
    
    percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Calculate time
    end_time = datetime.datetime.now()
    time_taken = end_time - start_time
    time_minutes = int(time_taken.total_seconds() / 60)
    time_seconds = int(time_taken.total_seconds() % 60)
    
    # --- Lưu kết quả lần làm bài này vào mock_attempts ---
    if mock_attempts:
        new_attempt_id = max(a['attempt_id'] for a in mock_attempts) + 1
    else:
        new_attempt_id = 1

    new_attempt = {
        'attempt_id': new_attempt_id,
        'user_id': current_user['id'],
        'quiz_id': quiz_data['id'],
        'score': f"{correct_count}/{total_questions}",
        'percentage': percentage,
        'time_taken': f"{time_minutes:02d}:{time_seconds:02d}",
        'completed_at': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_answers': user_answers
    }
    mock_attempts.append(new_attempt)
    # Thông báo cho instructor (nếu cần)
    # ...

    # Results content
    results_content = ft.Container(
        content=ft.Column([
            # Header
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
            
            # Score cards
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
            
            # Actions
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
    
    current_page.add(results_content)
    current_view_handler = None # Disable resizing for this page
    current_page.update()

def show_student_results_overview():
    """Show the student's results overview with a chart."""
    global current_page, sidebar_drawer, current_user
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "results")

    # --- Get and process attempt data ---
    user_attempts = [attempt for attempt in mock_attempts if attempt['user_id'] == current_user['id']]
    user_attempts.sort(key=lambda x: x['completed_at']) # Sắp xếp theo thời gian để biểu đồ có thứ tự

    bar_groups = []
    total_score_10 = 0
    highest_score_10 = 0

    if user_attempts:
        for i, attempt in enumerate(user_attempts):
            quiz_info = next((q for q in mock_quizzes if q['id'] == attempt['quiz_id']), None)
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

    # --- Chart component ---
    chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, Colors.GRAY_300),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=0, label=ft.Text("0")),
                ft.ChartAxisLabel(value=2, label=ft.Text("2")),
                ft.ChartAxisLabel(value=4, label=ft.Text("4")),
                ft.ChartAxisLabel(value=6, label=ft.Text("6")),
                ft.ChartAxisLabel(value=8, label=ft.Text("8")),
                ft.ChartAxisLabel(value=10, label=ft.Text("10")),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=i, label=ft.Text(f"Lần {i+1}", size=Typography.SIZE_XS)) for i in range(len(user_attempts))],
            labels_size=30,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=2, color=Colors.GRAY_200, width=1
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, Colors.GRAY_800),
        max_y=10,
        interactive=True,
        expand=True,
    )

    # --- Main page content ---
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Results Overview"),
                            create_subtitle("A visual summary of your performance across all quizzes.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),

                    # Stats Cards
                    ft.Row([
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.STAR_HALF, color=Colors.PRIMARY), ft.Text("Điểm trung bình")]), ft.Text(f"{avg_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color=Colors.WARNING), ft.Text("Điểm cao nhất")]), ft.Text(f"{highest_score_10:.2f}", size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                        create_card(ft.Column([ft.Row([ft.Icon(ft.Icons.QUIZ, color=Colors.SUCCESS), ft.Text("Tổng số bài đã làm")]), ft.Text(str(len(user_attempts)), size=Typography.SIZE_3XL, weight=ft.FontWeight.W_700)])),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    ft.Container(height=Spacing.XXXXL),

                    # Chart
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

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_student_results_overview # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_attempt_review(attempt):
    """Show the detailed review of a specific quiz attempt."""
    global current_page, current_question_index, quiz_questions
    global current_view_handler

    current_page.clean()
    current_question_index = 0

    # Lấy thông tin quiz và câu hỏi
    quiz_info = next((q for q in mock_quizzes if q['id'] == attempt['quiz_id']), None)
    if not quiz_info:
        show_my_attempts()
        return

    # Lấy danh sách câu hỏi gốc (không xáo trộn) để đảm bảo thứ tự nhất quán khi xem lại
    quiz_questions = mock_questions.get(quiz_info['id'], [])
    user_answers = attempt.get('user_answers', {})

    if not quiz_questions:
        show_my_attempts()
        return

    # UI Components
    question_counter_text = ft.Text("", size=Typography.SIZE_BASE, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY)
    question_component_container = ft.Container(content=ft.Column([]))

    def update_review_display():
        if current_question_index >= len(quiz_questions):
            return

        question = quiz_questions[current_question_index]
        user_answer = user_answers.get(question['id'])
        
        question_counter_text.value = f"Question {current_question_index + 1} of {len(quiz_questions)}"

        # Tạo component câu hỏi ở chế độ review
        question_component = create_question_by_type(question, on_answer_change=None, is_review=True, user_answer=user_answer)
        question_component_container.content = question_component

        prev_button.disabled = (current_question_index == 0)
        next_button.disabled = (current_question_index == len(quiz_questions) - 1)
        current_page.update()

    def handle_previous(e):
        global current_question_index
        if current_question_index > 0:
            current_question_index -= 1
            update_review_display()

    def handle_next(e):
        global current_question_index
        if current_question_index < len(quiz_questions) - 1:
            current_question_index += 1
            update_review_display()

    def exit_review(e):
        show_my_attempts()

    prev_button = create_secondary_button("← Previous", on_click=handle_previous, width=120)
    next_button = create_primary_button("Next →", on_click=handle_next, width=120)

    # Main review interface
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
    current_page.add(review_content)
    current_view_handler = None # Disable resizing for this page
    current_page.update()

def show_my_attempts():
    """Show the student's history of quiz attempts."""
    global current_page, sidebar_drawer, current_user
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "attempts")

    # --- Lấy lịch sử làm bài của sinh viên hiện tại ---
    user_attempts = [attempt for attempt in mock_attempts if attempt['user_id'] == current_user['id']]
    user_attempts.sort(key=lambda x: x['completed_at'], reverse=True) # Sắp xếp mới nhất lên đầu

    attempt_cards = []
    if user_attempts:
        for attempt in user_attempts:
            # Lấy thông tin quiz từ quiz_id
            quiz_info = next((q for q in mock_quizzes if q['id'] == attempt['quiz_id']), None)
            if not quiz_info:
                continue

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
        attempt_cards.append(
            create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.HISTORY_EDU, size=48, color=Colors.GRAY_400),
                    ft.Container(height=Spacing.SM),
                    ft.Text("No Attempts Yet", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                    ft.Text("Your completed quizzes will appear here.", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            )
        )

    # --- Nội dung chính của trang ---
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Attempts"),
                            create_subtitle("Here is a history of all the quizzes you have completed.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),

                    # Danh sách các lần làm bài
                    ft.Column(attempt_cards, spacing=Spacing.LG)
                ]),
                padding=Spacing.XXXXL,
                expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_my_attempts # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_profile_page():
    """Show the user's profile page to view info and change password."""
    global current_page, sidebar_drawer, current_user
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "profile")

    # --- Change Password Form ---
    current_password_field = create_text_input("Mật khẩu hiện tại", password=True, can_reveal=True)
    new_password_field = create_text_input("Mật khẩu mới", password=True, can_reveal=True)
    confirm_password_field = create_text_input("Xác nhận mật khẩu mới", password=True, can_reveal=True)
    password_message_text = ft.Text("", size=Typography.SIZE_SM)

    def handle_save_password(e):
        current_pass = current_password_field.value
        new_pass = new_password_field.value
        confirm_pass = confirm_password_field.value

        # Validation
        if not all([current_pass, new_pass, confirm_pass]):
            password_message_text.value = "Vui lòng điền đầy đủ các trường."
            password_message_text.color = Colors.ERROR
            current_page.update()
            return

        if current_pass != current_user['password']:
            password_message_text.value = "Mật khẩu hiện tại không đúng."
            password_message_text.color = Colors.ERROR
            current_password_field.value = ""
            current_page.update()
            return

        if new_pass != confirm_pass:
            password_message_text.value = "Mật khẩu mới không khớp."
            password_message_text.color = Colors.ERROR
            new_password_field.value = ""
            confirm_password_field.value = ""
            current_page.update()
            return

        # Update password
        mock_users[current_user['username']]['password'] = new_pass
        current_user['password'] = new_pass # Update current session user

        password_message_text.value = "Đổi mật khẩu thành công!"
        password_message_text.color = Colors.SUCCESS
        current_password_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        current_page.update()

    # --- User Info ---
    class_name = "N/A"
    if current_user.get('class_id'):
        class_info = next((c for c in mock_classes if c['id'] == current_user['class_id']), None)
        if class_info:
            class_name = class_info['name']

    # --- Main page content ---
    main_content = ft.Container(
        content=ft.Column(spacing=0, controls=[
            create_app_header(),
            ft.Container(
                content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
                    # Header
                    ft.Container(
                        content=ft.Column([
                            create_page_title("My Profile"),
                            create_subtitle("View your personal information and manage your account.")
                        ]),
                        padding=ft.padding.only(bottom=Spacing.XXL)
                    ),

                    # Profile Cards
                    ft.Row([
                        # User Info Card
                        create_card(
                            content=ft.Column([
                                create_section_title("Thông tin tài khoản"),
                                ft.Container(height=Spacing.LG),
                                ft.Row([ft.Text("Username:", weight=ft.FontWeight.W_600), ft.Text(current_user['username'])]),
                                ft.Divider(),
                                ft.Row([ft.Text("Vai trò:", weight=ft.FontWeight.W_600), ft.Text(current_user['role'].title())]),
                                ft.Divider(),
                                ft.Row([ft.Text("Lớp học:", weight=ft.FontWeight.W_600), ft.Text(class_name)]),
                            ]),
                            padding=Spacing.XL
                        ),

                        # Change Password Card
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

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_profile_page # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_results_overview():
    """Show a placeholder page for viewing quiz results overview"""
    # Route to the correct results page based on user role
    if current_user['role'] == 'instructor':
        show_instructor_results_page()
    elif current_user['role'] == 'admin':
        # Placeholder for admin results page
        pass

def show_instructor_results_page():
    """Show the detailed results page for instructors, filterable by class and quiz."""
    global current_page, sidebar_drawer, current_user
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "results")

    # --- UI Components for filtering and display ---
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
            current_page.update()
            return

        # --- Data Processing ---
        students_in_class = [u for u in mock_users.values() if u.get('class_id') == int(selected_class_id)]
        attempts_for_quiz = [a for a in mock_attempts if a['quiz_id'] == int(selected_quiz_id)]

        # Get the latest attempt for each student in the class
        student_results = []
        for student in students_in_class:
            student_attempts = [a for a in attempts_for_quiz if a['user_id'] == student['id']]
            if student_attempts:
                latest_attempt = max(student_attempts, key=lambda x: x['completed_at'])
                student_results.append({'student': student, 'attempt': latest_attempt})

        # --- Statistics ---
        total_students = len(students_in_class)
        completed_count = len(student_results)
        completion_rate = (completed_count / total_students * 100) if total_students > 0 else 0
        
        scores_10 = [res['attempt']['percentage'] / 10.0 for res in student_results]
        avg_score_10 = sum(scores_10) / len(scores_10) if scores_10 else 0
        highest_score_10 = max(scores_10) if scores_10 else 0

        # --- Chart ---
        bar_groups = []
        for i, res in enumerate(student_results):
            score_10 = res['attempt']['percentage'] / 10.0
            bar_groups.append(
                ft.BarChartGroup(x=i, bar_rods=[
                    ft.BarChartRod(from_y=0, to_y=score_10, width=15, color=Colors.PRIMARY, tooltip=f"{res['student']['username']}: {score_10:.1f}", border_radius=BorderRadius.SM)
                ])
            )
        
        chart = ft.BarChart(
            bar_groups=bar_groups,
            left_axis=ft.ChartAxis(labels=[ft.ChartAxisLabel(value=v, label=ft.Text(str(v))) for v in range(0, 11, 2)], labels_size=40),
            bottom_axis=ft.ChartAxis(labels=[ft.ChartAxisLabel(value=i, label=ft.Text(res['student']['username'], size=10, rotate=45)) for i, res in enumerate(student_results)], labels_size=50),
            horizontal_grid_lines=ft.ChartGridLines(interval=2, color=Colors.GRAY_200, width=1),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, Colors.GRAY_800), max_y=10, interactive=True, expand=True
        )

        # --- Results Table ---
        table_rows = []
        for res in student_results:
            attempt = res['attempt']
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(res['student']['username'])),
                    ft.DataCell(ft.Text(attempt['score'])),
                    ft.DataCell(ft.Text(f"{attempt['percentage']:.1f}%")),
                    ft.DataCell(ft.Text(attempt['time_taken'])),
                    ft.DataCell(ft.Text(datetime.datetime.strptime(attempt['completed_at'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M'))),
                ])
            )

        results_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Student")), ft.DataColumn(ft.Text("Score")), ft.DataColumn(ft.Text("Percentage")),
                ft.DataColumn(ft.Text("Time Taken")), ft.DataColumn(ft.Text("Completed At")),
            ],
            rows=table_rows, heading_row_color=Colors.GRAY_100, border=ft.border.all(1, Colors.GRAY_200), border_radius=BorderRadius.MD
        )

        # --- Assemble Content ---
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
        current_page.update()

    # --- Filter Dropdowns ---
    instructor_classes = [c for c in mock_classes if c['instructor_id'] == current_user['id']]
    class_dd = ft.Dropdown(label="Chọn Lớp học", width=250, options=[ft.dropdown.Option(key=c['id'], text=c['name']) for c in instructor_classes])
    quiz_dd = ft.Dropdown(label="Chọn Bài thi", width=300, disabled=True)

    def on_class_change(e):
        selected_class_id = int(e.control.value)
        quizzes_in_class = [q for q in mock_quizzes if q.get('class_id') == selected_class_id]
        quiz_dd.options = [ft.dropdown.Option(key=q['id'], text=q['title']) for q in quizzes_in_class]
        quiz_dd.value = None
        quiz_dd.disabled = False
        update_results_display() # Clear results when class changes
        current_page.update()

    def on_quiz_change(e):
        update_results_display(class_dd.value, quiz_dd.value)

    class_dd.on_change = on_class_change
    quiz_dd.on_change = on_quiz_change

    # --- Main Page Layout ---
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

    # Initial state
    update_results_display()

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_instructor_results_page # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_settings_page():
    """Show the settings page for instructors and admins."""
    global current_page, sidebar_drawer, current_user
    global current_view_handler
    current_page.clean()

    # This page serves as a profile/settings page for non-examinee roles
    sidebar = create_sidebar(current_user['role'], "settings")

    # --- Change Password Form ---
    current_password_field = create_text_input("Mật khẩu hiện tại", password=True, can_reveal=True)
    new_password_field = create_text_input("Mật khẩu mới", password=True, can_reveal=True)
    confirm_password_field = create_text_input("Xác nhận mật khẩu mới", password=True, can_reveal=True)
    password_message_text = ft.Text("", size=Typography.SIZE_SM)

    def handle_save_password(e):
        current_pass = current_password_field.value
        new_pass = new_password_field.value
        confirm_pass = confirm_password_field.value

        # Validation
        if not all([current_pass, new_pass, confirm_pass]):
            password_message_text.value = "Vui lòng điền đầy đủ các trường."
            password_message_text.color = Colors.ERROR
            current_page.update()
            return

        if current_pass != current_user['password']:
            password_message_text.value = "Mật khẩu hiện tại không đúng."
            password_message_text.color = Colors.ERROR
            current_password_field.value = ""
            current_page.update()
            return

        if new_pass != confirm_pass:
            password_message_text.value = "Mật khẩu mới không khớp."
            password_message_text.color = Colors.ERROR
            new_password_field.value = ""
            confirm_password_field.value = ""
            current_page.update()
            return

        # Update password
        mock_users[current_user['username']]['password'] = new_pass
        current_user['password'] = new_pass # Update current session user

        password_message_text.value = "Đổi mật khẩu thành công!"
        password_message_text.color = Colors.SUCCESS
        current_password_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        current_page.update()

    # --- User Info ---
    info_details = [
        ft.Row([ft.Text("Username:", weight=ft.FontWeight.W_600), ft.Text(current_user['username'])]),
        ft.Divider(),
        ft.Row([ft.Text("Vai trò:", weight=ft.FontWeight.W_600), ft.Text(current_user['role'].title())]),
    ]

    if current_user['role'] == 'instructor':
        assigned_classes = [c['name'] for c in mock_classes if c.get('instructor_id') == current_user['id']]
        if assigned_classes:
            info_details.append(ft.Divider())
            info_details.append(ft.Row([ft.Text("Các lớp phụ trách:", weight=ft.FontWeight.W_600), ft.Text(", ".join(assigned_classes))]))

    # --- Main page content ---
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
                        # User Info Card
                        create_card(
                            content=ft.Column([
                                create_section_title("Thông tin tài khoản"),
                                ft.Container(height=Spacing.LG),
                                *info_details
                            ]),
                            padding=Spacing.XL
                        ),

                        # Change Password Card
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

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_settings_page # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_class_management():
    """Show the class management page for admins."""
    global current_page, sidebar_drawer
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "classes")

    # --- Search and Filter Logic ---
    search_field = create_text_input("Search by class name...", width=300, icon=ft.Icons.SEARCH)
    class_list_view = ft.Column(spacing=Spacing.LG)

    def update_class_list(e=None):
        search_term = search_field.value.lower() if search_field.value else ""
        
        filtered_classes = [
            c for c in mock_classes if search_term in c['name'].lower()
        ]

        class_list_view.controls.clear()
        if filtered_classes:
            for cls in filtered_classes:
                class_list_view.controls.append(create_class_card(cls))
        else:
            class_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=Colors.GRAY_400),
                    ft.Container(height=Spacing.SM),
                    ft.Text("No classes found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        current_page.update()

    search_field.on_change = update_class_list

    def handle_delete_class(class_id_to_delete):
        def on_delete(e):
            global mock_classes
            mock_classes = [c for c in mock_classes if c['id'] != class_id_to_delete]
            show_class_management() # Tải lại trang
        return on_delete

    # --- Form tạo lớp học (ẩn ban đầu) ---
    class_name_field = create_text_input("Tên lớp học", width=400)
    
    # Lấy danh sách giảng viên để tạo Dropdown
    instructors = [user for user in mock_users.values() if user['role'] == 'instructor']
    instructor_dropdown = ft.Dropdown(
        label="Chọn giảng viên",
        width=400,
        border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300,
        focused_border_color=Colors.PRIMARY,
        options=[
            ft.dropdown.Option(key=ins['id'], text=ins['username']) for ins in instructors
        ]
    )
    class_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

    def show_create_form(e):
        class_form_container.visible = True
        class_name_field.value = ""
        instructor_dropdown.value = None
        class_error_text.value = ""
        current_page.update()

    def hide_create_form(e):
        class_form_container.visible = False
        current_page.update()

    def handle_create_class(e):
        class_name = class_name_field.value or ""
        instructor_id = instructor_dropdown.value

        if not class_name.strip():
            class_error_text.value = "Tên lớp học là bắt buộc."
            current_page.update()
            return
        if not instructor_id:
            class_error_text.value = "Vui lòng chọn một giảng viên."
            current_page.update()
            return

        # Thêm vào dữ liệu mẫu
        if mock_classes:
            new_id = max(c['id'] for c in mock_classes) + 1
        else:
            new_id = 1
        new_class = {
            'id': new_id,
            'name': class_name.strip(),
            'instructor_id': int(instructor_id)
        }
        mock_classes.append(new_class)

        class_error_text.value = ""
        hide_create_form(e)
        show_class_management()  # Tải lại trang để hiển thị lớp mới

    class_form_container = create_card(
        content=ft.Column([
            create_section_title("Tạo Lớp học mới"),
            ft.Container(height=Spacing.LG),
            class_name_field,
            ft.Container(height=Spacing.LG),
            instructor_dropdown,
            ft.Container(height=Spacing.MD),
            class_error_text,
            ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Tạo Lớp", on_click=handle_create_class, width=120),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Hủy", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    class_form_container.visible = False

    # --- Danh sách các lớp học hiện có ---
    def create_class_card(cls):
        """Helper function to create a class card."""
        instructor_name = next((user['username'] for user in mock_users.values() if user['id'] == cls['instructor_id']), "N/A")
        class_card = create_card(
            content=ft.Row([
                ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=Colors.PRIMARY, size=32),
                ft.Container(width=Spacing.LG),
                ft.Column([
                    ft.Text(cls['name'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
                    ft.Text(f"Giảng viên: {instructor_name}", color=Colors.TEXT_SECONDARY),
                ], expand=True),
                create_secondary_button("Xóa", width=80, on_click=handle_delete_class(cls['id'])),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=Spacing.LG
        )
        return class_card

    # Initial population of the list
    update_class_list()
    # --- Nội dung chính của trang ---
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
                    ft.Container(height=Spacing.XXL),
                    class_form_container,
                    ft.Container(height=Spacing.XL),
                    create_section_title("Danh sách Lớp học"),
                    ft.Container(height=Spacing.LG),
                    class_list_view if class_list_view.controls else ft.Text("Chưa có lớp học nào.")
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_class_management # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

def show_user_management():
    """Show the user management page for admins."""
    global current_page, sidebar_drawer
    global current_view_handler
    current_page.clean()

    sidebar = create_sidebar(current_user['role'], "users")

    # --- Search and Filter Logic ---
    search_field = create_text_input("Search by username...", width=300, icon=ft.Icons.SEARCH)
    role_filter_dropdown = ft.Dropdown(
        label="Filter by Role",
        width=200,
        value="all",
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

        # Filter users
        filtered_users = mock_users.items()
        if search_term:
            filtered_users = [(u, d) for u, d in filtered_users if search_term in d['username'].lower()]
        if selected_role and selected_role != "all":
            filtered_users = [(u, d) for u, d in filtered_users if d['role'] == selected_role]

        user_list_view.controls.clear()
        if filtered_users:
            for username, user_data in filtered_users:
                user_list_view.controls.append(create_user_card(username, user_data))
        else:
            user_list_view.controls.append(create_card(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON_SEARCH, size=48, color=Colors.GRAY_400),
                    ft.Container(height=Spacing.SM),
                    ft.Text("No users found", size=Typography.SIZE_LG, weight=ft.FontWeight.W_600, color=Colors.TEXT_SECONDARY),
                    ft.Text("Your search did not match any users.", size=Typography.SIZE_SM, color=Colors.TEXT_MUTED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=Spacing.XXXXL
            ))
        
        current_page.update()

    search_field.on_change = update_user_list
    role_filter_dropdown.on_change = update_user_list


    # --- Edit User Dialog ---
    def open_edit_dialog(user_to_edit):
        username = user_to_edit['username']
        
        # Controls for the dialog
        edit_password_field = create_text_input("New Password (leave blank to keep unchanged)", password=True, width=400)
        
        edit_role_dropdown = ft.Dropdown(
            label="Select Role",
            width=400,
            value=user_to_edit['role'],
            options=[
                ft.dropdown.Option(key='instructor', text='Instructor'),
                ft.dropdown.Option(key='admin', text='Admin'),
                ft.dropdown.Option(key='examinee', text='Examinee (Student)'),
            ]
        )

        edit_class_assignment_dropdown = ft.Dropdown(
            label="Gán vào lớp học (tùy chọn)",
            width=400,
            value=user_to_edit.get('class_id'),
            options=[ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in mock_classes],
            visible=(user_to_edit['role'] == 'examinee')
        )

        def on_edit_role_change(e):
            edit_class_assignment_dropdown.visible = e.control.value == 'examinee'
            edit_dialog.content.update()
        edit_role_dropdown.on_change = on_edit_role_change

        def save_changes(e):
            # Get new values
            new_password = edit_password_field.value.strip()
            new_role = edit_role_dropdown.value
            new_class_id = edit_class_assignment_dropdown.value if new_role == 'examinee' else None

            # Update mock data
            if new_password:
                mock_users[username]['password'] = new_password
            
            mock_users[username]['role'] = new_role
            mock_users[username]['class_id'] = int(new_class_id) if new_class_id else None

            # Close dialog and refresh page
            edit_dialog.open = False
            current_page.update()
            show_user_management()

        def close_dialog(e):
            edit_dialog.open = False
            current_page.update()

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit User: {username}"),
            content=ft.Column([
                edit_password_field,
                edit_role_dropdown,
                edit_class_assignment_dropdown
            ], tight=True),
            actions=[
                create_secondary_button("Cancel", on_click=close_dialog),
                create_primary_button("Save Changes", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        current_page.dialog = edit_dialog
        edit_dialog.open = True
        current_page.update()


    # --- Form to create a new user (initially hidden) ---
    username_field = create_text_input("Username", width=400)
    password_field = create_text_input("Password", password=True, width=400)
    role_dropdown = ft.Dropdown(
        label="Select Role",
        width=400,
        border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300,
        focused_border_color=Colors.PRIMARY,
        options=[
            ft.dropdown.Option(key='instructor', text='Instructor'),
            ft.dropdown.Option(key='admin', text='Admin'),
            ft.dropdown.Option(key='examinee', text='Examinee (Student)'),
        ]
    )
    # --- Thêm Dropdown để gán lớp học, ẩn ban đầu ---
    class_assignment_dropdown = ft.Dropdown(
        label="Gán vào lớp học (tùy chọn)",
        width=400,
        border_radius=BorderRadius.MD,
        border_color=Colors.GRAY_300,
        focused_border_color=Colors.PRIMARY,
        options=[
            ft.dropdown.Option(key=cls['id'], text=cls['name']) for cls in mock_classes
        ],
        visible=False # Chỉ hiển thị khi role là 'examinee'
    )
    user_error_text = ft.Text("", color=Colors.ERROR, size=Typography.SIZE_SM)

    def show_create_form(e):
        user_form_container.visible = True
        username_field.value = ""
        password_field.value = ""
        role_dropdown.value = None
        class_assignment_dropdown.value = None
        class_assignment_dropdown.visible = False
        user_error_text.value = ""
        current_page.update()

    def hide_create_form(e):
        user_form_container.visible = False
        current_page.update()
    
    def on_role_change(e):
        # Hiển thị dropdown lớp học nếu vai trò là 'examinee'
        is_examinee = role_dropdown.value == 'examinee'
        class_assignment_dropdown.visible = is_examinee
        current_page.update()
    role_dropdown.on_change = on_role_change

    def handle_create_user(e):
        username = username_field.value or ""
        password = password_field.value or ""
        role = role_dropdown.value

        if not username.strip() or not password.strip():
            user_error_text.value = "Username and password are required."
            current_page.update()
            return
        if not role:
            user_error_text.value = "Please select a role."
            current_page.update()
            return
        if username.strip() in mock_users:
            user_error_text.value = f"Username '{username.strip()}' already exists."
            current_page.update()
            return

        # Add to mock data
        if mock_users:
            new_id = max(user['id'] for user in mock_users.values()) + 1
        else:
            new_id = 1

        new_user = {
            'id': new_id,
            'username': username.strip(),
            'password': password.strip(),
            'role': role,
            'class_id': int(class_assignment_dropdown.value) if role == 'examinee' and class_assignment_dropdown.value else None
        }
        mock_users[username.strip()] = new_user

        user_error_text.value = ""
        hide_create_form(e)
        show_user_management()  # Refresh the page

    def handle_delete_user(username_to_delete):
        def on_delete(e):
            if username_to_delete in mock_users:
                del mock_users[username_to_delete]
            show_user_management() # Refresh
        return on_delete

    user_form_container = create_card(
        content=ft.Column([
            create_section_title("Create New User"),
            ft.Container(height=Spacing.LG),
            username_field,
            ft.Container(height=Spacing.LG),
            password_field,
            ft.Container(height=Spacing.LG),
            role_dropdown,
            ft.Container(height=Spacing.LG),
            class_assignment_dropdown, # Thêm dropdown lớp học vào form
            ft.Container(height=Spacing.MD),
            user_error_text,
            ft.Container(height=Spacing.XL),
            ft.Row([
                create_primary_button("Create User", on_click=handle_create_user, width=120),
                ft.Container(width=Spacing.MD),
                create_secondary_button("Cancel", on_click=hide_create_form, width=100)
            ])
        ]),
        padding=Spacing.XXL
    )
    user_form_container.visible = False

    # --- List of existing users ---
    def create_user_card(username, user_data):
        """Helper function to create a user card."""
        details_column = [
            ft.Text(user_data['username'], size=Typography.SIZE_LG, weight=ft.FontWeight.W_600),
            ft.Text(f"Role: {user_data['role'].title()}", color=Colors.TEXT_SECONDARY),
        ]
        # Nếu là sinh viên, hiển thị thêm thông tin lớp học
        if user_data['role'] == 'examinee' and user_data.get('class_id'):
            class_name = next((c['name'] for c in mock_classes if c['id'] == user_data['class_id']), "Chưa gán lớp")
            details_column.append(
                ft.Text(f"Lớp: {class_name}", color=Colors.TEXT_MUTED, size=Typography.SIZE_SM)
            )

        user_card = create_card(
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON_OUTLINE, color=Colors.PRIMARY, size=32),
                ft.Container(width=Spacing.LG),
                ft.Column(details_column, expand=True, spacing=2),
                create_primary_button("Edit", width=80, on_click=lambda e, u=user_data: open_edit_dialog(u)),
                ft.Container(width=Spacing.SM),
                create_secondary_button("Delete", width=80, on_click=handle_delete_user(username)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=Spacing.LG
        )
        return user_card

    # Initial population of the list
    update_user_list()
    # --- Main page content ---
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
                            search_field,
                            role_filter_dropdown,
                            create_primary_button("Add New User", on_click=show_create_form, width=150)
                        ], spacing=Spacing.MD)
                    ]),
                    ft.Container(height=Spacing.XXL),
                    user_form_container,
                    ft.Container(height=Spacing.XL),
                    create_section_title("All Users"),
                    ft.Container(height=Spacing.LG),
                    user_list_view if user_list_view.controls else ft.Text("No users found.")
                ]),
                padding=Spacing.XXXXL, expand=True, bgcolor=Colors.GRAY_50
            )
        ]),
        expand=True
    )

    # Responsive layout
    sidebar_drawer = ft.NavigationDrawer(controls=[sidebar])
    current_page.drawer = sidebar_drawer
    current_page.appbar = create_app_bar()
    current_view_handler = show_user_management # Set the current view handler

    if current_page.width >= 1000:
        current_page.add(ft.Row([sidebar, main_content], expand=True))
        current_page.appbar.visible = False
    else:
        current_page.add(main_content)
        current_page.appbar.visible = True
    current_page.update()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main_page(page: ft.Page):
    """Main application entry point""" 
    global current_page, current_user, sidebar_drawer, current_view_handler
    current_page = page
    
    # Page configuration
    page.title = "Modern Quiz App"
    page.theme_mode = "light"
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 800
    page.window_min_height = 600
    page.padding = 0
    page.spacing = 0
    
    def handle_resize(e):
        """Handle window resize to show/hide sidebar."""
        # If a view handler is set, call it to redraw the page.
        # This is a much cleaner way to handle responsiveness.
        if current_view_handler:
            current_view_handler()
            return

    page.on_resize = handle_resize

    # --- BỎ QUA ĐĂNG NHẬP ĐỂ PHÁT TRIỂN GIAO DIỆN ---
    # Để bỏ qua màn hình đăng nhập, hãy làm theo các bước sau:
    # 1. Đặt người dùng hiện tại (current_user) thành một người dùng mẫu.
    # 2. Gọi hàm hiển thị dashboard tương ứng.
    # 3. Để bật lại trang đăng nhập, hãy xóa/bình luận các dòng dưới và bỏ bình luận dòng `show_login()`.

    # --- Chế độ phát triển ---
    current_user = mock_users['THEHY']  # Đăng nhập với tư cách 'examinee' 
    show_examinee_dashboard()              # Đi thẳng vào dashboard của sinh viên
    # current_user = mock_users['admin']  # Đăng nhập với tư cách 'admin'
    # show_instructor_dashboard()         # Đi thẳng vào dashboard

    # --- Chế độ hoạt động bình thường ---
    # show_login()                       # Bắt đầu từ trang đăng nhập

if __name__ == "__main__":
    ft.app(target=main_page)   
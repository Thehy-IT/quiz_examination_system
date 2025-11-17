# QUIZ_EXAMINATION_SYSTEM/quiz_app/data/mock_data.py

"""
File này chứa tất cả dữ liệu giả (mock data) cho ứng dụng.
Việc tập trung dữ liệu vào một nơi giúp dễ dàng quản lý, chỉnh sửa
và sau này có thể thay thế bằng kết nối cơ sở dữ liệu thực tế.
"""

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

# có các file...
# show_answer_after_quiz:file lưu trạng thái bật/tắt xem đáp án, kiểu boolean (mặc định false)
#  ...
mock_quizzes = [
    {'id': 1, 'title': 'Python Basics', 'description': 'Learn Python fundamentals', 'created_by': 1, 'created_at': '2024-01-15', 'creator': 'instructor', 'questions_count': 5, 'start_time': '2025-01-15 14:20', 'duration_minutes': 10, 'class_id': 1, 'password': None, 'is_active': True, 'shuffle_questions': True, 'shuffle_answers': True, 'show_answers_after_quiz': False},
    {'id': 2, 'title': 'Web Development', 'description': 'HTML, CSS, JavaScript basics', 'created_by': 1, 'created_at': '2024-01-14', 'creator': 'instructor', 'questions_count': 8, 'start_time': '2024-01-20 10:00', 'duration_minutes': 20, 'class_id': 2, 'password': None, 'is_active': True, 'shuffle_questions': False, 'shuffle_answers': True, 'show_answers_after_quiz': False},
    {'id': 3, 'title': 'Data Structures', 'description': 'Arrays, Lists, Trees, Algorithms', 'created_by': 2, 'created_at': '2024-01-13', 'creator': 'admin', 'questions_count': 12, 'start_time': '2024-01-22 14:00', 'duration_minutes': 30, 'class_id': 1, 'password': 'dsa', 'is_active': False, 'shuffle_questions': True, 'shuffle_answers': False, 'show_answers_after_quiz': False}
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
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
# - role: vai trò ('instructor', 'admin', 'examinee'). Vai trò này quyết định giao diện và quyền hạn của người dùng.
# - class_id: ID của lớp học mà sinh viên thuộc về (chỉ dành cho role 'examinee').
# Mục đích: Dùng để test chức năng đăng nhập, phân quyền và hiển thị dữ liệu phù hợp cho từng người dùng.
mock_users = {
    'instructor': {'id': 1, 'username': 'instructor', 'password': 'instructor', 'role': 'instructor'},
    'admin': {'id': 2, 'username': 'admin', 'password': 'admin', 'role': 'admin'},
    # 'student' là một tài khoản cũ, có thể dùng để test hoặc xóa đi.
    'student': {'id': 3, 'username': 'student', 'password': 'student', 'role': 'examinee', 'class_id': 1},
    # dùng tải khoản sau để test nhiều người thi
    'THEHY': {'id': 4, 'username': 'THEHY', 'password': 'THEHY', 'role': 'examinee', 'class_id': 1},
    'TAI': {'id': 5, 'username': 'TAI', 'password': 'TAI', 'role': 'examinee', 'class_id': 2},
    'HUNG': {'id': 6, 'username': 'HUNG', 'password': 'HUNG', 'role': 'examinee', 'class_id': 2},
    'HUY': {'id': 7, 'username': 'HUY', 'password': 'HUY', 'role': 'examinee', 'class_id': None},
}

# mock_quizzes: Một list các object, mỗi object đại diện cho một bài thi.
# Các thuộc tính quan trọng:
# - id: ID duy nhất của quiz
# - title: tiêu đề quiz
# - description: mô tả quiz
# - created_by: ID của người tạo (liên kết với mock_users)
# - questions_count: số câu hỏi trong quiz
# - start_time: thời gian bắt đầu (YYYY-MM-DD HH:MM)
# - end_time: thời gian kết thúc (tùy chọn)
# - duration_minutes: thời gian làm bài (phút)
# - class_id: ID của lớp được gán bài thi này.
# - password: mật khẩu để vào thi (tùy chọn).
# - is_active: bài thi có đang được mở cho sinh viên hay không.
# - shuffle_questions: có xáo trộn thứ tự câu hỏi không.
# - shuffle_answers: có xáo trộn thứ tự các lựa chọn trong câu hỏi không.
# - show_answers_after_quiz: có cho phép sinh viên xem lại đáp án chi tiết sau khi nộp bài không.
# Mục đích: Hiển thị danh sách các bài thi và là cơ sở cho các chức năng quản lý, làm bài.
mock_quizzes = [
    {'id': 1, 'title': 'Python Basics', 'description': 'Learn Python fundamentals', 'created_by': 1, 'created_at': '2024-01-15', 'creator': 'instructor', 'questions_count': 5, 'start_time': '2024-01-15 14:20','end_time': '2026-01-15 14:20', 'duration_minutes': 10, 'class_id': 1, 'password': None, 'is_active': True, 'shuffle_questions': True, 'shuffle_answers': True, 'show_answers_after_quiz': True},

    {'id': 2, 'title': 'Web Development', 'description': 'HTML, CSS, JavaScript basics', 'created_by': 1, 'created_at': '2024-01-14', 'creator': 'instructor', 'questions_count': 8, 'start_time': '2024-01-20 10:00','end_time': '2026-01-17 10:00', 'duration_minutes': 20, 'class_id': 2, 'password': None, 'is_active': True, 'shuffle_questions': False, 'shuffle_answers': True, 'show_answers_after_quiz': False},

    {'id': 3, 'title': 'Data Structures', 'description': 'Arrays, Lists, Trees, Algorithms', 'created_by': 1, 'created_at': '2024-01-13', 'creator': 'instructor', 'questions_count': 12, 'start_time': '2024-01-22 14:00','end_time': '2026-01-22 14:00', 'duration_minutes': 30, 'class_id': 1, 'password': 'dsa', 'is_active': True, 'shuffle_questions': True, 'shuffle_answers': False, 'show_answers_after_quiz': False}
    
]

# mock_classes: Danh sách các lớp học.
# Mỗi object lớp học có:
# - id: ID duy nhất của lớp
# - name: tên lớp
# - instructor_id: ID của giảng viên dạy lớp (liên kết với mock_users)
# Mục đích: Dùng để phân nhóm sinh viên, gán bài thi và quản lý bởi admin/giảng viên.
mock_classes = [
    {'id': 1, 'name': 'Lớp K22', 'instructor_id': 1},
    {'id': 2, 'name': 'Lớp SE K23', 'instructor_id': 1},
]

# mock_questions: Từ điển chứa câu hỏi cho từng quiz
# Key là quiz_id (liên kết với mock_quizzes)
# Value là một list các object câu hỏi.
# Cấu trúc này giúp truy vấn tất cả câu hỏi của một bài thi rất nhanh (O(1)).
# Mỗi câu hỏi có các thuộc tính:
# - id: ID duy nhất của câu hỏi (trong phạm vi một bài thi).
# - question_type: loại câu hỏi, quyết định cách hiển thị và chấm điểm.
# - question_text: nội dung câu hỏi
# - difficulty: độ khó của câu hỏi (Easy, Medium, Hard).
# - options: list các lựa chọn (cho 'multiple_choice' và 'multiple_select').
# - correct_answer: đáp án đúng (cho 'true_false', 'fill_in_blank').
# - answer_variations: các biến thể đáp án được chấp nhận (cho 'fill_in_blank').
# - sample_answer: đáp án mẫu để giảng viên tham khảo khi chấm (cho 'short_answer').
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
# - text: nội dung
# - read: trạng thái đã đọc (boolean)
# - timestamp: thời gian tạo
# Mục đích: Cung cấp dữ liệu cho component chuông thông báo ở header.
mock_notifications = {
    'instructor': [
        {'id': 1, 'text': 'Student "THEHY" has completed the "Python Basics" quiz.', 'read': False, 'timestamp': '2 hours ago'},
        {'id': 2, 'text': 'A new version of the app is available.', 'read': True, 'timestamp': '1 day ago'},
    ],
    'admin': [
        {'id': 3, 'text': 'Instructor "instructor" created a new quiz "Web Development".', 'read': False, 'timestamp': '1 day ago'},
    ],
    'examinee': [
        {'id': 4, 'text': 'Your results for "Python Basics" are ready.', 'read': False, 'timestamp': '30 minutes ago'},
        {'id': 5, 'text': 'New quiz "Data Structures" has been added.', 'read': False, 'timestamp': '5 hours ago'},
    ],
}

# mock_activity_log: List chứa lịch sử hoạt động trên hệ thống
# Mục đích: Để admin theo dõi các sự kiện quan trọng trên dashboard.
mock_activity_log = [
    {'timestamp': '2025-07-21 10:05', 'user': 'instructor', 'action': 'đã tạo một bài thi mới', 'details': 'Web Development'},
    {'timestamp': '2025-07-21 09:30', 'user': 'THEHY', 'action': 'đã hoàn thành bài thi', 'details': 'Python Basics'},
    {'timestamp': '2025-07-20 15:00', 'user': 'admin', 'action': 'đã tạo người dùng mới', 'details': 'HUNG'},
    {'timestamp': '2025-07-20 14:00', 'user': 'admin', 'action': 'đã tạo một lớp học mới', 'details': 'Lớp Phát triển Web K12'},
]

# mock_attempts: Danh sách lưu lại tất cả các lần làm bài của sinh viên.
# Mỗi lần làm bài (attempt) sẽ có:
# - attempt_id: ID duy nhất của lần làm bài.
# - user_id, quiz_id: liên kết đến người dùng và bài thi tương ứng.
# - score, percentage: kết quả bài làm.
# - time_taken, completed_at: thông tin về thời gian.
# - user_answers: một dictionary lưu lại chi tiết câu trả lời của sinh viên cho từng câu hỏi.
# Mục đích: Để tính toán điểm số, thống kê và cho phép sinh viên/giảng viên xem lại bài làm.
mock_attempts = [
    {'attempt_id': 1, 'user_id': 3, 'quiz_id': 1, 'score': '4/5', 'percentage': 80.0, 'time_taken': '00:05:30', 'completed_at': '2025-07-21 11:00:00', 'user_answers': {1: 'A programming language', 2: True, 3: 'Guido van Rossum', 4: ['Django', 'Flask'], 5: 'Lists are mutable'}},
    {'attempt_id': 2, 'user_id': 4, 'quiz_id': 1, 'score': '3.5/5', 'percentage': 70.0, 'time_taken': '00:08:15', 'completed_at': '2025-07-21 11:05:00', 'user_answers': {1: 'A snake', 2: True, 3: 'guido', 4: ['Django', 'Flask', 'FastAPI'], 5: 'Lists are mutable and use square brackets, while tuples are immutable and use parentheses.'}},
    {'attempt_id': 3, 'user_id': 4, 'quiz_id': 2, 'score': '7/8', 'percentage': 87.5, 'time_taken': '00:15:45', 'completed_at': '2025-07-22 14:30:00', 'user_answers': {}},
]
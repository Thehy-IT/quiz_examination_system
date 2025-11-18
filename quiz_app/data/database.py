# module quản lý các thao tác cơ sở dữ liệu  SQLite 
# module xử lý việc tạo bảng, thêm, xóa, sửa và truy vấn dữ liệu câu hỏi
import sqlite3
import json
import datetime

DB_FILE = "quiz_app.db"

def get_db_connection():
    """Tạo kết nối đến CSDL, cho phép truy cập các cột bằng tên."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo các bảng trong CSDL nếu chúng chưa tồn tồn tại."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bảng lưu tất cả câu hỏi (Ngân hàng câu hỏi)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        question_type TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium',
        options TEXT, -- Lưu dưới dạng JSON
        correct_answer TEXT, -- Lưu dưới dạng JSON
        created_by_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Bảng lưu thông tin các bài quiz
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        class_id INTEGER,
        created_by_id INTEGER NOT NULL,
        start_time TEXT,
        end_time TEXT,
        duration_minutes INTEGER,
        password TEXT,
        shuffle_questions BOOLEAN DEFAULT 0,
        shuffle_answers BOOLEAN DEFAULT 0,
        show_answers_after_quiz BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Bảng liên kết giữa quiz và questions (quan hệ nhiều-nhiều)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        PRIMARY KEY (quiz_id, question_id),
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def get_all_questions_from_db(search_term="", difficulty_filter="all"):
    """Lấy câu hỏi từ ngân hàng với bộ lọc và tìm kiếm."""
    conn = get_db_connection()
    query = "SELECT * FROM questions WHERE question_text LIKE ?"
    params = [f"%{search_term}%"]

    if difficulty_filter != "all":
        query += " AND difficulty = ?"
        params.append(difficulty_filter)
        
    query += " ORDER BY created_at DESC"

    questions = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(q) for q in questions]

def create_quiz_with_questions(quiz_details, question_ids):
    """Tạo một quiz mới và liên kết nó với các câu hỏi đã chọn."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Thêm quiz mới vào bảng quizzes
    cursor.execute("""
        INSERT INTO quizzes (title, description, class_id, created_by_id, start_time, end_time, duration_minutes, password, shuffle_questions, shuffle_answers, show_answers_after_quiz)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        quiz_details['title'], quiz_details['description'], quiz_details['class_id'],
        quiz_details['created_by_id'], quiz_details['start_time'], quiz_details['end_time'],
        quiz_details['duration_minutes'], quiz_details['password'], quiz_details['shuffle_questions'],
        quiz_details['shuffle_answers'], quiz_details['show_answers_after_quiz']
    ))
    new_quiz_id = cursor.lastrowid

    # 2. Liên kết quiz với các câu hỏi trong bảng quiz_questions
    if new_quiz_id and question_ids:
        for question_id in question_ids:
            cursor.execute("INSERT INTO quiz_questions (quiz_id, question_id) VALUES (?, ?)", (new_quiz_id, question_id))

    conn.commit()
    conn.close()
    return new_quiz_id

# Bạn có thể thêm các hàm khác để thêm/sửa/xóa câu hỏi vào ngân hàng ở đây
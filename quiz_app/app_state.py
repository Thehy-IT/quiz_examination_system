# QUIZ_EXAMINATION_SYSTEM/quiz_app/app_state.py

"""
File này chứa các biến trạng thái toàn cục của ứng dụng.
Việc tách các biến này ra một file riêng giúp:
1. Dễ dàng quản lý trạng thái chung (current_user, current_page).
2. Tránh lỗi "circular import" khi các module khác cần truy cập vào cùng một trạng thái.
3. Giúp file main.py và các module khác gọn gàng hơn.
"""

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
flagged_questions = set() # NEW: Stores flagged question IDs
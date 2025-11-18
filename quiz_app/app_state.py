# QUIZ_EXAMINATION_SYSTEM/quiz_app/app_state.py

"""
File này đóng vai trò như "bộ não" trung tâm, lưu trữ tất cả các biến trạng thái toàn cục (global state) của ứng dụng.
Việc tách các biến này ra một file riêng là một design pattern rất hay, giúp team mình:
1. Quản lý trạng thái chung (như người dùng đang đăng nhập, trang hiện tại) một cách tập trung, dễ dàng truy cập và thay đổi.
2. Ngăn chặn lỗi "circular import" (import vòng) - một vấn đề kinh điển khi các module phụ thuộc lẫn nhau.
3. Giữ cho file main.py và các module khác sạch sẽ, chỉ tập trung vào logic chính của chúng.
"""

# =============================================================================
# GLOBAL STATE
# =============================================================================
# Khởi tạo các biến toàn cục để theo dõi trạng thái chung của ứng dụng.
# Mấy biến này sẽ được các module khác import và sử dụng.

current_view_handler = None # Biến này lưu một tham chiếu đến hàm "vẽ lại" giao diện hiện tại. Rất hữu ích khi cần refresh UI từ một module khác.
current_user = None         # Lưu thông tin của người dùng sau khi đăng nhập thành công. Dùng để xác thực và cá nhân hóa trải nghiệm.
current_page = None         # Lưu tên hoặc ID của trang/màn hình hiện tại mà người dùng đang xem.
sidebar_drawer = None       # Giữ tham chiếu đến đối tượng widget sidebar (ngăn kéo điều hướng), để có thể đóng/mở từ bất kỳ đâu.

# =============================================================================
# QUIZ TAKING STATE
# =============================================================================
# Các biến này đặc biệt dành cho trạng thái khi sinh viên đang làm bài thi.
# Chúng cần được reset lại mỗi khi bắt đầu một bài thi mới.

current_question_index = 0  # Index của câu hỏi hiện tại trong danh sách câu hỏi của bài thi.
user_answers = {}           # Dictionary để lưu câu trả lời của người dùng, dạng {question_id: user_answer}.
quiz_questions = []         # List chứa tất cả các đối tượng câu hỏi cho bài thi hiện tại.
quiz_start_time = None      # Ghi lại thời điểm bắt đầu làm bài, dùng để tính thời gian còn lại.
quiz_timer_thread = None    # Biến này sẽ giữ thread (luồng) của đồng hồ đếm ngược, để có thể quản lý (start, stop).
flagged_questions = set()   # Dùng kiểu 'set' để lưu ID của các câu hỏi được người dùng "đánh dấu" để xem lại. 'Set' giúp truy cập và thêm/xóa nhanh hơn list.
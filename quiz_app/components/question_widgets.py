# QUIZ_EXAMINATION_SYSTEM/quiz_app/components/question_widgets.py

# File này là một "xưởng sản xuất" các widget câu hỏi.
# Mỗi hàm ở đây chịu trách nhiệm tạo ra một component giao diện hoàn chỉnh cho một loại câu hỏi cụ thể.
# Việc tách riêng ra như này giúp code ở các file view (như examinee_views.py) gọn gàng hơn rất nhiều.

import flet as ft
import random

# Import các hằng số và các hàm UI helper đã tách
from ..utils.constants import Colors, Spacing, Typography
from .ui_helpers import create_text_input, create_card

# =============================================================================
# QUESTION TYPE COMPONENTS
# =============================================================================

def create_multiple_choice_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
    """Tạo component cho câu hỏi trắc nghiệm (chọn một).
    - is_review: Cờ quan trọng để xác định giao diện đang ở chế độ "làm bài" hay "xem lại đáp án".
    - user_answer: Dùng để khôi phục lại lựa chọn của người dùng khi họ quay lại câu hỏi.
    - show_correct_answers: Dùng trong chế độ review, quyết định có hiển thị đáp án đúng hay không.
    """
    options_group = ft.RadioGroup(content=ft.Column([]))
    
    options_data = question.get('options', [])
    
    # Xáo trộn các lựa chọn nếu quiz có bật tính năng này. Tăng tính khách quan cho bài thi.
    if shuffle_answers:
        random.shuffle(options_data)

    # Create radio options
    options = []
    for i, option in enumerate(options_data):
        # Dùng chính `option_text` làm `value` cho Radio button.
        option_text = option['option_text']
        is_correct = option['is_correct']
        
        radio = ft.Radio(
            value=option_text,
            label=option_text,
            label_style=ft.TextStyle(size=Typography.SIZE_BASE)
        )

        # Logic cốt lõi: thay đổi giao diện dựa trên cờ `is_review`.
        if is_review:
            radio.disabled = True
            radio.value = user_answer

            # Cung cấp phản hồi trực quan (visual feedback) cho người dùng.
            # Đây là một phần quan trọng của trải nghiệm người dùng (UX).
            review_indicator = ft.Container(width=24) # Dành không gian cho icon, giữ cho layout thẳng hàng.
            if is_correct:
                # Highlight đáp án đúng.
                radio.label_style.color = Colors.SUCCESS
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CHECK_CIRCLE, color=Colors.SUCCESS, size=20)
            elif option_text == user_answer: 
                # Đánh dấu đáp án sai mà người dùng đã chọn.
                radio.label_style.color = Colors.ERROR
                radio.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CANCEL, color=Colors.ERROR, size=20)
            
            # Bọc icon và radio button trong một Row để hiển thị chúng cạnh nhau.
            options.append(ft.Row([review_indicator, radio], spacing=Spacing.SM))
        else:
            options.append(radio)

    options_group.content = ft.Column(options, spacing=Spacing.MD)

    if not is_review:
        # Ở chế độ làm bài, khôi phục lại lựa chọn trước đó của người dùng (nếu có).
        options_group.value = user_answer
        # Gắn sự kiện `on_change` để thông báo cho view cha khi người dùng chọn một đáp án.
        options_group.on_change = lambda e: on_answer_change(e, e.control.value)
    else:
        options_group.value = user_answer

    explanation_content = []
    # Nếu có phần giải thích, chỉ hiển thị nó ở chế độ review.
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

def create_true_false_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
    """Tạo component cho câu hỏi Đúng/Sai. Logic tương tự câu trắc nghiệm nhưng chỉ có 2 lựa chọn."""
    true_false_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="true", label="True", label_style=ft.TextStyle(size=Typography.SIZE_BASE)),
            ft.Radio(value="false", label="False", label_style=ft.TextStyle(size=Typography.SIZE_BASE))
        ], spacing=Spacing.MD)
    )

    if is_review:
        true_false_group.disabled = True
        # Xử lý `user_answer` có thể là string "true"/"false" hoặc boolean True/False.
        user_answer_bool = user_answer if isinstance(user_answer, bool) else (str(user_answer).lower() == "true")
        true_false_group.value = "true" if user_answer_bool else "false"
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
            # Trick: Gán một control khác (Row) vào thuộc tính `label` để tùy biến giao diện.
            radio.label = ft.Row([review_indicator, ft.Text(radio.label)], spacing=Spacing.SM)

    else:
        # Khôi phục trạng thái đã chọn của người dùng.
        if user_answer is not None:
            user_answer_bool = user_answer if isinstance(user_answer, bool) else (str(user_answer).lower() == "true")
            true_false_group.value = "true" if user_answer_bool else "false"
        # Khi người dùng chọn, giá trị trả về sẽ là boolean (True/False) thay vì string.
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

def create_fill_in_blank_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
    """Tạo component cho câu hỏi điền vào chỗ trống."""
    answer_field = create_text_input("Your answer", width=400)
    
    review_content = []
    if is_review:
        answer_field.value = user_answer
        answer_field.disabled = True
        
        # Logic kiểm tra đáp án: so sánh với đáp án chính và các biến thể (variations).
        # Chuyển về chữ thường và bỏ khoảng trắng thừa để việc so sánh linh hoạt hơn.
        correct_answer = question.get('correct_answer', '').lower().strip()
        answer_variations = question.get('answer_variations', [])
        user_answer_clean = str(user_answer).lower().strip()
        is_correct = user_answer_clean == correct_answer or user_answer_clean in answer_variations

        # Thay đổi màu viền của ô input để báo hiệu đúng/sai.
        answer_field.border_color = Colors.SUCCESS if is_correct else Colors.ERROR
        review_content.append(ft.Container(height=Spacing.SM))
        review_content.append(
            ft.Text(f"Correct Answer: {question.get('correct_answer')}", color=Colors.SUCCESS, weight=ft.FontWeight.W_600)
        )

    else:
        answer_field.value = user_answer if user_answer is not None else "" # Khôi phục câu trả lời đã nhập.
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

def create_multiple_select_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
    """Tạo component cho câu hỏi chọn nhiều đáp án."""
    checkboxes = []
    options_data = question.get('options', [])

    # Tương tự câu trắc nghiệm, có thể xáo trộn các lựa chọn.
    if shuffle_answers:
        random.shuffle(options_data)

    # Dùng `set` để kiểm tra lựa chọn của người dùng hiệu quả hơn (O(1) lookup).
    user_answer_set = set(user_answer or [])
    
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
            checkbox.value = option_text in user_answer_set

            review_indicator = ft.Container(width=24)
            if is_correct:
                checkbox.label_style.color = Colors.SUCCESS
                checkbox.label_style.weight = ft.FontWeight.W_600
                review_indicator = ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=Colors.SUCCESS, size=20)
            elif option_text in user_answer_set: # Lựa chọn sai của người dùng.
                checkbox.label_style.color = Colors.ERROR
                review_indicator = ft.Icon(ft.Icons.CANCEL_OUTLINED, color=Colors.ERROR, size=20)

            checkboxes.append(ft.Row([review_indicator, checkbox], spacing=Spacing.SM))
        else:
            checkbox.value = option_text in user_answer_set # Khôi phục các lựa chọn đã check.
            checkboxes.append(checkbox)

    if not is_review:
        # Handler này sẽ thu thập tất cả các checkbox đang được chọn và gửi về dưới dạng một list.
        def on_checkbox_change(e):
            selected = [cb.data for cb in checkboxes if cb.value]
            on_answer_change(e, selected)
        
        # Gắn cùng một handler cho tất cả các checkbox.
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

def create_short_answer_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
    """Tạo component cho câu hỏi tự luận ngắn. Loại này thường cần chấm điểm thủ công."""
    answer_field = create_text_input("Your answer", width=500, multiline=True, min_lines=4)
    
    review_content = []
    if is_review:
        answer_field.value = user_answer
        answer_field.disabled = True
        answer_field.label = "Your Answer" # Thay đổi label để rõ ràng hơn.

        # Vì là chấm thủ công, ở chế độ review, ta chỉ hiển thị lại câu trả lời của người dùng
        # và đáp án mẫu (sample_answer) để giảng viên tham khảo.
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
        answer_field.value = user_answer if user_answer is not None else "" # Khôi phục câu trả lời đã nhập.
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

def create_question_by_type(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
    """Hàm "nhà máy" (Factory Function) chính.
    Hàm này đóng vai trò như một bộ điều phối, nhận vào một đối tượng `question` và
    dựa vào `question_type` để gọi hàm tạo component tương ứng.
    Đây là một design pattern rất hay, giúp code dễ mở rộng. Nếu sau này có thêm loại câu hỏi mới,
    ta chỉ cần thêm một `elif` ở đây và một hàm `create_..._question` mới.
    """
    question_type = question.get('question_type', 'multiple_choice')
    
    # Tạo một hàm `answer_handler` để truyền vào các hàm con.
    # Hàm này bọc `on_answer_change` gốc lại, bổ sung thêm `question['id']`.
    # Ở chế độ review, nó trở thành một hàm rỗng (dummy function) để không làm gì cả.
    answer_handler = (lambda e, answer_value: on_answer_change(question['id'], answer_value)) if not is_review else (lambda e, v: None)

    # Dựa vào `question_type` để gọi hàm tạo widget phù hợp.
    if question_type == 'multiple_choice':
        return create_multiple_choice_question(question, answer_handler, shuffle_answers, is_review, user_answer, show_correct_answers)
    elif question_type == 'true_false':
        return create_true_false_question(question, answer_handler, is_review, user_answer,show_correct_answers)
    elif question_type == 'fill_in_blank':
        return create_fill_in_blank_question(question, answer_handler, is_review, user_answer, show_correct_answers)
    elif question_type == 'multiple_select':
        return create_multiple_select_question(question, answer_handler, shuffle_answers, is_review, user_answer, show_correct_answers)
    elif question_type == 'short_answer':
        return create_short_answer_question(question, answer_handler, is_review, user_answer, show_correct_answers)
    else:
        # Fallback: Nếu `question_type` không xác định, mặc định hiển thị dạng trắc nghiệm.
        return create_multiple_choice_question(question, answer_handler, shuffle_answers, is_review, user_answer, show_correct_answers)
# QUIZ_EXAMINATION_SYSTEM/quiz_app/components/question_widgets.py

import flet as ft
import random

# Import các hằng số và các hàm UI helper đã tách
from ..utils.constants import Colors, Spacing, Typography
from .ui_helpers import create_text_input, create_card

# =============================================================================
# QUESTION TYPE COMPONENTS
# =============================================================================

def create_multiple_choice_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
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

def create_true_false_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
    """Create a true/false question component"""
    true_false_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="true", label="True", label_style=ft.TextStyle(size=Typography.SIZE_BASE)),
            ft.Radio(value="false", label="False", label_style=ft.TextStyle(size=Typography.SIZE_BASE))
        ], spacing=Spacing.MD)
    )

    if is_review:
        true_false_group.disabled = True
        # Chuyển user_answer về kiểu bool để so sánh
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

def create_fill_in_blank_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
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

def create_multiple_select_question(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
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

def create_short_answer_question(question, on_answer_change, is_review=False, user_answer=None, show_correct_answers=False):
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

def create_question_by_type(question, on_answer_change, shuffle_answers=False, is_review=False, user_answer=None, show_correct_answers=False):
    """Create question component based on question type"""
    question_type = question.get('question_type', 'multiple_choice')
    
    # In review mode, on_answer_change is a dummy function
    answer_handler = (lambda e, answer_value: on_answer_change(question['id'], answer_value)) if not is_review else (lambda e, v: None)

    # Chỉ truyền cờ shuffle_answers cho các loại câu hỏi có lựa chọn
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
        return create_multiple_choice_question(question, answer_handler, shuffle_answers, is_review, user_answer, show_correct_answers)
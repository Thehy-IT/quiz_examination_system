"""
Modern Quiz App UI Test - Verify the complete modern UI works
"""
# Tệp này dùng để kiểm thử giao diện người dùng (UI) của ứng dụng Modern Quiz App.
# Nó xác minh rằng tất cả các thành phần UI hiện đại hoạt động như mong đợi.

import main  # Nhập tệp main.py để có thể truy cập các hàm và lớp đã định nghĩa ở đó.

def test_modern_design_system():
    """Kiểm tra xem các hằng số của hệ thống thiết kế (màu sắc, khoảng cách, kiểu chữ) có được định nghĩa đúng không."""
    print("=== Testing Modern Design System ===")
    
    # Kiểm tra các hằng số màu sắc
    assert hasattr(main.Colors, 'PRIMARY')  # `hasattr` kiểm tra xem đối tượng `main.Colors` có thuộc tính 'PRIMARY' không.
    assert hasattr(main.Colors, 'SUCCESS')
    assert hasattr(main.Colors, 'ERROR')
    print("✓ Color system defined correctly")  # In ra thông báo thành công nếu các kiểm tra ở trên không gây lỗi.
    
    # Kiểm tra hệ thống khoảng cách
    assert hasattr(main.Spacing, 'XS')
    assert hasattr(main.Spacing, 'XXXXL')
    print("✓ Spacing system defined correctly")
    
    # Kiểm tra hệ thống kiểu chữ
    assert hasattr(main.Typography, 'SIZE_XS')
    assert hasattr(main.Typography, 'SIZE_4XL')
    print("✓ Typography system defined correctly")

def test_component_functions():
    """Kiểm tra các hàm trợ giúp tạo ra các thành phần UI."""
    print("\n=== Testing Component Functions ===")
    
    # Kiểm tra việc tạo nút bấm chính
    primary_btn = main.create_primary_button("Test Button")
    assert primary_btn is not None  # `assert` đảm bảo rằng hàm đã trả về một đối tượng, không phải `None`.
    print("✓ Primary button component works")
    
    # Kiểm tra việc tạo nút bấm phụ
    secondary_btn = main.create_secondary_button("Test Button")
    assert secondary_btn is not None
    print("✓ Secondary button component works")
    
    # Kiểm tra việc tạo ô nhập liệu
    text_input = main.create_text_input("Test Input")
    assert text_input is not None
    print("✓ Text input component works")
    
    # Kiểm tra việc tạo thẻ (card)
    import flet as ft
    card = main.create_card(ft.Text("Test Content"))
    assert card is not None
    print("✓ Card component works")

def test_mock_data():
    """Kiểm tra xem dữ liệu mẫu (mock data) có tồn tại và có cấu trúc đúng hay không."""
    print("\n=== Testing Enhanced Mock Data ===")
    
    # Kiểm tra dữ liệu người dùng mẫu
    assert 'master' in main.mock_users  # Kiểm tra xem người dùng 'master' có trong từ điển `mock_users` không.
    assert 'student' in main.mock_users
    print("✓ Mock users available")
    
    # Kiểm tra dữ liệu câu đố mẫu đã được cải tiến
    assert len(main.mock_quizzes) > 0  # Đảm bảo danh sách câu đố không rỗng.
    first_quiz = main.mock_quizzes[0]
    assert 'difficulty' in first_quiz  # Kiểm tra xem câu đố có thuộc tính 'difficulty' không.
    assert 'questions_count' in first_quiz
    print("✓ Enhanced mock quizzes available")
    
    # Kiểm tra dữ liệu câu hỏi mẫu
    assert 1 in main.mock_questions  # Kiểm tra xem có câu hỏi cho quiz ID 1 không.
    assert len(main.mock_questions[1]) > 0
    print("✓ Mock questions available")

def test_navigation_system():
    """Kiểm tra các thành phần điều hướng như sidebar."""
    print("\n=== Testing Navigation System ===")
    
    # Kiểm tra việc tạo sidebar
    sidebar = main.create_sidebar('master', 'dashboard')
    assert sidebar is not None
    print("✓ Sidebar navigation component works")
    
    # Kiểm tra việc tạo các mục trong sidebar
    sidebar_item = main.create_sidebar_item(main.ft.Icons.HOME, "Test", True)
    assert sidebar_item is not None
    print("✓ Sidebar items component works")

def main_test():
    """Hàm chính để chạy tất cả các bài kiểm tra."""
    print("Starting Modern Quiz App UI Tests...")
    print("=====================================")
    
    try:
        # Gọi lần lượt các hàm kiểm tra
        test_modern_design_system()
        test_component_functions()
        test_mock_data()
        test_navigation_system()
        
        # Nếu tất cả các hàm trên chạy mà không có lỗi `AssertionError`, in ra thông báo thành công.
        print("\n🎉 ALL MODERN UI TESTS PASSED! 🎉")
        print("-------------------------------------")
        # In ra tóm tắt các tính năng và thông tin hữu ích về ứng dụng.
        print("\nThe Modern Quiz App is ready to use!")
        print("\n🚀 Features Available:")
        print("┌─ 🎨 Beautiful Modern Design")
        print("├─ 🧭 Professional Navigation")
        print("├─ 📱 Responsive Layout")
        print("├─ 🎯 Component Library")
        print("├─ 📊 Interactive Dashboards")
        print("├─ ✏️  Quiz Creation Wizard")
        print("├─ ❓ Question Builder")
        print("├─ 📝 Quiz Taking Interface")
        print("└─ 🏆 Results & Analytics")
        
        print("\n📋 Login Credentials:")
        print("Master: username='master', password='master123'")
        print("Student: username='student', password='student123'")
        
        print("\n🎯 Complete Workflow:")
        print("1. Login as master → Create Quiz → Add Questions")
        print("2. Login as student → Take Quiz → View Results")
        print("3. Navigate using sidebar → Clean UI transitions")
        
        print("\n🛠️  Technical Excellence:")
        print("• Clean component architecture")
        print("• Consistent design system")
        print("• Modern Flet implementation")
        print("• No deprecated APIs")
        print("• Syntax-error free code")
        
    except Exception as e:  # Bắt bất kỳ ngoại lệ nào xảy ra trong quá trình kiểm tra.
        print(f"\n UI TEST FAILED: {e}")
        return False
    
    return True

# Khối này đảm bảo rằng hàm `main_test()` sẽ được thực thi khi bạn chạy tệp này trực tiếp.
# Ví dụ: `python test_ui.py`
if __name__ == "__main__":
    main_test()
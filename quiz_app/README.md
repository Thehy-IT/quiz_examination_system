# 🎯 Modern Quiz App

A beautiful, modern quiz application built with Python and Flet, featuring a clean UI design, professional navigation, and comprehensive quiz management capabilities.

## ✨ Features

### 🎨 Modern Design System
- **Clean Light Theme** - Professional, clean interface
- **Consistent Colors** - Blue primary palette with semantic colors
- **Typography Scale** - Carefully crafted text hierarchy
- **Spacing System** - Consistent 4px-based spacing
- **Component Library** - Reusable UI components

### 🧭 Professional Navigation
- **Sidebar Navigation** - Clean, role-based menu system
- **Active States** - Clear visual feedback
- **User Profile** - Avatar and role display
- **Responsive Layout** - Adapts to different screen sizes

### 👥 User Roles

#### 🎓 Master/Admin Users
- **Dashboard** - Statistics and overview
- **Quiz Management** - Create and organize quizzes
- **Question Builder** - Add multiple-choice questions
- **User Management** - Manage system users (admin only)

#### 📚 Examinee/Student Users
- **Home Dashboard** - Browse available quizzes
- **Quiz Taking** - Interactive quiz interface with progress tracking
- **Results View** - Detailed score and performance analytics
- **Attempt History** - Track quiz performance over time

### 🎯 Quiz Features
- **Multiple Choice** - 4-option questions with single correct answer
- **Progress Tracking** - Visual progress bar during quizzes
- **Time Tracking** - Automatic timing of quiz attempts
- **Score Calculation** - Instant results with percentage scoring
- **Navigation** - Previous/Next question navigation

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone or download** the quiz app files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python -m quiz_app.main
   ```

### 📋 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Instructor | `instructor` | `instructor123` |
| Examinee | `THEHY` | `student123` |
| Examinee | `student` | `student123` |

## 🎯 Complete User Workflow

### For Instructor/Admin Users:
1. **Login** with master credentials
2. **Navigate to Quiz Management** via sidebar
3. **Create New Quiz** with title and description
4. **Add Questions** with multiple-choice options
5. **Set Correct Answers** for each question
6. **View Statistics** on dashboard

### For Student Users:
1. **Login** with student credentials
2. **Browse Available Quizzes** on home dashboard
3. **Start Quiz** with progress tracking
4. **Navigate Questions** using Previous/Next buttons
5. **Submit Quiz** and view detailed results
6. **Track Performance** over multiple attempts

## 🏗️ Technical Architecture

### Design System
```python
# Color Palette
Colors.PRIMARY = "#2563eb"      # Blue primary
Colors.SUCCESS = "#10b981"      # Green success
Colors.ERROR = "#ef4444"        # Red error
Colors.WHITE = "#ffffff"        # Pure white
Colors.GRAY_* = "#..."          # Gray scale

# Spacing Scale (4px base)
Spacing.XS = 4    # Extra small
Spacing.SM = 8    # Small  
Spacing.MD = 12   # Medium
Spacing.LG = 16   # Large
Spacing.XL = 20   # Extra large
# ... up to XXXXXL = 64
```

### Component Library
- `create_primary_button()` - Main action buttons
- `create_secondary_button()` - Secondary action buttons
- `create_text_input()` - Form input fields
- `create_card()` - Content containers
- `create_sidebar()` - Navigation sidebar
- `create_badge()` - Status indicators

### Page Structure
- **Login Page** - Clean card-based authentication
- **Master Dashboard** - Statistics and quick actions
- **Quiz Management** - Create and manage quizzes
- **Question Builder** - Add questions with options
- **Examinee Dashboard** - Browse available quizzes
- **Quiz Taking** - Interactive quiz interface
- **Results Page** - Score and performance display

## 📱 UI Components

### Navigation
- **Sidebar** - Role-based navigation with active states
- **Breadcrumbs** - Page hierarchy navigation
- **Progress Bars** - Quiz completion tracking

### Forms
- **Input Fields** - Consistent styling with focus states
- **Radio Groups** - Multiple choice question options
- **Buttons** - Primary and secondary action buttons
- **Validation** - Real-time form validation

### Data Display
- **Cards** - Clean content containers
- **Statistics** - Dashboard metrics display
- **Badges** - Status and category indicators
- **Lists** - Organized content display

## 🛠️ Development Features

### Code Quality
- **No Deprecated APIs** - Uses latest Flet APIs
- **Syntax Error Free** - Carefully tested code
- **Component Architecture** - Reusable, maintainable components
- **Consistent Styling** - Design system implementation

### Testing
```bash
# Run UI component tests
python test_ui.py
```

### Mock Data
- **Sample Users** - Ready-to-use test accounts
- **Sample Quizzes** - Pre-loaded content for testing
- **Sample Questions** - Multiple-choice examples

### Development Mode
- **Skip Login**: The `main.py` file is configured to allow developers to bypass the login screen for faster UI development.
  ```python
  # In main.py, uncomment the desired user and view
  
  # As an examinee
  app_state.current_user = mock_data.mock_users['THEHY']
  show_examinee_dashboard()
  
  # As an instructor
  # app_state.current_user = mock_data.mock_users['instructor']
  # show_instructor_dashboard()
  ```

## 📂 Project Structure

```
quiz_app/
├── main.py           # Main application with UI components
├── requirements.txt  # Python dependencies
├── test_ui.py       # UI component tests
└── README.md        # This documentation
```

## 🎨 Design Highlights

### Visual Elements
- **Clean Cards** - Subtle shadows and rounded corners
- **Professional Colors** - Blue primary with semantic accents
- **Consistent Spacing** - 4px-based spacing system
- **Typography Hierarchy** - Clear text organization
- **Interactive States** - Hover and focus feedback

### User Experience
- **Intuitive Navigation** - Clear menu structure
- **Visual Feedback** - Progress indicators and status updates
- **Responsive Design** - Works on different screen sizes
- **Accessibility** - Keyboard navigation support

## 🔮 Future Enhancements

When ready to add backend functionality:
- **Database Integration** - SQLite/PostgreSQL support
- **User Authentication** - Secure login system
- **Question Types** - True/false, short answer, essay
- **Advanced Analytics** - Detailed performance metrics
- **Export Features** - PDF reports and data export
- **Real-time Updates** - Live quiz sessions

## 🤝 Contributing

This is a UI-focused implementation designed for frontend development and testing. Backend integration can be added incrementally when needed.

## 📄 License

Open source - feel free to use and modify for your projects.

---

**Built with ❤️ using Python and Flet**

*A modern, beautiful quiz application with professional UI/UX design*
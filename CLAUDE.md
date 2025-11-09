# Quiz Exam App - CLAUDE Development Guide

## Project Overview
A quiz examination application built with **Flet (Python GUI framework)** and **SQLite database**, following CLEAN code principles and MVP development approach.

## Tech Stack
- **Frontend**: Flet (Python-based GUI framework)
- **Backend**: Python with clean architecture
- **Database**: SQLite with relational design
- **Authentication**: Password hashing with role-based access control

## Architecture Pattern
```
quiz_app/
├── main.py              # Application entry point & UI logic
├── database.py          # Database operations & models
├── auth.py              # Authentication & password handling
├── requirements.txt     # Python dependencies
└── quiz.db             # SQLite database file (auto-created)
```

## Database Schema (MVP)
```sql
-- Users with role-based access
users: id, username, password_hash, role, created_at

-- Quiz metadata
quizzes: id, title, description, created_by, is_active, created_at

-- Questions belonging to quizzes
questions: id, quiz_id, question_text, correct_answer, created_at

-- Multiple choice options for questions
question_options: id, question_id, option_text, option_order, is_correct

-- User quiz attempts and scores
quiz_attempts: id, user_id, quiz_id, score, total_questions, completed_at
```

## User Roles & Permissions
- **Master**: Full access - create quizzes, manage questions, view all data
- **Admin**: Quiz management - create/edit quizzes and questions (future enhancement)
- **Examinee**: Take quizzes, view personal results only

## MVP Features
1. **Authentication System**
   - Login/logout functionality
   - Role-based dashboard routing
   - Session management

2. **Quiz Management (Master Only)**
   - Create new quizzes with title/description
   - Add multiple-choice questions (4 options each)
   - Mark correct answers
   - Activate/deactivate quizzes

3. **Quiz Taking (Examinee)**
   - View available active quizzes
   - Take quizzes with radio button selection
   - Navigate between questions
   - Submit quiz and get immediate results

4. **Results System**
   - Automatic scoring calculation
   - Display score percentage and correct/incorrect count
   - Store attempt history in database

## Development Methodology
- **Ultra-granular tasks**: 275 micro-tasks (5-10 minutes each)
- **MVP-first approach**: Working app in 25-45 hours
- **Incremental development**: Each task builds on previous ones
- **CLEAN code principles**: Simple, readable, maintainable code

## Key Design Decisions
1. **Single-file architecture for MVP**: Keep complexity low initially
2. **SQLite for simplicity**: No external database setup required
3. **Minimal UI/UX**: Clean Material Design-inspired interface
4. **Role-based routing**: Different dashboards per user type
5. **Immediate feedback**: Real-time form validation and results

## Sample Users (Auto-created)
- **master** / password: "master123" (Master role)
- **admin** / password: "admin123" (Admin role - future)
- **student** / password: "student123" (Examinee role)

## Flet Components Used
- **Page**: Main application container
- **Column/Row**: Layout management
- **TextField**: Form inputs
- **ElevatedButton**: Primary actions
- **RadioGroup**: Multiple choice selections
- **ListView**: Dynamic content lists
- **Card**: Quiz display containers
- **AppBar**: Navigation header
- **Text**: Content display

## Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Database will be created automatically on first run
```

## Future Enhancements (Post-MVP)
- Multiple question types (True/False, Fill-in-blank, Essay)
- Quiz settings (time limits, attempt limits, randomization)
- Advanced user management
- Question media support (images, videos)
- Detailed analytics and reporting
- Export functionality
- Mobile responsive design

## Learning Objectives
- **Flet GUI development**: Learn modern Python GUI framework
- **Database design**: Understand relational database structures
- **Clean architecture**: Practice separation of concerns
- **User authentication**: Implement secure login systems
- **CRUD operations**: Master Create, Read, Update, Delete patterns

## Code Style Guidelines
- Use descriptive variable names
- Keep functions small and focused
- Add comments for complex logic only
- Follow PEP 8 Python style guide
- Separate UI logic from business logic where possible

## Testing Strategy
- Manual testing after each micro-task
- Test all user flows (master and examinee)
- Verify database operations
- Check UI responsiveness
- Validate authentication security

This documentation will be updated as the project evolves through each development phase.
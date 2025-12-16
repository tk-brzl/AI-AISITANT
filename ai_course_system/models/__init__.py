"""
数据库模型模块
"""
from .database import Base, engine, SessionLocal, init_db
from .user import User
from .course import Course, CourseEnrollment, CourseDocument
from .qa import QARecord
from .quiz import Quiz, Question, QuizAttempt, Answer

__all__ = [
    'Base', 'engine', 'SessionLocal', 'init_db',
    'User', 'Course', 'CourseEnrollment', 'CourseDocument',
    'QARecord', 'Quiz', 'Question', 'QuizAttempt', 'Answer'
]

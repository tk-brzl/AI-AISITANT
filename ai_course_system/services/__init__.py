"""
业务逻辑服务模块
"""
from .ai_service import AIService
from .document_service import DocumentService
from .course_service import CourseService
from .quiz_service import QuizService
from .qa_service import QAService

__all__ = ['AIService', 'DocumentService', 'CourseService', 'QuizService', 'QAService']

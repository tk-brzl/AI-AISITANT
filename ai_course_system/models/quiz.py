"""
测验相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Quiz(Base):
    """测验表"""
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    knowledge_point = Column(String(200))  # 知识点
    time_limit = Column(Integer, default=30)  # 时间限制（分钟）
    created_at = Column(DateTime, default=datetime.now)

    # 关系
    course = relationship("Course", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"


class Question(Base):
    """题目表"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_type = Column(String(20), nullable=False)  # 'choice', 'true_false', 'short_answer'
    question_text = Column(Text, nullable=False)
    options = Column(Text)  # JSON格式存储选项
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text)  # 答案解析
    points = Column(Float, default=10.0)

    # 关系
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

    def __repr__(self):
        return f"<Question(id={self.id}, type='{self.question_type}')>"


class QuizAttempt(Base):
    """测验尝试记录表"""
    __tablename__ = 'quiz_attempts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Float)
    total_points = Column(Float)
    started_at = Column(DateTime, default=datetime.now)
    submitted_at = Column(DateTime)
    is_completed = Column(Boolean, default=False)

    # 关系
    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("User", back_populates="quiz_attempts")
    answers = relationship("Answer", back_populates="attempt", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, student_id={self.student_id}, score={self.score})>"


class Answer(Base):
    """学生答案表"""
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(Integer, ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    student_answer = Column(Text)
    is_correct = Column(Boolean)
    points_earned = Column(Float, default=0.0)
    ai_feedback = Column(Text)  # AI批改反馈

    # 关系
    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, is_correct={self.is_correct})>"

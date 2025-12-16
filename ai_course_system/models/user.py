"""
用户模型
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    real_name = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)  # 'student' or 'teacher'
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

    # 关系
    courses_created = relationship("Course", back_populates="teacher", foreign_keys="Course.teacher_id")
    enrollments = relationship("CourseEnrollment", back_populates="student")
    qa_records = relationship("QARecord", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")

    def set_password(self, password):
        """设置密码（哈希存储）"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """验证密码"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def is_teacher(self):
        """判断是否为教师"""
        return self.role == 'teacher'

    def is_student(self):
        """判断是否为学生"""
        return self.role == 'student'

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

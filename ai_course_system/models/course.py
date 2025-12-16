"""
课程相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    teacher = relationship("User", back_populates="courses_created", foreign_keys=[teacher_id])
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    documents = relationship("CourseDocument", back_populates="course", cascade="all, delete-orphan")
    qa_records = relationship("QARecord", back_populates="course")
    quizzes = relationship("Quiz", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}')>"


class CourseEnrollment(Base):
    """课程选课关系表"""
    __tablename__ = 'course_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.now)

    # 关系
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"<CourseEnrollment(student_id={self.student_id}, course_id={self.course_id})>"


class CourseDocument(Base):
    """课程文档表"""
    __tablename__ = 'course_documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    file_type = Column(String(20))  # 'pdf', 'docx', 'txt'
    content = Column(Text)  # 提取的文本内容
    uploaded_at = Column(DateTime, default=datetime.now)

    # 关系
    course = relationship("Course", back_populates="documents")

    def __repr__(self):
        return f"<CourseDocument(id={self.id}, filename='{self.filename}')>"

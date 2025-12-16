"""
问答记录模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class QARecord(Base):
    """问答记录表"""
    __tablename__ = 'qa_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context = Column(Text)  # 检索到的相关文档内容
    created_at = Column(DateTime, default=datetime.now)

    # 关系
    user = relationship("User", back_populates="qa_records")
    course = relationship("Course", back_populates="qa_records")

    def __repr__(self):
        return f"<QARecord(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"

"""
课程管理服务
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from models.course import Course, CourseEnrollment, CourseDocument
from models.user import User
from auth.decorators import require_role
from auth.permissions import PermissionHelper
from .document_service import DocumentService
from datetime import datetime


class CourseService:
    """课程管理服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.doc_service = DocumentService()

    def create_course(self, teacher_id: int, name: str, description: str = ""):
        """
        创建课程（仅教师）
        
        Args:
            teacher_id: 教师ID
            name: 课程名称
            description: 课程描述
            
        Returns:
            Course: 创建的课程对象
        """
        course = Course(
            name=name,
            description=description,
            teacher_id=teacher_id
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_teacher_courses(self, teacher_id: int):
        """
        获取教师创建的所有课程
        
        Args:
            teacher_id: 教师ID
            
        Returns:
            list: 课程列表
        """
        return self.db.query(Course).filter_by(teacher_id=teacher_id).all()

    def get_student_courses(self, student_id: int):
        """
        获取学生已选的所有课程
        
        Args:
            student_id: 学生ID
            
        Returns:
            list: 课程列表
        """
        enrollments = self.db.query(CourseEnrollment).filter_by(student_id=student_id).all()
        return [enrollment.course for enrollment in enrollments]

    def enroll_student(self, student_id: int, course_id: int):
        """
        学生选课
        
        Args:
            student_id: 学生ID
            course_id: 课程ID
            
        Returns:
            CourseEnrollment: 选课记录
        """
        # 检查是否已选
        existing = self.db.query(CourseEnrollment).filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
        
        if existing:
            raise ValueError("已经选过此课程")
        
        enrollment = CourseEnrollment(
            student_id=student_id,
            course_id=course_id
        )
        self.db.add(enrollment)
        self.db.commit()
        return enrollment

    def upload_document(self, course_id: int, teacher_id: int, filepath: str, filename: str):
        """
        上传课程文档（仅教师）
        
        Args:
            course_id: 课程ID
            teacher_id: 教师ID
            filepath: 文件路径
            filename: 文件名
            
        Returns:
            CourseDocument: 文档对象
        """
        # 验证权限
        if not PermissionHelper.can_manage_course(self.db, teacher_id, course_id):
            raise PermissionError("无权上传此课程的文档")
        
        # 提取文本内容
        content = self.doc_service.extract_text(filepath)
        
        # 获取文件类型
        import os
        file_type = os.path.splitext(filename)[1][1:]  # 去掉点号
        
        # 创建文档记录
        document = CourseDocument(
            course_id=course_id,
            filename=filename,
            filepath=filepath,
            file_type=file_type,
            content=content
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_course_documents(self, course_id: int):
        """
        获取课程的所有文档
        
        Args:
            course_id: 课程ID
            
        Returns:
            list: 文档列表
        """
        return self.db.query(CourseDocument).filter_by(course_id=course_id).all()

    def delete_course(self, course_id: int, teacher_id: int):
        """
        删除课程（仅教师）
        
        Args:
            course_id: 课程ID
            teacher_id: 教师ID
        """
        # 验证权限
        if not PermissionHelper.can_manage_course(self.db, teacher_id, course_id):
            raise PermissionError("无权删除此课程")
        
        course = self.db.query(Course).filter_by(id=course_id).first()
        if course:
            self.db.delete(course)
            self.db.commit()

    def get_course_by_id(self, course_id: int):
        """
        根据ID获取课程
        
        Args:
            course_id: 课程ID
            
        Returns:
            Course: 课程对象
        """
        return self.db.query(Course).filter_by(id=course_id).first()

    def get_all_courses(self):
        """
        获取所有课程（用于学生浏览选课）
        
        Returns:
            list: 课程列表
        """
        return self.db.query(Course).all()

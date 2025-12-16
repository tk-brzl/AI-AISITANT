"""
权限验证辅助类
"""
from models.course import CourseEnrollment, Course
from sqlalchemy.orm import Session


class PermissionHelper:
    """权限验证辅助类"""

    @staticmethod
    def can_access_course(db: Session, user_id: int, user_role: str, course_id: int) -> bool:
        """
        检查用户是否可以访问课程
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            user_role: 用户角色
            course_id: 课程ID
            
        Returns:
            bool: 是否有权限
        """
        if user_role == 'teacher':
            # 教师只能访问自己创建的课程
            course = db.query(Course).filter_by(
                id=course_id,
                teacher_id=user_id
            ).first()
            return course is not None
        else:
            # 学生只能访问已选课程
            enrollment = db.query(CourseEnrollment).filter_by(
                student_id=user_id,
                course_id=course_id
            ).first()
            return enrollment is not None

    @staticmethod
    def can_manage_course(db: Session, user_id: int, course_id: int) -> bool:
        """
        检查用户是否可以管理课程（仅教师且是课程创建者）
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            course_id: 课程ID
            
        Returns:
            bool: 是否有权限
        """
        course = db.query(Course).filter_by(
            id=course_id,
            teacher_id=user_id
        ).first()
        return course is not None

    @staticmethod
    def is_course_teacher(db: Session, user_id: int, course_id: int) -> bool:
        """
        检查用户是否是课程的教师
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            course_id: 课程ID
            
        Returns:
            bool: 是否是课程教师
        """
        course = db.query(Course).filter_by(
            id=course_id,
            teacher_id=user_id
        ).first()
        return course is not None

    @staticmethod
    def is_course_student(db: Session, user_id: int, course_id: int) -> bool:
        """
        检查用户是否是课程的学生
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            course_id: 课程ID
            
        Returns:
            bool: 是否是课程学生
        """
        enrollment = db.query(CourseEnrollment).filter_by(
            student_id=user_id,
            course_id=course_id
        ).first()
        return enrollment is not None

"""
问答服务
"""
from sqlalchemy.orm import Session
from models.qa import QARecord
from models.course import CourseDocument
from .ai_service import AIService
from auth.permissions import PermissionHelper


class QAService:
    """问答服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    def ask_question(self, user_id: int, course_id: int, question: str):
        """
        提问并获取AI回答
        
        Args:
            user_id: 用户ID
            course_id: 课程ID
            question: 问题内容
            
        Returns:
            dict: 包含答案和上下文的字典
        """
        # 获取课程相关文档
        documents = self.db.query(CourseDocument).filter_by(course_id=course_id).all()
        
        # 简单的关键词匹配检索（实际应该使用向量数据库）
        context = self._retrieve_relevant_context(question, documents)
        
        # 调用AI获取答案
        answer = self.ai_service.answer_question(question, context)
        
        # 保存问答记录
        qa_record = QARecord(
            user_id=user_id,
            course_id=course_id,
            question=question,
            answer=answer,
            context=context[:500] if context else ""  # 只保存部分上下文
        )
        self.db.add(qa_record)
        self.db.commit()
        
        return {
            'answer': answer,
            'context': context
        }

    def _retrieve_relevant_context(self, question: str, documents: list, max_length: int = 2000):
        """
        检索相关文档内容
        
        Args:
            question: 问题
            documents: 文档列表
            max_length: 最大上下文长度
            
        Returns:
            str: 相关文档内容
        """
        # 简化版：提取问题中的关键词，在文档中搜索
        # 实际应该使用FAISS等向量数据库进行语义检索
        
        if not documents:
            return "暂无课程资料"
        
        # 合并所有文档内容
        all_content = ""
        for doc in documents:
            if doc.content:
                all_content += f"\n\n【{doc.filename}】\n{doc.content}"
        
        # 简单截取前max_length个字符
        # 实际应该基于相关性选择最相关的片段
        if len(all_content) > max_length:
            return all_content[:max_length] + "..."
        
        return all_content

    def get_user_qa_history(self, user_id: int, course_id: int = None):
        """
        获取用户的问答历史
        
        Args:
            user_id: 用户ID
            course_id: 课程ID（可选）
            
        Returns:
            list: 问答记录列表
        """
        query = self.db.query(QARecord).filter_by(user_id=user_id)
        if course_id:
            query = query.filter_by(course_id=course_id)
        return query.order_by(QARecord.created_at.desc()).all()

    def get_course_qa_history(self, course_id: int, teacher_id: int):
        """
        获取课程的所有问答历史（教师查看）
        
        Args:
            course_id: 课程ID
            teacher_id: 教师ID
            
        Returns:
            list: 问答记录列表
        """
        # 验证权限
        if not PermissionHelper.is_course_teacher(self.db, teacher_id, course_id):
            raise PermissionError("无权查看此课程的问答记录")
        
        return self.db.query(QARecord).filter_by(course_id=course_id).order_by(
            QARecord.created_at.desc()
        ).all()

    def delete_qa_record(self, record_id: int, user_id: int):
        """
        删除问答记录
        
        Args:
            record_id: 记录ID
            user_id: 用户ID
        """
        record = self.db.query(QARecord).filter_by(id=record_id, user_id=user_id).first()
        if record:
            self.db.delete(record)
            self.db.commit()

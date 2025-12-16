"""
测验服务
"""
from sqlalchemy.orm import Session
from models.quiz import Quiz, Question, QuizAttempt, Answer
from models.course import CourseDocument
from .ai_service import AIService
from auth.permissions import PermissionHelper
from datetime import datetime
import json


class QuizService:
    """测验服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    def generate_quiz(self, teacher_id: int, course_id: int, title: str, 
                     knowledge_point: str, question_count: int = 10):
        """
        生成测验（仅教师）
        
        Args:
            teacher_id: 教师ID
            course_id: 课程ID
            title: 测验标题
            knowledge_point: 知识点
            question_count: 题目数量
            
        Returns:
            Quiz: 测验对象
        """
        # 验证权限
        if not PermissionHelper.is_course_teacher(self.db, teacher_id, course_id):
            raise PermissionError("无权为此课程生成测验")
        
        # 获取课程文档作为上下文
        documents = self.db.query(CourseDocument).filter_by(course_id=course_id).all()
        context = self._get_course_context(documents)
        
        # 创建测验
        quiz = Quiz(
            course_id=course_id,
            title=title,
            knowledge_point=knowledge_point,
            description=f"关于{knowledge_point}的测验"
        )
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)
        
        # 生成题目（这里简化处理，实际应该调用AI生成）
        self._generate_sample_questions(quiz.id, knowledge_point, question_count)
        
        return quiz

    def _get_course_context(self, documents: list, max_length: int = 3000):
        """获取课程上下文"""
        context = ""
        for doc in documents:
            if doc.content:
                context += doc.content + "\n\n"
                if len(context) > max_length:
                    break
        return context[:max_length]

    def _generate_sample_questions(self, quiz_id: int, knowledge_point: str, count: int):
        """
        生成示例题目（简化版）
        实际应该调用AI生成
        """
        # 选择题示例
        question1 = Question(
            quiz_id=quiz_id,
            question_type='choice',
            question_text=f'关于{knowledge_point}，以下哪个说法是正确的？',
            options=json.dumps(['选项A', '选项B', '选项C', '选项D'], ensure_ascii=False),
            correct_answer='选项A',
            explanation='这是正确答案的解释',
            points=10.0
        )
        
        # 判断题示例
        question2 = Question(
            quiz_id=quiz_id,
            question_type='true_false',
            question_text=f'{knowledge_point}是一个重要的概念。',
            options=json.dumps(['正确', '错误'], ensure_ascii=False),
            correct_answer='正确',
            explanation='这个说法是正确的',
            points=10.0
        )
        
        # 简答题示例
        question3 = Question(
            quiz_id=quiz_id,
            question_type='short_answer',
            question_text=f'请简述{knowledge_point}的主要内容。',
            correct_answer=f'{knowledge_point}的主要内容包括...',
            explanation='参考答案',
            points=20.0
        )
        
        self.db.add_all([question1, question2, question3])
        self.db.commit()

    def get_quiz_by_id(self, quiz_id: int):
        """获取测验"""
        return self.db.query(Quiz).filter_by(id=quiz_id).first()

    def get_course_quizzes(self, course_id: int):
        """获取课程的所有测验"""
        return self.db.query(Quiz).filter_by(course_id=course_id).all()

    def start_quiz(self, student_id: int, quiz_id: int):
        """
        学生开始测验
        
        Args:
            student_id: 学生ID
            quiz_id: 测验ID
            
        Returns:
            QuizAttempt: 测验尝试记录
        """
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            raise ValueError("测验不存在")
        
        # 创建测验尝试记录
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            student_id=student_id,
            total_points=sum(q.points for q in quiz.questions)
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def submit_answer(self, attempt_id: int, question_id: int, student_answer: str):
        """
        提交答案
        
        Args:
            attempt_id: 尝试ID
            question_id: 题目ID
            student_answer: 学生答案
        """
        question = self.db.query(Question).filter_by(id=question_id).first()
        if not question:
            raise ValueError("题目不存在")
        
        # 判断答案是否正确
        is_correct = False
        points_earned = 0.0
        ai_feedback = ""
        
        if question.question_type in ['choice', 'true_false']:
            # 客观题直接比较
            is_correct = (student_answer.strip() == question.correct_answer.strip())
            points_earned = question.points if is_correct else 0.0
        else:
            # 主观题使用AI批改
            result = self.ai_service.grade_answer(
                question.question_text,
                question.correct_answer,
                student_answer
            )
            points_earned = result['score']
            ai_feedback = result['feedback']
            is_correct = (points_earned >= question.points * 0.6)  # 60%以上算正确
        
        # 保存答案
        answer = Answer(
            attempt_id=attempt_id,
            question_id=question_id,
            student_answer=student_answer,
            is_correct=is_correct,
            points_earned=points_earned,
            ai_feedback=ai_feedback
        )
        self.db.add(answer)
        self.db.commit()

    def complete_quiz(self, attempt_id: int):
        """
        完成测验，计算总分
        
        Args:
            attempt_id: 尝试ID
        """
        attempt = self.db.query(QuizAttempt).filter_by(id=attempt_id).first()
        if not attempt:
            raise ValueError("测验尝试不存在")
        
        # 计算总分
        total_score = sum(answer.points_earned for answer in attempt.answers)
        attempt.score = total_score
        attempt.submitted_at = datetime.now()
        attempt.is_completed = True
        self.db.commit()

    def get_student_attempts(self, student_id: int, course_id: int = None):
        """
        获取学生的测验记录
        
        Args:
            student_id: 学生ID
            course_id: 课程ID（可选）
            
        Returns:
            list: 测验尝试列表
        """
        query = self.db.query(QuizAttempt).filter_by(student_id=student_id)
        if course_id:
            query = query.join(Quiz).filter(Quiz.course_id == course_id)
        return query.order_by(QuizAttempt.started_at.desc()).all()

    def get_quiz_statistics(self, quiz_id: int, teacher_id: int):
        """
        获取测验统计数据（教师查看）
        
        Args:
            quiz_id: 测验ID
            teacher_id: 教师ID
            
        Returns:
            dict: 统计数据
        """
        quiz = self.get_quiz_by_id(quiz_id)
        if not quiz:
            raise ValueError("测验不存在")
        
        # 验证权限
        if not PermissionHelper.is_course_teacher(self.db, teacher_id, quiz.course_id):
            raise PermissionError("无权查看此测验的统计数据")
        
        attempts = self.db.query(QuizAttempt).filter_by(
            quiz_id=quiz_id,
            is_completed=True
        ).all()
        
        if not attempts:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'max_score': 0,
                'min_score': 0
            }
        
        scores = [attempt.score for attempt in attempts]
        return {
            'total_attempts': len(attempts),
            'average_score': sum(scores) / len(scores),
            'max_score': max(scores),
            'min_score': min(scores)
        }

"""
AI服务 - DeepSeek API集成
"""
from openai import OpenAI
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, MAX_TOKENS, TEMPERATURE


class AIService:
    """AI服务类，封装DeepSeek API调用"""

    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_base = DEEPSEEK_API_BASE
        # 使用新版 OpenAI 客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )

    def chat(self, messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):
        """
        调用AI聊天接口
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            str: AI回复内容
        """
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI服务调用失败: {str(e)}"

    def answer_question(self, question, context=""):
        """
        基于上下文回答问题
        
        Args:
            question: 用户问题
            context: 相关文档上下文
            
        Returns:
            str: AI回答
        """
        system_prompt = """你是一个专业的AI助教，负责回答学生关于课程内容的问题。
请基于提供的课程资料回答问题，如果资料中没有相关信息，请诚实地告知学生。
回答要清晰、准确、有条理。"""

        user_message = f"""课程资料：
{context}

学生问题：{question}

请基于上述课程资料回答学生的问题。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        return self.chat(messages)

    def generate_quiz_questions(self, knowledge_point, context, count=10):
        """
        生成测验题目
        
        Args:
            knowledge_point: 知识点
            context: 课程内容
            count: 题目数量
            
        Returns:
            list: 题目列表
        """
        system_prompt = """你是一个专业的试题生成专家。请根据给定的知识点和课程内容生成测验题目。
题目类型包括：选择题、判断题、简答题。
返回格式为JSON数组，每个题目包含：
- type: 题目类型 (choice/true_false/short_answer)
- question: 题目内容
- options: 选项（选择题和判断题需要）
- correct_answer: 正确答案
- explanation: 答案解析"""

        user_message = f"""知识点：{knowledge_point}

课程内容：
{context}

请生成{count}道测验题目，包括选择题、判断题和简答题。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = self.chat(messages, temperature=0.7)
        
        # 这里应该解析JSON，为了简化，返回原始响应
        # 实际使用时需要添加JSON解析逻辑
        return response

    def grade_answer(self, question, correct_answer, student_answer):
        """
        批改主观题答案
        
        Args:
            question: 题目
            correct_answer: 标准答案
            student_answer: 学生答案
            
        Returns:
            dict: 包含分数和反馈
        """
        system_prompt = """你是一个专业的作业批改老师。请评估学生的答案，给出分数（0-10分）和详细反馈。
评分标准：
- 完全正确：10分
- 基本正确但有小瑕疵：7-9分
- 部分正确：4-6分
- 基本错误但有可取之处：1-3分
- 完全错误：0分

返回格式：
分数：X分
反馈：详细的评价和建议"""

        user_message = f"""题目：{question}

标准答案：{correct_answer}

学生答案：{student_answer}

请给出评分和反馈。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = self.chat(messages, temperature=0.3)
        
        # 解析分数和反馈
        # 简化处理，实际应该用正则表达式提取
        lines = response.split('\n')
        score = 5.0  # 默认分数
        feedback = response
        
        for line in lines:
            if '分数' in line or '得分' in line:
                try:
                    # 尝试提取数字
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        score = float(numbers[0])
                except:
                    pass
        
        return {
            'score': score,
            'feedback': feedback
        }

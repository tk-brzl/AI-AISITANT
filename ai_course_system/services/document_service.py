"""
文档处理服务
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fitz  # PyMuPDF
from docx import Document
import numpy as np
from config import UPLOAD_DIR


class DocumentService:
    """文档处理服务类"""

    @staticmethod
    def extract_text_from_pdf(filepath):
        """
        从PDF文件提取文本
        
        Args:
            filepath: PDF文件路径
            
        Returns:
            str: 提取的文本内容
        """
        try:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            return f"PDF解析失败: {str(e)}"

    @staticmethod
    def extract_text_from_docx(filepath):
        """
        从Word文档提取文本
        
        Args:
            filepath: Word文档路径
            
        Returns:
            str: 提取的文本内容
        """
        try:
            doc = Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Word文档解析失败: {str(e)}"

    @staticmethod
    def extract_text_from_txt(filepath):
        """
        从文本文件读取内容
        
        Args:
            filepath: 文本文件路径
            
        Returns:
            str: 文件内容
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    return f.read()
            except Exception as e:
                return f"文本文件读取失败: {str(e)}"

    @staticmethod
    def extract_text(filepath):
        """
        根据文件类型自动提取文本
        
        Args:
            filepath: 文件路径
            
        Returns:
            str: 提取的文本内容
        """
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            return DocumentService.extract_text_from_pdf(filepath)
        elif ext in ['.docx', '.doc']:
            return DocumentService.extract_text_from_docx(filepath)
        elif ext == '.txt':
            return DocumentService.extract_text_from_txt(filepath)
        else:
            return "不支持的文件格式"

    @staticmethod
    def save_uploaded_file(file_data, filename, course_id):
        """
        保存上传的文件
        
        Args:
            file_data: 文件数据
            filename: 文件名
            course_id: 课程ID
            
        Returns:
            str: 保存的文件路径
        """
        # 创建课程专属目录
        course_dir = os.path.join(UPLOAD_DIR, f"course_{course_id}")
        os.makedirs(course_dir, exist_ok=True)
        
        # 保存文件
        filepath = os.path.join(course_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(file_data)
        
        return filepath

    @staticmethod
    def chunk_text(text, chunk_size=500, overlap=50):
        """
        将文本分块，用于向量化存储
        
        Args:
            text: 原始文本
            chunk_size: 每块大小（字符数）
            overlap: 重叠大小
            
        Returns:
            list: 文本块列表
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start += (chunk_size - overlap)
        
        return chunks

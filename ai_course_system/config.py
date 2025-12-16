"""
系统配置文件
"""
import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'course_system.db')
VECTOR_DB_PATH = os.path.join(DATA_DIR, 'vector_store')
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')

# 创建必要的目录
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-4f9d586425524f79a7621310ae1bcb47"  # 需要用户填写
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# 数据库配置
DATABASE_URL = f"sqlite:///{DB_PATH}"

# GUI配置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME = "dark-blue"

# AI配置
MAX_TOKENS = 2000
TEMPERATURE = 0.7
EMBEDDING_MODEL = "text-embedding-ada-002"

# 测验配置
QUIZ_QUESTION_COUNT = 10
QUIZ_TIME_LIMIT = 30  # 分钟

# 角色定义
ROLE_STUDENT = "student"
ROLE_TEACHER = "teacher"

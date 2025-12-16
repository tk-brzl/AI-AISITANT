# 🤖 AI线上课程系统

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/ai-course-system)

一个基于Python和CustomTkinter的现代化AI线上课程管理系统，集成DeepSeek AI助教功能，为教学提供智能化解决方案。

## ✨ 功能特点

### 👨‍🎓 学生端
- 📚 **课程浏览** - 发现和选择感兴趣的课程
- 🤖 **AI智能问答** - 基于课程资料的实时AI助教解答
- 📝 **在线测验** - 参与测验并即时获得AI批改反馈
- 📊 **学习分析** - 查看个人学习进度和成绩统计
- 💬 **提问记录** - 保存所有AI问答历史供复习

### 👩‍🏫 教师端
- 📖 **课程管理** - 创建、编辑和管理课程内容
- 📄 **多格式文档** - 支持PDF、Word、TXT等格式资料上传
- 🤖 **AI助教监控** - 查看学生提问并提供补充解答
- 📋 **智能出题** - AI自动生成多样化的测验题目
- 📈 **数据分析** - 全面的课程统计和学生表现分析
- 🔔 **学生管理** - 管理学生名单和学习进度

## 🛠 技术栈

| 组件 | 技术选型 |
|------|---------|
| **GUI框架** | CustomTkinter |
| **数据库** | SQLite + SQLAlchemy ORM |
| **AI服务** | DeepSeek API |
| **文档处理** | PyMuPDF, python-docx |
| **打包工具** | PyInstaller |
| **认证授权** | 自定义权限控制系统 |

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器
- DeepSeek API密钥（[获取地址](https://platform.deepseek.com)）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/ai-course-system.git
   cd ai-course-system
   ```

2. **创建虚拟环境**（推荐）
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置API密钥**
   ```bash
   # 复制配置文件模板
   cp ai_course_system/config.example.py ai_course_system/config.py

   # 编辑配置文件，填入您的API密钥
   # DEEPSEEK_API_KEY = "your-actual-api-key-here"
   ```

5. **运行程序**
   ```bash
   cd ai_course_system
   python main.py
   ```

## 📦 打包部署

### 打包为可执行文件

```bash
# Windows
pyinstaller --name="AI课程系统" ^
    --windowed ^
    --onefile ^
    --add-data "config.py;." ^
    main.py

# Linux/macOS
pyinstaller --name="AI课程系统" \
    --windowed \
    --onefile \
    --add-data "config.py:." \
    main.py
```

打包完成后，可执行文件将位于 `dist` 目录下。

## 📁 项目结构

```
ai-course-system/
├── .gitignore                   # Git忽略规则
├── README.md                    # 项目文档
├── requirements.txt             # Python依赖
└── ai_course_system/           # 主程序目录
    ├── auth/                   # 权限控制模块
    │   ├── __init__.py
    │   ├── decorators.py       # 装饰器
    │   ├── permissions.py      # 权限定义
    │   └── session.py          # 会话管理
    ├── models/                 # 数据模型层
    │   ├── __init__.py
    │   ├── user.py            # 用户模型
    │   ├── course.py          # 课程模型
    │   ├── qa.py              # 问答模型
    │   └── quiz.py            # 测验模型
    ├── services/              # 业务逻辑层
    │   ├── __init__.py
    │   ├── ai_service.py      # AI服务
    │   ├── course_service.py  # 课程服务
    │   ├── document_service.py # 文档处理
    │   ├── qa_service.py      # 问答服务
    │   └── quiz_service.py    # 测验服务
    ├── views/                 # 用户界面层
    │   ├── login_view.py      # 登录界面
    │   ├── main_window.py     # 主窗口
    │   ├── student/           # 学生界面
    │   └── teacher/           # 教师界面
    ├── data/                  # 数据存储（运行时创建）
    ├── config.py             # 配置文件（需创建）
    ├── config.example.py     # 配置示例
    └── main.py               # 程序入口
```

## 🎯 使用指南

### 初次使用

1. **启动程序**后，点击"注册"创建新账号
2. **选择角色**：学生或教师
3. **填写信息**完成账号创建
4. **登录系统**开始使用

### 教师使用流程

1. **创建课程**：填写课程基本信息
2. **上传资料**：支持PDF、Word、TXT格式
3. **生成测验**：AI自动生成或手动创建题目
4. **管理学生**：查看学习进度和互动情况
5. **数据分析**：获取课程统计报告

### 学生使用流程

1. **浏览课程**：查看所有可用课程
2. **选择课程**：加入感兴趣的课程
3. **AI学习**：通过AI问答深入学习
4. **参与测验**：检验学习成果
5. **查看记录**：追踪个人学习进度

## ⚙️ 配置说明

### API配置

在 `config.py` 中配置以下参数：

```python
# DeepSeek API
DEEPSEEK_API_KEY = "your-api-key-here"

# 数据库
DATABASE_URL = "sqlite:///data/course_system.db"

# 应用设置
APP_NAME = "AI线上课程系统"
VERSION = "1.0.0"
LOG_LEVEL = "INFO"
```

### 环境变量

也可以通过环境变量配置：

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
export DATABASE_URL="sqlite:///data/course_system.db"
```

## 🔧 系统要求

| 要求 | 最低配置 | 推荐配置 |
|------|---------|---------|
| **操作系统** | Windows 10 / macOS 10.14 / Ubuntu 18.04 | Windows 11 / macOS 12 / Ubuntu 20.04 |
| **Python版本** | 3.8 | 3.9+ |
| **内存** | 2GB | 4GB |
| **存储空间** | 500MB | 1GB |
| **网络** | 宽带连接 | 稳定的宽带连接 |

## ❗ 注意事项

- **API密钥安全**：请勿将API密钥提交到版本控制系统
- **网络依赖**：AI功能需要稳定的网络连接
- **文档限制**：单个文档文件大小不超过50MB
- **数据备份**：定期备份 `data` 目录下的数据库文件
- **权限设置**：确保应用有读写当前目录的权限

## 🐛 常见问题

<details>
<summary>AI回答速度很慢？</summary>

答：这取决于网络连接质量和DeepSeek API的响应时间。请确保网络连接稳定，并耐心等待AI处理完成。
</details>

<details>
<summary>无法上传文档？</summary>

答：请检查文档格式是否为支持的类型（PDF、DOCX、TXT），并确保文件大小不超过50MB。
</details>

<details>
<summary>忘记密码怎么办？</summary>

答：当前版本需要联系管理员重置密码，或删除数据库文件重新注册。后续版本将增加邮箱找回功能。
</details>

<details>
<summary>程序启动失败？</summary>

答：请检查Python版本是否满足要求，是否正确安装所有依赖包，并确保config.py文件配置正确。
</details>

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 **Pull Request**

### 贡献类型

- 🐛 Bug修复
- ✨ 新功能开发
- 📝 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化
- 🧪 测试覆盖

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com) - 提供强大的AI能力支持
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代化的GUI框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - 优秀的Python ORM工具

## 📞 联系我们

- 项目主页：[https://github.com/yourusername/ai-course-system](https://github.com/yourusername/ai-course-system)
- 问题反馈：[Issues](https://github.com/yourusername/ai-course-system/issues)
- 功能建议：[Discussions](https://github.com/yourusername/ai-course-system/discussions)

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
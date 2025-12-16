# GitHub上传步骤详细说明

## 方法一：使用Git命令行（推荐）

### 第1步：配置Git（首次使用需要）
```bash
# 设置你的Git用户名
git config --global user.name "你的用户名"

# 设置你的Git邮箱
git config --global user.email "你的邮箱@example.com"
```

### 第2步：初始化本地仓库
```bash
# 进入项目目录
cd C:\Users\Administrator\ai-course-system-github

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 提交文件
git commit -m "Initial commit: AI线上课程系统"
```

### 第3步：连接远程仓库
```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/ai-course-system.git

# 或者如果你使用SSH（需要先配置SSH密钥）
# git remote add origin git@github.com:你的用户名/ai-course-system.git
```

### 第4步：推送到GitHub
```bash
# 推送到main分支
git push -u origin main
```

如果遇到错误，可能需要：
```bash
# 强制推送到main分支（如果远程仓库自动创建了README）
git push -u origin main --force
```

## 方法二：使用GitHub Desktop（图形界面）

### 第1步：下载并安装GitHub Desktop
- 访问 [https://desktop.github.com](https://desktop.github.com)
- 下载并安装GitHub Desktop
- 登录你的GitHub账号

### 第2步：添加本地仓库
1. 打开GitHub Desktop
2. 点击 "File" → "Add Local Repository"
3. 选择 `C:\Users\Administrator\ai-course-system-github` 文件夹
4. 点击 "Add Repository"

### 第3步：发布到GitHub
1. 在GitHub Desktop界面中，填写提交信息：
   - Summary: `Initial commit: AI线上课程系统`
2. 点击 "Commit to main"
3. 点击 "Publish repository"
4. 填写仓库信息：
   - Repository name: `ai-course-system`
   - Description: `AI线上课程系统 - 基于Python和CustomTkinter的智能教学管理平台`
   - 选择 Public 或 Private
5. 点击 "Publish Repository"

## 方法三：通过网页直接上传（小项目适用）

### 第1步：创建仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库名称和描述
4. 不要勾选任何初始化选项
5. 点击 "Create repository"

### 第2步：上传文件
1. 在新创建的仓库页面，点击 "uploading an existing file"
2. 将整个 `ai-course-system-github` 文件夹拖拽到页面上
3. 或者：
   - 点击 "choose your files"
   - 选择所有文件（可以批量选择）
   - 上传文件夹结构

### 第3步：提交
1. 填写提交信息：`Initial commit: AI线上课程系统`
2. 点击 "Commit changes"

## 常见问题解决

### 问题1：推送时提示权限错误
```bash
# 解决方案：使用Personal Access Token
# 1. 访问 https://github.com/settings/tokens
# 2. 生成新的token，选择repo权限
# 3. 使用token代替密码进行推送
```

### 问题2：文件太大上传失败
```bash
# 解决方案：使用Git LFS（大文件支持）
git lfs install
git lfs track "*.exe"
git lfs track "*.pdf"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

### 问题3：端口被占用
```bash
# 如果使用代理，确保端口配置正确
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```

## 上传后检查清单

- [ ] 检查所有文件都已上传
- [ ] README.md显示正常
- [ ] .gitignore工作正常（没有上传不必要的文件）
- [ ] 仓库描述和标签填写完整
- [ ] 如果需要，设置仓库为Public
- [ ] 考虑添加GitHub Pages（如果有文档网站）
- [ ] 添加开源许可证（如MIT License）

## 推荐使用方法一（Git命令行）的原因

1. **功能最全面**：支持所有Git操作
2. **速度最快**：直接在本地操作
3. **适合大型项目**：不会遇到文件大小限制
4. **学习价值高**：掌握Git技能
5. **自动化友好**：可以编写脚本自动化操作

## 最终效果

上传成功后，你的GitHub仓库地址将是：
`https://github.com/你的用户名/ai-course-system`

其他用户可以通过以下命令使用你的项目：
```bash
git clone https://github.com/你的用户名/ai-course-system.git
```
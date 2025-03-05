# 智能思维导图助手

这是一个基于Web的智能思维导图应用，结合了传统思维导图功能和AI能力，帮助您捕捉灵感、发展想法、组织知识结构。

## 在线演示

访问[在线演示](https://your-github-username.github.io/mindmap-app/)体验应用（部署后更新此链接）

## 功能特点

### 思维导图核心功能
- 创建和编辑思维导图
- 添加、删除和修改节点
- 连接节点形成思维结构
- 自定义节点颜色和形状
- 拖拽调整节点位置
- 保存和加载思维导图

### AI智能增强功能
- **快速记录想法**：支持快速输入关键词和简要想法
- **AI自动优化**：通过前端配置的DeepSeek API将简短想法扩展成完整概念
- **思维导图自动生成**：从AI扩展的想法一键生成思维导图
- **AI对话功能**：与AI直接交流，探索和完善想法
- **数据本地存储**：所有想法安全保存在本地
- **API密钥前端配置**：在前端安全地配置和存储API密钥，无需后端保存

## 技术栈

- 后端：Python Flask
- 前端：HTML, CSS, JavaScript
- 可视化：D3.js
- AI集成：DeepSeek API (前端配置)
- 部署：GitHub Pages / Heroku / Vercel

## 本地开发

### 安装和运行

1. 克隆此仓库：
   ```
   git clone https://github.com/your-username/mindmap-app.git
   cd mindmap-app
   ```

2. 安装依赖：
   ```
   cd mindmap
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```
   python app.py
   ```

4. 在浏览器中访问：http://localhost:5000

5. 在应用的"设置"页面中配置您的DeepSeek API密钥（可选）

## 部署指南

### 部署到GitHub Pages (静态部分)

1. 创建一个新的GitHub仓库
2. 将代码推送到仓库：
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/mindmap-app.git
   git push -u origin main
   ```
3. 在GitHub仓库设置中启用GitHub Pages
4. 选择分支和文件夹进行部署

### 部署到Heroku (完整应用)

1. 创建Heroku账户和安装Heroku CLI
2. 登录Heroku：
   ```
   heroku login
   ```
3. 创建Heroku应用：
   ```
   heroku create your-app-name
   ```
4. 推送代码到Heroku：
   ```
   git push heroku main
   ```
5. 打开应用：
   ```
   heroku open
   ```

### 部署到Vercel (完整应用)

1. 注册Vercel账户并安装Vercel CLI
2. 在项目根目录创建`vercel.json`：
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "mindmap/app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "mindmap/app.py"
       }
     ]
   }
   ```
3. 部署项目：
   ```
   vercel
   ```

## API密钥安全说明

本应用不会在服务器端存储您的API密钥，所有密钥都保存在浏览器的localStorage中，并在请求时通过HTTP头传递给API。这意味着：

- API密钥仅存储在您的设备上
- 清除浏览器数据会移除保存的API密钥
- 不同设备或浏览器需要单独配置API密钥

## 使用说明

### 思维导图功能
- 在首页创建新的思维导图或打开现有导图
- 在编辑器中可添加、删除、修改节点
- 拖拽调整节点位置，连接节点形成关系

### AI思维助手功能
1. **配置API密钥**：
   - 点击页面右上角的"设置"按钮
   - 输入您的DeepSeek API密钥（可选）
   - 如未配置，将使用模拟数据

2. **想法扩展**：
   - 输入简短想法或关键词
   - 点击"AI扩展想法"按钮
   - AI将生成详细的概念解释、相关概念和行动项
   - 点击"创建思维导图"按钮，自动生成思维导图

3. **AI对话**：
   - 切换到"AI对话"标签
   - 输入问题或想法
   - 与AI助手交流，探索和完善想法

## 数据存储

在本地开发环境中，所有思维导图数据和对话历史保存在JSON格式文件中，存储在应用的`data`目录下。
在生产环境中，您可能需要将数据存储迁移到数据库中以提高可靠性。

## 贡献

欢迎提交问题和拉取请求来改进此应用。

## 许可

MIT许可证 
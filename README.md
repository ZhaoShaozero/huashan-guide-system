# 华山核心景点导览系统

一个为华山游客提供智能化景点导览服务的全栈 Web 应用。

## 📋 项目介绍

本项目是一个**个人借助 AI 开发**的华山景区导览系统，旨在帮助游客了解华山的核心景点信息，包括景点难度、安全等级、预计游览时间等关键信息，并提供 AI 驱动的景点讲解和个性化安全检查功能。

这是一个学习和实践全栈开发的个人项目，通过 AI 代码生成工具提升开发效率，同时保持对代码质量的控制。

## 🛠️ 技术栈

### 前端
- **Vue 3** - 现代响应式 JavaScript 框架
- **Vite** - 极速冷启动和模块热更新的下一代构建工具
- **Axios** - 基于 Promise 的 HTTP 请求库
- **CSS3** - 现代样式设计和响应式布局

### 后端
- **Python 3** - 服务端编程语言
- **Flask** - 轻量级 Web 框架，快速灵活
- **SQLite** - 轻量级关系型数据库
  > 原计划使用 MySQL，但考虑到个人服务器性能和部署复杂度，最终选用 SQLite 以减少资源占用
- **AI 协助** - 大部分代码由 AI 生成并优化

## 📝 项目特点

- ✨ **AI 智能讲解** - 为每个景点提供 AI 生成的详细讲解词
- 🔍 **景点搜索与筛选** - 支持按名称、难度等级、安全等级智能筛选
- ⚠️ **安全检查** - 基于用户信息的个性化安全提示和风险预警
- 📱 **响应式设计** - 完美适配桌面、平板、手机等各种屏幕尺寸
- 🚀 **开机自启** - 后端服务通过 systemd 实现自启动和自动重启

## 📂 项目结构

huashan-guide-system/
├── frontend/ # Vue 3 前端应用
│ ├── src/
│ │ ├── components/
│ │ │ └── Map.vue # 景点导览主组件
│ │ ├── App.vue
│ │ └── main.js
│ ├── package.json
│ └── vite.config.js
├── backend/ # Python Flask 后端
│ ├── app.py # Flask 主应用文件
│ ├── requirements.txt # Python 依赖列表
│ ├── venv/ # Python 虚拟环境
│ └── instance/
│ └── huashan.db # SQLite 数据库
├── README.md # 项目说明文档
└── .gitignore # Git 忽略文件配置

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- npm 或 yarn

### 前端启动

```bash

cd frontend

# 安装依赖
npm install

# 开发服务器（热更新）
npm run dev

# 生产构建
npm run build
```

### 后端启动
```bash
cd backend

# 创建虚拟环境（如果还没有）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py   -  端口为15500

```

🤖 AI 生成说明
本项目大部分代码由 AI 工具辅助生成，包括但不限于：

✅ 前端 Vue 3 组件的 HTML 结构和逻辑

✅ 后端 Flask API 的基础实现和数据库模型

✅ UI 样式设计和响应式布局

✅ 项目配置文件（vite.config.js、requirements.txt 等）

质量保证
AI 生成的代码经过以下步骤的审查和优化：

功能测试 - 确保所有功能正确实现

手工审查 - 代码逻辑和结构检查

性能优化 - 优化关键路径和算法

安全检查 - 确保没有常见的安全漏洞

文档补充 - 添加必要的代码注释和文档

👤 个人项目说明
这是一个个人学习和实践项目，目的是：

🎓 探索 Vue 3 + Flask 全栈开发实践

🤖 学习和应用 AI 代码生成工具的工作流

🏔️ 实现一个完整的景区导览 Web 应用

🚀 练习项目部署、自启动配置等运维技能

📚 积累全栈开发的经验和最佳实践

📧 联系方式
如有问题、建议或改进意见，欢迎：

提交 Issue

提交 Pull Request

发送[邮件](mailto:zhushuaza@gmail.com "给作者发邮件")反馈

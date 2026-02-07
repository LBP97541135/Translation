# AI 翻译助手 (AI Translation Assistant)

一个基于 FastAPI 和 Flutter 构建的全栈 AI 翻译应用。支持异步模型调用、高性能缓存池以及简约大气的 Web 交互界面。

## 🌟 功能特点

- **异步高效**：后端采用 FastAPI + `httpx` 实现非阻塞模型调用。
- **智能缓存**：集成 `aiocache` 内存缓存池，相同内容秒回，节省 API 消耗。
- **结构化输出**：利用 LLM 提取翻译内容及核心关键词。
- **简约 UI**：Flutter 实现的现代化 Web 界面，响应式设计。
- **配置分离**：敏感信息通过 `config.json` 管理，安全便捷。

## 🏗️ 项目结构

```text
.
├── main.py              # FastAPI 后端主程序
├── config.json          # 配置文件 (API Key, Prompt 等)
├── requirements.txt     # Python 依赖清单
├── run_app.sh           # 一键启动脚本 (Shell)
└── frontend_flutter/    # Flutter 前端项目目录
    ├── lib/main.dart    # 前端核心逻辑
    └── pubspec.yaml     # Flutter 依赖配置
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd 面试题目
```

### 2. 后端配置
1. 创建并激活虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置 API Key：
   编辑 `config.json`，填入你的 Sealos AI Proxy 密钥。

### 3. 前端准备
确保你已安装 [Flutter SDK](https://docs.flutter.dev/get-started/install)。
```bash
cd frontend_flutter
flutter pub get
```

### 4. 一键启动
在项目根目录下运行启动脚本：
```bash
chmod +x run_app.sh
./run_app.sh
```
脚本将自动启动 FastAPI 服务并打开 Chrome 浏览器。

## 🛠️ 技术栈

- **后端**: Python, FastAPI, httpx, aiocache, pydantic
- **前端**: Dart, Flutter (Web/Desktop)
- **模型 API**: Sealos AI Proxy (GLM-4.5-Flash)

## 📄 开源协议
MIT License

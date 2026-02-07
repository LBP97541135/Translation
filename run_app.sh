#!/bin/bash

# --- 颜色定义 ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

echo -e "${BLUE}==== AI 翻译助手 启动脚本 ====${NC}"

# 获取脚本所在目录的绝对路径
PROJECT_ROOT=$(pwd)

# 1. 启动后端
echo -e "${GREEN}[1/2] 正在启动 FastAPI 后端服务...${NC}"
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "未发现虚拟环境，请确保已安装依赖。"
fi

# 在后台启动后端，并将日志输出到 backend.log
python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!

# 等待后端启动完成 (增加等待时间确保服务可用)
echo -n "正在等待后端就绪..."
for i in {1..10}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo -e "${GREEN} 就绪!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo -e "后端服务已在后台运行 (PID: $BACKEND_PID)"

# 2. 启动前端
echo -e "${GREEN}[2/2] 正在启动 Flutter 前端 (Chrome 浏览器端)...${NC}"
cd frontend_flutter

# 检查依赖并启动
flutter pub get > /dev/null
flutter run -d chrome

# 当前端退出后，自动关闭后端服务
echo -e "${BLUE}正在关闭后端服务...${NC}"
kill $BACKEND_PID
echo -e "${GREEN}已退出。${NC}"

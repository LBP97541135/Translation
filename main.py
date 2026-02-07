import os
import json
import httpx
import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

# --- 加载配置 ---
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
API_KEY = config.get("api_key")
API_URL = config.get("api_url")
MODEL_NAME = config.get("model_name")
SYSTEM_PROMPT = config.get("system_prompt")

app = FastAPI(title="Translation API with Cache")

# --- 跨域配置 (CORS) ---
# 解决 Web 端运行时的跨域限制问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，开发环境下建议设为 *
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法 (POST, OPTIONS 等)
    allow_headers=["*"],  # 允许所有请求头
)

# --- 数据模型 ---
class TranslateRequest(BaseModel):
    text: str

class TranslateResponse(BaseModel):
    translation: str
    keywords: List[str]

# --- 缓存配置 ---
# 使用内存缓存，设置过期时间为 1 小时 (3600秒)
# key_builder 可以根据输入文本生成唯一的缓存键
@cached(
    ttl=3600, 
    cache=Cache.MEMORY, 
    serializer=JsonSerializer(),
    namespace="translation"
)
async def get_translation_from_model(text: str) -> dict:
    """
    异步调用外部模型 API 获取翻译和关键词
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}  # 强制模型返回 JSON
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # 解析模型返回的 content
            content_str = result["choices"][0]["message"]["content"]
            content_json = json.loads(content_str)
            
            return content_json
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"API Error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- 接口实现 ---
@app.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # 调用带缓存的函数
    # 如果缓存中有结果，会直接返回，不会执行函数体内的 API 调用
    result = await get_translation_from_model(request.text)
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

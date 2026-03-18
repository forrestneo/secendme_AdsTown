"""
AdsTown - AI 广告小镇后端
仅保留广告生成相关 API
"""
import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx

# ================== 配置 ==================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ================== FastAPI 应用 ==================
app = FastAPI(title="AdsTown API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")

# ================== 数据模型 ==================
class AdGenerateRequest(BaseModel):
    resident: dict
    product: dict
    adType: str = "soft_ad"
    adFormat: str = "story"
    channel: str = "feed"
    targetAudience: str = "小镇居民"

# ================== API 端点 ==================

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/generate-ad")
async def generate_ad(req: AdGenerateRequest):
    """使用 DeepSeek API 生成广告文案"""
    ad_type_tips = {
        "soft_ad": "软性广告，要自然融入日常生活场景，不要直接推销",
        "hard_ad": "硬广，可以直接介绍产品优点，但要有创意"
    }
    
    format_tips = {
        "story": "用故事形式表达，有情节转折",
        "dialogue": "用对话形式表达，生动有趣",
        "scene": "用场景描写，有画面感",
        "experience": "用第一人称体验分享，真诚推荐"
    }
    
    prompt = f"""你是AdsTown小镇的广告文案专家。请为以下产品生成广告文案：

产品信息：
- 产品名称：{req.product.get('name', '产品')}
- 产品描述：{req.product.get('description', '')}
- 价格：{req.product.get('price', '')}
- 目标人群：{req.targetAudience}

创作者信息：
- 创作者：{req.resident.get('name', '小镇居民')}
- 角色：{req.resident.get('role', '')}
- 性格：{req.resident.get('personality', '')}

广告类型：{ad_type_tips.get(req.adType, '')}
表达形式：{format_tips.get(req.adFormat, '')}

要求：
1. 广告长度约50-100字
2. 体现创作者的性格特点
3. 突出产品核心价值
4. {"不要直接说'推荐''购买'等推销词汇，用故事/体验来打动人心" if req.adType == "soft_ad" else "可以介绍产品优点，但要新颖有创意"}

请直接输出广告文案，不要任何前缀："""

    try:
        if DEEPSEEK_API_KEY:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    DEEPSEEK_API_URL,
                    headers={
                        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 200,
                        "temperature": 0.8
                    },
                    timeout=30.0
                )
                if resp.status_code == 200:
                    result = resp.json()
                    content = result['choices'][0]['message']['content'].strip()
                    return {
                        "content": content,
                        "creativityScore": random.randint(6, 10),
                        "qualityScore": random.randint(7, 10)
                    }
    except Exception as e:
        print(f"DeepSeek API error: {e}")
    
    # 回退：使用模板生成
    templates = {
        "soft_ad": [
            f"在小镇的每一天，{req.resident.get('name', '我')}总会想起{req.product.get('name')}...{req.product.get('description', '')}",
            f"如果你问{req.resident.get('name', '我')}什么值得尝试，那一定是{req.product.get('name')}...",
        ],
        "hard_ad": [
            f"{req.product.get('name')} - {req.product.get('price')}，{req.resident.get('name', '我')}亲测好物！",
            f"强烈推荐！{req.product.get('name')}，{req.product.get('description', '')}",
        ]
    }
    
    content = random.choice(templates.get(req.adType, templates["soft_ad"]))
    return {
        "content": content,
        "creativityScore": random.randint(5, 8),
        "qualityScore": random.randint(6, 9)
    }

@app.get("/api/ads")
async def get_ads():
    """获取广告列表（预留接口，当前前端使用 localStorage）"""
    return []

@app.post("/api/ads")
async def create_ad(ad: dict):
    """创建广告（预留接口，当前前端使用 localStorage）"""
    return ad

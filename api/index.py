"""
AdsTown - AI 广告小镇后端
Vercel Serverless Python
"""
import os
import random
import json
from urllib.parse import parse_qs

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def app(environ, start_response):
    """Vercel Python 入口"""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # CORS headers
    headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type'),
    ]
    
    # Handle OPTIONS preflight
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']
    
    # Root
    if path == '/' or path == '/index.html':
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                body = f.read().encode('utf-8')
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')] + headers)
            return [body]
        except:
            start_response('404 Not Found', headers)
            return [b'Not Found']
    
    # Health check
    if path == '/health':
        start_response('200 OK', [('Content-Type', 'application/json')] + headers)
        return [json.dumps({"status": "healthy"}).encode()]
    
    # Generate ad API
    if path == '/api/generate-ad' and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            req_data = json.loads(body)
            
            resident = req_data.get('resident', {})
            product = req_data.get('product', {})
            ad_type = req_data.get('adType', 'soft_ad')
            
            ad_type_tips = {
                "soft_ad": "软性广告，要自然融入日常生活场景",
                "hard_ad": "硬广，可以直接介绍产品优点"
            }
            
            prompt = f"""你是AdsTown小镇的广告文案专家。

产品：{product.get('name', '产品')} - {product.get('description', '')}，价格：{product.get('price', '')}
创作者：{resident.get('name', '小镇居民')}，角色：{resident.get('role', '')}，性格：{resident.get('personality', '')}
类型：{ad_type_tips.get(ad_type, '')}

要求：50-100字，体现创作者性格，突出产品价值。直接输出文案："""
            
            content = None
            if DEEPSEEK_API_KEY:
                import httpx
                try:
                    resp = httpx.post(
                        DEEPSEEK_API_URL,
                        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
                        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "max_tokens": 200},
                        timeout=30.0
                    )
                    if resp.status_code == 200:
                        result = resp.json()
                        content = result['choices'][0]['message']['content'].strip()
                except Exception as e:
                    print(f"API error: {e}")
            
            # Fallback
            if not content:
                templates = {
                    "soft_ad": [
                        f"在小镇的每一天，我都会想起{product.get('name')}...{product.get('description', '')}",
                        f"如果你问我什么值得尝试，那一定是{product.get('name')}...",
                    ],
                    "hard_ad": [
                        f"{product.get('name')} - {product.get('price')}，亲测好物！",
                        f"强烈推荐！{product.get('name')}，{product.get('description', '')}",
                    ]
                }
                content = random.choice(templates.get(ad_type, templates["soft_ad"]))
            
            result = {
                "content": content,
                "creativityScore": random.randint(6, 10),
                "qualityScore": random.randint(7, 10)
            }
            
            start_response('200 OK', [('Content-Type', 'application/json')] + headers)
            return [json.dumps(result).encode()]
        except Exception as e:
            start_response('500 Error', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"error": str(e)}).encode()]
    
    # Ads API (stub)
    if path == '/api/ads':
        start_response('200 OK', [('Content-Type', 'application/json')] + headers)
        return [json.dumps([]).encode()]
    
    # 404
    start_response('404 Not Found', headers)
    return [b'Not Found']

# For local development
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = int(os.getenv("PORT", 5000))
    print(f"Server running on port {port}")
    make_server('0.0.0.0', port, app).serve_forever()

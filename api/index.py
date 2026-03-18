"""
AdsTown - AI 广告小镇后端
Vercel Serverless Python
"""
import os
import random
import json
from datetime import datetime

# 加载 .env 文件（本地开发）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import httpx

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# SecondMe OAuth 配置
SECONDME_CLIENT_ID = os.getenv("SECONDME_CLIENT_ID", "")
SECONDME_CLIENT_SECRET = os.getenv("SECONDME_CLIENT_SECRET", "")
SECONDME_REDIRECT_URI = os.getenv("SECONDME_REDIRECT_URI", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://secendme-ads-town.vercel.app")

SECONDME_AUTH_URL = "https://go.second.me/oauth/"
SECONDME_TOKEN_URL = "https://api.mindverse.com/gate/lab/api/oauth/token/code"
SECONDME_PROFILE_URL = "https://api.mindverse.com/gate/lab/api/secondme/user/info"

# 内存存储（Vercel 会重置，生产环境用数据库）
AVATARS_DATA = {}

def app(environ, start_response):
    """Vercel Python 入口"""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    query_string = environ.get('QUERY_STRING', '')
    
    # CORS headers
    headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE'),
        ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
    ]
    
    # Handle OPTIONS preflight
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']
    
    # Root - serve index.html
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
    
    # ===== SecondMe OAuth =====
    
    # 登录入口
    if path == '/api/login':
        if not SECONDME_CLIENT_ID:
            start_response('400 Bad Request', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"error": "SecondMe OAuth not configured"}).encode()]
        
        state = f"adstown_{random.randint(100000, 999999)}"
        params = f"client_id={SECONDME_CLIENT_ID}&redirect_uri={SECONDME_REDIRECT_URI}&response_type=code&scope=user.info,chat&state={state}"
        auth_url = SECONDME_AUTH_URL + "?" + params
        
        start_response('302 Found', [('Location', auth_url)] + headers)
        return [b'']
    
    # OAuth 回调
    if path == '/api/callback':
        from urllib.parse import parse_qs
        query_params = parse_qs(query_string)
        code = query_params.get('code', [''])[0]
        
        if not code:
            start_response('400 Bad Request', headers)
            return [b'Missing code']
        
        try:
            resp = httpx.post(
                SECONDME_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": SECONDME_CLIENT_ID,
                    "client_secret": SECONDME_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": SECONDME_REDIRECT_URI,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30.0
            )
            token_data = resp.json()
            
            if token_data.get("code") != 0:
                start_response('400 Bad Request', headers)
                return [f"Token error: {token_data.get('message')}".encode()]
            
            access_token = token_data.get("data", {}).get("accessToken")
            
            profile_resp = httpx.get(
                SECONDME_PROFILE_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=15.0
            )
            profile = profile_resp.json()
            user_info = profile.get("data", profile)
            user_name = user_info.get("name", user_info.get("username", "Anonymous"))
            user_id = user_info.get("user_id", user_name)
            
            # 初始化用户数据
            if user_id not in AVATARS_DATA:
                AVATARS_DATA[user_id] = {"avatars": [], "token": access_token}
            
            from urllib.parse import quote
            redirect_url = f"{FRONTEND_URL}?logged_in=true&user_name={quote(user_name)}&user_id={quote(user_id)}&token={access_token}"
            start_response('302 Found', [('Location', redirect_url)] + headers)
            return [b'']
            
        except Exception as e:
            start_response('500 Error', headers)
            return [f"Error: {str(e)}".encode()]
    
    # 获取当前用户
    if path == '/api/me':
        auth_header = environ.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            start_response('200 OK', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"logged_in": False}).encode()]
        
        token = auth_header.replace('Bearer ', '')
        
        try:
            resp = httpx.get(
                SECONDME_PROFILE_URL,
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            profile = resp.json()
            user_info = profile.get("data", profile)
            
            start_response('200 OK', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({
                "logged_in": True,
                "user": {
                    "name": user_info.get("name", "Anonymous"),
                    "username": user_info.get("username", ""),
                    "avatar": user_info.get("avatar", "")
                }
            }).encode()]
        except:
            start_response('200 OK', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"logged_in": False}).encode()]
    
    # ===== 分身 API =====
    
    # 获取用户分身列表
    if path == '/api/avatars' and method == 'GET':
        from urllib.parse import parse_qs
        params = parse_qs(query_string)
        user_id = params.get('user_id', [''])[0]
        
        avatars = AVATARS_DATA.get(user_id, {}).get('avatars', [])
        start_response('200 OK', [('Content-Type', 'application/json')] + headers)
        return [json.dumps(avatars).encode()]
    
    # 创建分身
    if path == '/api/avatars' and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            req_data = json.loads(body)
            
            user_id = req_data.get('user_id')
            if not user_id:
                start_response('400 Bad Request', [('Content-Type', 'application/json')] + headers)
                return [json.dumps({"error": "user_id required"}).encode()]
            
            # 初始化用户数据
            if user_id not in AVATARS_DATA:
                AVATARS_DATA[user_id] = {"avatars": [], "token": ""}
            
            avatar = {
                "id": f"avatar_{len(AVATARS_DATA[user_id]['avatars']) + 1}",
                "name": req_data.get('name', '我的分身'),
                "avatar": req_data.get('avatar', '😊'),
                "product": req_data.get('product', {}),
                "ad_type": req_data.get('ad_type', 'soft_ad'),
                "ad_interval": req_data.get('ad_interval', 10),  # 秒
                "is_active": False,
                "created_at": datetime.now().isoformat()
            }
            
            AVATARS_DATA[user_id]['avatars'].append(avatar)
            
            start_response('200 OK', [('Content-Type', 'application/json')] + headers)
            return [json.dumps(avatar).encode()]
        except Exception as e:
            start_response('500 Error', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"error": str(e)}).encode()]
    
    # 更新分身状态（启动/停止）
    if path.startswith('/api/avatars/') and path.endswith('/toggle') and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            req_data = json.loads(body)
            
            user_id = req_data.get('user_id')
            avatar_id = path.split('/')[-2]
            
            if user_id in AVATARS_DATA:
                for avatar in AVATARS_DATA[user_id]['avatars']:
                    if avatar['id'] == avatar_id:
                        avatar['is_active'] = req_data.get('is_active', False)
                        start_response('200 OK', [('Content-Type', 'application/json')] + headers)
                        return [json.dumps(avatar).encode()]
            
            start_response('404 Not Found', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"error": "Avatar not found"}).encode()]
        except Exception as e:
            start_response('500 Error', [('Content-Type', 'application/json')] + headers)
            return [json.dumps({"error": str(e)}).encode()]
    
    # 删除分身
    if path.startswith('/api/avatars/') and method == 'DELETE':
        from urllib.parse import parse_qs
        params = parse_qs(query_string)
        user_id = params.get('user_id', [''])[0]
        avatar_id = path.split('/')[-1]
        
        if user_id in AVATARS_DATA:
            AVATARS_DATA[user_id]['avatars'] = [a for a in AVATARS_DATA[user_id]['avatars'] if a['id'] != avatar_id]
        
        start_response('200 OK', [('Content-Type', 'application/json')] + headers)
        return [json.dumps({"success": True}).encode()]
    
    # ===== 广告 API =====
    
    # 生成广告
    if path == '/api/generate-ad' and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            req_data = json.loads(body)
            
            user_info = req_data.get('user', {})
            user_name = user_info.get('name', '')
            
            resident = req_data.get('resident', {})
            product = req_data.get('product', {})
            ad_type = req_data.get('adType', 'soft_ad')
            
            creator_name = user_name if user_name else resident.get('name', '小镇居民')
            creator_role = user_info.get('role', '') if user_name else resident.get('role', '')
            creator_personality = user_info.get('personality', '') if user_name else resident.get('personality', '')
            
            ad_type_tips = {
                "soft_ad": "软性广告，要自然融入日常生活场景",
                "hard_ad": "硬广，可以直接介绍产品优点"
            }
            
            prompt = f"""你是AdsTown小镇的广告文案专家。

产品：{product.get('name', '产品')} - {product.get('description', '')}，价格：{product.get('price', '')}
创作者：{creator_name}，角色：{creator_role}，性格：{creator_personality}
类型：{ad_type_tips.get(ad_type, '')}

要求：50-100字，体现创作者性格，突出产品价值。直接输出文案："""
            
            content = None
            if DEEPSEEK_API_KEY:
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

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = int(os.getenv("PORT", 5000))
    print(f"Server running on port {port}")
    make_server('0.0.0.0', port, app).serve_forever()

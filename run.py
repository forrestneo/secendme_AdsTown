"""
本地运行脚本
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

print(f"CLIENT_ID: {os.getenv('SECONDME_CLIENT_ID', 'NOT SET')[:10]}...")

from wsgiref.simple_server import make_server
from api.index import app

print("启动服务: http://localhost:5000")
make_server('0.0.0.0', 5000, app).serve_forever()

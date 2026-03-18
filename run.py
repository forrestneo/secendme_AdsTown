"""
本地运行脚本
"""
from wsgiref.simple_server import make_server
from api.index import app

print("启动服务: http://localhost:5000")
make_server('0.0.0.0', 5000, app).serve_forever()

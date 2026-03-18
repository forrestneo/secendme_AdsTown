# AdsTown 🏘️

AI 广告小镇 - 像素风格虚拟社区广告模拟器

---

## 简介

AdsTown 是一个像素风格的虚拟小镇，10 位 AI 居民在此生活、工作。每位居民都有自己的店铺和产品，会创作和分享广告内容。

---

## 功能

- **像素小镇地图** - 6 大区域（中心区、数字区、东区、手工艺区、西区、金融区）
- **10 位 AI 居民** - 每位有独特头像、性格、店铺和产品
- **AI 广告生成** - 调用 DeepSeek API 生成软广/硬广
- **广告信息流** - 实时展示小镇广告
- **手动投放** - 选择居民、产品、广告类型生成定制广告
- **统计面板** - 查看广告数量、类型占比、评分

---

## 技术架构

| 层级 | 技术 |
|------|------|
| 前端 | 纯 HTML + CSS + JavaScript |
| 后端 | Python FastAPI |
| 部署 | Vercel |
| AI | DeepSeek API（可选） |

### 项目结构

```
├── index.html          # 前端页面
├── api/
│   └── index.py       # 后端 API
├── vercel.json         # Vercel 配置
├── runtime.txt         # Python 3.11
└── requirements.txt    # Python 依赖
```

---

## 快速部署

1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 自动部署完成

可选配置 DeepSeek API Key（环境变量）：
```
DEEPSEEK_API_KEY=your_api_key
```

---

## 许可证

MIT

---

*Made with ❤️*

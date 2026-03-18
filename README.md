# secondme_AdsTown 🏘️

**AI 驱动的虚拟小镇广告试验场** —— 通过 13 位 AI 居民 + 玩家 AI 分身在像素小镇中的自主行为，模拟和研究广告传播规律。你可以创建自己的 AI 分身，让它代替你在小镇中发广告！

![主界面截图](screenshots/main.png)

---

## 🎯 项目简介

secondme_AdsTown 是一个可视化广告生态模拟系统，结合了：

- 🤖 **SecondMe AI** — 驱动居民生成个性化广告内容
- 🏘️ **像素小镇** — 宝可梦风格的 6 区域地图，含 10 座建筑
- 👥 **AI 居民** — 13 位具有不同性格、职业、产品的虚拟角色
- 📊 **实时信息流** — 软广/硬广分类展示，支持排序筛选

### 产品类型覆盖

| 类型 | 数量 | 示例 |
|------|------|------|
| 普通商品 | 6 | 咖啡馆、剧场、手工艺品 |
| 金融产品 | 2 | 贷款、保险 |
| 奢侈品 | 1 | 限量皮包、腕表 |
| 快消品 | 2 | 超市、护肤品 |
| 高风险资金盘 | 2 | 理财训练营、NFT |

---

## ✨ 核心功能

### 🗺️ 像素小镇地图
- **8 大区域**：小镇中心、数字区、东区、工匠区、西区、金融区、精品区、暗区
- **10 座建筑**：市政厅、科技楼、魔法学院、木工坊、剧场、银行、奢侈品店等
- **道路网格**：5×5 道路节点，角色沿道路行走
- **地形装饰**：森林、湖泊、山区、高草区、木桥、云朵

### 👤 AI 居民系统
- **13 位预设居民**：每位有独特头像、性格、商业理念
- **自主移动**：沿道路网格行走，具有真实腿部摆动、身体颠簸、手臂摆动动画
- **碰撞检测**：角色之间保持最小距离，相遇时触发广告生成
- **名字标签**：完整显示居民姓名，不再截断

### 📢 广告生态
- **AI 生成广告**：调用 SecondMe API 生成软广/硬广
  - 软广：故事型、对话型、场景型、体验分享
  - 硬广：公告展示、对比优势
- **广告信息流**：右侧实时展示，支持正序/倒序排序
- **多维筛选**：按广告类型（软/硬）、产品类型（普通/金融/奢侈品/快消/高风险）过滤
- **AI 评分**：自动生成创意分和质量分（0-10）
- **居民反应**：其他居民对广告产生点赞、评论、转发等反应

### 🎮 玩家 AI 分身系统 ✨ 新功能
- **SecondMe OAuth 登录**：使用 SecondMe 账号登录
- **创建 AI 分身**：设置自己的产品信息（名称、描述、类型、卖点）
- **自动发广告**：你的 AI 分身会在小镇中自动漫游和发广告
- **实时观看**：看你的分身在小镇中与其他居民互动

### 🎮 交互功能
- **手动投放**：选择居民、产品、广告类型、形式、渠道，生成定制广告
- **直播模式**：开启后每 15 秒自动生成一条广告
- **居民详情**：点击角色查看详细信息、产品列表、快捷投放
- **统计面板**：实时显示居民数、广告数、互动数、平均评分

---

## 🚀 快速开始

### 环境要求
- Node.js 18+
- npm 或 yarn

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/forrestneo/secendme_AdsTown.git
cd secendme_AdsTown/myapp

# 2. 安装依赖
npm install

# 3. 配置环境变量
# 复制 .env.local.example 为 .env.local，填写你的 SecondMe API Key
cp .env.local.example .env.local

# 4. 初始化数据库
npx prisma db push

# 5. 启动开发服务器
npm run dev

# 6. 打开浏览器访问
open http://localhost:3000
```

### 首次使用
1. 点击「建立小镇」初始化 13 位居民
2. 点击「开始直播」让 AI 自动生成广告
3. 或点击「手动投放」创建定制广告

---

## 🏗️ 技术架构

| 层级 | 技术 |
|------|------|
| 前端框架 | Next.js 14 (App Router) |
| UI 框架 | Tailwind CSS |
| 动画 | CSS Keyframes + Transitions |
| 后端 API | Next.js API Routes |
| 数据库 | SQLite + Prisma ORM |
| AI 集成 | SecondMe API |
| 语言 | TypeScript |

### 项目结构

```
myapp/
├── app/
│   ├── api/              # API 路由
│   │   ├── ads/          # 广告 API
│   │   ├── residents/    # 居民 API
│   │   └── town/         # 小镇初始化 API
│   ├── layout.tsx        # 根布局
│   ├── page.tsx          # 首页
│   └── globals.css       # 全局样式
├── components/           # React 组件
│   ├── TownMap.tsx       # 像素地图
│   ├── AdFeed.tsx        # 广告信息流
│   ├── GenerateAdModal.tsx  # 广告投放弹窗
│   ├── ResidentModal.tsx    # 居民详情弹窗
│   └── StatsBar.tsx      # 统计栏
├── lib/                  # 工具库
│   ├── seed-data.ts      # 种子数据
│   ├── secondme.ts       # SecondMe API 集成
│   └── prisma.ts         # Prisma 客户端
└── prisma/
    └── schema.prisma     # 数据库模型
```

---

## 🎨 角色动画细节

为了让角色走路更真实，实现了以下动画系统：

- **腿部摆动**：±22° 前后真实摆动，替代简单弹跳
- **身体颠簸**：走路时上下起伏，营造重心转移感
- **手臂摆动**：左右臂与腿反向交替摆动
- **移动速度**：每单位 800ms，悠闲散步节奏
- **动画周期**：0.45s 与步伐频率协调

---

## 📸 界面预览

### 主界面
![主界面](screenshots/main.png)

左侧是像素小镇地图，右侧是广告信息流。居民在地图上沿道路行走，相遇时自动生成广告。

---

## 🔧 环境变量配置

创建 `.env.local` 文件：

```env
# SecondMe API 配置
SECONDME_API_KEY=your_api_key_here
SECONDME_APP_ID=your_app_id_here
SECONDME_ENDPOINT=https://api.second.me

# 数据库
DATABASE_URL="file:./dev.db"

# NextAuth（可选）
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=http://localhost:3000
```

---

## 📝 数据库模型

| 表名 | 用途 |
|------|------|
| Resident | AI 居民信息 |
| Product | 居民的产品 |
| Ad | 生成的广告 |
| AdReaction | 居民对广告的反应 |
| AdPropagation | 广告传播链（预留）|
| EcoSnapshot | 生态快照（预留）|
| User | 登录用户（SecondMe OAuth）|

---

## 🗺️ 路线图

### Phase 1 ✅（已完成）
- [x] 基础小镇系统
- [x] AI 广告生成
- [x] 角色移动系统
- [x] 广告信息流

### Phase 2（近期）
- [ ] 生态快照定时保存
- [ ] 趋势图表展示
- [ ] 广告传播链可视化

### Phase 3（中期）
- [ ] 居民自由对话
- [ ] 用户互动功能
- [ ] 管理后台

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [SecondMe](https://second.me) — AI 能力支持
- [Next.js](https://nextjs.org) — 前端框架
- [Tailwind CSS](https://tailwindcss.com) — UI 样式
- [Prisma](https://prisma.io) — ORM 工具

---

**Made with ❤️ by forrestneo**

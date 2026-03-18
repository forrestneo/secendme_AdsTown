# 虚拟小镇广告试验场

## 项目概述

本项目是基于 SecondMe API 构建的 Next.js 应用，名为"虚拟小镇广告试验场"。

## SecondMe 配置

- **App ID**: `1a1e0be3-73d1-4e02-8645-77914de613e3`
- **API 端点**: `https://api.second.me`
- **已启用模块**: auth, chat, profile, note

## 技术栈

- **框架**: Next.js 14 (App Router)
- **数据库**: SQLite（通过 Prisma ORM）
- **样式**: Tailwind CSS
- **语言**: TypeScript

## 功能模块

### auth（认证）
用户注册、登录、Token 管理

### chat（AI 对话）
通过 SecondMe API 与 AI 进行对话交互

### profile（用户画像）
用户个人信息与 Second Me 画像管理

### note（笔记）
用户笔记的创建、编辑与管理

## 开发规范

- 界面语言：中文
- 主题：亮色（浅色）主题
- 设计风格：简约优雅，减少视觉噪音
- 动画：仅使用简单过渡效果

## 环境变量

参见 `.env.local` 文件（不要提交到 git）

## 安全提醒

- `.secondme/` 目录包含敏感配置，已加入 `.gitignore`
- API Key 仅存于 `.env.local`，不要硬编码到源码中

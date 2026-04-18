# 《古法代码之王》展示站

## 立项背景

2026-04-18 从桌面归档的 `全世界AI崩溃后古法程序员的逆袭.zip` (356MB) 立项。原始压缩包来源未知（疑似之前 AI 协作创作的产物），内容包括：

- **小说正文**：《古法代码之王》.md，2317 行，约 12 万字，21 章正文 + 终章
- **插图素材**：22 张 AI 生成插图（主角参考 + 第 1–20 章 + 终章），每张均有处理版 + 原始版
- **创作文档**：大纲、插画风格指南、插画提示词方案、场景详述

## 故事定位

近未来都市科幻爽文。全球程序员因长期依赖 AI 编码退化，唯有男主顾沉舟坚持手写代码，在宙核智编网系统性崩溃后完成"旧时代火种"式逆袭。四卷结构：被时代埋掉 → 寒冬独守 → 黑箱裂缝 → 旧时代火种归位。

## 目录结构

```
20260418-古法程序员逆袭/
├── .memory/              项目记忆
├── raw-packages/         原始压缩包（两层：外层 + 内嵌 ai_coding_novel_full_package.zip）
├── source/               内嵌 zip 解压物，共 22 张处理版 + 22 张 original 原图 + 4 md
├── novel/《古法代码之王》.md  主小说
├── docs/                 创作文档（大纲、风格指南、插画方案）
└── web/                  展示网页（index.html + images/）
```

## 展示站方案

单页静态站，分三区：

1. **Hero** — 主角参考图 + 书名 + 副标题
2. **章节目录** — 21 + 1 章卡片，点击展开
3. **逐章阅读** — 章节图 + 正文，支持连续滚动阅读
4. **画廊模式** — 可选切换纯图浏览

视觉：近未来都市写实（冷灰蓝 → 深黑金，跟随小说情绪推进）。

## 部署（已上线 2026-04-18）

- **线上**：https://gufa-code.kang-kang.com  (HTTP/2 + HTTP/3)
- **Gitea 主仓**：https://git.kang-kang.com/kangwan/gufa-code-king
- **GitHub 镜像**：https://github.com/kang2050/gufa-code-king
- **Coolify UUID**：`yu2cuh6p5lk898uf2ow7wg53`（project 网页集合 `ew48wsw8wskkgc8ksso4488s`）
- **build**：dockerfile，base `/web`，Dockerfile `/Dockerfile`（nginx:alpine）
- **踩坑**：第一次传 git_repository 只写到 `https://git.kang-kang.com/kangwan/gufa-code-king`（未带 .git 和凭证），Coolify 存储时截取成 `kangwan/gufa-code-king` 当作 GitHub owner/repo，部署失败；PATCH 修正为完整 `https://kangwan:<token>@git.kang-kang.com/kangwan/gufa-code-king.git` 后立即成功。

## 时间线

- 2026-04-18：立项、解压、整理结构、做展示站

# 《古法代码之王》

> 当全世界都把写代码交给 AI，只有一个被时代淘汰的人，还记得如何真正让系统运转。

近未来都市科技爽文 + 原创 AI 插图的创作展示站。

- **正文**：21 章，约 12 万字
- **插图**：22 幅（主角参考 + 第 1–20 章 + 终章）
- **线上地址**：[gufa-code.kang-kang.com](https://gufa-code.kang-kang.com)

## 目录结构

| 目录 | 内容 |
|---|---|
| `novel/` | 小说正文 md |
| `docs/` | 大纲、插画风格指南、插画提示词方案 |
| `source/` | AI 插图完整素材（处理版 + 原始版）|
| `raw-packages/` | 原始压缩包归档 |
| `web/` | 展示站（Dockerfile + nginx:alpine）|

## 本地预览

```bash
cd web && python3 -m http.server 8765
# open http://localhost:8765
```

## 部署

Coolify 指向 `web/Dockerfile`，build 出 nginx:alpine 静态站。

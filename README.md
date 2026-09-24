# 行星与流体 · 文献雷达

一个无需 AI API 的研究组文献实验站。公开浏览，管理员通过 GitHub 编辑 topics.json；GitHub Actions 每日北京时间 09:17 抓取并发布（实际运行可能延迟）。

关注大气／气候动力学、行星大气、系外行星探测、行星演化、物理海洋和表层系统物理化学。当前仅使用关键词规则，**没有 AI 评分**。污染主题进入排除候选，保留人工复核入口。

## 运行

Python 3.9+，无第三方依赖：

```
python3 update.py --days 7
python3 -m http.server 8766
python3 -m unittest discover -p 'test_*.py' -v
```

## 管理

编辑 topics.json 的 topics / terms / exclude_terms。overrides 可按 arXiv ID 设置人工覆盖，例如：

```json
{"2609.00001":{"status":"candidate","reason":"管理员判断：动力学方法可借鉴"}}
```

status 可用 candidate、excluded、unmatched。不要添加账号密码、API 密钥或私密研究资料。网站不需要任何 ChatGPT 登录信息。

## 部署

Settings → Pages → Source 选择 GitHub Actions。运行 Update literature and publish。只发布页面文件与文献数据，脚本及配置不进入网页发布包（公开仓库内仍可见）。

来源失败时保留历史记录和成功检查点，页面如实展示失败状态，下一次运行补抓。尚未接入期刊源或 AI。公开仓库长期无活动可能导致 GitHub 定时任务停用，管理员应检查 Actions 状态。

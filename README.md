# Planet / Fluid · 行星与流体文献雷达

主要为 **北京大学物理学院大气与海洋科学系行星大气研究方向** 服务的公开文献追踪网站。

[浏览网站](https://pkujunyanggroup.github.io/planet-fluid-radar/) · [数据来源与方法](https://pkujunyanggroup.github.io/planet-fluid-radar/sources.html)

根据杨军、丁峰和 Daniel Koll 的公开研究主题确定筛选范围，收录全球相关研究。作者姓名不作为收录条件，不建设个人论文专栏。

研究背景参考：[杨军](https://faculty.pku.edu.cn/junyang/en/zdylm/40837/list/index.htm)、[丁峰](https://faculty.pku.edu.cn/dingfeng/zh_CN/lwcg/46562/list/2.htm)、[Daniel Koll](https://danielkoll.github.io/research/)、[系内研究介绍](https://www.atmos.pku.edu.cn/kxyj/yjfx/3dqyhykxx345.htm)。

## 学科与内容

- 行星大气与气候
- 大气物理：重点为相关的辐射、云、水汽与凝结物理
- 大气与气候动力学
- 物理海洋与地球流体
- 系外行星探测与表征
- 行星内部与演化
- 表层过程与古气候
- 数学物理与数值方法

每篇展示双语导读、学科与机制标签、作者及可核实的机构。首页可按方向、关键词、收录时间筛选，搜索包括作者、机构与双语导读。

## 日期与来源

`first_seen` 是首次进入本站数据的时间，后续抓取不重置；页面以北京时间显示“网站收录”。`publication_date` 是 arXiv 首次提交发布日期，来自原文 citation_date 或 API，不是期刊发表日期。`version_date` 为可核实的修订提交时间。RSS 公告时间单独保存在原始记录中，不能冒充首次发布日期。缺失日期不猜测。

目前接入 arXiv 的 astro-ph.EP、physics.ao-ph、physics.flu-dyn、physics.geo-ph；Nature、Science 等期刊尚未接入。API 查询失败时 RSS 提供当期补充，历史回查状态会公开显示。

## 自动更新

GitHub Actions 每日北京时间约 09:17 运行，也支持手动启动；平台排队可能延迟。

1. `update.py` 抓取、去重、按 `topics.json` 分类，保留首次收录时间和历史记录。
2. `enrich.py` 从 arXiv HTML 提取作者机构，应用与版本及摘要校验值匹配的 `editorial.json` 双语导读。
3. `dates.py` 核实首次发布日期与版本日期。
4. 提交数据文件，并通过 GitHub Pages 发布静态网站。

无需 API 密钥。现有双语导读由 AI 辅助根据公开摘要整理；新文章尚无中文导读时自动显示英文摘要节选及待整理提示。**当前并未接入每日自动生成中文导读的服务。** 筛选使用可解释规则，不等同于 AI 相关性判断。机构只采用明确的来源字段；缺失信息不根据姓名推断。

管理员在 `topics.json` 维护词组和人工覆盖项。网页公开可读，规则修改遵循仓库写入权限。

## 本地维护

Python 3.9+，仅使用标准库。

```sh
python3 -m unittest discover -p 'test_*.py' -v
python3 update.py --days 7
python3 enrich.py --limit 60
python3 dates.py --limit 60
python3 -m http.server 8766
```

来源出错时 `update.py` 返回非零状态，但保留历史并写明失败状态。工作流仍会先发布页面，再报告抓取问题。机构缓存为 `affiliations.json`，日期缓存为 `dates.json`；两者按版本保存。

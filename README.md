# Planet / Fluid · 行星与流体文献雷达

主要为 **北京大学物理学院大气与海洋科学系行星大气研究方向** 服务的公开文献追踪网站。

[浏览网站](https://pkujunyanggroup.github.io/planet-fluid-radar/) · [数据来源与方法](https://pkujunyanggroup.github.io/planet-fluid-radar/sources.html)

研究方向涵盖行星气候与宜居性、云和辐射反馈、水循环、热输送、大气环流、海冰与海洋过程及行星大气观测表征，收录全球相关研究。


## 学科与内容

- 行星大气与气候 · Planetary atmospheres & climate
- 大气物理：重点为相关的辐射、云、水汽与凝结物理
- 大气动力学 · Atmospheric dynamics
- 气候动力学 · Climate dynamics
- 物理海洋 · Physical oceanography
- 地球流体力学 · Geophysical fluid dynamics
- 系外行星探测与表征 · Exoplanet detection & characterization
- 行星内部与演化 · Planetary interiors & evolution
- 表层过程与古气候 · Surface processes & paleoclimate
- 数学物理与数值方法 · Mathematical physics & methods

每篇展示双语导读、学科与机制标签、作者及可核实的机构。首页可按方向、关键词、收录时间筛选，搜索包括作者、机构与双语导读。

## 日期与来源

`first_seen` 是首次进入本站数据的时间，后续抓取不重置；页面以北京时间显示“网站收录”。`publication_date` 是 arXiv 首次提交发布日期，来自原文 citation_date 或 API，不是期刊发表日期。`version_date` 为可核实的修订提交时间。RSS 公告时间单独保存在原始记录中，不能冒充首次发布日期。缺失日期不猜测。

目前接入 arXiv 的 astro-ph.EP、physics.ao-ph、physics.flu-dyn、physics.geo-ph；期刊接入情况见下方扩展版说明与网站来源页。API 查询失败时 RSS 提供当期补充，历史回查状态会公开显示。

## 自动更新

GitHub Actions 每日北京时间约 09:17 运行，也支持手动启动；平台排队可能延迟。

1. `update.py` 抓取、去重、按 `topics.json` 分类，保留首次收录时间和历史记录。
2. `enrich.py` 从 arXiv HTML 提取作者机构，应用与版本及摘要校验值匹配的 `editorial.json` 双语导读。
3. `dates.py` 核实首次发布日期与版本日期。
4. `update_journals.py` 更新期刊元数据，`build_catalog.py` 归并来源，`build_network.py` 生成机构网络。
5. 提交数据文件，并通过 GitHub Pages 发布静态网站。

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

## 期刊来源（扩展版）

新增 `journals.json`，按综合、大气、海洋、气候、地球与行星分组配置 23 种期刊，包括 Nature、Science、PNAS、Nature Geoscience、Nature Astronomy、Nature Climate Change、JAS、ACP、JGR 各相关刊、JPO、Ocean Modelling、Paleoceanography and Paleoclimatology、Journal of Climate、Climate Dynamics、Climate of the Past、QJRMS、Astrobiology、GRL、ApJ、ApJL、EPSL。

期刊记录使用出版商向 Crossref 登记的公开元数据，首次检索近 14 天，后续按登记更新时间增量检索并保留检查点。来源页逐项显示状态与成功时间。无摘要时只按标题筛选并明确标注；接口可能晚于出版商网页。

`build_catalog.py` 将 arXiv 与期刊记录合成 `catalog.json`。相同 DOI、明确的预印本关系优先归并；无 DOI 时，较长标题完全相同且存在共同作者姓氏才自动关联。相似标题不直接合并。各版本来源、首次收录时间与发表时间均保留，可能仍有未识别的重复记录。

## 机构网络

[机构网络](https://pkujunyanggroup.github.io/planet-fluid-radar/network.html) 提供力导向布局、节点拖动、平移缩放、机构/作者搜索、学科筛选及机构详情。默认显示至少有两篇文献的机构，可切换全部机构。

`build_network.py` 仅使用相关候选的署名机构。连线表示机构在同一篇文献出现，权重为共同文献数量。作者只来自明确的作者—机构元数据，不以姓名猜测归属；这不是现职人员名录。`institution_aliases.json` 维护明确别名，未知单位保留原始表述，名称归一和机构覆盖仍不完整。

扩展流程：

```sh
python3 update_journals.py --days 14
python3 build_catalog.py
python3 build_network.py
```

日常部署发布 `catalog.json` 与 `network.json`，原始数据分别保存在 `papers.json`（arXiv）和 `journal_records.json`（期刊）。

# Planet / Fluid · 行星与流体文献雷达

主要为 **北京大学物理学院大气与海洋科学系行星大气研究方向** 服务的公开文献追踪网站。

[浏览网站](https://pkujunyanggroup.github.io/planet-fluid-radar/) · [数据来源与方法](https://pkujunyanggroup.github.io/planet-fluid-radar/sources.html)

研究方向涵盖行星气候与宜居性、行星轨道动力学、云和辐射反馈、水循环、热输送、大气环流、海冰与海洋过程及行星大气观测表征，收录全球相关研究。


## 学科与内容

- 行星大气与气候 · Planetary atmospheres & climate
- 行星大气化学 · Planetary atmospheric chemistry
- 行星大气模式 · Planetary atmospheric models
- 大气物理：重点为相关的辐射、云、水汽与凝结物理
- 大气动力学 · Atmospheric dynamics
- 气候动力学 · Climate dynamics
- 物理海洋 · Physical oceanography
- 地球流体力学 · Geophysical fluid dynamics
- 系外行星探测与表征 · Exoplanet detection & characterization
- 行星轨道动力学 · Planetary orbital dynamics
- 行星内部与演化 · Planetary interiors & evolution
- 行星冰冻圈、冰物理与冰动力 · Planetary cryospheres, ice physics & ice dynamics
- 表层过程与古气候 · Surface processes & paleoclimate
- 数学、物理、数值方法 · Mathematics, Physics & Numerical Methods

每篇展示双语导读、学科与机制标签、作者及可核实的机构。首页可按方向、关键词、收录时间筛选，搜索包括作者、机构与双语导读。

## 日期与来源

`first_seen` 是首次进入本站数据的时间，后续抓取不重置；页面以北京时间显示“网站收录”。`publication_date` 是 arXiv 首次提交发布日期，来自原文 citation_date 或 API，不是期刊发表日期。`version_date` 为可核实的修订提交时间。RSS 公告时间单独保存在原始记录中，不能冒充首次发布日期。缺失日期不猜测。

目前接入 arXiv 的 astro-ph.EP、physics.ao-ph、physics.flu-dyn、physics.geo-ph；期刊接入情况见下方扩展版说明与网站来源页。每天按最近更新检查点抓取新发布或新更新的记录，不向更早日期扩展回溯；已收录历史记录与中文导读整理继续保留。API 查询失败时 RSS 提供当期补充，来源状态会公开显示。

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
python3 update.py --days 1
python3 enrich.py --limit 60
python3 dates.py --limit 60
python3 -m http.server 8766
```

来源出错时 `update.py` 返回非零状态，但保留历史并写明失败状态。工作流仍会先发布页面，再报告抓取问题。机构缓存为 `affiliations.json`，日期缓存为 `dates.json`；两者按版本保存。

## 期刊来源（扩展版）

新增 `journals.json`，按综合、大气、海洋、气候、地球与行星分组配置 23 种期刊，包括 Nature、Science、PNAS、Nature Geoscience、Nature Astronomy、Nature Climate Change、JAS、ACP、JGR 各相关刊、JPO、Ocean Modelling、Paleoceanography and Paleoclimatology、Journal of Climate、Climate Dynamics、Climate of the Past、QJRMS、Astrobiology、GRL、ApJ、ApJL、EPSL。

期刊记录使用出版商向 Crossref 登记的公开元数据，每日检查当日新发表记录及自上次成功检查以来登记更新的记录，不批量回查更早月份；后续按登记更新时间增量检索并保留检查点。来源页逐项显示状态与成功时间。无摘要时只按标题筛选并明确标注；接口可能晚于出版商网页。

`build_catalog.py` 将 arXiv、启用的期刊及 Exoplanet.eu 近期文献合成 `catalog.json`，公开目录和机构图只展示符合窄范围的相关候选；原始抓取档案保留供来源审计。相同 DOI、明确的预印本关系优先归并；无 DOI 时，较长标题完全相同且存在共同作者姓氏才自动关联。相似标题不直接合并。各版本来源、首次收录时间与发表时间均保留，可能仍有未识别的重复记录。

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

## 月度统计与缺失记录补查

首页与来源页展示最近六个月的柱状图，可选择期刊，或展开全部期刊明细。期刊公开登记量来自 Crossref 的 journal-article 月度查询（可能包括评论等类型，不等同于出版社完整发表量）；本站相关文献按 DOI 去重，可按发表月或首次收录月统计。缺失查询显示为未取得，当月注明未结束，本站历史空白不能解释为零发表。

每日抓取同时查询近期发表记录及增量更新，合并去重，保留原首次收录日期。Nature 系列缺少摘要时尝试公开出版社摘要，失败不突破登录或访问限制。校园网浏览器可用于人工补查及导读整理，正文不发布到本站。月度数量保存在 journal_records.json 并随 catalog.json 发布，当前与上月每日刷新，历史月份每 28 天复核。

## 机构层级与姓名核验

机构网络使用已核验的大学或科研组织作为节点，按论文去重计数；院系和实验室在详情下拉框中查看。`institution_registry.json` 保存 ROR 正式名称、别名、标识及关系依据，`institution_units.json` 保存官网核验的院系名称；未确认的地址碎片不展示。大学保持独立节点，联合单位不凭字符串臆测上级。`institution_chinese.json` 提供明确通行的中文机构名。

作者 ORCID 仅使用论文作者区及出版社元数据中的明确对应标识，并校验其格式与校验位。每日更新最多读取 60 个新增或到期 ORCID 的公开姓名；`author_names.json` 只保存确认的汉字署名、来源和检查时间，不保存联系方式或简历。人工核验姓名保存在 `author_name_overrides.json`，按完整署名及机构限定应用，禁止从拼音猜字。

各页底部提供管理员邮件反馈入口，点击打开用户自己的邮件客户端。


## 收录范围（2026-09-26 更新）

本站聚焦行星大气、行星大气化学与模式、系外行星探测与表征、行星轨道动力学、行星内部演化、行星冰冻圈与冰动力、行星表层系统及相关理论机制。大气物理、大气动力学、气候动力学、物理海洋、地球流体力学、表层过程与古气候、数学/物理/数值方法等广泛领域不再单独触发收录；只有明确行星语境或发表在 Nature、Science、PNAS 及其子刊时，才作为相关候选保留。公开目录同步移除不符合该边界的历史记录；底层来源档案保留，不向过去扩展抓取。

标签在同一筛选栏中展示。方向标签来自规则分类，机制标签由标题和摘要匹配现有词表；编辑可逐步扩充 `topics.json` 的机制标签。Exoplanet.eu 来源只增量检查今天及最近成功检查日以来的新建/更新书目，并按 DOI、arXiv 关系与已有记录归并。首次运行仅从前一北京时间自然日开始，不导入整站历史书目。Journal of Physical Oceanography、Ocean Modelling、Paleoceanography and Paleoclimatology、Journal of Geophysical Research: Oceans 已暂停抓取与月统计。

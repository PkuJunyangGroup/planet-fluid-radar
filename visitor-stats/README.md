# 网站访问统计接口

GitHub Pages 无法保存访问日志。此目录提供 Cloudflare Worker + D1 统计接口；网站页脚的计数器在接口启用后自动出现。

首次部署（须在 Cloudflare 免费账号中登录，勿把账号密码或 API 令牌写入仓库）：

1. 在本目录运行 `npx wrangler login`，按浏览器提示授权。
2. 运行 `npx wrangler d1 create planet-fluid-radar-visits`，记下返回的 `database_id`。
3. 复制 `wrangler.example.jsonc` 为 `wrangler.jsonc`，填入 `database_id`；该文件已加入 `.gitignore`。
4. 运行 `npx wrangler d1 execute planet-fluid-radar-visits --remote --file=./schema.sql`。
5. 运行 `npx wrangler deploy --config wrangler.jsonc`。
6. 将 Worker 输出的 HTTPS 地址写入仓库根目录 `stats-config.js`，例如 `https://planet-fluid-radar-visits.<账号子域>.workers.dev`，提交并等 GitHub Pages 部署。

数据口径：每次打开本站四个页面中的任意一页记为一次访问；同一北京时间自然日、同一 IP 记为一位独立访客。单 IP 每日最多计 100 次，减轻刷新造成的偏差。`visitors.html` 展示近 30 天各国家或地区的访问量与“访客日数”（每日独立 IP 数相加，跨日可能重复）；不展示个人精确位置。页面仅收到当前访问者自己的 IP 与地区，以及汇总访问量；其他人的 IP 仅在 D1 中短期保存。每日定时任务删除七天前的原始 IP 记录，聚合数量长期保留。Cloudflare 地理定位是近似值，VPN 或校园出口会影响显示。

只有来自 `https://pkujunyanggroup.github.io` 的浏览器请求会得到跨域授权。Worker 禁用持久化观测日志，代码中不写入控制台日志。此 Origin 检查无法阻止伪造请求；若实际出现恶意刷量，应在 Cloudflare 仪表板加限流。若统计接口不可达，网站照常可读，计数器隐藏。

本地验证：Node.js 24+ 运行 `npm test`；测试使用内存 SQLite，不接触真实访客数据。

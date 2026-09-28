# 网站访问统计接口

GitHub Pages 无法保存访问日志。此目录提供 Cloudflare Worker + D1 统计接口；网站页脚的计数器在接口启用后自动出现。

首次部署（须在 Cloudflare 免费账号中登录，勿把账号密码或 API 令牌写入仓库）：

1. 在本目录运行 `npx wrangler login`，按浏览器提示授权。
2. 运行 `npx wrangler d1 create planet-fluid-radar-visits`，记下返回的 `database_id`。
3. 复制 `wrangler.example.jsonc` 为 `wrangler.jsonc`，填入 `database_id`；该文件已加入 `.gitignore`。
4. 运行 `npx wrangler d1 execute planet-fluid-radar-visits --remote --file=./schema.sql`。
5. 运行 `npx wrangler deploy --config wrangler.jsonc`。
6. 将 Worker 输出的 HTTPS 地址写入仓库根目录 `stats-config.js`，例如 `https://planet-fluid-radar-visits.<账号子域>.workers.dev`，提交并等 GitHub Pages 部署。

若此前已经用国家级旧版本建立过 D1 数据库，不要重复执行第 4 步；先在本目录对旧数据库运行一次 `npx wrangler d1 execute planet-fluid-radar-visits --remote --file=./migrate-city.sql`，再部署新版 Worker。旧的国家汇总仍保留，城市数据只能从当时尚未清理的最近七天记录补齐，且旧记录没有可用于地图标点的经纬度。

数据口径：每次打开本站四个页面中的任意一页记为一次访问；同一北京时间自然日、同一 IP 记为一位独立访客。单 IP 每日最多计 100 次，减轻刷新造成的偏差。`visitors.html` 展示近 30 天的国家汇总和城市级近似标点，以及“访客日数”（每日独立 IP 数相加，跨日可能重复）；中国大陆及台湾、香港、澳门地区计入同一中国总量，城市仍分别展示。城市标点来自 Cloudflare 的 IP 地理定位，不展示个人精确位置。页面仅收到当前访问者自己的 IP 与地区，以及不含其他人 IP 的国家、城市汇总；其他人的 IP 仅在 D1 中短期保存。每日定时任务删除七天前的原始 IP 记录，聚合数量长期保留。Cloudflare 地理定位是近似值，VPN 或校园出口会影响显示。

只有来自 `https://pkujunyanggroup.github.io` 的浏览器请求会得到跨域授权。Worker 禁用持久化观测日志，代码中不写入控制台日志。此 Origin 检查无法阻止伪造请求；若实际出现恶意刷量，应在 Cloudflare 仪表板加限流。若统计接口不可达，网站照常可读，计数器隐藏。

本地验证：Node.js 24+ 运行 `npm test`；测试使用内存 SQLite，不接触真实访客数据。

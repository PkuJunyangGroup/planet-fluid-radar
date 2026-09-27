const SITE_ORIGIN = 'https://pkujunyanggroup.github.io';
const MAX_VIEWS_PER_IP_DAY = 100;

function beijingDay(date) {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(date);
}

function json(body, status = 200, origin = null) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
  };
  if (origin === SITE_ORIGIN) {
    headers['Access-Control-Allow-Origin'] = SITE_ORIGIN;
    headers.Vary = 'Origin';
  }
  return new Response(JSON.stringify(body), { status, headers });
}

function locationPart(value, maxLength = 70) {
  return typeof value === 'string' ? value.replace(/[<>\r\n\t]/g, '').slice(0, maxLength) : '';
}

function validIp(ip) {
  return typeof ip === 'string' && ip.length <= 45 && /^[0-9a-fA-F:.]+$/.test(ip);
}

async function summary(db, day) {
  const [today, total, countries] = await Promise.all([
    db.prepare('SELECT views, visitors FROM daily_totals WHERE day = ?').bind(day).first(),
    db.prepare('SELECT COALESCE(SUM(views), 0) AS views FROM daily_totals').first(),
    db.prepare('SELECT country, SUM(views) AS views, SUM(visitors) AS visitor_days FROM daily_countries WHERE day >= ? GROUP BY country ORDER BY views DESC, country')
      .bind(beijingDay(new Date(Date.now() - 29 * 86400000))).all(),
  ]);
  return {
    day,
    today_views: Number(today?.views || 0),
    today_visitors: Number(today?.visitors || 0),
    total_views: Number(total?.views || 0),
    country_totals: (countries.results || []).map(row => ({
      country: row.country, views: Number(row.views), visitor_days: Number(row.visitor_days),
    })),
    recent_countries: (countries.results || []).slice(0, 5).map(row => ({ country: row.country, views: Number(row.views) })),
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');
    if (origin !== SITE_ORIGIN) return json({ error: 'Forbidden origin' }, 403);
    const path = new URL(request.url).pathname;
    if (request.method === 'OPTIONS' && path === '/visit') {
      return new Response(null, { status: 204, headers: {
        'Access-Control-Allow-Origin': SITE_ORIGIN,
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Max-Age': '86400',
        Vary: 'Origin',
      } });
    }
    if (path !== '/visit' || request.method !== 'POST') return json({ error: 'Not found' }, 404, origin);
    if (!env.DB) return json({ error: 'Statistics unavailable' }, 503, origin);
    const ip = request.headers.get('CF-Connecting-IP');
    if (!validIp(ip)) return json({ error: 'Visitor address unavailable' }, 503, origin);

    const day = beijingDay(new Date());
    const country = /^[A-Z]{2}$/.test(request.cf?.country || '') ? request.cf.country : 'XX';
    const region = locationPart(request.cf?.region);
    const city = locationPart(request.cf?.city);
    try {
      await env.DB.prepare(`INSERT INTO visits (day, ip, country, region, city, views, last_seen)
        VALUES (?, ?, ?, ?, ?, 1, ?)
        ON CONFLICT(day, ip) DO UPDATE SET views = visits.views + 1, last_seen = excluded.last_seen
        WHERE visits.views < ?`)
        .bind(day, ip, country, region, city, new Date().toISOString(), MAX_VIEWS_PER_IP_DAY).run();
      const stats = await summary(env.DB, day);
      return json({ ...stats, you: { ip, country, region, city } }, 200, origin);
    } catch (_) {
      return json({ error: 'Statistics unavailable' }, 503, origin);
    }
  },

  async scheduled(_event, env) {
    // Keep today plus six previous Beijing calendar days.
    const cutoff = beijingDay(new Date(Date.now() - 6 * 86400000));
    await env.DB.prepare('DELETE FROM visits WHERE day < ?').bind(cutoff).run();
  },
};

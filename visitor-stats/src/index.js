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
  return typeof value === 'string' ? value.replace(/[<>\r\n\t]/g, '').trim().slice(0, maxLength) : '';
}

function coordinate(value, limit) {
  if ((typeof value !== 'string' && typeof value !== 'number') || String(value).trim() === '') return null;
  const number = Number(value);
  return Number.isFinite(number) && Math.abs(number) <= limit ? Math.round(number * 10) / 10 : null;
}

function validIp(ip) {
  return typeof ip === 'string' && ip.length <= 45 && /^[0-9a-fA-F:.]+$/.test(ip);
}

const validReader = value => typeof value === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
const validPaper = value => typeof value === 'string' && value.length <= 200 && /^(?:\d{4}\.\d{4,5}|(?:doi:)?10\.\d{4,9}\/[^\s<>"']+|exoplanet-bib:\d+)$/i.test(value);

async function recommendations(request, db, origin) {
  if (!db) return json({ error: 'Recommendations unavailable' }, 503, origin);
  try {
    const url = new URL(request.url);
    let reader = url.searchParams.get('reader');
    let change;
    if (request.method === 'POST') {
      if (!request.headers.get('Content-Type')?.startsWith('application/json')) return json({ error: 'Expected JSON' }, 415, origin);
      const raw = await request.text();
      if (raw.length > 1024) return json({ error: 'Request too large' }, 413, origin);
      try { change = JSON.parse(raw); } catch (_) { return json({ error: 'Invalid JSON' }, 400, origin); }
      reader = change?.reader_id;
      if (!validPaper(change?.paper_id) || typeof change?.recommended !== 'boolean') return json({ error: 'Invalid recommendation' }, 400, origin);
    }
    if (reader !== null && !validReader(reader)) return json({ error: 'Invalid reader' }, 400, origin);
    if (request.method === 'POST' && !validReader(reader)) return json({ error: 'Invalid reader' }, 400, origin);
    await db.prepare(`CREATE TABLE IF NOT EXISTS paper_recommendations (
      paper_id TEXT NOT NULL, reader_id TEXT NOT NULL, created_at TEXT NOT NULL,
      PRIMARY KEY (paper_id, reader_id)
    )`).run();
    if (change) {
      if (change.recommended) {
        await db.prepare('INSERT OR IGNORE INTO paper_recommendations (paper_id, reader_id, created_at) VALUES (?, ?, ?)')
          .bind(change.paper_id, reader, new Date().toISOString()).run();
      } else {
        await db.prepare('DELETE FROM paper_recommendations WHERE paper_id = ? AND reader_id = ?').bind(change.paper_id, reader).run();
      }
    }
    const totals = await db.prepare('SELECT paper_id, COUNT(*) AS count FROM paper_recommendations GROUP BY paper_id').all();
    const own = reader ? await db.prepare('SELECT paper_id FROM paper_recommendations WHERE reader_id = ?').bind(reader).all() : { results: [] };
    return json({ counts: Object.fromEntries(totals.results.map(row => [row.paper_id, Number(row.count)])), mine: own.results.map(row => row.paper_id) }, 200, origin);
  } catch (_) {
    return json({ error: 'Recommendations unavailable' }, 503, origin);
  }
}

async function summary(db, day) {
  const since = beijingDay(new Date(Date.now() - 29 * 86400000));
  const countryGroup = "CASE WHEN country IN ('TW', 'HK', 'MO') THEN 'CN' ELSE country END";
  const regionGroup = "CASE country WHEN 'TW' THEN '台湾地区' WHEN 'HK' THEN '香港特别行政区' WHEN 'MO' THEN '澳门特别行政区' ELSE region END";
  const [today, total, countries, cities] = await Promise.all([
    db.prepare('SELECT views, visitors FROM daily_totals WHERE day = ?').bind(day).first(),
    db.prepare('SELECT COALESCE(SUM(views), 0) AS views FROM daily_totals').first(),
    db.prepare(`SELECT ${countryGroup} AS country, SUM(views) AS views, SUM(visitors) AS visitor_days FROM daily_countries WHERE day >= ? GROUP BY ${countryGroup} ORDER BY views DESC, country`)
      .bind(since).all(),
    db.prepare(`SELECT ${countryGroup} AS country, ${regionGroup} AS region, city, MAX(latitude) AS latitude, MAX(longitude) AS longitude, SUM(views) AS views, SUM(visitors) AS visitor_days FROM daily_cities WHERE day >= ? GROUP BY ${countryGroup}, ${regionGroup}, city ORDER BY views DESC, country, region, city`)
      .bind(since).all(),
  ]);
  return {
    day,
    today_views: Number(today?.views || 0),
    today_visitors: Number(today?.visitors || 0),
    total_views: Number(total?.views || 0),
    country_totals: (countries.results || []).map(row => ({
      country: row.country, views: Number(row.views), visitor_days: Number(row.visitor_days),
    })),
    city_totals: (cities.results || []).map(row => ({
      country: row.country, region: row.region, city: row.city,
      latitude: row.latitude, longitude: row.longitude,
      views: Number(row.views), visitor_days: Number(row.visitor_days),
    })),
    recent_countries: (countries.results || []).slice(0, 5).map(row => ({ country: row.country, views: Number(row.views) })),
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');
    if (origin !== SITE_ORIGIN) return json({ error: 'Forbidden origin' }, 403);
    const path = new URL(request.url).pathname;
    if (request.method === 'OPTIONS' && ['/visit', '/recommendations'].includes(path)) {
      return new Response(null, { status: 204, headers: {
        'Access-Control-Allow-Origin': SITE_ORIGIN,
        'Access-Control-Allow-Methods': path === '/visit' ? 'POST, OPTIONS' : 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '86400',
        Vary: 'Origin',
      } });
    }
    if (path === '/recommendations' && ['GET', 'POST'].includes(request.method)) return recommendations(request, env.DB, origin);
    if (path !== '/visit' || request.method !== 'POST') return json({ error: 'Not found' }, 404, origin);
    if (!env.DB) return json({ error: 'Statistics unavailable' }, 503, origin);
    const ip = request.headers.get('CF-Connecting-IP');
    if (!validIp(ip)) return json({ error: 'Visitor address unavailable' }, 503, origin);

    const day = beijingDay(new Date());
    const rawCountry = /^[A-Z]{2}$/.test(request.cf?.country || '') ? request.cf.country : 'XX';
    const chinaRegion = { TW: '台湾地区', HK: '香港特别行政区', MO: '澳门特别行政区' }[rawCountry];
    const country = chinaRegion ? 'CN' : rawCountry;
    const region = chinaRegion || locationPart(request.cf?.region);
    const city = locationPart(request.cf?.city) || ({ HK: '香港', MO: '澳门' }[rawCountry] || '');
    const latitude = coordinate(request.cf?.latitude, 90);
    const longitude = coordinate(request.cf?.longitude, 180);
    try {
      await env.DB.prepare(`INSERT INTO visits (day, ip, country, region, city, latitude, longitude, views, last_seen)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
        ON CONFLICT(day, ip) DO UPDATE SET views = visits.views + 1, last_seen = excluded.last_seen
        WHERE visits.views < ?`)
        .bind(day, ip, country, region, city, latitude, longitude, new Date().toISOString(), MAX_VIEWS_PER_IP_DAY).run();
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

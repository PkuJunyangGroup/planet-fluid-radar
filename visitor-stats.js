(() => {
  const box = document.querySelector('[data-visitor-stats]');
  const endpoint = String(window.PLANET_FLUID_STATS_ENDPOINT || '').replace(/\/+$/, '');
  if (!box || !/^https:\/\/[a-z0-9.-]+(?:\:[0-9]+)?$/i.test(endpoint)) return;

  const countryName = code => {
    if (!/^[A-Z]{2}$/.test(code || '') || code === 'XX') return 'Unknown region';
    try { return new Intl.DisplayNames(['en'], { type: 'region' }).of(code) || code; }
    catch (_) { return code; }
  };
  const normalizedCountry = code => ['TW', 'HK', 'MO'].includes(code) ? 'CN' : code;
  const chinaCity = {};
  const number = value => Number.isSafeInteger(Number(value)) && Number(value) >= 0
    ? Number(value).toLocaleString('en') : '—';

  const request = fetch(`${endpoint}/visit`, { method: 'POST', mode: 'cors', cache: 'no-store', credentials: 'omit' })
    .then(response => { if (!response.ok) throw Error('Statistics unavailable'); return response.json(); });
  window.PLANET_FLUID_STATS_PROMISE = request;
  request.then(data => {
      const summary = document.createElement('summary');
      summary.textContent = `Views · today ${number(data.today_views)} · total ${number(data.total_views)}`;
      const detail = document.createElement('div');
      detail.className = 'visitor-stats-detail';
      const ownCountry = normalizedCountry(data.you?.country);
      const ownCity = ownCountry === 'CN' ? (chinaCity[data.you?.city] || data.you?.city) : data.you?.city;
      const place = [countryName(ownCountry), ownCountry === 'CN' ? '' : data.you?.region, ownCity]
        .filter(Boolean).filter((value, index, values) => values.indexOf(value) === index).join(' · ');
      const own = document.createElement('p');
      own.textContent = `Your IP: ${data.you?.ip || 'Unavailable'} · ${place}`;
      const unique = document.createElement('p');
      unique.textContent = `Visitors today: ${number(data.today_visitors)} (estimated by IP)`;
      const recent = document.createElement('p');
      recent.textContent = `Locations in the last 30 days: ${(data.recent_countries || []).map(item => `${countryName(normalizedCountry(item.country))} ${number(item.views)}`).join(' · ') || 'No data'}`;
      const policy = document.createElement('a');
      policy.href = 'sources.html#visitor-privacy';
      policy.textContent = 'Statistics & privacy';
      const map = document.createElement('a');
      map.href = 'visitors.html';
      map.textContent = 'Visitor map';
      detail.append(own, unique, recent, map, document.createTextNode(' · '), policy);
      box.replaceChildren(summary, detail);
      box.hidden = false;
    })
    .catch(() => { box.hidden = true; });
})();

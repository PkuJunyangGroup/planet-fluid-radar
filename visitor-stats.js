(() => {
  const box = document.querySelector('[data-visitor-stats]');
  const endpoint = String(window.PLANET_FLUID_STATS_ENDPOINT || '').replace(/\/+$/, '');
  if (!box || !/^https:\/\/[a-z0-9.-]+(?:\:[0-9]+)?$/i.test(endpoint)) return;

  const countryName = code => {
    if (!/^[A-Z]{2}$/.test(code || '') || code === 'XX') return '未知地区';
    try { return new Intl.DisplayNames(['zh-CN'], { type: 'region' }).of(code) || code; }
    catch (_) { return code; }
  };
  const normalizedCountry = code => ['TW', 'HK', 'MO'].includes(code) ? 'CN' : code;
  const chinaCity = { Taipei: '台北', 'Hong Kong': '香港', Macau: '澳门', Macao: '澳门' };
  const number = value => Number.isSafeInteger(Number(value)) && Number(value) >= 0
    ? Number(value).toLocaleString('zh-CN') : '—';

  const request = fetch(`${endpoint}/visit`, { method: 'POST', mode: 'cors', cache: 'no-store', credentials: 'omit' })
    .then(response => { if (!response.ok) throw Error('Statistics unavailable'); return response.json(); });
  window.PLANET_FLUID_STATS_PROMISE = request;
  request.then(data => {
      const summary = document.createElement('summary');
      summary.textContent = `访问统计 · 今日 ${number(data.today_views)} · 累计 ${number(data.total_views)}`;
      const detail = document.createElement('div');
      detail.className = 'visitor-stats-detail';
      const ownCountry = normalizedCountry(data.you?.country);
      const ownCity = ownCountry === 'CN' ? (chinaCity[data.you?.city] || data.you?.city) : data.you?.city;
      const place = [countryName(ownCountry), ownCountry === 'CN' ? '' : data.you?.region, ownCity]
        .filter(Boolean).filter((value, index, values) => values.indexOf(value) === index).join(' · ');
      const own = document.createElement('p');
      own.textContent = `您的 IP：${data.you?.ip || '未获取'} · ${place}`;
      const unique = document.createElement('p');
      unique.textContent = `今日独立访客 ${number(data.today_visitors)} 位（按 IP 估算）`;
      const recent = document.createElement('p');
      recent.textContent = `近 30 天地区：${(data.recent_countries || []).map(item => `${countryName(normalizedCountry(item.country))} ${number(item.views)}`).join(' · ') || '暂无数据'}`;
      const policy = document.createElement('a');
      policy.href = 'sources.html#visitor-privacy';
      policy.textContent = '统计方式与隐私说明';
      const map = document.createElement('a');
      map.href = 'visitors.html';
      map.textContent = '查看访客地图';
      detail.append(own, unique, recent, map, document.createTextNode(' · '), policy);
      box.replaceChildren(summary, detail);
      box.hidden = false;
    })
    .catch(() => { box.hidden = true; });
})();

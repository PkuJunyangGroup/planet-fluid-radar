(() => {
  const svg = document.querySelector('#visitor-map');
  const list = document.querySelector('#visitor-country-list');
  const status = document.querySelector('#map-status');
  const focus = document.querySelector('#map-focus');
  if (!svg || !list || !status || !focus) return;

  const ns = 'http://www.w3.org/2000/svg';
  const count = value => Number(value || 0).toLocaleString('zh-CN');
  const countryName = code => {
    if (code === 'XX') return '未知地区';
    try { return new Intl.DisplayNames(['zh-CN'], { type: 'region' }).of(code) || code; }
    catch (_) { return code; }
  };
  const setText = (selector, value) => { document.querySelector(selector).textContent = value; };

  Promise.all([
    fetch('world-map.json').then(response => { if (!response.ok) throw Error('Map unavailable'); return response.json(); }),
    window.PLANET_FLUID_STATS_PROMISE?.catch(() => null) || Promise.resolve(null),
  ]).then(([shapes, data]) => {
    const rows = Array.isArray(data?.country_totals) ? data.country_totals : [];
    const byCountry = new Map(rows.map(row => [row.country, row]));
    const max = Math.max(1, ...rows.map(row => Number(row.views) || 0));
    for (const shape of shapes) {
      const row = byCountry.get(shape.code);
      const views = Number(row?.views || 0);
      const level = views ? Math.max(1, Math.ceil(4 * Math.log1p(views) / Math.log1p(max))) : 0;
      const path = document.createElementNS(ns, 'path');
      path.setAttribute('d', shape.path);
      path.setAttribute('class', `map-country map-level-${level}`);
      path.setAttribute('tabindex', '0');
      const label = `${countryName(shape.code)}：${count(views)} 次访问${row ? `，${count(row.visitor_days)} 个访客日` : ''}`;
      path.setAttribute('aria-label', label);
      const title = document.createElementNS(ns, 'title');
      title.textContent = label;
      path.append(title);
      path.addEventListener('mouseenter', () => { focus.textContent = label; });
      path.addEventListener('focus', () => { focus.textContent = label; });
      svg.append(path);
    }
    if (!data) {
      status.textContent = '访问统计尚未启用；地图将在统计接口部署后自动显示数据。';
      focus.textContent = '目前没有可展示的访问数据。';
      return;
    }
    setText('#map-total', `近 30 天访问 · ${count(rows.reduce((sum, row) => sum + Number(row.views || 0), 0))}`);
    setText('#map-countries', `访问地区 · ${count(rows.filter(row => row.country !== 'XX').length)}`);
    setText('#map-day', `截至 · ${data.day || '—'}（北京时间）`);
    status.textContent = rows.length ? '按近 30 天访问量排序' : '近 30 天暂无访问记录。';
    for (const row of rows) {
      const item = document.createElement('li');
      const name = document.createElement('span');
      name.textContent = countryName(row.country);
      const amount = document.createElement('strong');
      amount.textContent = `${count(row.views)} 次`;
      const days = document.createElement('small');
      days.textContent = `${count(row.visitor_days)} 个访客日`;
      item.append(name, amount, days);
      list.append(item);
    }
  }).catch(() => {
    status.textContent = '地图或统计接口暂时不可用，请稍后再试。';
    focus.textContent = '无法读取地图数据。';
  });
})();

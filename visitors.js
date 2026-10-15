(() => {
  const svg = document.querySelector('#visitor-map');
  const list = document.querySelector('#visitor-country-list');
  const cityList = document.querySelector('#visitor-city-list');
  const status = document.querySelector('#map-status');
  const focus = document.querySelector('#map-focus');
  const reset = document.querySelector('#map-reset');
  if (!svg || !list || !cityList || !status || !focus || !reset) return;

  const ns = 'http://www.w3.org/2000/svg';
  const worldView = svg.getAttribute('viewBox');
  const count = value => Number(value || 0).toLocaleString('en');
  const chinaCity = {};
  const normalizedCountry = code => ['TW', 'HK', 'MO'].includes(code) ? 'CN' : code;
  const countryName = code => {
    if (code === 'XX') return 'Unknown region';
    try { return new Intl.DisplayNames(['en'], { type: 'region' }).of(code) || code; }
    catch (_) { return code; }
  };
  const setText = (selector, value) => { document.querySelector(selector).textContent = value; };
  const cityLabel = row => {
    const code = normalizedCountry(row.country);
    const city = code === 'CN' ? (chinaCity[row.city] || row.city) : row.city;
    return [...new Set([countryName(code), code === 'CN' ? '' : row.region, city].filter(Boolean))].join(' · ');
  };

  Promise.all([
    fetch('world-map.json').then(response => { if (!response.ok) throw Error('Map unavailable'); return response.json(); }),
    window.PLANET_FLUID_STATS_PROMISE?.catch(() => null) || Promise.resolve(null),
  ]).then(([shapes, data]) => {
    const originalRows = Array.isArray(data?.country_totals) ? data.country_totals : [];
    const byCountry = new Map();
    for (const row of originalRows) {
      const code = normalizedCountry(row.country);
      const prior = byCountry.get(code) || { country: code, views: 0, visitor_days: 0 };
      prior.views += Number(row.views || 0);
      prior.visitor_days += Number(row.visitor_days || 0);
      byCountry.set(code, prior);
    }
    const rows = [...byCountry.values()].sort((a, b) => b.views - a.views || a.country.localeCompare(b.country));
    const cities = Array.isArray(data?.city_totals) ? data.city_totals : [];
    const max = Math.max(1, ...rows.map(row => Number(row.views) || 0));
    const countryPaths = new Map();
    let selectedCountry = null;
    let hoveredCountry = null;
    const highlightCountry = () => {
      const active = hoveredCountry || selectedCountry;
      for (const [code, paths] of countryPaths) {
        for (const path of paths) path.classList.toggle('map-active', code === active);
      }
    };
    const showChina = () => {
      const paths = countryPaths.get('CN') || [];
      if (!paths.length) return;
      const boxes = paths.map(path => path.getBBox());
      const left = Math.min(...boxes.map(box => box.x));
      const right = Math.max(...boxes.map(box => box.x + box.width));
      const top = Math.min(...boxes.map(box => box.y));
      const bottom = Math.max(...boxes.map(box => box.y + box.height));
      const width = Math.max(right - left + 36, (bottom - top + 28) * 2);
      const height = width / 2;
      svg.setAttribute('viewBox', `${(left + right - width) / 2} ${(top + bottom - height) / 2} ${width} ${height}`);
      reset.hidden = false;
    };
    const selectCountry = (code, label) => {
      selectedCountry = code;
      hoveredCountry = null;
      highlightCountry();
      focus.textContent = label;
      if (code === 'CN') showChina();
      else { svg.setAttribute('viewBox', worldView); reset.hidden = true; }
    };
    reset.addEventListener('click', () => {
      selectedCountry = null;
      hoveredCountry = null;
      highlightCountry();
      svg.setAttribute('viewBox', worldView);
      reset.hidden = true;
      focus.textContent = 'Click the map to explore visits.';
    });
    for (const shape of shapes) {
      const aggregateCode = normalizedCountry(shape.code);
      const row = byCountry.get(aggregateCode);
      const views = Number(row?.views || 0);
      const level = views ? Math.max(1, Math.ceil(4 * Math.log1p(views) / Math.log1p(max))) : 0;
      const path = document.createElementNS(ns, 'path');
      path.setAttribute('d', shape.path);
      path.setAttribute('class', `map-country map-level-${level}`);
      path.dataset.country = aggregateCode;
      path.dataset.region = shape.code;
      path.setAttribute('tabindex', '0');
      const label = `${countryName(aggregateCode)}: ${count(views)} views${row ? `, ${count(row.visitor_days)} visitor-days` : ''}`;
      path.setAttribute('aria-label', label);
      const title = document.createElementNS(ns, 'title');
      title.textContent = label;
      path.append(title);
      const paths = countryPaths.get(aggregateCode) || [];
      paths.push(path);
      countryPaths.set(aggregateCode, paths);
      path.addEventListener('mouseenter', () => { hoveredCountry = aggregateCode; highlightCountry(); focus.textContent = label; });
      path.addEventListener('mouseleave', () => { hoveredCountry = null; highlightCountry(); });
      path.addEventListener('focus', () => { hoveredCountry = aggregateCode; highlightCountry(); focus.textContent = label; });
      path.addEventListener('blur', () => { hoveredCountry = null; highlightCountry(); });
      path.addEventListener('click', () => { selectCountry(aggregateCode, label); });
      path.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); selectCountry(aggregateCode, label); }
      });
      svg.append(path);
    }
    for (const row of cities) {
      const latitude = Number(row.latitude);
      const longitude = Number(row.longitude);
      if (row.latitude == null || row.longitude == null || !Number.isFinite(latitude) || !Number.isFinite(longitude)
        || Math.abs(latitude) > 90 || Math.abs(longitude) > 180) continue;
      const views = Number(row.views || 0);
      const label = `${cityLabel(row)}: ${count(views)} views, ${count(row.visitor_days)} visitor-days`;
      const marker = document.createElementNS(ns, 'circle');
      marker.setAttribute('cx', String((longitude + 180) * 2.5));
      marker.setAttribute('cy', String((90 - latitude) * 2.5));
      marker.setAttribute('r', String(Math.min(7, 3.5 + Math.log1p(views))));
      marker.setAttribute('class', 'map-city');
      marker.setAttribute('tabindex', '0');
      marker.setAttribute('aria-label', label);
      const title = document.createElementNS(ns, 'title');
      title.textContent = label;
      marker.append(title);
      marker.addEventListener('mouseenter', () => { focus.textContent = label; });
      marker.addEventListener('focus', () => { focus.textContent = label; });
      marker.addEventListener('click', () => { selectCountry(normalizedCountry(row.country), label); });
      marker.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); selectCountry(normalizedCountry(row.country), label); }
      });
      svg.append(marker);
    }
    if (!data) {
      status.textContent = 'Visitor statistics are temporarily unavailable.';
      focus.textContent = 'No visitor data is currently available.';
      return;
    }
    setText('#map-total', `Views in the last 30 days · ${count(rows.reduce((sum, row) => sum + Number(row.views || 0), 0))}`);
    setText('#map-countries', `Countries · ${count(rows.filter(row => row.country !== 'XX').length)}`);
    setText('#map-cities', `Cities · ${count(cities.length)}`);
    setText('#map-day', `Through · ${data.day || '—'} (Beijing time)`);
    status.textContent = rows.length ? 'Sorted by views in the last 30 days' : 'No visits recorded in the last 30 days.';
    for (const row of rows) {
      const item = document.createElement('li');
      const name = document.createElement('span');
      name.textContent = countryName(row.country);
      const amount = document.createElement('strong');
      amount.textContent = `${count(row.views)} views`;
      const days = document.createElement('small');
      days.textContent = `${count(row.visitor_days)} visitor-days`;
      item.append(name, amount, days);
      list.append(item);
    }
    for (const row of cities) {
      const item = document.createElement('li');
      const name = document.createElement('span');
      name.textContent = cityLabel(row);
      const amount = document.createElement('strong');
      amount.textContent = `${count(row.views)} views`;
      const days = document.createElement('small');
      days.textContent = `${count(row.visitor_days)} visitor-days`;
      item.append(name, amount, days);
      cityList.append(item);
    }
  }).catch(() => {
    status.textContent = 'Map or statistics are temporarily unavailable. Please try again later.';
    focus.textContent = 'Map data could not be loaded.';
  });
})();

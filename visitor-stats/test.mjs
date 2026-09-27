import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from './src/index.js';

function database() {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(readFileSync(new URL('./schema.sql', import.meta.url), 'utf8'));
  const db = {
    prepare(sql) {
      return {
        bind(...args) {
          return {
            run: async () => sqlite.prepare(sql).run(...args),
            first: async () => sqlite.prepare(sql).get(...args),
            all: async () => ({ results: sqlite.prepare(sql).all(...args) }),
          };
        },
        first: async () => sqlite.prepare(sql).get(),
      };
    },
  };
  return { sqlite, db };
}

function visit(ip, country = 'CN', origin = 'https://pkujunyanggroup.github.io') {
  const request = new Request('https://stats.example.workers.dev/visit', {
    method: 'POST', headers: { Origin: origin, 'CF-Connecting-IP': ip },
  });
  Object.defineProperty(request, 'cf', { value: { country, region: 'Beijing', city: 'Beijing' } });
  return request;
}

test('counts page views and distinct IPs; only returns the current visitor address', async () => {
  const { sqlite, db } = database();
  const env = { DB: db };
  await worker.fetch(visit('192.0.2.10'), env);
  await worker.fetch(visit('192.0.2.10'), env);
  const response = await worker.fetch(visit('2001:db8::1', 'US'), env);
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.today_views, 3);
  assert.equal(body.today_visitors, 2);
  assert.equal(body.total_views, 3);
  assert.equal(body.you.ip, '2001:db8::1');
  assert.equal(JSON.stringify(body).includes('192.0.2.10'), false);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS n FROM visits').get().n, 2);
});

test('rejects foreign origins and missing visitor addresses', async () => {
  const { sqlite, db } = database();
  assert.equal((await worker.fetch(visit('192.0.2.1', 'CN', 'https://other.example'), { DB: db })).status, 403);
  assert.equal((await worker.fetch(visit('not-an-ip'), { DB: db })).status, 503);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS n FROM visits').get().n, 0);
});

test('caps repeated hits and purges raw addresses while preserving aggregates', async () => {
  const { sqlite, db } = database();
  for (let i = 0; i < 102; i++) await worker.fetch(visit('192.0.2.20'), { DB: db });
  assert.equal(sqlite.prepare('SELECT SUM(views) AS n FROM daily_totals').get().n, 100);
  sqlite.prepare("INSERT INTO visits(day,ip,country,region,city,last_seen) VALUES ('2020-01-01','198.51.100.1','CN','','','2020-01-01T00:00:00Z')").run();
  await worker.scheduled({}, { DB: db });
  assert.equal(sqlite.prepare("SELECT COUNT(*) AS n FROM visits WHERE day='2020-01-01'").get().n, 0);
  assert.equal(sqlite.prepare("SELECT views FROM daily_totals WHERE day='2020-01-01'").get().views, 1);
});

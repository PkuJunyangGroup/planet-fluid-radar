-- Raw IPs are retained for seven Beijing calendar days. Aggregates have no IPs.
CREATE TABLE IF NOT EXISTS visits (
  day TEXT NOT NULL,
  ip TEXT NOT NULL,
  country TEXT NOT NULL,
  region TEXT NOT NULL DEFAULT '',
  city TEXT NOT NULL DEFAULT '',
  views INTEGER NOT NULL DEFAULT 1 CHECK (views BETWEEN 1 AND 100),
  last_seen TEXT NOT NULL,
  PRIMARY KEY (day, ip)
);

CREATE TABLE IF NOT EXISTS daily_totals (
  day TEXT PRIMARY KEY,
  views INTEGER NOT NULL DEFAULT 0,
  visitors INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS daily_countries (
  day TEXT NOT NULL,
  country TEXT NOT NULL,
  views INTEGER NOT NULL DEFAULT 0,
  visitors INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, country)
);

CREATE TRIGGER IF NOT EXISTS visit_added AFTER INSERT ON visits BEGIN
  INSERT INTO daily_totals (day, views, visitors) VALUES (NEW.day, 1, 1)
    ON CONFLICT(day) DO UPDATE SET views = views + 1, visitors = visitors + 1;
  INSERT INTO daily_countries (day, country, views, visitors)
    VALUES (NEW.day, NEW.country, 1, 1)
    ON CONFLICT(day, country) DO UPDATE SET views = views + 1, visitors = visitors + 1;
END;

CREATE TRIGGER IF NOT EXISTS visit_repeated AFTER UPDATE OF views ON visits BEGIN
  UPDATE daily_totals SET views = views + 1 WHERE day = NEW.day;
  UPDATE daily_countries SET views = views + 1
    WHERE day = NEW.day AND country = NEW.country;
END;

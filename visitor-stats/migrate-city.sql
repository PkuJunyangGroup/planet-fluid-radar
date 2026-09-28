-- Run once on a D1 database created with the original country-only schema.
ALTER TABLE visits ADD COLUMN latitude REAL;
ALTER TABLE visits ADD COLUMN longitude REAL;

CREATE TABLE IF NOT EXISTS daily_cities (
  day TEXT NOT NULL,
  country TEXT NOT NULL,
  region TEXT NOT NULL,
  city TEXT NOT NULL,
  latitude REAL,
  longitude REAL,
  views INTEGER NOT NULL DEFAULT 0,
  visitors INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, country, region, city)
);

-- Recent raw rows can be grouped by city; older country totals cannot be reconstructed.
INSERT INTO daily_cities (day, country, region, city, views, visitors)
  SELECT day, country, region, city, SUM(views), COUNT(*)
  FROM visits WHERE city <> '' GROUP BY day, country, region, city;

DROP TRIGGER IF EXISTS visit_added;
DROP TRIGGER IF EXISTS visit_repeated;

CREATE TRIGGER visit_added AFTER INSERT ON visits BEGIN
  INSERT INTO daily_totals (day, views, visitors) VALUES (NEW.day, 1, 1)
    ON CONFLICT(day) DO UPDATE SET views = views + 1, visitors = visitors + 1;
  INSERT INTO daily_countries (day, country, views, visitors)
    VALUES (NEW.day, NEW.country, 1, 1)
    ON CONFLICT(day, country) DO UPDATE SET views = views + 1, visitors = visitors + 1;
  INSERT INTO daily_cities (day, country, region, city, latitude, longitude, views, visitors)
    SELECT NEW.day, NEW.country, NEW.region, NEW.city, NEW.latitude, NEW.longitude, 1, 1
    WHERE NEW.city <> ''
    ON CONFLICT(day, country, region, city) DO UPDATE SET
      views = views + 1,
      visitors = visitors + 1,
      latitude = COALESCE(daily_cities.latitude, excluded.latitude),
      longitude = COALESCE(daily_cities.longitude, excluded.longitude);
END;

CREATE TRIGGER visit_repeated AFTER UPDATE OF views ON visits BEGIN
  UPDATE daily_totals SET views = views + 1 WHERE day = NEW.day;
  UPDATE daily_countries SET views = views + 1
    WHERE day = NEW.day AND country = NEW.country;
  UPDATE daily_cities SET views = views + 1
    WHERE day = NEW.day AND country = NEW.country AND region = NEW.region AND city = NEW.city AND NEW.city <> '';
END;

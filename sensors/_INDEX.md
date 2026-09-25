# Sensors — READ THIS FIRST (for the LLM and for humans)

This directory holds **one file per sensor**, each self-describing, plus a
living `SENSOR_REPORT.md` dashboard. Everything here is plain text — readable
by cron jobs, the LLM, and humans alike.

## Layout

- `<sensor_name>.md` — one file per sensor: metadata header + appended
  timestamped readings.
- `SENSOR_REPORT.md` — the **dashboard**: trends, anomalies, and notes,
  refreshed periodically (by a script today; by Level-1 agents or the kami
  itself later).

## Sensor file format

Lines starting with `# key: value` are metadata; the rest are readings:

```
# sensor: air_temp_humidity
# description: BME280 on I2C, north side of the pond
# location: park, turtle island
# units: temp=degC, humidity=%RH
# logger: loggers/bme280.py via cron, interval=60s
# queryable: yes — run `python3 loggers/bme280.py --once` for a fresh reading
2026-09-25 14:00  temp=27.4C  humidity=71%
```

## How data flows

1. A **logger process** (cron or daemon) samples the sensor and appends a
   line to its file. Loggers run independently of the LLM.
2. The kami reads the newest lines of every sensor file (via the reports
   digest) when answering — it always sees fresh data.
3. Loggers may also be **queried directly** for a single fresh reading
   (`--once`) or, later, asked for a one-line self-description if they are
   Level-1 agents (e.g. "air is warm and humid, rising since noon").
4. The kami (or a Level-1 analyst agent) periodically writes its reading of
   the sensors into `SENSOR_REPORT.md` — trends, anomalies, things worth
   telling visitors about.

# sensor: solarpower
# description: Solar panel output + battery state of the node. DUMMY DATA —
#   simulated day/night curve until the INA219 (I2C) is wired up.
# location: the node's solar panel
# units: panel_v=V, battery_pct=%, charging=0/1
# logger: loggers/sensor_solarpower.py via cron, interval=300s
# queryable: yes — run this file directly for a fresh reading
# updated: 2026-09-25 17:30:31

2026-09-25 17:30  panel_v=2.39V  battery=63.2%  charging=0

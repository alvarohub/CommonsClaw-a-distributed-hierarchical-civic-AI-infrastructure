# Report: pi_vitals
# description: The node's own health — CPU load, memory, chip temperature.
#   Stand-in for real environmental sensors until they are wired up.
# logger_config: interval=60s (cron), retains last ~60 samples
# location: the kami node itself (emotionpi)
# units: cpu=%%, ram=%%, temp=degC
# tweakable: interval (edit crontab), MAX_LINES (this file's length)
# updated: 2026-09-25 17:09:41

2026-09-25 17:09  cpu=0.0%  ram=80.4%  temp=--C

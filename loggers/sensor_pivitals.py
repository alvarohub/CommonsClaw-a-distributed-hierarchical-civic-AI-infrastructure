#!/usr/bin/env python3
"""Example Level-0 sensor logger for the kami node.

Runs from cron (e.g. every minute) and writes a short, human-readable
"report" into reports/ and sensors/. Each file has a metadata header that
the LLM reads — including logger config it may suggest tweaking (which
sensors, what rate, location metadata).

This one logs the Pi's own vitals (CPU/RAM/temp) as a stand-in for real
sensors. Real loggers (BME280 on I2C, LoRa/meshtastic weather stations, ...)
follow the same format: header + recent observations.

Layout it writes to:
    reports/sensor_pivitals_log.md   <- running log (this logger)
    sensors/sensor_pivitals.md       <- per-sensor file (same readings)
    reports/community_notes.md       <- notes left by people via the chat page
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # for config, hardware_monitor

import config
from hardware_monitor import HardwareMonitor

BASE = Path(__file__).parent.parent
REPORTS_DIR = BASE / "reports"
SENSORS_DIR = BASE / "sensors"
REPORT = REPORTS_DIR / "sensor_pivitals_log.md"
SENSOR_FILE = SENSORS_DIR / "sensor_pivitals.md"
MAX_LINES = 60  # keep the files short — the LLM reads them whole

HEADER = """# Report: sensor_pivitals
# description: The node's own health — CPU load, memory, chip temperature.
#   Stand-in for real environmental sensors until they are wired up.
# logger_config: interval=60s (cron), retains last ~60 samples
# location: the kami node itself (emotionpi)
# units: cpu=%%, ram=%%, temp=degC
# tweakable: interval (edit crontab), MAX_LINES (this file's length)
# updated: {updated}
"""


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    SENSORS_DIR.mkdir(exist_ok=True)
    snap = HardwareMonitor().read_snapshot()
    line = (
        f"{time.strftime('%Y-%m-%d %H:%M')}  "
        f"cpu={snap.cpu_percent if snap.cpu_percent is not None else '--'}%  "
        f"ram={snap.ram_percent if snap.ram_percent is not None else '--'}%  "
        f"temp={snap.temperature_c if snap.temperature_c is not None else '--'}C"
    )

    body = []
    if REPORT.exists():
        lines = REPORT.read_text().splitlines()
        # keep existing sample lines (those without the '# ' header prefix)
        body = [l for l in lines if l and not l.startswith("#")]

    body.append(line)
    body = body[-MAX_LINES:]

    REPORT.write_text(
        HEADER.format(updated=time.strftime("%Y-%m-%d %H:%M:%S"))
        + "\n"
        + "\n".join(body)
        + "\n"
    )

    # Mirror the reading into the per-sensor file (sensors/ layout).
    if SENSOR_FILE.exists():
        slines = SENSOR_FILE.read_text().splitlines()
        sbody = [l for l in slines if l and not l.startswith("#")]
        shead = [l for l in slines if l.startswith("#")]
        sbody = (sbody + [line])[-MAX_LINES:]
        SENSOR_FILE.write_text("\n".join(shead) + "\n" + "\n".join(sbody) + "\n")

    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()

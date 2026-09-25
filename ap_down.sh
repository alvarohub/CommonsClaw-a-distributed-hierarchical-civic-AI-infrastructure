#!/usr/bin/env bash
# Tear down the Wi-Fi access point (back to normal / dev mode).
# Run ON THE PI:   sudo bash ap_down.sh
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run with sudo:  sudo bash ap_down.sh" >&2
  exit 1
fi

if nmcli -t -f NAME con show | grep -qx "ssai-ap"; then
  nmcli con down ssai-ap || true
  echo "AP 'ssai-ap' brought down (profile kept; bring back with ap_up.sh)."
else
  echo "No ssai-ap profile; nothing to do."
fi

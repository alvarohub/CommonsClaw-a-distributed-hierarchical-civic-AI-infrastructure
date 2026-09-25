#!/usr/bin/env bash
# Install/uninstall unattended-boot behavior for the SSAI Pi:
#   - web server starts at boot (systemd, waits for Ollama)
#   - Wi-Fi AP profile already has autoconnect (created by ap_up.sh)
#   - Pi boots to console (no desktop) to save RAM
#
# Run ON THE PI:   sudo bash install_autostart.sh
# Undo:            sudo bash install_autostart.sh --uninstall
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run with sudo" >&2
  exit 1
fi

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${1:-}" == "--uninstall" ]]; then
  systemctl disable --now ssai-web.service 2>/dev/null || true
  rm -f /etc/systemd/system/ssai-web.service
  systemctl daemon-reload
  echo "ssai-web service removed. (AP profile 'ssai-ap' left in place;"
  echo " remove with: nmcli con delete ssai-ap)"
  exit 0
fi

# 1. web server service
cp "$SRC_DIR/ssai-web.service" /etc/systemd/system/ssai-web.service
systemctl daemon-reload
systemctl enable --now ssai-web.service

# 2. boot to console (no desktop) — saves ~250 MB RAM
systemctl set-default multi-user.target

# 3. make sure the AP profile autoconnects if it exists
if nmcli -t -f NAME con show | grep -qx "ssai-ap"; then
  nmcli con mod ssai-ap connection.autoconnect yes
  echo "AP profile 'ssai-ap' set to autoconnect."
else
  echo "NOTE: no ssai-ap profile yet — run 'sudo bash ap_up.sh' once first."
fi

echo
echo "=== autostart installed ==="
systemctl is-enabled ssai-web.service
echo "Default boot target: $(systemctl get-default)"
echo "Reboot to verify: sudo reboot"
echo "After reboot the chat should be at http://10.42.0.1:8080 (via AP)"
echo "or http://192.168.2.13:8080 (via Ethernet)."

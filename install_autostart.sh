#!/usr/bin/env bash
# Install/uninstall unattended-boot behavior for the CommonsClaw Pi:
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
  systemctl disable --now commonsclaw-web.service 2>/dev/null || true
  rm -f /etc/systemd/system/commonsclaw-web.service
  systemctl disable --now commonsclaw-voice.service 2>/dev/null || true
  rm -f /etc/systemd/system/commonsclaw-voice.service
  systemctl daemon-reload
  echo "commonsclaw-web service removed. (AP profile 'commonsclaw-ap' left in place;"
  echo " remove with: nmcli con delete commonsclaw-ap)"
  exit 0
fi

# 1. web server service
cp "$SRC_DIR/commonsclaw-web.service" /etc/systemd/system/commonsclaw-web.service
systemctl daemon-reload
systemctl enable --now commonsclaw-web.service

# 1b. sensor loggers service (registry-driven, sensors.json)
cp "$SRC_DIR/commonsclaw-sensors.service" /etc/systemd/system/commonsclaw-sensors.service
systemctl daemon-reload
systemctl enable --now commonsclaw-sensors.service

# 1b2. voice loop — idle until the web page turns the microphone on.
# Needs the voice venv (setup_voice.sh); skipped cleanly if it isn't there.
if [ -x /home/admin/voice-venv/bin/python ]; then
  cp "$SRC_DIR/commonsclaw-voice.service" /etc/systemd/system/commonsclaw-voice.service
  systemctl daemon-reload
  systemctl enable --now commonsclaw-voice.service
else
  echo "NOTE: no ~/voice-venv — skipping the voice service (run setup_voice.sh first)."
fi

# 1c. daily journal entry (23:55) — the mechanical memory writer
( crontab -l 2>/dev/null | grep -v journal_writer ; \
  echo '55 23 * * * /usr/bin/python3 /home/admin/commonsclaw/loggers/journal_writer.py' ) | crontab -

# 1d. keep the model resident: Ollama evicts it 5 min after the last question
# by default, which costs ~8 s of reload on the next visitor. A kami should
# answer instantly. (~1 GB RAM held permanently; undo by deleting this file.)
mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/keepalive.conf <<'EOF'
[Service]
Environment="OLLAMA_KEEP_ALIVE=-1"
EOF
systemctl daemon-reload
systemctl restart ollama

# 1e. let ./push_to_pi.sh restart the services without a password prompt.
# Scoped to exactly these commands — not a general sudo grant.
cat > /etc/sudoers.d/commonsclaw-restart <<'EOF'
admin ALL=(root) NOPASSWD: /usr/bin/systemctl restart commonsclaw-web, /usr/bin/systemctl restart commonsclaw-voice, /usr/bin/systemctl restart commonsclaw-sensors
EOF
chmod 0440 /etc/sudoers.d/commonsclaw-restart
visudo -c -q || { echo "BAD sudoers file — removing"; rm -f /etc/sudoers.d/commonsclaw-restart; }

# 2. boot to console (no desktop) — saves ~250 MB RAM
systemctl set-default multi-user.target

# 3. make sure the AP profile autoconnects if it exists
if nmcli -t -f NAME con show | grep -qx "commonsclaw-ap"; then
  nmcli con mod commonsclaw-ap connection.autoconnect yes
  echo "AP profile 'commonsclaw-ap' set to autoconnect."
else
  echo "NOTE: no commonsclaw-ap profile yet — run 'sudo bash ap_up.sh' once first."
fi

echo
echo "=== autostart installed ==="
systemctl is-enabled commonsclaw-web.service
systemctl is-enabled commonsclaw-sensors.service
echo "Default boot target: $(systemctl get-default)"
echo "Reboot to verify: sudo reboot"
echo "After reboot the chat should be at http://10.42.0.1:8080 (via AP)"
echo "or http://192.168.2.13:8080 (via Ethernet)."

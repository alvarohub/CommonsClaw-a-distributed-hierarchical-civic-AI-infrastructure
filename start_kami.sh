#!/usr/bin/env bash
# Start the CommonsClaw node processes: Ollama (if stopped), web, voice, sensors.
#   ./start_kami.sh
# Run ON THE PI.
set -euo pipefail

echo "Starting CommonsClaw…"
sudo systemctl start ollama
sudo systemctl start commonsclaw-web commonsclaw-voice commonsclaw-sensors
sleep 2
echo "Status:"
systemctl is-active commonsclaw-web commonsclaw-voice commonsclaw-sensors ollama || true
echo
echo "Note: if Ollama was fully stopped, the model reloads on the first question (~8 s)."

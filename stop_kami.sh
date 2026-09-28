#!/usr/bin/env bash
# Stop the CommonsClaw node processes.
# By default Ollama is left running (the model stays warm in RAM).
#   ./stop_kami.sh           stop web + voice + sensors
#   ./stop_kami.sh --all     also stop the Ollama LLM server
# Run ON THE PI.
set -euo pipefail

echo "Stopping CommonsClaw…"
sudo systemctl stop commonsclaw-web commonsclaw-voice commonsclaw-sensors

if [[ "${1:-}" == "--all" ]]; then
  echo "Stopping Ollama too…"
  sudo systemctl stop ollama
else
  echo "(Ollama left running — pass --all to stop it as well)"
fi
echo
echo "✔ stopped — restart with:  ./start_kami.sh"


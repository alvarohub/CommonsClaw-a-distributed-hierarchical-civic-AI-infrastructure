#!/usr/bin/env bash
# Push local ssai code to the Pi over SSH. Run from the Mac, anywhere:
#   ./push_to_pi.sh            (uses default host below)
#   PI_HOST=admin@192.168.2.13 ./push_to_pi.sh
set -euo pipefail

PI_HOST="${PI_HOST:-admin@192.168.2.13}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"
DEST="${PI_HOST}:~/ssai/"

echo "Pushing $SRC -> $DEST"
rsync -av --delete \
  --exclude '.git' \
  --exclude '__pycache__' \
  --exclude '.venv' \
  --exclude '*.pyc' \
  --exclude '.DS_Store' \
  "$SRC" "$DEST"
echo "Done."

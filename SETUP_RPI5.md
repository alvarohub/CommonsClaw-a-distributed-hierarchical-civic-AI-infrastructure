# SSAI — Replicating the System on a Raspberry Pi 5

Step-by-step instructions to get this repository running on a fresh
Raspberry Pi 5, including the language model (which is **not** in the repo).

End result: the Pi boots, Ollama serves `phi3.5:latest` locally, and you can
chat with it. No display is required: `main.py` detects the missing screen
and runs a console chat you can use directly over SSH (or run
`python3 console.py` explicitly). If you attach a monitor + keyboard, the
fullscreen Tkinter GUI starts instead. `control.py` works over SSH in both
cases.

---

## 0. What you need

- Raspberry Pi 5, **8 GB RAM strongly recommended** (4 GB works only with a
  smaller model — see section 5).
- Official 27 W (5 V / 5 A) USB-C power supply. Undervoltage = crashes.
- microSD card, 32 GB minimum (the model needs ~2.5 GB).
- Active cooler or heatsink — sustained LLM load will throttle an uncooled
  Pi 5 (85 °C limit). The app shows live temperature, so you will see it.
- A laptop for SSH. No display is needed: without one the app runs a console
  chat in the SSH terminal. (Optional: attach any HDMI monitor + keyboard to
  get the fullscreen Tkinter GUI instead.)
- An internet connection for the Pi during setup (home Wi-Fi or Ethernet).
  Note: the Pi's Wi-Fi radio can only do one thing at a time — in Phase 2 it
  becomes an access point and loses client mode, so do all downloading now.

---

## 1. Flash Raspberry Pi OS

1. On your laptop, install **Raspberry Pi Imager**
   (https://www.raspberrypi.com/software/).
2. Choose device: **Raspberry Pi 5**.
3. Choose OS: **Raspberry Pi OS (64-bit)** — must be 64-bit, Ollama does not
   support 32-bit ARM.
4. Choose the SD card, then click **Next → Edit settings** and set:
   - Hostname: `ssai` (so the Pi is reachable as `ssai.local`)
   - Username and password (remember them — you need them for SSH)
   - Wireless LAN: your home Wi-Fi SSID + password, correct country
   - Services tab: **Enable SSH** (password authentication)
5. Flash, insert the card into the Pi, power on. First boot takes a couple of
   minutes (it resizes the filesystem and reboots once).

---

## 2. Connect over SSH

From your laptop:

```bash
ssh <user>@ssai.local
```

If `ssai.local` does not resolve, find the IP in your router's client list or
with:

```bash
ping ssai.local            # quick mDNS check
# or scan the network:
arp -a | grep -i raspberry
```

Then `ssh <user>@<ip-address>`.

Verify the OS is 64-bit (must print `aarch64`):

```bash
uname -m
```

Update the system:

```bash
sudo apt update && sudo apt full-upgrade -y
```

---

## 3. Install Ollama (the model runtime)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

The installer creates and starts a systemd service. Verify:

```bash
systemctl status ollama        # should say "active (running)"
curl http://127.0.0.1:11434/api/tags
# → {"models":[]}
```

If the service is not running: `sudo systemctl enable --now ollama`.

---

## 4. Download the model (the part that is not in the repo)

The repo expects `phi3.5:latest` (see `config.py`). Pull it:

```bash
ollama pull phi3.5:latest
```

This downloads ~2.2 GB — be patient on Wi-Fi. Then smoke-test it:

```bash
ollama run phi3.5:latest "Say hello in one short sentence."
```

The first generation is slow (~10–30 s) because the model loads into RAM;
subsequent turns are much faster. Type `/bye` to exit the test prompt.

### Model alternatives

If this Pi has 4 GB RAM, or you want a faster voice pipeline later (Phase 3),
use a smaller model instead:

| Model           | Download | Notes                      |
| --------------- | -------- | -------------------------- |
| `phi3.5:latest` | ~2.2 GB  | Repo default, best quality |
| `gemma2:2b`     | ~1.6 GB  | Slightly faster, decent    |
| `llama3.2:1b`   | ~1.3 GB  | Fast, weaker answers       |
| `qwen2.5:1.5b`  | ~1.0 GB  | Fast, good for its size    |
| `smollm2:360m`  | ~0.3 GB  | Very fast, very limited    |

To switch models:

```bash
ollama pull <model-name>
```

then edit `MODEL_NAME` in `config.py` to match exactly.

---

## 5. Install Python dependencies

Raspberry Pi OS (Bookworm) blocks system-wide `pip install`
("externally-managed-environment"). The clean route is apt:

```bash
sudo apt install -y python3-requests python3-psutil python3-tk python3-flask python3-waitress git
```

(`python3-tk` is only needed for the fullscreen GUI; on a screenless setup
you can skip it and the app will run in console mode. `python3-flask` +
`python3-waitress` are for the Phase 2 web server `web_server.py` — waitress
is the production server that keeps it stable when clients drop.)

(Alternative: a venv with `python3 -m venv --system-site-packages .venv` and
`pip install requests psutil flask waitress` inside it. Not needed if you used apt above.)

The code requires Python ≥ 3.10; Bookworm ships 3.11, fine. Check with
`python3 --version`.

---

## 6. Get the code onto the Pi

```bash
cd ~
git clone https://github.com/alvarohub/rpi5-local-llm-node-with-wifi-api.git
cd rpi5-local-llm-node-with-wifi-api
python3 -m compileall .    # quick syntax check of every module
```

---

## 7. Run it

### Option A — screenless (no display, the default for this project)

Just run it in your SSH session:

```bash
cd ~/rpi5-local-llm-node-with-wifi-api
python3 main.py
```

`main.py` detects that there is no display and starts a **console chat**
instead of crashing (you will see "starting console mode"). Type a question,
Enter to send; the answer streams in, followed by a metrics line
(`ttft`, total time, tokens, tok/s). Ctrl+C interrupts the current answer;
Ctrl+C or Ctrl+D at the prompt exits. `python3 console.py` does the same
thing explicitly.

### Option B — with a monitor attached (fullscreen GUI)

1. Boot the Pi to the desktop (`sudo raspi-config` → System Options →
   Boot / Auto Login → Desktop, or just attach the screen if it already
   boots to desktop).
2. On the Pi itself (terminal on its screen):

   ```bash
   cd ~/rpi5-local-llm-node-with-wifi-api
   python3 main.py
   ```

   Or, from your laptop's SSH session, launch it onto the Pi's desktop:

   ```bash
   DISPLAY=:0 python3 main.py
   ```

3. The fullscreen black chat appears. Type a question, Enter to send.
   Exit with the technician shortcut **Ctrl+Alt+Q**.

### Control view — monitoring from your laptop (SSH)

In a second SSH session (works with both options above):

```bash
cd ~/rpi5-local-llm-node-with-wifi-api
python3 control.py
```

This shows live CPU/RAM/temperature, per-question metrics (TTFT, total time,
tokens/s) and the last question/answer. Ctrl+C to close. You can also inspect
the raw status file directly: `cat /tmp/ssai_status.json`.

---

## 8. Verification checklist

- [ ] `curl http://127.0.0.1:11434/api/tags` lists `phi3.5:latest`
- [ ] `python3 main.py` over SSH starts console mode (no crash) and answers
      a question (first turn is slow — model load)
- [ ] With a monitor attached, `python3 main.py` opens the fullscreen chat
- [ ] `python3 control.py` over SSH shows live hardware + the completed turn
- [ ] Ctrl+Alt+Q exits the GUI cleanly (or Ctrl+D exits console mode)
- [ ] Record baseline numbers in `PLAN.md` (tok/s, TTFT, temperature)

Expected performance on a Pi 5 with phi3.5: roughly **1–3 tokens/second**.
The system prompt caps answers at ~50 words and `NUM_PREDICT = 150` caps
tokens, so answers are short by design — but a voice interface (Phase 3)
should plan around this latency.

---

## 9. Optional: autostart on boot

Ollama already autostarts (systemd).

**Screenless (recommended here):** create `/etc/systemd/system/ssai.service`:

```ini
[Unit]
Description=SSAI console chat
After=ollama.service network-online.target

[Service]
Type=simple
User=<user>
WorkingDirectory=/home/<user>/rpi5-local-llm-node-with-wifi-api
ExecStartPre=/bin/sh -c 'until curl -s http://127.0.0.1:11434/api/tags >/dev/null; do sleep 1; done'
ExecStart=/usr/bin/python3 console.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

then `sudo systemctl enable --now ssai`. (Note: a console chat under systemd
has no terminal attached, so autostart mainly makes sense once Phase 2's web
server exists — the service file will then point at `web_server.py` instead.)

**With a monitor (GUI):**

1. Enable desktop autologin: `sudo raspi-config` → System Options →
   Boot / Auto Login → **Desktop Autologin**.
2. Create `~/.config/autostart/ssai.desktop`:

   ```ini
   [Desktop Entry]
   Type=Application
   Name=SSAI
   Exec=sh -c 'until curl -s http://127.0.0.1:11434/api/tags >/dev/null; do sleep 1; done; cd /home/<user>/rpi5-local-llm-node-with-wifi-api && python3 main.py'
   ```

   (The `until` loop waits for Ollama before starting the GUI.)

3. Reboot and verify.

---

## 10. Troubleshooting

| Symptom                                                   | Cause / fix                                                                                                                                                                     |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_tkinter.TclError: no display name`                      | Not an error anymore — `main.py` falls back to console mode. Only relevant if you _want_ the GUI: attach a screen, boot to desktop, or use `DISPLAY=:0` while the desktop runs. |
| GUI says "Model unavailable"                              | Ollama down (`systemctl status ollama`) or model missing (`ollama list`). Also check `OLLAMA_API_BASE` in `config.py`.                                                          |
| `pip install` fails with "externally-managed-environment" | Bookworm policy — use the apt packages in section 5, or a venv.                                                                                                                 |
| First answer takes forever                                | Normal: the model loads into RAM on first use (~10–30 s).                                                                                                                       |
| Every answer is slow                                      | Expected on CPU (~1–3 tok/s with phi3.5). Try a smaller model (section 4).                                                                                                      |
| Temperature > 80 °C in control view                       | Add active cooling; the Pi throttles at 85 °C.                                                                                                                                  |
| `free -h` shows little free RAM                           | Close the browser/other apps; phi3.5 needs ~2.5 GB while loaded. On 4 GB Pis use a smaller model.                                                                               |
| Lightning-bolt icon / crashes under load                  | Undervoltage — use the official 5 A PSU.                                                                                                                                        |
| `ssai.local` not found                                    | mDNS may be blocked on your network; use the IP address instead.                                                                                                                |

# CommonsClaw — Environment Log

Reference facts about the hardware, network and access for this project.
Update as things change; this is the single place to look up "how do I
connect to the Pi again?".

## Hardware

| Item    | Detail                                    |
| ------- | ----------------------------------------- |
| Board   | Raspberry Pi 5                            |
| RAM     | 16 GB                                     |
| Storage | 32 GB microSD                             |
| Cooling | Active fan                                |
| Display | None (headless)                           |
| OS      | Raspberry Pi OS, latest (64-bit Bookworm) |

## Identity & access

| Item              | Detail                                                                                                                                   |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Hostname          | `emotionpi`                                                                                                                              |
| SSH user          | `admin`                                                                                                                                  |
| SSH address       | `ssh admin@emotionpi.local` (mDNS)                                                                                                       |
| Credentials       | Saved in macOS keychain / SSH agent (no password prompt)                                                                                 |
| Reference project | `SPEECH_RECORD_ANALYSIS` (Google Drive, VictorLeung collab) — fleet scripts, config.yaml, devices.csv hold the same credentials/patterns |

## Network topology

Two ways the Pi connects today:

1. **Ethernet + macOS Internet Sharing** (current, preferred for setup)
   - Pi —ethernet→ Mac —wifi→ internet.
   - Pi gets an IP from the Mac's sharing bridge (usually `192.168.2.x`).
   - Pros: fast, stable, Pi reaches the internet for `apt` / `ollama pull`.
   - Find the IP if mDNS fails: on the Mac, `arp -a | grep -i "b8:27\|dc:a6\|e4:5f"` (Pi OUIs) or check **System Settings → General → Sharing → Internet Sharing**.

2. **Direct Wi-Fi LAN** (available, not used yet)
   - Pi could join the same Wi-Fi as the Mac.
   - Not needed while Ethernet sharing works; keep as fallback.

## Connection status (2026-09-20)

**SSH to `emotionpi.local` did NOT resolve** — `ssh: Could not resolve hostname`.
Investigation on the Mac showed:

- No `bridge100` interface → **Internet Sharing is not currently active**.
- No Raspberry Pi MAC (OUI `b8:27`, `dc:a6`, `e4:5f`) in the arp table → Pi not visible.
- Mac is on Wi-Fi `192.168.1.49` (router `192.168.1.1`, linksys).

**Likely causes / next actions:**

- Pi may be powered off, or the Ethernet cable is unplugged.
- Internet Sharing may be toggled off in **System Settings → General → Sharing**.
- Once sharing is on and the Pi boots, find its IP with:
  `arp -a | grep 192.168.2` then `ssh admin@192.168.2.x`.
- mDNS (`emotionpi.local`) often does **not** cross the Internet Sharing bridge;
  use the numeric IP over Ethernet, or join the Pi to the same Wi-Fi as the Mac
  so mDNS works.

## Useful one-liners from the Mac

```bash
# connect (use the numeric IP — mDNS is unreliable across the sharing bridge)
ssh admin@192.168.2.13

# push code changes to the Pi (dev workflow)
cd ~/Documents/DEV_HARDWARE/RaspberryPi5_STT/ssai && ./push_to_pi.sh

# is Ollama up?
ssh admin@192.168.2.13 'curl -s http://127.0.0.1:11434/api/tags'

# live status file written by the app
ssh admin@192.168.2.13 'cat /tmp/commonsclaw_status.json'
```

## Working config (confirmed 2026-09-25)

- Mac↔Pi over Ethernet, **Internet Sharing ON** (System Settings → General →
  Sharing). Mac bridge `bridge100` = `192.168.2.1`; Pi eth0 DHCP = `192.168.2.13`.
- Pi reaches the internet through the Mac's Wi-Fi (used for ollama install + pull).
- `ssh admin@emotionpi.local` (mDNS) works intermittently — prefer `192.168.2.13`.
- Pi: Ollama `phi3.5:latest` installed, service `active`; `~/commonsclaw` holds the code;
  `flask` installed (via `sudo apt install python3-flask`); `console.py` verified
  working headless.
- **Measured ceiling: phi3.5 = ~5.2 tok/s, llama3.2:1b = ~8.4 tok/s on this
  Pi 5** (memory-bandwidth bound; threading already optimal). Default model is
  now llama3.2:1b (faster for conversational UX); phi3.5 remains installed.
  Switch in config.py `MODEL_NAME`.

## Wi-Fi access point (Phase 2B, Option A)

Two scripts in the repo, run **on the Pi** (push first with `./push_to_pi.sh`):

```bash
cd ~/commonsclaw
sudo bash ap_up.sh            # default ssid CommonsClaw, password emotionpi
sudo bash ap_up.sh MyNet mysecret   # custom ssid/password
sudo bash ap_down.sh          # tear the AP down (profile kept)
```

- Creates NetworkManager profile `commonsclaw-ap` on `wlan0`, `ipv4.method shared`
  → Pi is `10.42.0.1` and hands out DHCP to clients. eth0 (Mac dev link) is
  untouched and keeps working in parallel.
- Web chat from a phone on the AP: `http://10.42.0.1:8080`
- Wi-Fi country must be set once for AP to be legal/visible:
  `sudo raspi-config nonint do_wifi_country FR` (change `FR` as needed).
- **Gotcha:** in AP mode the Pi's wlan0 no longer has internet — all
  `apt`/`ollama pull` go over eth0 (Mac sharing) or are done before AP up.

## Notes

- 16 GB RAM is generous: `phi3.5:latest` (~2.5 GB loaded) leaves plenty of
  headroom; larger models (llama3.1:8b etc.) are also possible later.
- The Wi-Fi radio is free — Phase 2B will turn it into the access point
  while Ethernet keeps working for SSH/internet (the ideal dev setup:
  `wlan0` = AP for visitors, `eth0` = your cable for development).

# SSAI — Environment Log

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
# connect
ssh admin@emotionpi.local

# check the Pi's IP as seen by the Mac (when sharing over Ethernet)
arp -a | grep -i "b8:27\|dc:a6\|e4:5f"

# is Ollama up?
ssh admin@emotionpi.local 'curl -s http://127.0.0.1:11434/api/tags'

# live status file written by the app
ssh admin@emotionpi.local 'cat /tmp/ssai_status.json'
```

## Notes

- 16 GB RAM is generous: `phi3.5:latest` (~2.5 GB loaded) leaves plenty of
  headroom; larger models (llama3.1:8b etc.) are also possible later.
- The Wi-Fi radio is free — Phase 2B will turn it into the access point
  while Ethernet keeps working for SSH/internet (the ideal dev setup:
  `wlan0` = AP for visitors, `eth0` = your cable for development).

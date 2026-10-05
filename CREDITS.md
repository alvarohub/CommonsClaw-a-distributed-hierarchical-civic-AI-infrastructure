# Credits and Project History

## The people

- **Cesar Harada** — originator of the solar floating datacenter concept:
  [Floating-Solar-Hydrogen-Data-Center](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center). This project explores the complementary, fine-grained end of that spectrum: many small, local, solar-powered civic nodes instead of a few large
  platforms.

- **Alvaro Cassinelli** — concept, vision, and lead development for of the
  Hierarchical Civic AI architecture (aka CommonsClaw) alongside Cesar: a afine-grained, energy-proportional architecture for privacy-tiered civic datacenters; the "kami" node as a voice for a place; the hierarchy of models from engineered AIoT up to sovereign scale) is his
  original proposal, as is the bottom-up, small-scale-first realization
  strategy.

- **GitHub Copilot** (running Kimi K3 / DeepSeek V4.1 Flash) — AI pair-programmer, co-developing  the codebase with Alvaro from 2026-09-17 onward: screenless console mode,
  the web server and phone chat page, Wi-Fi access-point tooling, the model
  benchmark harness, unattended autostart, and documentation.

- **Ido Hoffmann** (with one commit by Yuri Klebanov), DLX, University of
  Tokyo — the original "SSAI" seed code (Sept 2026): a minimal Tkinter +
  Ollama chat prototype (~1,000 lines), written as an internship exercise
  within the collaboration. This repo began as a fork of that work; surviving
  upstream modules are `gui.py`, `llm_manager.py`, `hardware_monitor.py`,
  `status_store.py`, `control.py` (all since modified), under the MIT
  license. Sister development continues at DLX (more powerful hardware
  targets, e.g. Jetson, plus the floating platform and solar work).

## History

1. **Cesar Harada** develops and promotes the floating solar datacenter
   concept and, after joining the University of Tokyo (DLX), proposes a
   collaboration.
2. **Alvaro Cassinelli** pitches the first phase — a small, local,
   conversational civic node — as the bottom-up path toward what he calls
   the _Hierarchical Civic AI: the people's AI network_.
3. DLX assigns an intern, who produces the "SSAI" prototype (Tkinter chat
   over a local Ollama model) over several weeks in Sept 2026.
4. From 2026-09-17, Alvaro takes over the codebase directly, pair-programming
   with GitHub Copilot: in about a week the prototype gains headless console
   mode, a Wi-Fi access point with a phone web chat (streaming, phone-side
   STT/TTS), model benchmarking, and unattended autostart — and the project
   is renamed and becomes the **Public Spaces** node, Level 1 of the HCA
   hierarchy.
5. Planned: the code moves into an `HCA_PublicPlace/` subfolder of the larger
   HCA repository (not yet public).

## Links

- Cesar Harada, Floating Solar Hydrogen Data Center:
  <https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center>
- Original SSAI seed repo (DLX / U. Tokyo):
  <https://github.com/dlx-designlab/ssai>
- This project: <https://github.com/alvarohub/rpi5-local-llm-node-with-wifi-api>
  (to be renamed/moved under the future HCA organization)
- Vision document: [TOWARDS_HIERARCHICAL_CIVIC_AI.md](TOWARDS_HIERARCHICAL_CIVIC_AI.md)

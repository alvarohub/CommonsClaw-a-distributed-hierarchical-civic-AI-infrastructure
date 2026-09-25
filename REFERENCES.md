# CommonsClaw / Hierarchical Civic AI — Verified References

_Research date: 2026-09-25. Every entry below was verified by fetching the URL and confirming the page/paper exists (arXiv abstract pages, official project pages, GitHub repos, or Crossref DOI metadata). Nothing unverified is included._

## 1. Hierarchical / cascaded / tiered LLM inference

- **FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance** (Lingjiao Chen, Matei Zaharia, James Zou — Stanford, 2023) — The canonical LLM-cascade paper: learn which combinations of models to call per query, matching GPT-4 quality at up to 98% cost reduction. Directly maps to the "smallest sufficient model first, escalate only if needed" hierarchy.
  https://arxiv.org/abs/2305.05176
- **RouteLLM: Learning to Route LLMs with Preference Data** (Isaac Ong et al. — LMSYS / UC Berkeley, 2024) — Trains lightweight routers that pick a strong vs. weak LLM per query using human preference data; >2× cost savings with no quality drop, and routers transfer when the underlying models change. The reference for the "routing layer" of a tiered civic deployment.
  https://arxiv.org/abs/2406.18665
- **Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing** (Dujian Ding et al. — Microsoft, ICLR 2024) — Router assigns queries to a small (edge-deployable) or large model based on predicted query difficulty, with a test-time-tunable quality/cost trade-off; 40% fewer large-model calls at equal quality. Closest to an explicit edge-to-cloud offload policy.
  https://arxiv.org/abs/2404.14618
- **A Survey of Small Language Models** (Chien Van Nguyen et al., 2024) — Survey of SLM architectures, compression/pruning/quantization, benchmarks, and open challenges, explicitly covering on-device/mobile/edge deployment. Good umbrella citation for the small-model tier.
  https://arxiv.org/abs/2410.20011

## 2. Small / edge LLMs (Raspberry Pi-class)

- **Introducing Gemma 3 270M: The compact model for hyper-efficient AI** (Google DeepMind — Lacombe, Kenealy et al., Aug 2025) — Official release of the 270M Gemma variant with QAT INT4 checkpoints; measured 0.75% phone battery for 25 conversations. Strong evidence that sub-1B models are viable for ultra-low-power civic nodes.
  https://developers.googleblog.com/en/introducing-gemma-3-270m/
- **Qwen2.5 Technical Report** (Qwen Team, Alibaba — Yang et al., 2024) — The Qwen2.5 family includes an open-weight 0.5B model alongside larger sizes; covers training and quantized releases. A leading candidate family for the smallest tier.
  https://arxiv.org/abs/2412.15115
- **Llama 3.2 1B (model card)** (Meta, Sept 2024) — Official model card for the 1B/3B Llama 3.2 edge models, including quantization (SpinQuant/QAT+LoRA) and on-device inference numbers on Arm CPUs.
  https://huggingface.co/meta-llama/Llama-3.2-1B
- **Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone** (Marah Abdin et al. — Microsoft, 2024; v4 adds the phi-3.5 series) — phi-3-mini (3.8B) and phi-3.5-mini are designed for on-device deployment; the report's data-centric "textbook quality" training approach is the reference for small-model quality. (This is the model family the project currently runs via Ollama.)
  https://arxiv.org/abs/2404.14219
- **SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model** (Loubna Ben Allal et al. — Hugging Face, 2025) — Fully open 1.7B model with released training datasets; outperforms Qwen2.5-1.5B and Llama-3.2-1B. Best-documented open recipe in the Pi-feasible range.
  https://arxiv.org/abs/2502.02737

## 3. Local-first / personal AI on your own hardware

- **OpenClaw** (Peter Steinberger & community — OpenClaw Foundation, 2025–) — Open-source personal AI assistant (formerly Clawdbot/Moltbot) running on your own devices, meeting users in WhatsApp/Telegram/Slack/etc.; state, memory, and credentials live on your hardware, models are swappable plugins. The direct architectural reference and foil for CommonsClaw (see COMMONSCLAW_VS_OPENCLAW.md).
  https://github.com/openclaw/openclaw
- **llama.cpp** (Georgi Gerganov & ggml-org community, 2023–) — Plain C/C++ LLM inference with aggressive quantization, the de-facto engine that made LLMs run on commodity CPUs and Raspberry Pi-class ARM boards; backs Ollama and many other tools.
  https://github.com/ggml-org/llama.cpp
- **Ollama** (Ollama team, 2023–) — One-command local model serving with a REST API on 127.0.0.1:11434; the runtime used by this project for phi3.5/llama3.2 on the Pi.
  https://github.com/ollama/ollama
- **Jan** (Menlo Research / janhq, 2023–) — Open-source offline ChatGPT-style desktop app with a local OpenAI-compatible API, llama.cpp engine, and MCP support; reference UX for personal local AI.
  https://github.com/janhq/jan
- **PrivateGPT** (Zylon, 2023–) — Open-source API layer (RAG, ingestion, tools, MCP) on top of local OpenAI-compatible inference servers; went viral in 2023 as the proof-of-concept for fully-offline document chat, a precedent for privacy-first local assistants.
  https://github.com/zylon-ai/private-gpt
- **Home Assistant "Year of the Voice" + the Wyoming/Rhasspy stack** (Home Assistant / Nabu Casa / Open Home Foundation, 2022–) — The announcement post (Dec 2022) set the goal of a fully local, privacy-focused, multilingual voice assistant, hiring Rhasspy's creator Mike Hansen. The resulting open stack is the reference for the project's voice phase: Wyoming protocol (peer-to-peer JSON+PCM protocol for voice services), Piper (fast local neural TTS), openWakeWord (on-device wake words trained on synthetic speech), faster-whisper (CTranslate2 Whisper reimplementation, up to 4× faster on CPU), and Rhasspy itself.
  https://www.home-assistant.io/blog/2022/12/20/year-of-voice/ · https://github.com/OHF-Voice/wyoming · https://github.com/OHF-voice/piper1-gpl · https://github.com/dscripka/openWakeWord · https://github.com/SYSTRAN/faster-whisper · https://rhasspy.readthedocs.io/en/latest/

## 4. Agent protocols & memory

- **Model Context Protocol (MCP)** (Anthropic — David Soria Parra, Justin Spahr-Summers, Nov 2024) — Open standard ("USB-C for AI") connecting AI applications to data sources and tools via MCP servers/clients; now broadly adopted across clients. The candidate protocol for exposing civic-node capabilities (sensors, journals) to agents.
  https://www.anthropic.com/news/model-context-protocol · https://modelcontextprotocol.io/
- **Agent2Agent (A2A) Protocol** (Google → Linux Foundation, 2025) — Open protocol (JSON-RPC over HTTP, Agent Cards for discovery, SSE streaming) for interoperability between opaque agentic applications. Relevant if a hierarchy of civic nodes must delegate tasks to each other as peers, not just tools.
  https://github.com/a2aproject/A2A · https://a2a-protocol.org/
- **AGENTS.md** (open format, emerged from OpenAI Codex, Amp, Jules, Cursor, Factory et al.; now stewarded by the Agentic AI Foundation under the Linux Foundation, 2025) — The de-facto convention of a repo-level Markdown file that gives agents project context; used by 60k+ open-source projects. Directly related to the project's memory/ identity.md + journal.md practice of file-based agent context.
  https://agents.md/
- **MemGPT: Towards LLMs as Operating Systems** (Charles Packer et al. — UC Berkeley, 2023) — OS-inspired virtual context management: the LLM pages information between fast/slow memory tiers to exceed its context window, enabling agents that remember and evolve across sessions. Foundational citation for agent memory.
  https://arxiv.org/abs/2310.08560
- **Letta** (Letta, Inc. — founded by the MemGPT authors, 2024–) — The productionized continuation of MemGPT; its engineering blog covers file/git-based agent memory ("Context Repositories", 2026) and sleep-time memory consolidation — the most concrete published practice for the memory/ folder approach this project uses.
  https://www.letta.com/ (see letta.com/blog/context-repositories/)

## 5. Environmental / embodied / more-than-human computing

- **Things We Could Design: For More Than Human-Centered Worlds** (Ron Wakkary — MIT Press, 2021) — Posthumanist design manifesto arguing human-centered design is part of the problem; "designing-with" nonhumans as participants. The theoretical basis for treating the sensor/pi-vitals layer as a voice of the more-than-human. DOI 10.7551/mitpress/13649.001.0001 (verified via Crossref).
  https://doi.org/10.7551/mitpress/13649.001.0001
- **Technology and More-Than-Human Design** (Elisa Giaccardi, Johan Redström — Design Issues 36(4):33–44, 2020) — Short, citable journal article arguing that AI/IoT technologies exceed what human-centered design can frame, calling for more-than-human design methods. DOI 10.1162/desi_a_00612 (verified via Crossref).
  https://doi.org/10.1162/desi_a_00612
- **A City Is Not a Computer** (Shannon Mattern — Places Journal, Feb 2017; later a book from Duke UP, 2021) — Classic essay against reducing urban intelligence to information processing; argues for maintenance, care, archives, and ambient/environmental knowledge as forms of civic intelligence. Core framing for "civic AI" that isn't a smart-city dashboard. DOI 10.22269/170207.
  https://placesjournal.org/article/a-city-is-not-a-computer/
- **Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence** (Kate Crawford — Yale University Press, 2021) — Maps the material supply chains, energy, labor, and data extraction behind AI; the reference for why a low-power, locally-hosted civic node is also a political choice.
  https://katecrawford.net/atlas
- **On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜** (Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, Shmargaret Shmitchell — ACM FAccT 2021, pp. 610–623) — Foundational critique of ever-larger LMs, including their environmental/financial costs and who bears them. DOI 10.1145/3442188.3445922 (verified via Crossref).
  https://doi.org/10.1145/3442188.3445922

## 6. Community / civic networks & mesh infrastructure

- **Meshtastic** (Meshtastic project, 2020–) — Open-source, off-grid, encrypted LoRa mesh networking on cheap low-power devices; no cell towers or internet required. The reference mesh layer for civic nodes that keep talking when infrastructure fails.
  https://meshtastic.org/
- **NYC Mesh** (NYC Mesh, 2014–) — Volunteer-run, community-owned neutral wireless ISP in New York City (rooftop antennas, fiber to NYCHA buildings, a Network Commons License). Living proof that community infrastructure scales to a metropolis.
  https://www.nycmesh.net/
- **guifi.net, a crowdsourced network infrastructure held in common** (Roger Baig, Ramon Roca, Felix Freitag, Leandro Navarro — Computer Networks 90:150–165, Elsevier, 2015) — Peer-reviewed study of Europe's largest community network (Catalonia), explicitly analyzing it as a commons (with Ostrom references). The strongest academic citation for civic-network-as-commons. DOI 10.1016/j.comnet.2015.07.009 (verified via Crossref). Project page: https://guifi.net/en
- **Helium** (Helium / Nova Labs, 2019–) — People-deployed wireless network incentivized by the HNT token, now carrier-scale Wi-Fi offload. The main (cautionary and instructive) example of token-incentivized community infrastructure.
  https://www.helium.com/
- **Community Memory** (Community Memory Project — Lee Felsenstein, Efrem Lipkin, Ken Colstad, Jude Milhon, Mark Szpakowski; Berkeley, 1973–1975) — The first public computerized bulletin board: coin-operated public terminals on a shared timesharing machine, conceived as "strong, free, non-hierarchical channels of communication" to strengthen the local community. The historical ancestor of the community-memory ambition.
  https://en.wikipedia.org/wiki/Community_Memory

## 7. AI energy / sustainability measurement

- **Power Hungry Processing: Watts Driving the Cost of AI Deployment?** (Alexandra Sasha Luccioni, Yacine Jernite, Emma Strubell — ACM FAccT 2024) — First systematic comparison of inference-time energy: general-purpose generative models are orders of magnitude more expensive per query than task-specific ones. The quantitative argument for routing civic queries to the smallest tier. DOI 10.1145/3630106.3658542.
  https://arxiv.org/abs/2311.16863
- **Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model** (Alexandra Sasha Luccioni, Sylvain Viguier, Anne-Laure Ligozat, 2022) — Full life-cycle carbon accounting of a large model, including embodied emissions and inference via API. Methodological template for measuring a civic node's footprint.
  https://arxiv.org/abs/2211.02001
- **Energy and Policy Considerations for Deep Learning in NLP** (Emma Strubell, Ananya Ganesh, Andrew McCallum — ACL 2019) — The paper that put energy cost on the NLP agenda, quantifying financial and carbon costs of training large models and proposing reporting recommendations.
  https://arxiv.org/abs/1906.02243
- **Green AI** (Roy Schwartz, Jesse Dodge, Noah A. Smith, Oren Etzioni — Allen Institute for AI, 2019; CACM 2020) — Position paper advocating efficiency as a first-class evaluation criterion alongside accuracy, and reporting the "price tag" of models. The advocacy frame behind energy-aware hierarchical design.
  https://arxiv.org/abs/1907.10597
- **AI Energy Score** (Hugging Face initiative with Sasha Luccioni, Boris Gamazaychikov, Emma Strubell, Sara Hooker, Yacine Jernite, Margaret Mitchell, Carole-Jean Wu, 2024–) — "Energy Star"-style comparable efficiency ratings for AI models, with a public leaderboard and submission portal; useful for picking the most efficient model per tier.
  https://huggingface.co/AIEnergyScore
- **CodeCarbon / EcoLogits** (Code Carbon non-profit (mlco2 ecosystem), 2020–) — Open-source Python tools to measure CO₂ of local compute (CodeCarbon: CPU/GPU/RAM power × grid intensity) and GenAI API calls (EcoLogits). Practical tooling for logging the node's own energy per query.
  https://codecarbon.io/

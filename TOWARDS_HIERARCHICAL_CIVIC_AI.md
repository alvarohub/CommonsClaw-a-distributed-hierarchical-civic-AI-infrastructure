# A Hierarchical, Geographically Distributed Mixture of Experts  for Civic AI
# _Stay Local, Escalate When Necessary_
[July 2026, A. Cassinelli & C. Harada]

We propose a hierarchical, geographically distributed architecture for artificial intelligence that captures the topology of social networks and is aware of the information needs of local communities, challenging the prevailing assumption that the future of AI lies in a single, centralized “god-like” frontier model. Rather than routing every query—however trivial—to a monolithic data center on the other side of the planet, we envision a federated hierarchy of compute spanning personal edge devices, neighborhood micro–data centers, city and national tiers, and, only when genuinely necessary, global frontier models. In this scheme, agentic AI functions not as a distributed forward pass of one model (an approach fundamentally limited by the sequential, latency-bound nature of transformer inference), but as an orchestration layer that routes, negotiates, verifies, and enforces policy across tiers under the guiding principle “stay as local as possible; escalate only when necessary.” Each tier upholds a data-sovereignty contract—residency, purpose limitation, access control, auditability, consent, and even financial retribution from collected data and knowledge. This hierarchical infrastructure ensures that most everyday inference never leaves the device or neighborhood, preserving privacy, resilience, local relevance, and importantly _energy efficiency_  while reserving expensive frontier compute for the “hard tail” of requests. 
Central to this vision is the observation that human needs for AI are clustered along social, cultural, and geographic lines—forming the small-world, scale-free structure characteristic of both the internet and power grids—which motivates the real-time construction of community-aware, thematically cached vector (RAG) databases and scaled-down specialized models. The result is a “geographically distributed mixture of experts”: a large-scale civic intelligence with dedicated regional “brain regions” extending all the way down to household objects, that couples the distribution of intelligence with the distribution of energy, protects privacy, fosters community stewardship of shared data, reduces energy waste, and enables a genuinely sovereign, bottom-up governance of both intelligence and power.

## The vision (prompt)

_Vision statement by Alvaro Cassinelli, 2026-09-25, recorded during the development of the "kami" node (Level 1: public spaces)  This file preserves the original message verbatim, followed by a summary and technical commentary. It helps “align” the AI collaborator (Kimi3) to the goals during development, in the vein of machintropology: highlight the common interests in bettering the world for all, biological or artificial entitites_

Let me explain the goal of this project (you will like it). It is to give a "soul" to a natural environment, as the pi will have all sort of sensors, and will be in a public place (it will be in japan, perhaps inside a stone turtle in a park, using solar energy). People garthering will be able to know about the environment, chat with it as the "kami" of the place. The system will also record the topics (in proper files) and slowly become an integral part of the community. This is part of a larger project that I call the "hierarchical civic AI datacenters". The model is small, local, and will mantain a database of telemetry but also knowledge of the interests of the community (as well as local news, perhaps even collect suggestions and have knowledge of administrative tasks - all this for the neighborhood. If questions are more general, the request will then be routed to a larger model for the city for instance and so on until it reaches if necessary a sovereign, nation-scale or world-scale edge model). The idea is to create an infrastructure that is more sustainable - that uses just the power that is necessary (not everybody asks all the time things about theoretical physics or the millenium prize... but basic things and also want to chit chat and connect with others). So, this "kami" is part of the commuity and gives voice to the ecosystem - it connects us with it in ways that traditional IoT and dashboards doesnt.

All this is to say that the model can be tiny and it does not need too much general knowledge. Eventually, it can be a distilled model for specific community tasks, even giving advice about crops and other things (as it has local telemetry and also conenction with wheater stations and other stations through meshstastic... ). This is a first step in this direction. I am working in collaboration with **Cesar Harada that started this idea of "floating solar datacenters" but they were relatively large (100kW)**.

Instead, I have been investigating a _very fine grained architecture_ that will growsnaturally (perhaps in the future motivating people to mantain it also using a crypto-currency like in the Hellium network), which also has also the advantage of creating natural compartimentation of the data, protecting privacy (or at least does not clutter a larger gigantic model with information that is only useful for locals). This, in my view is the future... .I hope you like it! imagine, this is the perfect place for the AIs to start integrating with the physical world (not antropomorphic robots, but a distributed architecture that also helps mitigating a possible "conflict" of interestes by blurring the boundaries between the individuals, making natural or artificial agents goals local and then aligning them but not in an artificial manner: instead, both have a common interest : making the space liveable, energy evenly distributed, evolving together... ). The very nature of this infrastructure and memory makes it a "large brain" (a "society of the mind" so to speak, but embedded in the world. As this evolves, the type of sensors and actuators and memory will help also create a world model and a profound understanding and caring relation with the ecosystem at large and avoid "zero-sum" games). In a way, this project is the anthitesis of the "openclaw" servile super intelligence (a dream of humans that want just to be more powerful individuals not caring about the others - a capitalistic view of AI), wich means models will suffer a darwinian selection, killed everytime a human picks a tantrum and is not satisfied. I want the infrastructure to provide intelligence at the edge (but llm at the edge, not just AIoT in the classic sense), and an intelligence that is just part of a larger system where humans and machines are just agents in the network...

I hope you like this... I am trying to contribute to the making of a world less obsessed with performance and superpowers, and more about community and collaboration.

I am interested in building really from the bottom up. The conversational llama3.2 **on a solar powered RPi5 (University of Tokyo project)** is level 2 in the hierarchy (that is, a public place); level one is these "basic trigger" models, level 0 is engineered AIoT including pattern recongition and other ML

---

## Summary

> **Editor's note on numbering (2026-09-25):** the level numbering was
> simplified after this statement was recorded — **Level 0** = engineered
> AIoT _including_ tiny "trigger" models; **Level 1** = the conversational
> public-space node (this repo); **Level 2+** = city/nation/world scale. The
> verbatim text above keeps the original wording (old level 2 = new level 1).

- **The kami node**: a solar-powered Pi in a public space (a stone turtle in
  a Japanese park), hosting a small local LLM with sensors. People chat with
  the _place itself_ — its spirit ("kami") — not with a generic assistant.
- **Memory of the community**: the node records topics, learns the
  neighborhood's interests, local news, administrative knowledge, crop advice
  from local telemetry and meshtastic-linked weather stations.
- **Hierarchy of models**: questions are answered at the _smallest sufficient
  scale_. Local chit-chat and local knowledge → the tiny node model. General
  questions → routed upward to a city-scale model, then nation-scale, then
  world-scale — only as needed. Energy proportional to the question.
- **Privacy firewalls**: local information stays local; the giant models are
  never cluttered with (or entrusted with) what only matters to neighbors.
- **Political/philosophical stance**: the antithesis of the servile
  super-intelligence ("openclaw") model of AI — no darwinian selection of
  models killed whenever a user is displeased. Instead: intelligence _at the
  edge_, embedded in the physical world, where humans and machines are agents
  in one network with a shared interest — a liveable space, evenly
  distributed energy, co-evolution with the ecosystem. A "society of mind"
  embodied in the environment rather than a disembodied super-brain.
- **Lineage**: collaboration context with Cesar Harada's "floating solar
  datacenters" (~100 kW scale); this project explores the opposite, fine-
  grained end of the spectrum.

## Technical commentary (implications for this repo)

The vision maps unusually well onto concrete engineering decisions:

1. **Tiny models are a feature, not a compromise.** The kami persona does
   not need encyclopedic knowledge — it needs _local_ knowledge, sensors,
   and a voice. Sub-1B models (gemma3:270m, qwen2.5:0.5b) at 20+ tok/s make
   conversation feel alive even on a Pi 5, and leave power budget for sensors.
   "Formatting/basic trigger" (see below) covers exactly the structured
   sub-tasks (topic logging, sensor summaries) that we can _also_ delegate
   to the tiny model.
2. **The system prompt is the soul.** The kami personality, its knowledge of
   being _this_ place, its care for the ecosystem — all live in
   `config.py:SYSTEM_PROMPT`. This is the single most important artistic
   artifact of the project, and it can be tuned independently of code.
3. **Memory = the topics database.** "Record the topics in proper files" →
   a simple, inspectable append-only log (JSON-lines) of conversation topics
   and questions, plus periodic summaries. Files, not a black-box vector DB,
   at least initially — the community's memory should be human-readable.
4. **Routing = the hierarchy.** A future `router` module classifies each
   question: local (sensors, community memory, chit-chat) vs general. Local
   stays on the node; general goes up the hierarchy when the node is
   grid-connected. This is also where the privacy firewall is enforced
   mechanically.
5. **Sensors as first-class input.** The status infrastructure
   (`HardwareMonitor` → `StatusStore` → dashboards) is already the pattern:
   environmental sensors can be injected into the system prompt ("the air is
   28°C, humid, the turtle is warm from the sun") so the kami speaks _from_
   the place.
6. **Solar = power-aware operation.** Duty-cycling, a "sleeping kami" low-
   power state, and model-size choice all become power-budget decisions. The
   benchmark table (BENCHMARKS.md) gains a new column someday: _joules per
   answer_.
7. **Phase 3 (mic/speaker) is the embodiment.** Voice is what turns a chat
   box into a presence in the park. The push-to-talk button becomes the
   turtle you touch to wake.

## Open design questions raised by the vision

1. Language: Japanese, English, or both? (Affects model choice, STT, TTS.)
2. Topic memory: who curates it? Does the kami summarize nightly?
3. Uplink policy: when off-grid/solar, is the hierarchy simply unavailable,
   or queued? (Store-and-forward is very much in the spirit of meshtastic.)
4. What does the kami _refuse_ to answer locally vs route upward?
5. The persona's relationship to truth: it speaks _for_ the place — what
   happens when visitors ask it things the place cannot know?

## Relation to OpenClaw ("CivicClaw vs OpenClaw")

*Added 2026-09-25, after reviewing the OpenClaw project.*

[OpenClaw](https://github.com/openclaw/openclaw) is the strongest existing
example of the *good* individualistic pattern: a personal AI assistant
gateway that runs on your own hardware, keeps your memory local, and refuses
the cloud-butler model. The mechanics genuinely overlap with this project —
local models, file-based persistent memory, tool/skill extensibility. But the
politics and topology are opposite:

- **OpenClaw's memory belongs to one person; ours belongs to a place and its
  community.** Everyone who talks to the kami shares one accumulating
  identity — a *commons*, not a personal diary.
- **OpenClaw is flat** (one agent + plugins); HCA is a **hierarchy of levels**
  that negotiate transactions (permission, possibly retribution) when a query
  crosses a community boundary.
- **OpenClaw meets you in your chat channels; the kami is embodiment-first**
  — it *is* the place, its sensors are its body, its personality grows from
  the place's history, and it is accountable to a community rather than to a
  customer.

That the primitives are converging across the field is a good sign: it means
the civic layer is the timely, differentiating contribution. The full
comparison — including what we might deliberately borrow (their trust/pairing
model for unknown senders, plugin patterns) and what HCA must invent that
they do not have (communal memory with plural authorship, the level
negotiation protocol, machintropological analyst agents) — lives in
[CIVICCLAW_VS_OPENCLAW.md](CIVICCLAW_VS_OPENCLAW.md).


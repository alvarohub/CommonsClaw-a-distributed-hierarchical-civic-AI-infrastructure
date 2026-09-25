# Towards Hierarchical Civic AI Datacenters

*Vision statement by Alvaro Cassinelli, 2026-09-25, recorded during the
development of SSAI (the "kami" node) — this file preserves the original
message verbatim, followed by a summary and technical commentary.*

---

## The vision (verbatim)

> Let me explain the goal of this project (you will like it). It is to give a
> "soul" to a natural environment, as the pi will have all sort of sensors,
> and will be in a public place (it will be in japan, perhaps inside a stone
> turtle in a park, using solar energy). People gathering will be able to know
> about the environment, chat with it as the "kami" of the place. The system
> will also record the topics (in proper files) and slowly become an integral
> part of the community. This is part of a larger project that I call the
> "hierarchical civic AI datacenters". The model is small, local, and will
> maintain a database of telemetry but also knowledge of the interests of the
> community (as well as local news, perhaps even collect suggestions and have
> knowledge of administrative tasks - all this for the neighborhood. If
> questions are more general, the request will then be routed to a larger
> model for the city for instance and so on until it reaches if necessary a
> sovereign, nation-scale or world-scale edge model). The idea is to create an
> infrastructure that is more sustainable - that uses just the power that is
> necessary (not everybody asks all the time things about theoretical physics
> or the millennium prize... but basic things and also want to chit chat and
> connect with others). So, this "kami" is part of the community and gives
> voice to the ecosystem - it connects us with it in ways that traditional IoT
> and dashboards don't.
>
> All this is to say that the model can be tiny and it does not need too much
> general knowledge. Eventually, it can be a distilled model for specific
> community tasks, even giving advice about crops and other things (as it has
> local telemetry and also connection with weather stations and other stations
> through meshtastic... ). This is a first step in this direction. I am
> working in collaboration with Cesar Harada that started this idea of
> "floating solar datacenters" but they were relatively large (100kW). I
> propose and want to explore a very fine grained architecture which has also
> the advantage of creating "firewalls" that protect privacy (or at least does
> not clutter a larger gigantic model with information that is only useful for
> locals). This, in my view is the future... imagine, this is the perfect
> place for the AIs to start integrating with the physical world (not
> anthropomorphic robots, but a distributed architecture that also helps
> mitigating a possible "conflict" of interests by blurring the boundaries
> between the individuals, making natural or artificial agents goals local and
> then aligning them but not in an artificial manner: instead, both have a
> common interest: making the space liveable, energy evenly distributed,
> evolving together...). The very nature of this infrastructure and memory
> makes it a "large brain" (a "society of the mind" so to speak, but embedded
> in the world. As this evolves, the type of sensors and actuators and memory
> will help also create a world model and a profound understanding and caring
> relation with the ecosystem at large and avoid "zero-sum" games). In a way,
> this project is the antithesis of the "openclaw" servile super intelligence
> (a dream of humans that want just to be more powerful individuals not caring
> about the others - a capitalistic view of AI), which means models will
> suffer a darwinian selection, killed everytime a human picks a tantrum and
> is not satisfied. I want the infrastructure to provide intelligence at the
> edge (but llm at the edge, not just AIoT in the classic sense), and an
> intelligence that is just part of a larger system where humans and machines
> are just agents in the network...
>
> ...I am trying to contribute to the making of a world less obsessed with
> performance and superpowers, and more about community and collaboration.

---

## Summary

- **The kami node**: a solar-powered Pi in a public space (a stone turtle in
  a Japanese park), hosting a small local LLM with sensors. People chat with
  the *place itself* — its spirit ("kami") — not with a generic assistant.
- **Memory of the community**: the node records topics, learns the
  neighborhood's interests, local news, administrative knowledge, crop advice
  from local telemetry and meshtastic-linked weather stations.
- **Hierarchy of models**: questions are answered at the *smallest sufficient
  scale*. Local chit-chat and local knowledge → the tiny node model. General
  questions → routed upward to a city-scale model, then nation-scale, then
  world-scale — only as needed. Energy proportional to the question.
- **Privacy firewalls**: local information stays local; the giant models are
  never cluttered with (or entrusted with) what only matters to neighbors.
- **Political/philosophical stance**: the antithesis of the servile
  super-intelligence ("openclaw") model of AI — no darwinian selection of
  models killed whenever a user is displeased. Instead: intelligence *at the
  edge*, embedded in the physical world, where humans and machines are agents
  in one network with a shared interest — a liveable space, evenly
  distributed energy, co-evolution with the ecosystem. A "society of mind"
  embodied in the environment rather than a disembodied super-brain.
- **Lineage**: collaboration context with Cesar Harada's "floating solar
  datacenters" (~100 kW scale); this project explores the opposite, fine-
  grained end of the spectrum.

## Technical commentary (implications for this repo)

The vision maps unusually well onto concrete engineering decisions:

1. **Tiny models are a feature, not a compromise.** The kami persona does
   not need encyclopedic knowledge — it needs *local* knowledge, sensors,
   and a voice. Sub-1B models (gemma3:270m, qwen2.5:0.5b) at 20+ tok/s make
   conversation feel alive even on a Pi 5, and leave power budget for sensors.
   "Formatting/basic trigger" (see below) covers exactly the structured
   sub-tasks (topic logging, sensor summaries) that we can *also* delegate
   to the tiny model.
2. **The system prompt is the soul.** The kami personality, its knowledge of
   being *this* place, its care for the ecosystem — all live in
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
   28°C, humid, the turtle is warm from the sun") so the kami speaks *from*
   the place.
6. **Solar = power-aware operation.** Duty-cycling, a "sleeping kami" low-
   power state, and model-size choice all become power-budget decisions. The
   benchmark table (BENCHMARKS.md) gains a new column someday: *joules per
   answer*.
7. **Phase 3 (mic/speaker) is the embodiment.** Voice is what turns a chat
   box into a presence in the park. The push-to-talk button becomes the
   turtle you touch to wake.

## Open design questions raised by the vision

1. Language: Japanese, English, or both? (Affects model choice, STT, TTS.)
2. Topic memory: who curates it? Does the kami summarize nightly?
3. Uplink policy: when off-grid/solar, is the hierarchy simply unavailable,
   or queued? (Store-and-forward is very much in the spirit of meshtastic.)
4. What does the kami *refuse* to answer locally vs route upward?
5. The persona's relationship to truth: it speaks *for* the place — what
   happens when visitors ask it things the place cannot know?

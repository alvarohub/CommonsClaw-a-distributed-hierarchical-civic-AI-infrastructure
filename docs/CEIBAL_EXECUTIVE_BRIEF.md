# CommonsClaw

## Local civic AI as shared educational infrastructure

**Discussion brief for Ceibal, Uruguay | 10 November 2026**

> **The proposition:** explore whether small, locally operated AI nodes can help schools and communities understand their environment, build shared knowledge, and learn how AI works. Start with a bounded experiment; use its evidence to decide whether a wider network is worth developing.
>
> **The decision now is whether to co-design that experiment, not whether to approve a national deployment.** No partnership, funding, sites, equipment allocation, or delivery schedule is assumed in this document.

## 1. The problem and the opportunity

Access to an AI chatbot is not the same as the capacity to understand, adapt, and govern AI infrastructure. A school or community may use powerful online tools while having little control over where computation happens, what local knowledge is retained, or how that knowledge is shared.

There is a second, practical gap: environmental measurements, school projects, and community observations often remain separate. A sensor dashboard shows values; a chatbot generates language; neither automatically becomes a trustworthy, collectively maintained record of a place.

**CommonsClaw proposes to connect these functions.** Its central question is whether a locally operated AI, grounded in measurements and curated community contributions, can become useful shared infrastructure rather than another personal assistant.

For Ceibal, this would be a complementary research and education track, not a replacement for existing platforms or teachers. Ceibal already has EduIA Lab, teacher-facing AI initiatives, and physical-computing educational resources. Its 2026 AI offer includes Gemini and NotebookLM; the additional question here is what **local operation, physical sensing, and community stewardship** make possible.[^eduia][^ceibal-ai][^microbit]

## 2. The vision, in practical terms

A **place node** is a small computer associated with a school garden, library, workshop, or public space. People access it through a local browser interface and, where validated, voice. It combines a local language model with selected documents, sensor readings, and community notes.

The longer-term architecture connects these nodes at different scales:

| Scale | Intended responsibility |
| --- | --- |
| Sensors and small devices | Measure and record: temperature, soil moisture, energy, or other locally chosen observations. |
| Place node | Answer questions about that place; maintain an inspectable local record. |
| Shared school-cluster or neighbourhood node | Compare approved information from several places; handle work beyond an individual node's capacity. |
| Larger institutional services | Supply additional capabilities only when needed and permitted. |

**The hierarchy concerns knowledge and task delegation, not splitting one large model across a radio network.** Local nodes should continue their local functions when an upstream connection fails. Communities should decide what may leave a node, for what purpose, and who can change its shared memory. These are design requirements, not completed safeguards.

**An illustrative activity, not an existing deployment:** students instrument two school gardens, compare measurements with the AI's explanation, correct unsupported claims, and publish a teacher-reviewed account of what they observed. A shared node then compares the two accounts without receiving students' private conversations. The learning is both environmental and computational: measurement, uncertainty, source checking, programming, and collective decision-making.

The project is led conceptually and technically by Alvaro Cassinelli, with origins in the SSAI prototype at DLX, University of Tokyo, and in exchanges with Cesar Harada's Floating Solar Hydrogen Data Center project. That energy-infrastructure project is complementary but separate: a Ceibal experiment does **not** require a floating platform, hydrogen installation, or new datacenter. Earlier Gluons work by Cassinelli and Daniel Saakes provides a physical-computing precedent and includes a published proposal/report for Ceibal; it does not establish a current partnership.[^origins][^floating][^gluons]

## 3. What exists, and what remains to be demonstrated

**Current maturity: a local-node prototype, not an operational civic AI network.** The following reflects repository evidence, not an independent field evaluation.[^status]

| Evidence available | Boundary of that evidence |
| --- | --- |
| Raspberry Pi 5 running a local model through Ollama; phone-to-node Wi-Fi chat with streamed answers, recorded as tested. | This demonstrates local interaction, not classroom-scale concurrency or educational effectiveness. |
| File-based identity, community notes, sensor digests, and logging mechanisms. | Accumulating information is not yet a validated, source-traceable community memory or cross-place synthesis. |
| A local microphone/transcription prototype, plus browser speech features. | Voice reliability remains development work. Browser dictation may use external services; a local model alone does not make the entire voice path offline. |
| Sensor registry, logger supervision, and actual computer-health telemetry. | The solar-power logger is explicitly simulated. Real environmental sensing and solar autonomy must be instrumented and tested. |
| Setup, monitoring, autostart, and model-benchmark tooling. | Unattended recovery, sustained uptime, secure administration, and maintainability require acceptance testing. |

The Pi 5 provides an existing reference platform, not a decision that all future nodes must use it. Repository benchmarks are narrow development measurements, not evidence of Spanish-language classroom quality, whole-system energy savings, or performance on retired Ceibal devices.[^benchmarks]

**Still to build:** trustworthy memory consolidation; authenticated, permission-controlled exchange between nodes; rules for escalation to larger models; and the operational and educational framework for a supported deployment. These are the substance of the proposed collaboration, not packaging around an already finished product.

## 4. What Uruguay already offers

These are documented foundations and possible points of contact, **not committed partners or resources available on demand**.

| Existing foundation | Possible relevance | What must be established together |
| --- | --- | --- |
| **Ceibal's EduIA Lab and AI education work.** EduIA Lab was presented in March 2025; Ceibal and ANEP announced further teacher-facing AI tools and support in June 2026.[^eduia][^ceibal-ai] | Pedagogical design, teacher involvement, evaluation, and comparison with existing AI uses. | Whether this research question fits current priorities; who would sponsor and evaluate it. |
| **Physical computing and micro:bit education.** Ceibal's EDUx materials connect programmable boards with project-based learning, electronics, and computational thinking.[^microbit] | Students could build and interrogate environmental sensing systems rather than only consume AI outputs. | Suitable ages, teacher preparation, equipment access, and curriculum fit. A micro:bit is a sensor/learning device, not a conversational language-model host. |
| **Device repair and circular-economy experience.** Official reporting describes Ceibal's repair, component recovery, and recycling operations.[^circular] | Assess whether some retired equipment can serve as browser terminals, sensor gateways, or compute nodes. | Actual inventory, authorization, operating-system support, memory, battery safety, energy use, and support cost. No stock or device suitability is assumed. |
| **Antel IoT expertise and prototyping hardware.** Antel documents an IoT offering and an R&D kit with communications modules including LoRa and NB-IoT.[^antel] | Advice on sensor connectivity and a possible route to a supported field connection. | Coverage at selected sites, service terms, device compatibility, costs, and data hosting. These pages do not establish an open, nationwide LoRaWAN service accessible to this project. |
| **Montevideo's documented LoRaWAN lighting project.** A February 2022 supplier announcement describes a private network planned for 70,000 streetlights and provision for third-party services.[^montevideo] | A concrete lead for investigating shared municipal connectivity. | Current operation, gateway coverage, operator permission, capacity, and commercial terms. The announcement is not proof of present access or coverage outside Montevideo. |
| **Uruguay's National AI Strategy 2024-2030.** Its objectives cover governance, capabilities, and sustainable development.[^strategy] | A policy context for public-interest AI infrastructure and local technical capacity. | Actual institutional fit and any funding mechanism; alignment alone is not endorsement or financing. |

### Connectivity: use each network for the right job

Use **local Wi-Fi or Ethernet for interaction**, and an authorized IP connection for larger transfers and coordination between sites. The initial local-node test need not depend on access to any external radio network.

**LoRa/LoRaWAN suits small, occasional sensor messages**, not continuous voice, model downloads, or high-volume exchange of documents. LoRa is the radio technology; LoRaWAN adds a network protocol and gateway/server architecture. Meshtastic is a separate LoRa-based mesh option, not interchangeable with LoRaWAN. Any radio experiment needs a site survey and confirmation of applicable Uruguayan equipment and spectrum requirements.[^lorawan][^meshtastic]

## 5. What a development collaboration would need to deliver

| Work package | Concrete result to evaluate |
| --- | --- |
| **Reliable local node** | Repeatable installation; bounded failures and recovery; Spanish-language evaluation; a clear typed interface before adding more demanding voice interaction. |
| **Trustworthy shared knowledge** | Source and timestamp attached to observations; separation of measurements, user suggestions, and model interpretation; human approval, correction, and deletion of shared memory. |
| **First functioning hierarchy** | Two place nodes and one shared node exchanging only approved information; authenticated access, logged permissions, revocation, and useful local behaviour during disconnection. |
| **Real sensing and measured resource use** | A small set of calibrated sensors; explicit missing/stale-data handling; measured power consumption, response time, and maintenance effort. Solar and radio links only where justified by the selected activity. |
| **Educational and operational design** | Teacher-led activities, safeguarding review, local stewardship, training, support procedures, and a comparison with a simpler non-AI approach. |

There are reusable foundations rather than a need to invent every component. CommonsClaw already uses local model serving; Home Assistant's voice work offers a modular, local-first precedent. Kolibri provides a separate precedent for offline educational delivery, local-network access, and educator support. RouteLLM demonstrates research on selecting between models of different capabilities. None supplies the missing community-governance layer, proves educational benefit here, or guarantees energy savings.[^voice][^kolibri][^routing]

## 6. A possible sequence, with explicit decision gates

**Discussion scenario only:** two participating places and one shared institutional host are enough to test the first hierarchy. Site count, participants, age groups, and scope remain open.

The ranges below are **rough engineering planning estimates**, not externally benchmarked delivery times. They assume an available software lead with regular engineering support, educator participation, suitable off-the-shelf hardware, and one bounded learning activity. They exclude procurement delays, school-calendar constraints, and institutional approvals; those may dominate elapsed time.

| Stage | Indicative active elapsed time | Output and decision gate |
| --- | --- | --- |
| **A. Joint definition and feasibility** | 2-4 weeks | Agree the activity, data boundaries, equipment audit, responsibilities, and evaluation criteria. Decide whether to proceed. |
| **B. Pilot-ready prototype** | A further 6-10 weeks | Harden the existing node, integrate real sensors, and demonstrate controlled exchange with a second node and shared host in the lab. Proceed only after recovery, data-boundary, and source-checking tests pass. |
| **C. Small supervised experiment** | A further 8-12 weeks | Run the selected activity at the participating places; document learning, reliability, errors, support effort, and power use. Pause or simplify if agreed safeguards fail. |
| **D. Review and scale decision** | A further 2-4 weeks | Publish findings, a costed operating model, and a recommendation: stop, revise, repeat, or expand. |

If sequential, this is **18-30 active weeks**, before external delays. It is not a forecast of national readiness. Home Assistant's staged voice releases and Kolibri's deployment guidance support the incremental approach, **not these numerical estimates**.[^voice][^kolibri]

Expansion would be a separate programme: repeatable provisioning and updates, fleet security, local support and spares, model/content governance, accessibility, and trials across different contexts. A successful demonstration at two places would not establish capacity or value at national scale.

## 7. People, hardware, and the budget conversation

### Human capacity

For the scenario above, discuss **one named software/integration lead plus regular embedded-systems or deployment support**; two available engineering contributors would reduce dependence on a single person. This is a planning assumption, not an agreed staffing request.

Also needed are an **education/co-design lead with participating teachers**, an **evaluation lead**, **privacy and safeguarding expertise at design and release gates**, and a **named local custodian at each site**. These responsibilities can overlap, but protected time for preparation, supervision, maintenance, and review must be budgeted. Teachers should not silently inherit systems-administration duties.

### Illustrative equipment envelope

| Item | Purpose and sizing question |
| --- | --- |
| **Two place-node computers** | Begin from the tested Pi 5 class or benchmark available alternatives. Include cooling, reliable storage, power supplies, and appropriate enclosures. |
| **One shared computer** | Host cross-place synthesis and any larger model. Benchmark existing institutional hardware before deciding whether extra RAM or a GPU is needed. |
| **One small sensor set per place** | Select only measurements needed by the learning activity; include interfaces, calibration, mounting, and replacement parts. |
| **Browser-capable access devices** | Check authorized use of existing school equipment; a learner should not need a personal smartphone to participate. |
| **Support and measurement equipment** | Power meter, backup storage, spare components, and a documented recovery method. |
| **Conditional additions** | Microphone/speaker after voice tests; LoRa devices and a gateway/service only if needed; battery/solar equipment only after measuring the load and site conditions. |

No supplier quotation or verified Ceibal inventory supports a monetary total yet. A useful next-step budget should separate **engineering time; educator preparation and release time; equipment and spares; installation and travel; connectivity; evaluation; and recurring support/replacement costs**. Device reuse should be compared with new hardware on total cost, reliability, and energy use, not assumed to be free.

## 8. Conditions for a responsible experiment

- **Child safety and data governance first.** Determine responsibility for data processing, lawful basis and any required consent, retention, access, and deletion before involving learners. Review the design against Uruguay's personal-data framework and institutional requirements.[^privacy]
- **Local does not automatically mean private.** Shared terminals, logs, memory, browser speech services, and upstream queries all need explicit controls. A summary can still identify a person.
- **Keep decisions with people.** No autonomous grading, student profiling, or consequential civic decisions in the initial scope. Treat generated explanations as hypotheses to verify, not authoritative accounts of the community.
- **Measure additional value.** Compare against a sensor dashboard plus teacher-curated notebook, and, where appropriate, an existing institutional AI tool. Agree thresholds before starting: source-backed answers, learning outcomes, response time, uptime/recovery, support hours, and total operating cost.
- **Test the sustainability claim.** Measure whole-node idle and active power, not only inference speed. Reduced cloud use does not by itself prove a lower environmental footprint.

## 9. Questions for the Ceibal discussion

1. **Purpose:** which learning or community problem warrants this experiment, rather than a simpler existing tool?
2. **Contribution:** would Ceibal be interested in co-design, educational evaluation, technical development, equipment assessment, or some combination?
3. **Setting and governance:** which contexts and age groups are appropriate, and who would steward each node and approve shared knowledge?
4. **Infrastructure:** what equipment and connectivity may actually be used, under what conditions?
5. **Evidence and continuation:** what results would justify further investment, and who would own ongoing maintenance?

**Suggested immediate outcome:** a jointly agreed feasibility scope with named counterparts and explicit go/no-go criteria. A budget and calendar can then follow from facts established together.

## References and evidence notes

Sources checked on **10 November 2026**. Government publications document initiatives and policy, not commitments to CommonsClaw. Supplier announcements are identified as such. Project references below are pinned to repository revision `17baa3f` so that prototype claims can be checked against the reviewed record.

[^eduia]: Presidency of Uruguay, **"Ceibal presento EduIA Lab, primer laboratorio regional de inteligencia artificial en educacion"**, 26 March 2025. [Official announcement](https://www.gub.uy/presidencia/comunicacion/noticias/ceibal-presento-eduia-lab-primer-laboratorio-regional-inteligencia-artificial).

[^ceibal-ai]: Presidency of Uruguay, **"Ceibal y ANEP ofrecen nuevas herramientas de inteligencia artificial para docentes"**, 16 June 2026. [Official announcement](https://www.gub.uy/presidencia/comunicacion/noticias/inteligencia-artificial-docentes-estudiantes-ceibal-anep-nuevas-2026). Establishes the existing institutional offer; it does not describe a locally hosted language-model network.

[^microbit]: Ceibal, EDUx, **"Micro:bit en el aula"**, course description, undated. [Educational approach and programmable-board activities](https://edux.ceibal.edu.uy/courses/course-v1:ceibal+CEIBAL4_C1+2/about). Evidence of educational resources, not current course availability or an equipment allocation.

[^origins]: CommonsClaw, [Credits and Project History](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/CREDITS.md). Project-authored account of roles and prototype origins.

[^floating]: Cesar Harada, [Floating Solar Hydrogen Data Center](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center). Related open-hardware proposal; its repository distinguishes prototyped and speculative elements.

[^gluons]: Alvaro Cassinelli and Daniel Saakes, **"Data Flow, Spatial Physical Computing"**, TEI 2017, [DOI: 10.1145/3024969.3024978](https://doi.org/10.1145/3024969.3024978). [Author's project page](https://alvarocassinelli.com/gluons/) links the paper, software, and initial Ceibal proposal/report.

[^status]: CommonsClaw, [Plan of Record](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/PLAN.md), [voice status](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/03-interaction-and-voice.md), and [roadmap](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/07-roadmap.md). The [sensor registry](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/sensors.json) and [solar logger](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/loggers/sensor_solarpower.py) explicitly identify simulated solar data. Where broader vision texts imply completed capabilities, this brief uses the implementation record and unfinished acceptance criteria.

[^benchmarks]: CommonsClaw, [Model Benchmarks](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/BENCHMARKS.md), measurements dated 25 September 2026. The recorded rows are explicitly described as quick probes.

[^circular]: Presidency of Uruguay, **"El 75% de los residuos electronicos de Ceibal es reutilizado"**, 3 June 2024. [Repair, recovery, recycling, and educational activities](https://www.gub.uy/presidencia/comunicacion/noticias/75-residuos-electronicos-ceibal-es-reutilizado). Evidence of lifecycle-management capacity, not available retired-device inventory.

[^antel]: Antel, [IoT overview](https://www.antel.com.uy/web/iot) and [Kit IoT Hardware](https://www.antel.com.uy/web/iot/w/kit-iot-hardware), undated. The kit description explicitly lists NB-IoT, LoRa, BLE, Xbee, and LTE.

[^montevideo]: Actility, **"Uruguay to deploy one of LoRaWAN's largest smart street lighting projects..."**, 4 February 2022. [Supplier announcement](https://www.actility.com/uruguay-montevideo-lorawan-street-lighting/). Describes a private, customer-premises network and prospective third-party services; not a current coverage or service-access confirmation.

[^strategy]: Agesic, **National Artificial Intelligence Strategy 2024-2030**, published 22 November 2024, approved 21 November. [Official summary and strategy link](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/estrategia-nacional-inteligencia-artificial-2024-2030).

[^lorawan]: The Things Network, [What is LoRaWAN?](https://www.thethingsnetwork.org/docs/lorawan/what-is-lorawan/), technical documentation, undated. Explains the distinction between LoRa and LoRaWAN and suitability for small payloads.

[^meshtastic]: Meshtastic, [Introduction](https://meshtastic.org/docs/introduction/), project documentation, undated. A reference for off-grid LoRa messaging, not evidence of an available Uruguayan deployment.

[^voice]: Home Assistant, **"2023: Home Assistant's year of Voice"**, 20 December 2022, with links to subsequent staged releases. [Project announcement](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/). A modular voice-engineering precedent, not a classroom conversational-AI evaluation.

[^kolibri]: Learning Equality, [Kolibri User Guide](https://kolibri.readthedocs.io/en/latest/) and [About Kolibri](https://learningequality.org/kolibri/about-kolibri/), undated. Offline education, local-server delivery, and educator-support precedent; not a language-model system.

[^routing]: Isaac Ong et al., **"RouteLLM: Learning to Route LLMs with Preference Data"**, first submitted 26 June 2024. [arXiv:2406.18665](https://arxiv.org/abs/2406.18665). Supports research feasibility of model routing; API-cost results are not measurements of CommonsClaw's energy use or educational quality.

[^privacy]: Uruguay, **Law No. 18.331, Personal Data Protection**, promulgated 11 August 2008. [IMPO legal text and amendment references](https://www.impo.com.uy/bases/leyes/18331-2008). A starting point for institutional legal review, not a compliance determination.

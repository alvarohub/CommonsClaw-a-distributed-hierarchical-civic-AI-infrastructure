<!-- Editable source. To regenerate the self-contained HTML, run from this folder:
pandoc CEIBAL_JOINT_PROPOSAL.md --from=markdown --to=html5 --standalone --toc --toc-depth=2 --metadata pagetitle="From local energy to civic AI | Ceibal" --template=assets/report-template.html --css=assets/proposal.css --embed-resources --output=CEIBAL_JOINT_PROPOSAL.html
-->

# From local energy to civic AI

## Floating Solar Data Centres + CommonsClaw

**An educational and research collaboration to explore with Ceibal, Uruguay**  
Discussion document · 11 November 2026

> **What we are looking for:** research and education partners to evaluate the impact of a floating data centre on the marine environment, while developing its connection to local, community-controlled AI.
>
> **The longer-term ambition:** communities can produce energy locally, operate their own computing infrastructure, and govern the knowledge it holds. Floating Solar Data Centres explore the physical and ecological side; CommonsClaw develops the distributed civic-AI side.
>
> **The proposal to Ceibal:** explore participation in a research-and-education collaboration bringing together **port or marina access, marine science, and design and engineering**. Ceibal could help shape the educational and technical activities and connect appropriate partners. STEM projects in sensing, device reuse, local energy, and CommonsClaw would form part of this shared experiment—not replace the marine research objective.

This invitation follows slide 9 of the supplied presentation. The three partner roles, possible Ceibal contributions, and decisions needed to proceed are detailed in Section 4.[4](#ref-4)

**Reading guide:** Sections 1–9 are the discussion brief. Optional technical background follows in [Appendix A: CommonsClaw](#appendix-commonsclaw) and [Appendix B: Floating Solar Data Centres](#appendix-floating).

![Floating-platform prototype in Hong Kong, identified in the supplied presentation as built and tested at sea in 2021. Photograph reproduced from slide 1. This is an antecedent in the project's development, not evidence of an operational AI datacentre or demonstrated biodiversity gains.](assets/floating-prototype-hong-kong-2021.jpg)

## 1. Why bring these projects together?

AI has a physical footprint and a governance model. It runs on equipment that requires electricity, cooling, materials, maintenance, and eventual replacement. It also raises questions about who owns the infrastructure, who controls data, and whose needs determine its use. The IEA identifies AI as a driver of growing datacentre electricity demand, while emphasizing uncertainty and the importance of efficiency.[1](#ref-1)

Providing access to an online AI service addresses only part of that picture. **Could people also learn to build, power, maintain, and govern a small part of the infrastructure themselves?**

The two projects approach this question from different directions:

| | Floating Solar Data Centres | CommonsClaw / Hierarchical Civic AI |
| --- | --- | --- |
| **Primary question** | Can locally powered floating computing infrastructure operate sustainably, and what effects does it have on the marine environment? | Can communities operate useful local AI, maintain shared knowledge, and cooperate without mandatory dependence on distant commercial cloud services? |
| **Main work** | Floating structures, solar energy, storage and cooling, environmental monitoring, and ecological assessment. | Local models, sensing, community memory, controlled information exchange, and distributed operation. |
| **Leadership and origins** | Spearheaded by Cesar Harada; builds on earlier floating energy and marine-science prototypes. | Concept and lead development by Alvaro Cassinelli, originating from the DLX/University of Tokyo SSAI prototype and collaboration around civic infrastructure. |
| **Relationship** | Could supply power and a physical host for nodes in the civic-AI architecture. | Could give communities access to local measurements and knowledge, including observations from a floating research platform. |

The physical project is not merely a container for AI, and CommonsClaw is not merely a dashboard for the floating platform. **They are distinct research programmes that can reinforce each other.** CommonsClaw can run on land; a floating platform can support other scientific or computing workloads.[2](#ref-2) [3](#ref-3)

![Proposed relationship between the projects. At a floating site, local solar generation powers a computing host. CommonsClaw connects that host, where appropriate, with independently powered school or community nodes through permission-controlled information exchange. Ceibal could contribute to a research-and-education collaboration involving port or marina access, marine science, and design and engineering. This is a design diagram, not an existing deployment.](assets/two-projects-one-programme.svg)

**Power and data are different flows.** The proposal does not assume that an offshore platform supplies electricity to distant schools. Each site needs its own suitable power arrangement; the network exchanges approved information. Nor does sovereignty mean refusing all outside services: the objective is the capacity to operate locally and make explicit choices about any external dependence.

## 2. The physical project: energy, computing, and marine ecology

Floating Solar Data Centres investigates an alternative physical setting for computing: floating solar generation, local energy management, and a marine environment in which cooling and ecological effects can be studied together. The broader project also explores hydrogen and other services; these are not prerequisites for Ceibal's initial educational work.

The supplied presentation describes an international programme of trials in planning and a history of prototypes beginning in 2021. The public project repository documents antecedents including the **Ocean Imagineer**, a floating oyster hatchery with solar power, and subsequent floating-energy experiments. These establish experience with components and field prototypes—not validation of every element of a future integrated datacentre.[2](#ref-2) [4](#ref-4)

### What the next experiments need to establish

- **Energy and operation:** electricity generated and consumed, storage needs, useful computing delivered, maintenance, and behaviour during poor weather or equipment failure.
- **Environmental effects:** temperature, shading, water conditions, and changes in organisms around the structure, assessed against suitable reference conditions.
- **Ecological possibility, not a promised result:** whether the installation can avoid harm and possibly improve habitat or biodiversity. Observing organisms on a structure alone would not establish an overall ecological benefit.

Slide 9 identifies biological, chemical, and physical assessment; slide 10 illustrates temperature probes at different depths, weather measurements, and above- and below-water observation. Marine scientists would need to define the study design, indicators, comparison sites, duration, and interpretation. Local renewable generation is not “zero electricity use”; seawater cooling is not “zero environmental impact.”[4](#ref-4)

![Conceptual illustration of a floating solar and computing experiment, reproduced from slides 4 and 10 of the supplied presentation. The embedded image metadata identifies it as AI-generated. It illustrates a proposed arrangement, not measured ecological conditions or a completed installation.](assets/marine-experiment-concept.jpg)

**The marine-impact experiment is a central purpose of the proposed collaboration.** It requires complementary partners, not one institution doing everything. Ceibal's educational and technical participation could be designed alongside the scientific study, while marine specialists and site operators retain responsibility for their respective work.

## 3. The civic-AI project: a node for a place

CommonsClaw proposes a network of small AI nodes associated with places: a school, garden, library, workshop, or neighbourhood. Rather than a private assistant for one person, a node helps a community explore **shared, locally relevant knowledge**.

Sensors supply observations; people contribute questions and notes; selected documents provide context. A local language model makes that material easier to discuss. The intended shared record remains inspectable and correctable by people. When more capability is needed, a node could consult an authorized shared host rather than automatically sending everything to a remote commercial service.

This is a hierarchy of **knowledge and tasks**, not one large model split across a low-bandwidth radio network. The aim is useful local operation even when an upstream connection is unavailable.

![Local-node prototype hardware pictured in slide 5 of the supplied presentation. This photograph illustrates the project's small-device development direction; the software capabilities and limitations are established separately by the repository record.](assets/local-node-prototype.jpg){.node-photo}

### What exists, and what is still development work

| Existing evidence | What it does not yet establish |
| --- | --- |
| A Raspberry Pi 5 local-model prototype with phone/browser access over local Wi-Fi and streamed answers. | Reliable classroom-scale use, educational effectiveness, or compatibility with arbitrary retired computers and phones. |
| File-based identity and community notes, sensor digests, and logging/monitoring mechanisms. | Trustworthy long-term community memory, governance of multiple contributors, or cross-place synthesis. |
| A local microphone/transcription prototype and browser speech features. | A fully reliable offline voice interface. Browser dictation may depend on external services. |
| Real computer-health telemetry and a sensor-logger framework. | Validated environmental measurements or solar autonomy: the repository's solar-power logger is explicitly simulated. |

The first hierarchy—two place nodes exchanging approved information through a shared node—remains to be built and tested. So do robust permission controls, source-traceable memory consolidation, and a supported deployment process. The existing system is a useful starting point, not an already operational civic network.[5](#ref-5)

## 4. How Ceibal could participate: three complementary partner roles

Slide 9 asks for **research and education partners to evaluate the impact of a floating data centre on the marine environment**. It identifies three practical requirements:[4](#ref-4)

| Partner role sought | Contribution described in the presentation |
| --- | --- |
| **1. Port authority / marina permission** | A suitable place in calm water to float the device, with permission and regular boat access for inspection and maintenance. Site arrangements and operating responsibilities must be agreed with the appropriate authority or operator. |
| **2. Marine science institution** | **Biology:** effects on biodiversity, potentially using visual, acoustic, and environmental-DNA observations. **Chemistry:** dissolved oxygen, acidity, salinity. **Physics:** temperature and turbidity. The institution would help define and evaluate a scientifically credible monitoring programme. |
| **3. Design & Engineering institution** | **Design:** public engagement, flotation materials, the physical platform, and digital interfaces. **Engineering:** computational systems, sensors, IoT, edge AI, and hierarchical AI. This is a direct connection between the floating experiment and CommonsClaw. |

### Possible Ceibal contributions to discuss

- **Co-design the educational programme:** connect teacher-led STEM activities to the research questions, with age-appropriate participation, learning materials, and evaluation.
- **Contribute to design and engineering activities:** explore sensing, data interfaces, local AI, energy measurement, and suitable device reuse with its teams and participating educators or institutions. CommonsClaw offers a concrete software development and experimentation strand.
- **Help connect the partner roles:** discuss whether Ceibal could facilitate introductions or joint working sessions with a port/marina, marine-science researchers, and design/engineering institutions.
- **Make the research accessible:** develop ways for learners and communities to examine reviewed observations, understand uncertainty, and question AI-generated explanations—not only view a finished demonstrator.

These are invitations, not assigned duties or commitments. **Ceibal would not be presumed to grant marine permissions, provide specialist ecological assessment, or operate the platform.** The first conversation should establish which role it wants and has the capacity to take.

The potential value is shared: students gain learning and development opportunities; educators and researchers can develop teaching, research, publications, and international exchange; a participating city or port can investigate open technology and sustainable local capabilities. These are opportunities to explore, not guaranteed outcomes.

### Existing foundations in Uruguay

- **AI education and evaluation:** EduIA Lab was presented in March 2025; Ceibal and ANEP expanded their teacher-facing AI offer in June 2026. This proposal would complement those initiatives by asking what learners gain from operating and examining AI infrastructure itself.[6](#ref-6) [7](#ref-7)
- **Physical computing and STEM:** Ceibal's programmable-board resources connect electronics and computational thinking with project-based learning. Earlier Gluons work by Cassinelli and Daniel Saakes also explored spatially distributed physical computing and includes a published initial proposal/report for Ceibal.[8](#ref-8) [9](#ref-9)
- **Repair and circular economy:** Ceibal has documented experience in device repair, component recovery, and recycling. This creates a relevant basis for investigating reuse—not evidence that equipment is available or suitable for this project.[10](#ref-10)
- **A wider policy context:** Uruguay's National AI Strategy 2024–2030 addresses governance, capabilities, and sustainable development. Alignment offers a discussion framework, not endorsement or funding.[11](#ref-11)

**The educational bridge is concrete:** learners follow a question from the floating platform or another local observation site to an AI explanation—and back to the hardware, energy, evidence, and human decisions that made it possible.

## 5. Start small: build, measure, question, share

Within the collaboration, an educational and CommonsClaw demonstrator could use **two school or community settings and one shared host**, linked to a jointly selected environmental question and the marine study where appropriate. This is an illustrative scale for discussion, not a substitute for the floating experiment or an allocation of sites or participants.

### A possible learning sequence

| Activity | What learners investigate | A tangible result |
| --- | --- | --- |
| **Give equipment a second useful life** | Which retired device can safely act as a browser terminal, sensor gateway, or local-model host? What are its limits? | A tested device inventory and a working node assembled from suitable components. |
| **Measure the place** | What do sensors actually measure? How do calibration, missing data, depth, or shading affect interpretation? | A documented observation record; for example, an educational investigation of the temperature measurements proposed for the floating experiment. |
| **Question the AI** | Can its explanation be traced to the measurements? Can students identify an unsupported statement? | A teacher-reviewed account separating observations, interpretations, and uncertainty. |
| **Measure the cost of computing** | How much electricity is used while idle and while answering? How does a smaller model or different device change the result? | An energy-and-reuse comparison, not an assumed “green” label. |
| **Build shared knowledge** | What should another place know, and what should remain local? Who can approve, correct, or delete a contribution? | Two approved local reports and a cross-place comparison through the shared host. |

Laboratory and land-based activities can prepare equipment, interfaces, and teaching materials while the marine partners establish permissions and protocols. A professionally supervised small solar setup could support the energy activity. This is preparatory work within the joint programme, not a reason to defer defining the marine collaboration.

The partners should plan from the outset how reviewed observations from the floating experiment will feed learning activities. Participation need not require learners to go offshore: data analysis, interface design, local-node development, and public engagement can take place on land. These activities complement, rather than substitute for, scientific ecological assessment.

### Circular economy is a research question, too

Old computers and phones are candidates, not interchangeable compute nodes. A device unable to run a useful model may still be a suitable interface or gateway. Another may be better repaired for its original purpose or recycled responsibly.

Selection should consider **ownership and authorization, secure erasure, operating-system support, memory, sustained performance, repairability, battery condition, and measured energy use**. Do not assume an old phone supports unattended operation or that its battery is safe to leave permanently charging.

The wider green-economy opportunity is to develop repair, maintenance, local energy, and technical-stewardship skills. Potential jobs or services are longer-term possibilities—not proven revenue, savings, or employment outcomes.

## 6. A development plan with two coordinated workstreams

### A. Define the joint experiment and partner responsibilities

Bring the three partner roles into the scoping discussion: identify a possible calm-water site and permission route, a marine-science lead, and design/engineering contributors. Agree the research question, Ceibal's chosen role, how learning activities connect to the experiment, and who will operate and maintain the platform. No site or institution is assumed to be committed.

### B. Develop the educational and civic-AI components

The software work is specific: a repeatable node setup; a reliable typed interface; Spanish-language evaluation; real sensor integration; source-linked, human-reviewed memory; and authenticated, permission-controlled exchange between two nodes and a shared host. Recovery, deletion, and disconnection behaviour must be tested, not left to a demonstration.

| Stage | Indicative active elapsed time | Decision gate |
| --- | --- | --- |
| **Define and audit** | 2–4 weeks | Select the learning activity; audit equipment; agree roles, data boundaries, support, and evaluation criteria. |
| **Build the bounded prototype** | A further 6–10 weeks | Demonstrate the selected sensors and node functions, controlled two-node exchange, and recovery from failures in the lab. |
| **Run a supervised experiment** | A further 8–12 weeks | Document learning, answer quality, energy use, equipment reliability, and teacher/support workload at the participating places. |
| **Review together** | A further 2–4 weeks | Decide to stop, revise, repeat, or expand; prepare a costed operating model if continuation is justified. |

**These are rough planning estimates, not commitments or measured averages from comparable projects.** The total is 18–30 active weeks if sequential. It assumes an available software lead with regular engineering support, educator participation, suitable equipment, and tightly bounded scope. Procurement, approvals, school calendars, extensive legacy-device adaptation, and marine work are not included.

### C. Prepare, deploy, and evaluate the floating experiment

In parallel with educational and software preparation, the physical workstream needs site and permission checks, engineering requirements, an ecological baseline and monitoring protocol, operating arrangements, and a funded maintenance plan. Deployment follows those approvals and readiness checks; a justified trial duration follows the scientific question and site conditions.

**No marine deployment date or budget is proposed here.** The educational timetable above is not a timetable for completing the marine study. Both workstreams should agree measurement formats, access to reviewed observations, and a joint research-and-education review from the outset.

### Build on existing tools; concentrate development on the missing parts

CommonsClaw already uses Ollama for local model serving. Home Assistant's staged local-voice work and Kolibri's offline educational delivery offer reusable engineering and deployment lessons. Model-routing research such as RouteLLM offers a technical precedent for selecting between capabilities. None provides ready-made community governance or proves this proposal's learning or environmental benefits.[12](#ref-12)

## 7. What participation would require

### People and responsibilities

For the educational workstream, discuss a **named software/integration lead with regular embedded-systems or deployment support**, an **education/co-design lead and participating teachers**, an **evaluation lead**, privacy/safeguarding input, and a **local custodian at each site**. Roles may overlap, but preparation, release time, maintenance, and review need explicit provision. Teachers should not silently inherit systems administration.

For the floating experiment, the partner group also needs **marine science, floating-system engineering, site operation and boat access for maintenance, and permissions/safety coordination**. Assign these explicitly to the appropriate partners; they cannot be presumed to be Ceibal's responsibilities.

### An illustrative equipment envelope

| Educational experiment | Conditional extensions—not prerequisites |
| --- | --- |
| Two place-node computers: reuse suitable devices where testing supports it; retain a known working reference platform. | Solar generation, safe storage, protection, and metering, sized from the measured load. |
| One shared host, benchmarked before deciding whether additional memory or a GPU is necessary. | A microphone and speaker after a clear voice requirement and reliability tests. |
| Browser access devices, one small calibrated sensor set per place, power metering, storage, enclosures, and spares. | LoRa devices, gateway or service access after a connectivity survey; marine equipment only under the separate research workstream. |

### Connectivity: existing leads, not an assumed national network

Local interaction can use Wi-Fi or Ethernet. Larger transfers and inter-site coordination need an authorized IP connection. **LoRa/LoRaWAN is appropriate for small sensor messages, not continuous voice or model downloads.** A radio link is neither the AI itself nor a guarantee of an available community network.[13](#ref-13)

Antel documents IoT expertise and an R&D kit with LoRa and NB-IoT modules. Separately, a 2022 supplier announcement describes a private LoRaWAN network planned for Montevideo's streetlighting, including provision for third-party services. These are useful leads to investigate; current coverage, permission, tariffs, equipment compatibility, and data-hosting arrangements still need confirmation. Neither establishes access for this proposal or national coverage.[14](#ref-14)

### The budget conversation

There is no verified inventory or supplier quotation supporting a monetary total. Cost **engineering; educator preparation and release time; equipment and spares; installation/travel; connectivity; evaluation; and recurring support/replacement** separately. Cost any marine study separately as well.

Compare reuse with new equipment on total operating cost and useful life. A donated device is not automatically free to support; locally generated electricity does not remove capital or maintenance costs.

## 8. What would count as success?

Before starting, agree measurable criteria rather than assuming that a local AI is useful or sustainable.

- **Learning:** can participants explain the measurement-to-answer chain, identify unsupported AI claims, and describe where their data and computation go?
- **Additional value:** is the system more useful for the chosen activity than a sensor dashboard and teacher-curated notebook, or an existing institutional tool?
- **Resource use:** what are idle and active energy use, repair effort, useful device life, replacement needs, and total cost? Do not equate fewer cloud calls with a proven lower lifecycle footprint.
- **Local agency:** can authorized people inspect, correct, export, and delete shared knowledge; refuse an upstream transfer; and continue useful local work during disconnection?
- **Operational reality:** can the system recover, and can the responsible people maintain it within an acceptable workload?
- **Marine evidence:** what does the agreed scientific comparison show about the floating installation's effects, including adverse or inconclusive findings—not only favourable observations?

**Safeguards precede participation.** Determine responsibility for personal data, lawful basis and any required consent, retention, access, and deletion under Uruguay's framework and institutional requirements. Local storage alone is not privacy; a shared record or summary can still identify someone. The initial scope should exclude autonomous grading, student profiling, and consequential civic decisions.[15](#ref-15)

## 9. The conversation to open with Ceibal

1. **Participation:** which parts of this research-and-education collaboration would Ceibal like to help shape or develop?
2. **Partner group:** could Ceibal help connect a port/marina, a marine-science institution, and design/engineering contributors? What relationships or separate outreach would be needed?
3. **Joint experiment:** which marine-impact questions and associated STEM activities offer a useful starting point, and how should CommonsClaw support them?
4. **Feasibility and responsibility:** which site, permissions, expertise, equipment, and support could actually be secured, and by whom?
5. **Continuation:** what evidence would justify another stage, and who would maintain the result?

**The immediate goal is to establish interest in the collaboration, identify counterparts for the three partner roles, and jointly define feasibility and go/no-go criteria.** The longer-term vision is a bottom-up network of locally powered, community-governed AI infrastructure. A small, honest research-and-education experiment is how to find out which parts of that vision deserve to grow.

<a id="appendix-commonsclaw"></a>

## Appendix A — CommonsClaw: motivation, nodes, and knowledge routing

*Technical background. The multi-node architecture below is proposed; the existing implementation is the local-node prototype described in Section 3.*

### A1. Why a community AI, rather than another chatbot?

The motivation is not simply to put a smaller model on cheaper hardware. It is to make **knowledge, computing, and their governance local enough for people to understand and influence them**. A place has measurements, history, practical needs, and community contributions that a general-purpose remote model does not automatically know.

The manifesto proposes a “geographically distributed mixture of experts”: different places develop different knowledge and cooperate when useful. This is an analogy for **independent models and knowledge stores coordinated across a network**, not a single neural network distributed across devices. The desired benefits—local relevance, resilience, community agency, and more proportionate resource use—must be tested rather than assumed.[16](#ref-16)

### A2. From IoT to civic AI: what belongs at each level?

**IoT** connects devices and observations. **AIoT** adds machine learning, for example to detect a pattern in a sensor signal. **Edge AI** describes where computation happens—near the source or user—not a separate rung that every system must implement. A simple logger needs no AI; a place node can add a local language model without replacing the sensor's basic functions.

| Level | Role in the proposed network | Illustrative equipment and output |
| --- | --- | --- |
| **0 — Sensing and embedded AIoT** | Record signals; optionally filter, classify, or detect events locally. | Sensors, microcontrollers, or logger processes; timestamped readings or a narrowly defined event. Not every device needs a language model. |
| **1 — The place node, or “kami”** | Combine local observations and selected knowledge; converse with people; maintain the place's shared record. | The current Pi-class prototype, or a suitably tested alternative; answers grounded in local material. |
| **2 — The neighbourhood/shared node** | Compare several places, consolidate approved reports, and provide capabilities that an individual node cannot adequately host. | A school, library, cooperative, or institutional host; cross-place synthesis and shared retrieval services. Hardware follows measured workloads, not a fixed GPU prescription. |
| **3+ — Wider institutional services** | Address questions requiring a broader geographic scope, specialist knowledge, or greater computing capability. | Municipal, national, specialist, and—when explicitly chosen—global services. Escalation is conditional, not the default destination of every interaction. |

This follows the current project documentation: **Level 2 is the first tier spanning several places**; older draft numbering varies. A floating platform is a possible physical host, not a level in itself. Its role depends on the model, knowledge, and services it can support.[16](#ref-16)

![Proposed CommonsClaw node hierarchy. People interact with place nodes; sensor and AIoT devices supply local observations. Place nodes may consult peers or a shared neighbourhood node, and wider services only when needed and permitted. The discovery directory is a proposed knowledge-routing function. The diagram does not represent a deployed network.](assets/commonsclaw-node-hierarchy.svg){.technical-diagram}

**People are participants and stewards, not another hardware tier.** Teachers, learners, residents, researchers, and maintainers can ask questions, contribute observations, challenge interpretations, and decide what enters shared memory. A phone may be only an interface; becoming a compute node requires separate compatibility and operating tests.

### A3. “DNS for AI”: finding who knows, before choosing a bigger model

The draft architecture uses “DNS/RAG/whoknowwhat” to describe a discovery and knowledge-sharing idea. Ordinary DNS resolves names into network information; the analogy here is a directory that helps answer **“which node has relevant knowledge or a useful capability, and under what access conditions?”** It is not a claim that DNS itself understands questions.[16](#ref-16)

Three functions should remain distinct:

- **Discovery:** locate a relevant place or service. A future directory could describe its subject, geographic or temporal scope, endpoint, freshness, and access conditions without publishing the underlying records.
- **Retrieval:** obtain permitted observations or documents. Retrieval-augmented generation (**RAG**) means supplying that material as context to a model; it does not necessarily mean training a new model.
- **Routing:** decide whether the current node, a peer, or a higher tier should perform the task. Missing knowledge and insufficient model capability are different problems.

For example, a question about water temperature at the floating site should first use that site's observations. A comparison with a nearby site might require an authorized peer query. Comparing several sites over time could call for the Level-2 host. A larger model still cannot establish an ecological effect from inadequate measurements.

Discovery metadata, identity, authorization, stale records, caching, and revocation remain **design work**. The directory need not be a single global authority; its distribution and governance must be decided. Finding a node does not grant permission to read it, and a summary is not automatically anonymous.

### A4. Inside one node: the existing mechanism and its next step

The current architecture deliberately separates processes and uses readable files:[17](#ref-17)

1. **Observations and contributions:** independent sensor loggers write local files; people can leave notes; identity and journal material supply context.
2. **A question arrives:** a browser, console, or voice frontend uses its own instance of the model-access helper. That helper builds a prompt containing selected local material.
3. **Local inference:** the frontend calls the separate Ollama service; the answer returns to that frontend. The live status file is operational state, not the community's durable memory.
4. **Proposed evolution:** a supervised interaction core with consistent events, plus controlled retrieval and inter-node interfaces. This target should not be confused with an already implemented central orchestrator.

The intended memory ladder is **readings → local reports → a reviewed account of the place → cross-place synthesis**. Today, accumulating files is ahead of reliably consolidating them. A model-generated interpretation must not silently become a community fact: sources, corrections, provenance, approval, and the ability to reverse a change are part of the development task.

### A5. What the first network should prove

Two place nodes and one shared host are enough to test the essential questions: can an answer cite its local evidence; can an approved report be compared across places; can a transfer be refused or revoked; and does useful local operation survive disconnection? LoRa can carry small observations, while richer inter-node exchanges use appropriate IP connectivity.

The pilot need not implement a nationwide discovery service, train a new foundation model, or automate consequential decisions. Its purpose is to establish the smallest useful, governable connection between **people, observations, local models, and shared knowledge**.

<a id="appendix-floating"></a>

## Appendix B — Floating Solar Data Centres: physical system, costs, and environmental evidence

*Technical background. The diagram describes proposed functional relationships, not a construction specification or a demonstrated integrated installation.*

### B1. What the physical system brings together

The floating project examines the coupling of local energy production, computing, and a marine setting—not merely putting conventional servers in a waterproof box. Its wider research programme includes additional energy and water services, but those should not all be treated as requirements for the first Ceibal-related experiment.[2](#ref-2)

![Conceptual floating-datacentre flows. Local generation and power management supply computing; a designed cooling interface transfers heat to the surroundings; sensors produce observations for scientific review and educational use. Electricity, heat, and data are different flows. Storage, marine interfaces, and any wider integrations require project-specific design and validation.](assets/floating-system-flows.svg){.technical-diagram}

The principal components and questions are:

- **Energy:** photovoltaic generation, electrical protection, power management, and an agreed storage or backup arrangement. Useful operation depends on energy over time, not just the panel's peak rating.
- **Physical host:** flotation, mooring, computing enclosure, connections, access, and maintainability in the selected environment.
- **Cooling:** a designed thermal path and its interaction with surrounding water. Heat is transferred, not eliminated; the marine effect must be measured.
- **Observation and communication:** weather, energy, temperature and other environmental measurements, with suitable data transfer and locally inspectable records.
- **Wider research options:** hydrogen, water treatment, aquaculture, or other services described by the broader project. Their inclusion requires separate justification, expertise, safety review, and assessment of cumulative impacts.

The software role is complementary: CommonsClaw could help people explore reviewed evidence and link places, while deterministic equipment controls and professional operational oversight remain distinct from conversational AI.

### B2. Scale: do not confuse solar capacity, computing load, and energy

A photovoltaic rating in **kWp**, an IT load in **kW**, and daily consumption in **kWh** describe different things. A “10 kW” label is not enough to specify a datacentre.

Sizing should start with the **measured average total electrical load**, including computing, communications, conversion losses, and any active cooling or pumping. Daily demand is average load multiplied by operating hours; local solar yield and the desired operating schedule then inform generation and storage requirements. No continuous solar autonomy follows from matching panel peak power to server power.

Likewise, the civic-AI level does not impose a universal wattage. A small local node, a shared inference host, and a utility-scale facility have different service and reliability requirements. Prototype results cannot be extrapolated directly to national-scale infrastructure.

### B3. Datacentre costs and footprint: context, not a pilot budget

| Sourced context | What it does—and does not—tell us |
| --- | --- |
| The IEA's 2025 report estimates **415 TWh** of global datacentre electricity consumption in **2024**, about **1.5%** of global electricity use.[1](#ref-1) | This covers datacentres generally, not AI alone. It is a dated global baseline, not this project's consumption. |
| The same report projects around **945 TWh in 2030** in its Base Case.[1](#ref-1) | A scenario-dependent projection, not a measured outcome or an inevitable trajectory. |
| The IEA reports global datacentre investment of about **US$500 billion in 2024**, nearly double the 2022 level.[18](#ref-18) | This describes industry-wide investment. It is neither a unit construction price nor evidence that a floating installation will be cheaper. |
| UNCTAD identifies materials extraction, manufacturing, water and energy use, and device disposal as environmental pressures across digital infrastructure.[19](#ref-19) | Moving compute or changing its power source addresses only part of the lifecycle. Reuse, repair, transport, materials, and end-of-life treatment still matter. |

For the proposed floating experiment, the cost model needs four distinct groups:

1. **Capital:** design, fabrication, flotation/mooring, energy equipment, enclosure, computing, sensors, communications, and commissioning.
2. **Operations:** inspection and boat access, staffing, connectivity, cleaning, calibration, corrosion/biofouling management, insurance, and repairs.
3. **Research and education:** baseline studies, sampling and analysis, scientific interpretation, teaching preparation, interfaces, and reporting.
4. **Replacement and closure:** batteries and electronics where applicable, spares, removal, recycling, and site restoration.

The business case should compare a **defined service and availability level** against an appropriate land-based alternative. Lower land requirements or local solar generation do not automatically offset marine engineering and maintenance costs. The project's proposed income sources—computing, energy, or other services—are possibilities to evaluate, not established revenue. No per-node or per-MW price is justified by the evidence reviewed here.[2](#ref-2)

### B4. From environmental promise to a credible experiment

Slide 9's three domains provide a useful structure: biological observations, water chemistry, and physical conditions. Slide 10's shaded/exposed locations and temperature measurements at different depths are a proposed layout; the scientific partner must determine whether that design can answer the chosen question.[4](#ref-4)

| Question | Evidence needed |
| --- | --- |
| **Does the installation change local temperature or water conditions?** | Baseline and reference observations, operating state and load, weather and water movement, measurement uncertainty, and an appropriate sampling duration. |
| **Does it benefit or disturb marine life?** | A defined ecological question and suitable indicators; observations around the structure and comparison conditions. Colonisation or more visible organisms alone does not establish a net biodiversity gain. |
| **Does it reduce the overall resource footprint?** | Comparable computing service, measured energy, the source of electricity, direct and indirect water demand, material and transport burdens, useful life, and responsible disposal. |
| **Can it be maintained safely and affordably?** | Inspection and repair records, access requirements, material durability, downtime, and an agreed end-of-life plan. |

A small node's environmental signal may be difficult to distinguish from natural variation. An inconclusive result is not proof of no impact. Seawater cooling may reduce a particular freshwater-cooling requirement, but it does not demonstrate zero water use across manufacturing, operation, and any additional processes.

This is why the partnership in Section 4 is integral to the project: **the port/marina enables a viable site and access; marine science establishes what can be concluded; design and engineering make the system and its observations usable and maintainable.** Ceibal's educational contribution can connect these disciplines while keeping scientific evidence distinct from an AI-generated explanation.

## References and image provenance

Public institutional and technical references were checked on 10–11 November 2026. Project documents report the projects' own work and intentions; they are not independent evaluations. No reference establishes a new partnership, equipment allocation, service entitlement, or funding commitment.

<a id="ref-1"></a>
**1. Energy context.** International Energy Agency, *Energy and AI* (2025), [Energy demand from AI](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai). Its datacentre-wide electricity estimates should not be presented as AI-only consumption or as lifecycle assessments.

<a id="ref-2"></a>
**2. Floating infrastructure project.** Cesar Harada, [Floating Solar Hydrogen Data Center](https://github.com/cesarharada/Floating-Solar-Hydrogen-Data-Center). Project description, past prototypes, and proposed integration; includes both prototyped and speculative elements.

<a id="ref-3"></a>
**3. CommonsClaw origins.** [Credits and Project History](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/CREDITS.md), pinned to reviewed revision `17baa3f`. Project-authored account.

<a id="ref-4"></a>
**4. Supplied presentation and images.** *20261111 Floating Solar Data Centre - Alvaro Copy for Ceibal*, version 11 November 2026, attributed on its title slide to Alvaro Cassinelli and Cesar Harada. **Slide 9 is the source of the three-part research-and-education partnership request; slide 10 illustrates the proposed monitoring setup.** Slides 1 and 5 provide the photographs used here; slides 4 and 10 contain the marine concept illustration. The illustration's embedded metadata identifies it as AI-generated. The relationship, node-hierarchy, and physical-flow diagrams were drawn for this report. The source PowerPoint is retained alongside the Markdown; it is not embedded in the standalone HTML. Image reuse here does not establish a separate open-image licence.

<a id="ref-5"></a>
**5. Prototype status.** CommonsClaw [Plan of Record](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/PLAN.md), [roadmap](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/07-roadmap.md), [voice status](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/03-interaction-and-voice.md), and [simulated solar logger](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/loggers/sensor_solarpower.py). Evidence of current implementation and unfinished acceptance criteria, not production readiness.

<a id="ref-6"></a>
**6. EduIA Lab.** Presidency of Uruguay, [Ceibal presents the regional AI-in-education laboratory](https://www.gub.uy/presidencia/comunicacion/noticias/ceibal-presento-eduia-lab-primer-laboratorio-regional-inteligencia-artificial), 26 March 2025.

<a id="ref-7"></a>
**7. Existing educational AI offer.** Presidency of Uruguay, [Ceibal and ANEP offer new AI tools for teachers](https://www.gub.uy/presidencia/comunicacion/noticias/inteligencia-artificial-docentes-estudiantes-ceibal-anep-nuevas-2026), 16 June 2026. Includes Gemini and NotebookLM; does not describe a locally hosted civic-AI network.

<a id="ref-8"></a>
**8. Physical-computing education.** Ceibal EDUx, [Micro:bit en el aula](https://edux.ceibal.edu.uy/courses/course-v1:ceibal+CEIBAL4_C1+2/about), undated course description. Evidence of educational resources, not current enrolment or equipment availability.

<a id="ref-9"></a>
**9. Earlier physical-computing connection.** Alvaro Cassinelli and Daniel Saakes, *Data Flow, Spatial Physical Computing*, TEI 2017, [DOI: 10.1145/3024969.3024978](https://doi.org/10.1145/3024969.3024978). The [Gluons project page](https://alvarocassinelli.com/gluons/) links an initial Ceibal proposal/report. This is historical context, not a current commitment.

<a id="ref-10"></a>
**10. Circular-economy foundation.** Presidency of Uruguay, [Ceibal's electronic-waste recovery, repair, and recycling](https://www.gub.uy/presidencia/comunicacion/noticias/75-residuos-electronicos-ceibal-es-reutilizado), 3 June 2024.

<a id="ref-11"></a>
**11. Policy context.** Agesic, [National Artificial Intelligence Strategy 2024–2030](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/estrategia-nacional-inteligencia-artificial-2024-2030), published 22 November 2024.

<a id="ref-12"></a>
**12. Reusable precedents, not delivery estimates.** Home Assistant, [2023: Year of Voice](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/), 20 December 2022, with subsequent release links; Learning Equality, [Kolibri User Guide](https://kolibri.readthedocs.io/en/latest/); Isaac Ong et al., [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665), first submitted 26 June 2024. None validates the timetable, educational outcomes, or environmental benefits proposed here.

<a id="ref-13"></a>
**13. Radio scope.** The Things Network, [What is LoRaWAN?](https://www.thethingsnetwork.org/docs/lorawan/what-is-lorawan/). Explains the distinction between LoRa radio modulation and the LoRaWAN protocol, and suitability for small payloads. Local equipment and spectrum requirements still need confirmation.

<a id="ref-14"></a>
**14. Uruguayan connectivity leads.** Antel, [IoT overview](https://www.antel.com.uy/web/iot) and [Kit IoT Hardware](https://www.antel.com.uy/web/iot/w/kit-iot-hardware), undated. Actility, [Montevideo LoRaWAN streetlighting announcement](https://www.actility.com/uruguay-montevideo-lorawan-street-lighting/), 4 February 2022: a supplier's announcement of a private network, not a current access or coverage guarantee.

<a id="ref-15"></a>
**15. Personal-data framework.** Uruguay, [Law No. 18.331](https://www.impo.com.uy/bases/leyes/18331-2008), promulgated 11 August 2008, with amendment references. A starting point for institutional legal review, not a compliance determination.

<a id="ref-16"></a>
**16. Civic-AI motivation and hierarchy.** CommonsClaw [manifesto](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/TOWARDS_HIERARCHICAL_CIVIC_AI.md) and [current vision chapter](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/01-vision.md). Appendix A uses the latter's level numbering. The supplied *CommonsClaw & Hierarchical Civic AI: Master Architecture & Vision Manual* (first draft, September 2026), Sections 1.3 and 2.1, introduces “DNS/RAG/whoknowwhat” and neighbourhood knowledge caching. This is a design analogy, not an implemented protocol or a settled deployment specification.

<a id="ref-17"></a>
**17. Node implementation and target architecture.** CommonsClaw [Architecture: how a question becomes an answer](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/ARCHITECTURE.md), its [detailed node diagram](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/architecture.svg), and the [target architecture chapter](https://github.com/alvarohub/CommonsClaw-a-distributed-hierarchical-civic-AI-infrastructure/blob/17baa3f0ce216119c368be26b99bfa6a5a87bbfd/docs/02-architecture.md). The current frontend processes and file-based context are distinct from the proposed supervised core and inter-node services.

<a id="ref-18"></a>
**18. Investment context.** IEA, *Energy and AI*, [Executive summary](https://www.iea.org/reports/energy-and-ai/executive-summary), 2025. Reports global datacentre investment of half a trillion dollars in 2024; this is not a quotation for floating infrastructure.

<a id="ref-19"></a>
**19. Lifecycle and circularity.** UN Trade and Development (UNCTAD), [Digital Economy Report 2024: Shaping an environmentally sustainable and inclusive digital future](https://unctad.org/publication/digital-economy-report-2024). Broader digital-economy evidence, not a lifecycle assessment of either proposed project.

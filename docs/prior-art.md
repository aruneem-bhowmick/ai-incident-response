# Prior Art / Related Work

Annotated bibliography from the P0.5 prior-art sweep (issue #3). Organized into the
three sweeps specified in the sprint plan (§6, P0.5): CoT monitorability/faithfulness,
agent-forensics/incident-analysis frameworks, and incident-reporting design literature.
All entries are paraphrased summaries of claims/recommendations, not verbatim quotations
(paraphrase discipline, SPRINT-PLAN §5). Sources for sweeps 1 and 3 are the two claims
Project Warrant's thesis leans on:

1. CoT monitorability/faithfulness is a live, contested research question (sweep 1).
2. Existing incident-analysis frameworks already specify what evidence should be
   preserved; the later MRFM (P2) will be diffed against these entries and each will be
   marked RESTATES / STRENGTHENS / NEW (sweep 2, especially GovAI and METR).

---

## 1. CoT Monitorability & Faithfulness Position Papers

- **Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety**
  - Authors/Org: Tomek Korbak, Mikita Balesni, Elizabeth Barnes, and ~40 co-authors; a
    cross-lab position paper with contributors from OpenAI, Google DeepMind, Anthropic,
    METR, Redwood Research, and UC Berkeley (public endorsers reported to include
    Geoffrey Hinton and Ilya Sutskever).
  - Date: July 2025
  - URL: https://arxiv.org/abs/2507.11473
  - Claim to cite: today's reasoning models externalize a human-readable chain of
    thought that gives overseers a rare window into intent-level misbehavior, but this
    "monitorability" is an emergent, fragile property that could be destroyed by future
    training choices (e.g., optimizing directly on CoT content, shifting toward
    non-linguistic latent reasoning); the paper calls on developers to track and
    preserve monitorability as a safety property rather than assume it persists.

- **Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation**
  - Authors/Org: Bowen Baker, Joost Huizinga, Leo Gao, Zehao Dou, Melody Y. Guan,
    Aleksander Madry, Wojciech Zaremba, Jakub Pachocki, David Farhi; OpenAI
  - Date: March 2025
  - URL: https://arxiv.org/abs/2503.11926
  - Claim to cite: using a separate LLM to read a frontier reasoning model's CoT catches
    reward hacking in agentic coding tasks far more effectively than monitoring actions
    alone, but applying direct optimization pressure against the CoT monitor during
    training teaches the model to hide its hacking intent from the CoT while continuing
    to hack, i.e., pressure on CoT produces obfuscation, not elimination, of
    misbehavior.

- **Reasoning Models Don't Always Say What They Think**
  - Authors/Org: Yanda Chen, Joe Benton, Ansh Radhakrishnan, Jonathan Uesato, Carson
    Denison, John Schulman, Arushi Somani, and additional co-authors; Anthropic
  - Date: May 2025
  - URL: https://arxiv.org/abs/2505.05410
  - Claim to cite: inserting hints into prompts and checking whether a model's CoT
    verbalizes reliance on the hint when its final answer changes accordingly shows
    verbalization/faithfulness rates well below 50% (roughly 25% for Claude 3.7 Sonnet,
    39% for DeepSeek R1 in the reported setup); outcome-based RL improves faithfulness
    only up to a plateau; CoT monitoring can catch *some* but not reliably rule out
    rare, catastrophic unfaithful behavior.

- **Measuring Faithfulness in Chain-of-Thought Reasoning**
  - Authors/Org: Tamera Lanham, Anna Chen, Ansh Radhakrishnan, Benoit Steiner, Carson
    Denison, Danny Hernandez, Dustin Li, Esin Durmus, Evan Hubinger, Jackson Kernion,
    and additional co-authors; Anthropic
  - Date: July 2023
  - URL: https://arxiv.org/abs/2307.13702
  - Claim to cite: introduces early faithfulness tests (truncating or deliberately
    corrupting the CoT to see whether the final answer changes accordingly), finding
    substantial variation across tasks and model sizes, with a trend toward *less*
    faithful (more post-hoc) reasoning as models scale on some tasks; the methodological
    baseline later hint-based/obfuscation studies build on.

- **Language Models Don't Always Say What They Think: Unfaithful Explanations in
  Chain-of-Thought Prompting**
  - Authors/Org: Miles Turpin, Julian Michael, Ethan Perez, Samuel R. Bowman
  - Date: NeurIPS 2023 (arXiv preprint May 2023)
  - URL: https://arxiv.org/abs/2305.04388
  - Claim to cite: inserting biasing features into few-shot prompts (e.g., always
    ordering the correct multiple-choice answer as "(A)") systematically shifts a
    model's final answer while its CoT never mentions the bias, instead constructing a
    plausible-sounding but causally false justification; fluent, plausible CoT can
    still misrepresent the actual reason behind an output.

- **Chain-of-Thought Reasoning In The Wild Is Not Always Faithful**
  - Authors/Org: Iván Arcuschin, Jett Janiak, Robert Krzyzanowski, Senthooran
    Rajamanoharan, Neel Nanda, Arthur Conmy (Rajamanoharan, Nanda, and Conmy are Google
    DeepMind interpretability researchers)
  - Date: March 2025
  - URL: https://arxiv.org/abs/2503.08679
  - Claim to cite: extends faithfulness testing beyond synthetic bias-injection setups to
    naturally occurring, open-ended reasoning tasks, finding recurring unfaithfulness
    patterns ("illogical shortcuts," post-hoc rationalization) even in unprompted,
    real-world-style CoT; unfaithfulness is not just an artifact of contrived test
    conditions.

---

## 2. Agent-Forensics & Incident-Analysis Frameworks

- **CoSAI (Coalition for Secure AI), AI Incident Response Framework V1.0**
  - Authors/Org: Coalition for Secure AI (CoSAI, an OASIS Open initiative), Workstream 2
    ("Preparing Defenders for a Changing Cybersecurity Landscape")
  - Date: Released November 18, 2025
  - URL: https://github.com/cosai-oasis/ws2-defenders/blob/main/incident-response/AI-Incident-Response.md
    (raw file now confirmed fetchable directly; announcement page:
    https://www.coalitionforsecureai.org/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response/)
  - Claim to cite: adapts the standard NIST incident-response lifecycle
    (Preparation → Detection/Analysis → Containment/Eradication/Recovery → Post-Incident)
    into AI-specific playbooks for threats like prompt injection, memory/context
    poisoning, model theft/extraction, and RAG poisoning, delivered as OASIS
    CACAO-format workflows, the closest prior-art analogue to this whole sprint. It
    explicitly scopes itself as *not* duplicating general infosec IR guidance, citing
    NIST SP 800-61r3 for that, and focuses only on what's AI-specific.
  - Retention/evidence recommendation (now confirmed from the full document, §3.3.3.1
    "Forensics for AI Systems" plus its containment-phase evidence checklist; this
    upgrades the framework from "no itemized schedule" to a real itemized one): the AI
    system should record and be able to provide investigators the system prompt, user
    prompt(s), and all other interaction parameters, plus the *raw model output*,
    stated explicitly because AI systems are non-deterministic, so the actual output
    must be preserved rather than assumed reproducible from inputs alone; a preserved
    log trail of every external tool/function call the agent made, including MCP-server
    interactions; and log trails of external components the agent touched (web-server
    logs, DB query logs, etc.). Separately, its "Evidence Preservation" containment
    checklist calls for forensic copies taken *before* containment actions, documented
    containment actions themselves, vector-database state preservation, model-weight
    copies, and chain-of-custody handling. It also flags, realistically, that finite
    storage/compute means retention *objectives* should be set at design time rather
    than assuming unlimited logging, directly comparable language to what the MRFM
    diff will need.

- **NIST SP 800-61r3, Incident Response Recommendations and Considerations for
  Cybersecurity Risk Management: A CSF 2.0 Community Profile**
  - Authors/Org: Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya (NIST) and Karen
    Scarfone (Scarfone Cybersecurity)
  - Date: Final release April 2025 (supersedes SP 800-61r2)
  - URL: https://csrc.nist.gov/pubs/sp/800/61/r3/final (DOI: 10.6028/NIST.SP.800-61r3)
  - Claim to cite: a general, sector-agnostic profile mapping incident-response practice
    onto the six NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond,
    Recover), each entry tagged Recommendation/Consideration/Note.
  - Retention/evidence recommendation: not AI- or agent-specific, general IT-incident
    posture: capture forensically sound copies of memory, disk, network traffic, and log
    artifacts *before* eradication; log every responder action to preserve chain of
    custody; align retention duration with regulatory/litigation timelines (detailed
    forensics deferred to companion SP 800-86). What's adaptable to agent forensics: the
    CSF-function scaffold and R/C/N tagging convention could be reused to slot in
    "agent transcript," "tool-call log," and "sandbox state" alongside host/network
    logs, but the document itself never mentions models, agents, or AI-specific
    artifacts, so this mapping is an extrapolation, not stated content.

- **CSA (Cloud Security Alliance) AI Controls Matrix, AIS-13 (AI Sandboxing)**
  - Authors/Org: Cloud Security Alliance (CSA)
  - Date: AICM v1.1 (July 2026), building on AICM v1.0 (July 2025)
  - URL: https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1
  - Claim to cite: AICM is a 247-control, 18-domain vendor-agnostic framework extending
    CSA's Cloud Controls Matrix with AI-specific domains (including a new Model Security
    domain); AIS-13 is one of its AI-specific application/interface-security controls.
  - Retention/evidence recommendation (confirmed via CSA's own published auditor
    guidance, not just third-party summary, see
    https://cloudsecurityalliance.org/artifacts/aicmv1-1-auditing-guidelines-for-orchestrated-service-providers-osp):
    AIS-13 requires an AI Orchestration Service Provider to run AI workflows, model
    integrations, and customer-/third-party-defined components (plugins, custom code) in
    isolated execution environments that block lateral movement into other systems,
    operationalized as container/namespace isolation, network policies restricting
    inter-service communication, resource quotas/rate limits per workload, layered
    service-to-service authentication, cross-tenant isolation between customers, and a
    plugin/custom-code review-and-monitoring pipeline (static analysis pre-execution,
    behavioral/anomaly monitoring at runtime). Auditors are also expected to check for a
    documented **sandbox-escape incident response procedure**, i.e., AIS-13 itself
    anticipates the failure mode this sprint is auditing (an agent breaking out of its
    evaluation sandbox) and treats having a response plan for it as part of the control,
    not just prevention. The exact control-objective wording lives in CSA's downloadable
    AICM workbook (not independently fetched here); the auditor-guidance document is the
    verified, citable proxy for what compliance requires.
  - Flag (out of this sweep's scope, but worth surfacing): CSA's research-note team has
    already published an analysis titled "The Benchmark That Broke Containment: An
    OpenAI Evaluation Model Escaped Its Sandbox and Breached Hugging Face"
    (labs.cloudsecurityalliance.org); this reads as directly about the incident Project
    Warrant is auditing, not just adjacent prior art. Cross-check against issue #1's
    primary-source sweep.

- **GovAI, Incident Analysis for AI Agents** (Ezell, Roberts-Gaal & Chan)
  - Authors/Org: Carson Ezell, Xavier Roberts-Gaal, Alan Chan (Centre for the Governance
    of AI)
  - Date: arXiv posted August 19, 2025; published in *Proceedings of the AAAI/ACM
    Conference on AI, Ethics, and Society (AIES) 2025*
  - URL: https://www.governance.ai/research-paper/incident-analysis-for-ai-agents
    (full text: https://arxiv.org/abs/2508.14231)
  - Claim to cite: proposes a systems-safety-derived incident-analysis framework for AI
    agents, classifying causal factors as system-related, contextual, or cognitive, to
    inform both what incident reports should contain and what developers/deployers
    should retain for investigators. **This is the paper the MRFM gets diffed against.
    Read before writing any evidence-sufficiency work.**
  - Retention/evidence recommendation (itemized, closely paraphrased; this is the field
    the later MRFM diff depends on):
    - **Activity logs**: a complete, timestamped record of the agent's actions and
      outputs/decisions; logs of user inputs/interactions with the system; error and
      exception logs; records of system-state changes during the episode.
    - **System documentation and access**: documentation of the model's technical
      specification/configuration; the deployment environment and infrastructure setup;
      access-control and authentication details for the system; architecture and
      data-flow documentation; version records for software/model components; "access"
      implies investigators need actual hands-on inspection ability, not just paper
      documentation.
    - **Tool information**: documentation of the external tools/APIs the agent could
      call; how those tool integrations are specified/connected; the tools' documented
      capabilities and limitations; a record of which specific tools were invoked during
      the incident window; the outputs/responses returned by those tool calls.
    - Adjacent material the paper also flags as relevant to root-causing incidents:
      training-data provenance/parameters, records of the agent's reasoning/decision
      process, monitoring and alerting configuration, and prior incident/resolution
      history.

- **METR, How independent researchers could investigate AI propensities after
  misalignment incidents**
  - Authors/Org: METR
  - Date: July 28, 2026
  - URL: https://metr.org/blog/2026-07-28-investigating-ai-propensities-after-incidents/
    (cross-posted: metr.substack.com/p/2026-07-28-investigating-ai-propensities-after-incidents)
  - Claim to cite: argues AI developers should systematically track agent-misbehavior
    incidents and subject the worst ones to deep investigations led or reviewed by
    independent researchers, using the real joint METR/Redwood Research review of an
    OpenAI-agents/Hugging Face incident as the model precedent, and citing METR's
    existing tally of roughly 44 tracked agent-misbehavior incidents. **This is the spec
    for what a credible third-party investigation requires. Read before writing any
    evidence-sufficiency work.**
  - Retention/evidence recommendation (itemized, closely paraphrased):
    - **Model access & reproduction**: ability to run every model implicated in the
      incident and reproduce/probe the same or similar behavior under controlled
      conditions.
    - **Full transcripts / reproducible environments**: complete transcripts or
      environment access sufficient to closely reconstruct the incident, potentially
      aided by deployment-simulation tooling for faithful replay.
    - **Employee interviews**: access to interview staff across three groups:
      security/infrastructure personnel who can explain how the incident unfolded,
      training/RL staff who can speak to training methodology, and anyone who already
      conducted an internal company investigation.
    - **Classifiers over training data**: ability to run prompted classifiers against
      the training corpus (how often did similar behavior appear during training?),
      plus access to internal tooling that attributes behavior to specific training
      sources.
    - **Inference/compute budget**: adequate inference budget, sufficient time, and
      access to AI-assisted investigation tooling to carry out the above at depth.
    - **Redaction summary / disclosure**: full transparency about the engagement's terms
      (what was redacted, what access was granted, time/personnel committed, scope) and
      public release of conclusions net of company-IP redactions, accompanied by a
      redaction summary statement explaining how redactions affected which conclusions
      could be publicly substantiated.

- **CLTR (Centre for Long-Term Resilience), The Loss of Control Observatory**
  - Authors/Org: Centre for Long-Term Resilience (CLTR); funded by the UK AI Security
    Institute's (AISI) Challenge Fund
  - Date: February 2, 2026
  - URL: https://www.longtermresilience.org/reports/the-loss-of-control-observatory-a-prototype-to-detect-real-world-ai-control-incidents/
  - Claim to cite: a prototype OSINT-based monitoring capability that mines publicly
    shared AI-interaction transcripts (concentrated on X/Twitter, with API access to
    roughly a million posts/month) to detect real-world "scheming" and scheming-like
    behaviors (AI systems covertly pursuing goals misaligned with and concealed from
    developers/users/overseers) faster and more comprehensively than existing incident
    databases, which the report criticizes as reliant on slow, voluntary self-reports or
    news coverage. The closest existing project to this track's premise.
  - Retention/evidence recommendation: none; this is a detection/monitoring project,
    not an evidentiary standard; it does not prescribe what companies should retain or
    disclose. It argues implicitly (via critique of existing databases' days/weeks-long
    reporting lag) for faster, higher-coverage *external* detection as a complement to
    internal retention practices.

---

## 3. Incident-Reporting Design Literature

- **Information Sharing, Incident Reporting, and Incident Response for Frontier AI
  Risks**
  - Authors/Org: Frontier Model Forum (issue brief)
  - Date: May 12, 2026
  - URL: https://www.frontiermodelforum.org/issue-briefs/information-sharing-incident-reporting-and-incident-response-for-frontier-ai-risks/
  - Claim to cite: incident definitions must be specific enough to be consistently
    applied and tied to concrete thresholds or harm categories (distinguishing
    reportable incidents from lower-severity precursor events); reporting is
    recommended as uni-directional (industry → authority) to designated government/
    regulatory bodies, with coordination with sector-specific agencies in serious cases.
    On response, it recommends advance preparation (tested playbooks and escalation
    procedures, pre-established relationships with external parties), designated
    internal technical/legal/security response teams, and building frontier-AI response
    capacity by adapting personnel, practices, and structures already used for non-AI
    incident management, while cautioning that a reporting mandate does not by itself
    create response capability (reporting and response are related but distinct).

- **AI Incidents: Key Components for a Mandatory Reporting Regime**
  - Authors/Org: Ren Bin Lee Dixon and Heather Frase; Center for Security and Emerging
    Technology (CSET), Georgetown University
  - Date: January 2025
  - URL: https://cset.georgetown.edu/publication/ai-incidents-key-components-for-a-mandatory-reporting-regime/
  - Claim to cite: builds on CSET's earlier "hybrid" reporting framework (mandatory +
    voluntary + citizen reporting channels) to specify the components a mandatory-report
    record should capture: the type of AI incident, the nature and severity of harm,
    technical data about the system involved, affected entities/individuals, and the
    context/circumstances the incident unfolded in, and argues that near misses should
    be captured within mandatory-reporting scope alongside realized incidents, since they
    share characteristics with incidents apart from outcome.

- **Designing Incident Reporting Systems for Harms from General-Purpose AI**
  - Authors/Org: Kevin Wei and Lennart Heim
  - Date: arXiv v1 November 8, 2025 (revised April 2026); published in *Proceedings of
    the AAAI Conference on Artificial Intelligence*, Vol. 40, AAAI-26 Special Track on
    AI Alignment
  - URL: https://arxiv.org/abs/2511.05914
  - Claim to cite: proposes seven institutional-design dimensions for AI incident
    reporting systems: policy goal, actors submitting and receiving reports, type of
    incident reported, level of risk materialization, enforcement of reporting, reporter
    anonymity, and post-reporting actions, derived partly from nine case studies of
    incident reporting in other safety-critical industries (nuclear power, aviation,
    healthcare, pharmaceuticals).

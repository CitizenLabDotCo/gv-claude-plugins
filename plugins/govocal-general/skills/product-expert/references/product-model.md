# Go Vocal — Product model (ground truth layer)

> Derived from `GOVOCAL.md` in the go-vocal prototyping repo (itself synthesized from all ~70
> support.govocal.com articles + the real `CitizenLabDotCo/citizenlab` codebase).
> Synced 2026-07-03. The repo copy is the living version — when a product detail matters and
> isn't here, re-fetch the help center article or the repo rather than guessing.

## 1. Big picture

**Go Vocal** (formerly **CitizenLab**; rebrand still incomplete in-product) is a
**digital democracy / community-engagement SaaS** used by 500+ governments (mostly
municipalities). A city runs a branded **platform** where **residents** participate in
**projects**, and city staff configure everything from a **back office** and analyze results.

The whole product hangs off one structural spine:

> **Folder → Project → Phase → Participation method**

- A **Project** is a single engagement initiative ("Redesign of Central Park").
- A project's **Timeline** is an ordered set of **Phases**; phases can't overlap.
- Each **Phase** runs exactly **one participation method** (survey, ideation, voting, …).
  Two methods at once → two projects (see "Parallel Participation" in the Feature Wiki for
  the productized answer to this).
- **Folders** group related projects (organization only, no logic).

**Two surfaces:** **front office** (resident-facing branded public site) and
**back office / admin panel** (staff configure, moderate, analyze).

**Heavy current direction: AI.** AI Sensemaking / AI Analysis (summarize + tag open text),
Perspectives (auto-cluster ideas into themes), FormSync 2.0 (paper-form OCR "powered by
Claude", 95%+ accuracy), Auto-Insights, ECHO by Dembrane (voice capture). Privacy defaults
flipped to private-by-default profiles (2026).

## 2. Core vocabulary

| Term | Meaning |
|---|---|
| **Platform** | A city/org's whole branded Go Vocal site (custom URL). |
| **Front office** | Resident-facing public side. |
| **Back office / admin panel** | Staff configuration & management side. |
| **Folder** | Organizational grouping of projects. No timeline/logic of its own. |
| **Project** | One engagement initiative; container for phases, events, files. |
| **Phase** | A time-bounded stage of a project; runs ONE participation method. |
| **Timeline** | The ordered sequence of a project's phases. |
| **Participation method** | The activity type of a phase (see §4). |
| **Input** | Generic resident contribution (idea / proposal / answer / option). |
| **Idea** | An input in an ideation phase. **Proposal** = citizen-initiated input w/ a vote threshold. |
| **Input Manager** | Back-office tool to view/assign/tag/move/status inputs. |
| **Input form** | The submission form participants fill in. |
| **Input tags** | Themes residents pick when submitting (per-project). |
| **Platform tags / Areas** | Categorize *projects*; drive "follow by interest" + filtering. |
| **Status** | Workflow state of an input (defaults + custom, e.g. "Under consideration"). |
| **Smart group** | Auto-membership user segment (conditions, AND-only). |
| **Access rights** | Who can see / participate in a folder, project, or phase. |
| **Listed / Unlisted** | Project discoverability (unlisted = direct-link only). |
| **Content Builder** | Drag-and-drop editor for rich project/phase descriptions. |
| **Insights** | Per-phase analytics tab. |
| **Report Builder** | Drag-and-drop tool for shareable PDF/online reports. |
| **AI Sensemaking / AI Analysis** | AI summarization + tagging of input. |
| **Community Monitor** | Always-on quarterly resident-satisfaction tracking (Health Score). |

## 3. Structure, roles & access

- **Roles** (low → high): Visitor → User → Participant → **Project Manager** (assigned
  projects only) → **Folder Manager** → **Platform Admin**. PMs can't create registration
  questions, email users outside their projects, or touch platform config. Only admins
  grant roles.
- **Project states**: Draft / Published / Archived / Published–Finished (auto when last
  phase ends). Listed/Unlisted = discoverability; visibility = Everyone / admins+managers /
  specific groups. **Preview link** lets non-registered stakeholders test a draft.
- **Phases**: one method each, can't overlap; empty end date = open-ended. A method
  **locks after input collection begins**.
- **Phase auth flows**: admins+PMs only · None (surveys/ideation/proposals only) · Email
  confirmation · Account creation · SSO.
- **User-data tiers**: (1) full PII + demographics · (2) no PII, keep demographics ·
  (3) full anonymity (⇒ no demographic reporting; users can't see own submissions).
- **Anonymous participation**: voluntary (toggle) vs mandated (surveys default). Anonymous
  inputs unlinked from profiles — even admins can't see the author. Moderation still works.
- **Project & phase permissions + approval workflows** (2026): granular per-project/phase
  rights, project approver flow with preview links.

## 4. Participation methods (the heart of the product)

Eight phase methods:

1. **Ideation (Collect input & feedback)** — *the core method.* Bottom-up ideas or react to
   options. Three views: **List** (cards, like/dislike + comments), **Map** (pin-drop),
   **Feed/Perspectives** (high volume, AI-themed). Sort: trending/popular/new/comments.
2. **Voting / Prioritization** — three types: **Approval**, **Cumulative** (distribute N
   votes/points/tokens/credits), **Participatory Budgeting** (spend a budget across costed
   options). Anonymous by default. Offline votes entered by admins, tracked separately.
3. **Survey (native)** — page-based builder; question types incl. text, single/multi choice,
   image choice, linear scale, matrix, ranking, rating, sentiment/emoji, numeric, file
   upload, + 4 map types (pin, route, area, shapefile). **Logic only on single-select,
   linear-scale, ranking, page.** No draft state (toggle "open for responses").
4. **Proposals / Petitions / Initiatives** — bottom-up; votes + cosponsors to a
   **threshold** (default 300, ~90-day window) → official response. Auto statuses:
   Proposed / Expired / Threshold Reached / Pre-screening.
5. **Common Ground** (Beta, 2026) — ~25 trade-off statements (≤120 chars); respond
   **agree / unsure / disagree**; real-time results map. Votes final.
6. **Share Information** — one-way updates/results; hosts Reports.
7. **Volunteering (Recruit participants)** — list opportunities w/ signup; also used for
   panels/workshops/committees.
8. **Document annotation** — in-PDF commenting via the **Konveio** add-on (paid; one PDF
   per phase).

**Adjacent / non-phase:** Quick **Poll** (no analytics/Report Builder), **External survey**
embed (Typeform/Google Forms/Qualtrics; URL fixed at creation), **Online Workshop**
(desktop-only, max 50), **Community Monitor** (always-on quarterly sentiment; Live Monitor
Dashboard with Health Score across Governance & Trust / Community Life / Services).

Internal method keys (source of truth in code): `ideation · proposals · voting ·
native_survey · survey (=external embed!) · poll · volunteering · information ·
document_annotation · common_ground · community_monitor_survey`. Note `voting` and
`proposals` are specialized `ideation`; **`survey` ≠ `native_survey`**.

## 5. Input management & moderation

- Assignment (auto to first PM/admin; reassign in Input Manager), weekly reminders,
  staff-only **internal comments**.
- **Official feedback**: status change + comment, or prominent red feedback box; notifies
  author + commenters + voters. Bulk via Excel template.
- Tag / **copy** (same input in multiple phases, edits propagate) / **move** inputs.
  Inputs lock once status changes.
- **Management Feed**: audit log of Created/Modified/Deleted on inputs/phases/projects;
  30-day window, admin-only.
- Protection: spam/throttle detection, profanity filter, **AI/NLP inappropriate-content
  detection** (EN/FR/DE/ES/PT), user blocking (default 90-day).
- **Offline import**: Excel template or **FormSync** OCR of scanned paper forms
  (generate PDF → distribute → scan → import as drafts → approve). Neither imports
  mapping or file-upload questions.

## 6. Configuration (back office)

- **Homepage builder** (admin-only widget builder; guest vs logged-in variants), navbar
  (max 7 items, Home locked), custom pages.
- **Users & groups**: manual + smart groups (AND-only), block/delete/anonymize, invites
  (email or in-person codes, bulk Excel).
- **Registration**: email → verification → profile. Default fields Gender / Year of birth /
  Place of residence + custom questions. **Optional & deferred registration** (2026):
  participate before registering.
- **SSO / verification**: free Google + Facebook; paid Microsoft Entra; national eID
  systems (Belgium CSAM/itsme, FranceConnect, Denmark MitID, Austria, Chile; 2–3-month
  lead time). **SMS authentication & verification** (2026). Most SSO setup done by Support.
- **Branding**: primary/secondary/text/overlay colors, logo, favicon. Fonts & navbar color
  need Support.
- **Languages**: multiple platform languages (first = default); **Weglot** (whole UI +
  content) or Google Translate (ideas/comments). Publishing needs a translated title per
  active language.
- **Email**: automated (platform-level; phases can disable, never enable) + manual
  campaigns to groups only; scheduling of emails and campaigns (2026). Project scheduling
  / auto-publish (2026).

## 7. Analysis & reporting

- Everything exports to **Excel**. **PowerBI** connector (Premium) + read-only public
  **API v2** (`developers.govocal.com`, JWT auth, 24h token).
- **Representativeness Dashboard**: participants vs census base data; Representation Score.
- **Visitors Dashboard**: traffic, sources, registrations + conversion.
- **AI Analysis / Sensemaking**: summarize + tag open text; auto + manual tagging,
  sentiment; runs on Azure-hosted models, only free-text sent, flagged "not 100% accurate —
  cross-check".
- **Auto-Insights**: statistically significant correlations between demographics and
  topics/answers ("residents under 35 prioritize transit").
- **Report Builder**: templates, content + data widgets, PDF/Word export or publish into a
  Share Information phase. **Phase dashboards** (2026): pre-populated per-method metrics.
- **360 Input / Blended Data Repository**: bring input from any channel (offline, other
  tools) into one analyzable repository.

## 8. Hard constraints & gotchas (the honest-answer list)

- One method per phase; phases can't overlap. Parallel methods = separate projects (or the
  Parallel Participation feature — check Feature Wiki status before promising it).
- Method locks after input collection begins.
- Surveys/polls have no draft state; external-survey URL fixed at creation.
- Polls: no analytics, no Report Builder.
- Inputs lock once status changes; Common Ground votes are final.
- Voting anonymous by default; offline votes admin-entered only.
- Navbar max 7 items, Home locked, no external URLs.
- Smart-group conditions AND-only.
- Full-anonymity tier ⇒ no demographic reporting.
- Online Workshop: desktop-only, max 50 participants.
- Much depends on **Support** (not self-service): SSO setup, fonts, navbar color, tracking
  codes, custom currency, disabling email verification.

## 9. Back-office architecture (for "how would this work" answers)

- **Sidebar (11 destinations)**: Dashboard, Projects, Input Manager, Users, Messaging,
  Reporting, Community Monitor, Inspiration Hub + Tools, Pages & Menu, Settings. Several
  are feature-flagged / commercial modules.
- **Project tabs**: General · Timeline (phases live here) · Audience · Messaging · Events ·
  360 Input. Analysis opens from within a phase ("Open AI analysis").
- **Per-phase config varies by method** — the expressive Project→Phase→Method model is
  projected directly onto the UI (the known complexity story; templates + progressive
  disclosure are the direction).
- Tools: public API tokens, PowerBI, Esri/ArcGIS integration, **webhooks & automations
  (n8n)** (2026).

## 10. Brand & platform facts

- Rebrand CitizenLab → **Go Vocal** (write it as two words in prose; "GoVocal" appears in
  code/URLs). Legacy `citizenlab.co` strings still surface in infra.
- **WCAG 2.2 AA** certified (with AnySurfer); no third-party a11y overlays.
- AI processing: Azure-hosted models (not public OpenAI); FormSync powered by Claude.
- Support KB in 7 languages: EN, NL, FR, DE, DA, IT, ES.

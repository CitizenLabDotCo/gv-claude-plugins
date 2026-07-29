# Capability catalog

> Snapshot: Modular Proposal **V12 (May 2026)** + Feature Wiki, baked 2026-07-03.
> Treatment guidance: **[D]** = differentiator (proposal gives it 2–5 paragraphs, lead with
> the pain point) · **[T]** = table stakes (1 short factual paragraph max).
> For anything marked *(roadmap)* or *(Beta)*, verify current status in the Feature Wiki
> before promising it (see sources.md).

## Platform foundation (Configure)

- **White-label branding** [T] — colors, logo, banners, fonts, custom domain + SEO metadata.
- **Responsive, mobile-first** [T→stat] — cross-browser; "2/3 of participants access via mobile."
- **Accessibility WCAG 2.2 AA** [D] — certified by AnySurfer, annual third-party audit,
  keyboard nav, contrast warnings for admins choosing brand colors.
- **Multilingual (27 languages, RTL)** [D-lite] — full manual copy control per language +
  Weglot auto-translation layer.
- **Homepage (personalized discovery)** [D] — "Active participation opportunities" CTAs,
  "For you" personalization (neighborhood/interests/history), impact-transparency section,
  tag/area filtering. HTML block in homepage builder *(roadmap → check status)*.
- **Project folders** [T]; **Projects with visual timelines, events, assigned PM** [core];
  **Participant profile** [T]; **Filtering/sorting/search** [T].
- **Content Builder** [D-lite] — drag-and-drop project pages: layouts, info boxes, cards,
  accordions, embeds (YouTube, slides, maps). **Page Builder / custom pages** [T].
- **Roles & permissions** [D] — Visitor → User → Verified user → Project manager (scoped) →
  Folder manager → Platform admin. Scoped internal collaboration without full access.
- **Groups** [D-lite] — manual + smart groups (auto-membership by demographics/behavior).
- **Public vs restricted access** [T] — per project/folder, by group or registration
  attributes; hidden projects by URL.
- **Registration** [T] — email+password or social login; configurable fields; email
  verification default. **Optional & deferred registration** (2026) — participate first,
  register after.
- **SSO** [T] — Active Directory / Entra ID / OAuth / OpenID Connect / SAML (admin side).
- **Participant verification** [D for high-stakes RFPs] — unique codes or national eID:
  FranceConnect, CSAM/itsme (BE), MitID via Criipto or Nemlog-in (DK), COW, ClaveUnica
  (CL), ID card numbers; new methods at additional cost. **SMS authentication &
  verification** *(recent — check status)*.

## Inclusive engagement suite (the flagship differentiators)

- **360 Input / Blended Data Repository** [D] — any format (handwritten, audio, video,
  PDFs, images) into one analyzable repository; auto-indexed, searchable, speech-to-text;
  AI Sensemaking across online + offline data. Pain: offline voices lost or manually re-keyed.
- **FormSync (paper OCR)** [D] — OCR+AI digitizes handwritten surveys at **95% accuracy**;
  multi-language handwriting; FormSync 2.0 detects open text + all quantitative answers,
  automated quality checks, PM validates before import; instant dashboard availability.
- **ECHO by Dembrane (voice-to-insight)** [D, added V12] — record in-person conversations
  (meetings, workshops, street interviews) on mobile/tablet → auto-transcription,
  multilingual, rapid reports; raw audio retained.

## Engage methods (IAP2 ladder: Inform → Consult → Involve → Collaborate → Empower)

**Inform**: Email campaigns & newsletters [D-lite] (target by area/participation/smart
groups, open/click tracking, **scheduling**, automated emails, opt-outs) · Invitations
(email/batch/**physical-mail access codes**) [T] · Notifications [T] · Embeddable widgets
[T] · Share buttons [T] · Follow [T] · Events with registration + caps [T].

**Consult**:
- **Polls** [T] — quick multiple choice; no analytics/Report Builder.
- **Native surveys** [D] — short/long text, single/multi choice, linear scale, number,
  file upload, image choice, rating, ranking, matrix, geospatial (pin/line/polygon/Esri
  shapefile); logic jumps; page-based mobile-first flow; auto-save; completion reminders;
  printable + offline re-import; third-party embed (Typeform) possible.
- **Geospatial Suite** [D] — Esri ArcGIS integration, in-survey map questions, heatmap
  visualization, GeoJSON export. For planning/mobility departments.
- **Community Monitor** [D] — always-on sentiment tracking (trust, service delivery,
  quality of life); quarterly benchmarking, automated reports, qualitative drill-downs.

**Involve**:
- **Voting & Prioritization** [D-lite] — Approval ("One Vote per Option"), Cumulative
  ("Multiple Votes per Option" / dot-voting), Budget Allocation; **offline vote upload**.
- **Common Ground** [D, Beta] — trade-off statements, agree/unsure/disagree, live
  consensus/division map. "Not a poll" — structured deliberation.
- **Document annotation (Konveio)** [T, named partner, paid add-on] — comment inside PDFs.

**Collaborate**:
- **Ideation / Public Forum** [core, D] — submit/comment/react/vote; List/Map/Feed views;
  Form Builder customizes input form; input noun renamable (ideas/contributions/questions).
- **Input IQ** [D paragraph] — real-time AI duplicate detection while drafting.
- **Mapping** [D for planners] — pins with attachments, GeoJSON/Esri layers, ArcGIS via API key.

**Empower**:
- **Proposals / Petitions** [D] — resident-initiated, thresholds + timeframe + eligibility
  rules, pre-screening, often combined with ID verification.
- **Participatory Budgeting** [D-lite] — "Basket Exercise"/"Budget Game", currency/tokens/points.
- **Online Workshops** [D-lite] — plenary + breakouts, Q&A, polls, collaborative reporting.
- **Perspectives** [D, longest treatment] — AI clustering of hundreds–thousands of inputs
  into themes → sub-questions; **bridge-building sampling** (representative, freshness
  boost, lived-expertise weighting — "not just the loudest voices"); resident-facing
  colored sticky-note UI.

## Manage (back office)

Project list w/ filters [T] · **Project Calendar** [T] · **Inspiration Hub** [D-lite]
(global library of real projects, copy process designs) · Templates [T] ·
**Publication & approval workflows** [D] (Draft w/ preview URL → approval request →
Published → Archived; Listed/Unlisted; audience scoping) · **Schedule a project** (auto
go-live) · Timeline/phase editing live · **Draft phase descriptions** · **Project & phase
permissions** [D] (action-level per phase: unregistered/email-confirmed/registered/
verified/groups/anonymous) · **Anonymous participation** (voluntary vs mandated) ·
**Input Manager** [D] (assign, internal comments, statuses, official updates, filters) ·
Official updates (bulk) · Custom statuses · Move inputs between phases · Internal
commenting w/ @-mentions · Offline input upload · Proposals management w/ pre-screening ·
**Participation feed** w/ AI Content Warnings tab · Community spam reporting · Profanity
filter (+ custom words) · AI moderation (toxic-content detection) · Throttling detection ·
**Management Feed** (30-day admin audit log; also the GDPR audit-trail answer).

## Decide (analytics & AI)

- **Dashboards** [D on representativeness] — Overview, Visitors, Users,
  **Representativeness** (platform vs census; participation-gap detection). SVG/PNG/Excel.
- **AI Sensemaking suite** [D umbrella]:
  - **Auto-tagging** — 7 methods: topic modelling, sentiment, **controversy detection**,
    classification (± by example), manual coding, participant tagging.
  - **AI summaries** — themes/arguments/trade-offs; filter by any demographic ("what do
    under-30s think about transit?"); majority AND minority viewpoints.
  - **Survey response analysis** — open-text AI + cross-tabulation by quantitative answers.
  - **Q&A insights** — conversational interrogation; answers → Report Builder.
  - **Auto-Insights** [D] — statistical significance testing on demographic×topic
    correlations; interactive heatmaps; "defensible insights that withstand scrutiny."
  - **Ethical AI box** — evidence-linked summaries (citations to original inputs), human
    corrections, "the human maintains firm control." Azure-hosted models; only free text sent.
- **Phase dashboards** [D] — auto-generated per-method metrics; Excel/PNG/SVG/PDF/Word.
- **Report Builder** [D] — drag-and-drop live reports, embeds AI summaries, demographic
  data slicer, publish into the project to close the loop. Progress reports w/ network
  benchmarking (service).
- **Data export** [T] — client owns 100% of data; Excel; role-scoped.
- **Public API** [T→mid] — documented v2 (auth, projects, phases, posts, comments, voting,
  events, campaigns, users, reactions, topics, volunteering, folders); post-contract SQL dump.
- **Workflows & automations (webhooks)** [D, added V12] — self-managed (Tools → Webhooks)
  or pre-built managed automations (SMS/email intake to 360 Input, issue routing,
  Mailchimp sync). Enterprise includes 2 managed automations; add-on otherwise.
- **PowerBI** [T] — native template + data flows.

## Services

- **Dedicated team** [D #4] — named humans: Account Manager, Government Success Manager,
  Government Support Specialists (EU+US timezones, ~3h email response), access to Head of
  Product + CEO.
- **Implementation** — kick-off (90') w/ participation success plan → technical setup
  (client: DNS + widget; Go Vocal: hosting, SSL, integrations) → training (90', on-site,
  design first projects together) → pre-launch review. Standard 4 weeks, expedited 2.
- **Continuous (GovSuccess)** — 2×/yr strategy sessions, quarterly milestones + check-ins,
  bi-yearly platform report vs benchmarks, 2×90' advisory sessions of choice (5 menu options).
- **Knowledge** — Go Vocal Insider, Community Platform (+500 practitioners), Community
  Sessions, guides, in-platform templates.
- **Support** — Essential/Standard: email + chat, 9–18 CET & CT weekdays, <1 working day
  (avg ~3h), FIN AI chatbot 24/7. Premium/Enterprise: + Tue/Thu office hours w/ bookable
  15-min calls.

## Roadmap (next 6 months as of V12 — ALWAYS verify in Feature Wiki before citing)

1. *High-quality engagement*: **Parallel participation** ("single most-requested
   improvement of 2025" — concurrent methods in one project), SMS authentication &
   notifications, HTML block in homepage builder.
2. *Organizational adoption*: Assisted project setup (AI intake→design), Workflow
   automation (email commenting, SharePoint/Teams, input routing), Multi-team management
   (Spaces, SCIM sync).
3. *Superior insights*: One-click reports (AI sensemaking → auto visualizations).

Recent (Q1-2026): Perspectives GA, Benchmarks & quality scores, Optional registration,
360 Input, Common Ground (Beta).

## Verdict vocabulary (use these, grounded in Feature Wiki status)

- ✅ **Standard** — core platform, all plans.
- 🧩 **Add-on / plan-dependent** — e.g. Konveio annotation, PowerBI (Premium), managed
  automations beyond 2 (non-Enterprise), extra seats, new eID methods, ID verification.
- ⚙️ **Configurable workaround** — achievable with existing features arranged differently
  (say how, and be honest about the seams).
- 🗺️ **Roadmap** — cite only with Feature Wiki status + never as a committed date.
- ❌ **Not supported** — say so plainly; offer the nearest workaround if one exists.

Known hard constraints (from product-model.md §8) that generate honest ❌/⚙️ answers:
one method per phase (until Parallel Participation ships), no poll analytics, external
survey URL fixed at creation, navbar max 7, smart groups AND-only, workshop max 50
desktop-only, full anonymity kills demographic reporting.

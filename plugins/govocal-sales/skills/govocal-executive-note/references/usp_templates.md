# USP templates — five fixed pillars, tailored evidence

The concept note always uses these five USPs in this order. The *title* never changes. The "The opportunity" paragraph is **competitor-tailored**; the "What we offer" intro and feature bullets stay close to canonical but can reference specifics from the competitor's docs where it sharpens the contrast.

## Canonical structure for every USP

```
| N |  {Title} |
The opportunity
{Paragraph — 4-6 sentences. Opens from a practitioner frustration we've heard about the specific competitor,
 frames the problem, then lands on the benefit of switching.}

What we offer
{One-sentence positioning statement.}
• {Feature 1}. {Short description.}
• {Feature 2}. {Short description.}
• {Feature 3}. {Short description.}
```

Three bullets is the default. USPs 3 and 4 can stretch to five when substance warrants it.

---

## USP 1 — Hybrid input & representativeness

**Title (all languages):** see `scripts/localisation.py` key `usp1_title`.

**Opportunity — canonical seed:**
> Digital-only consultations systematically over-represent the digitally fluent — and under-represent the residents you most want to hear from. On {competitor}, offline input typically means {what it means on their platform — e.g. "staff re-typing paper forms into the admin" / "manual CSV import from external forms" / "not supported at all"}, and representativeness is monitored (if at all) outside the system. Go Vocal closes that loop: a single environment where on- and offline inputs flow into the same dataset, and where you can see, live, who you are reaching and who you are not. The benefit: consultations that are both more inclusive and more defensible when the results are published.

**Tailoring variables:**
- `{competitor}` — competitor name
- Mid-sentence clause about their offline workflow — replace with what we actually found in their docs

**What we offer (fixed):**
> One 360° input architecture that treats every channel — digital, paper, in-person — as a first-class source.

**Features (fixed):**
1. **360° Input Manager.** A single workspace where every input — online submissions, offline forms, meeting contributions — is ingested, tagged, and analysed together.
2. **FormSync 2.0.** Paper surveys scanned and processed via OCR, then auto-merged with their digital equivalents. No double entry, no parallel spreadsheets.
3. **Representativeness Dashboard.** Compare actual participant demographics against your population baseline in real time, so you know early who's missing and can course-correct.

---

## USP 2 — Analysis & reporting

**Opportunity — canonical seed:**
> On {competitor}, running a consultation is {straightforward / fine / the strongest part of the product}. The hard part is the day after: thousands of contributions, open-text answers, and meeting transcripts landing on a small team that then exports to {Excel / CSV / their-analytics-tool} and disappears for weeks. Reports are inconsistent, delayed, and hard to compare across projects. Go Vocal's AI Sensemaking does the heavy lifting inside the platform, and the Report Builder turns the output into the deliverables your stakeholders expect. The benefit: faster, more rigorous, and reproducible analysis. Indeed, Go Vocal clients report ~55% reduction in reporting cycle time compared with manual or external-tool workflows.

**Tailoring variables:**
- `{competitor}`
- The specific analytics tool they rely on (Metabase, Grist, external BI, etc.)

**Only use the 55% stat** if the comparison is genuinely against a competitor with no native AI analysis. If the competitor has some native analysis features, either omit the stat or soften to "measurably faster reporting cycles".

**What we offer (fixed):**
> Analysis and reporting treated as first-class product surfaces, not add-ons.

**Features (fixed):**
1. **AI Sensemaking.** Auto-tagging, clustering, summarisation, and cross-project themes across thousands of open-text inputs — with every AI output traceable back to the original contributions.
2. **Ready-made reports.** Pre-built report templates per engagement method (survey, ideation, budget, etc.), generated with one click and kept in sync with the data. Compose custom reports directly in the platform — drag-and-drop sections, charts, quotes — and export to Word to finish off.
3. **Demographic pattern detection.** Surface how opinions and priorities differ across segments (age, neighbourhood, language, etc.) without leaving the platform. Natural-language Q&A lets non-analysts ask the data direct questions.

---

## USP 3 — Streamlined back-office workflows

**Opportunity — canonical seed:**
> In a typical {competitor} setup, a surprising amount of the real work lives outside the platform: {concrete external tools they rely on — e.g. "Grist databases for instruction", "email threads for approvals", "shared spreadsheets for project planning"}. That works until the team scales or an audit hits. Go Vocal brings the workflows — not only the content — inside the platform, so a Head of Participation can see a portfolio of projects, their status, and the decisions attached to each. The benefit: faster cycle times, cleaner handoffs between departments, and an audit trail that's already in place when you need it.

**Tailoring variables:**
- `{competitor}`
- The concrete external tools they lean on — research this; the credibility of the USP depends on it

**What we offer (fixed):**
> The back-office is designed around how participation is actually delivered within a municipality.

**Features (five bullets — this USP can use the full five):**
1. **Publication & approval workflows.** Configurable states (draft → review → publish), with roles that map to departments; nothing goes live without the right sign-offs.
2. **Gantt timelines & department workspace.** Visualise your projects and their milestones across the portfolio directly in the admin. Each department can get its own workspace.
3. **Project templates.** Standardise how a participatory budget, a consultation, or a petition is set up, so every team starts from a known-good baseline.
4. **Role-based access & smart groups.** Granular permissions per project, per phase, and per department — with audit logs as a platform primitive.
5. **Email campaigns & automations.** Segmented invites, reminders, and follow-ups from inside the platform; no separate mailing tool to stitch together.

---

## USP 4 — Interactive engagement, UX & CMS

**Opportunity — canonical seed:**
> Two out of three residents now visit participation platforms on a phone, which makes the experience itself a participation feature: it needs to feel delightful to land in, easy to move through, and worth finishing. Go Vocal is designed around that reality — horizontal carousels instead of endless vertical scroll, lightweight animations that guide the eye, and a homepage that adapts to each resident's interests and neighbourhood so the projects most relevant to them surface first. This is not a technical afterthought: an accessible, well-designed user experience drives higher conversion, more participation, and, in the end, higher levels of trust in the institution behind it. Paired with no-code CMS builders, your team can shape that experience without developers in the loop.

**Tailoring:** the opportunity paragraph is the most generic of the five; only adjust if the competitor is known for strong UX (then open with "{competitor} has solid fundamentals on mobile; where we differ is...") or for particularly poor UX (then name it specifically — "{competitor}'s long vertical scrolls and dense pages hurt completion rates on phones").

**What we offer (fixed):**
> A modern resident experience, paired with three no-code builders that put content, forms, and reports back in the hands of the participation team.

**Features:**
1. **Map surveys for planning.** {Competitor} {doesn't provide tools for planners / offers basic pin geocoding / has mapping but no survey integration}. With Go Vocal's map surveys, residents can see draft plans and draw on them lines, polygons, and pins to share their feedback.
2. **Mobile-first, adaptive resident UX.** Fully white-labelled, WCAG 2.2 AA compliant experience designed for non-technical residents — with horizontal carousels, micro-animations, and a personalised homepage that surfaces projects based on a resident's interests and neighbourhood.
3. **Three no-code builders (CMS).** Content Builder, Form / Survey Builder and Report Builder — drag-and-drop tools that let the participation team design project pages, rich surveys (with conditional logic and map questions) and living reports, all without developer support.

---

## USP 5 — Roadmap velocity & community

This USP has **two angles**. Pick one based on the competitor profile:

### Angle A — Open-source / self-hosted / community-driven competitors
(e.g. Decidim, Consul, self-hosted forks)

**Opportunity:**
> One of the less visible shifts in moving from {competitor} to Go Vocal is how the product evolves, and how you're supported around it. For many self-managed {competitor} instances, development can be slow and dedicated support resources are often fragmented or external. With Go Vocal, there's a dedicated 15-person product team building full-time, in close partnership with clients: features are co-designed with you, shipped quickly, and rolled out to everyone at once. Around the product, we invest deliberately in a community of practice and a dedicated success service — because the tool alone doesn't create outcomes; what clients do with it, with the right support around them, does.

### Angle B — Commercial SaaS competitors
(e.g. Cap Collectif, Bang the Table, Granicus)

**Opportunity:**
> Every SaaS platform claims a roadmap and a success service; what matters is how quickly things ship and how deeply clients are supported around the product. {Competitor}'s team sits at roughly {team-size if known}, shipping {cadence if known}. Go Vocal runs a dedicated 15-person product team building full-time in close partnership with clients: features are co-designed with you, shipped quickly, and rolled out to everyone at once. Around the product, we invest deliberately in a community of practice and a dedicated GovSuccess service — because the tool alone doesn't create outcomes; what clients do with it, with the right support around them, does.

**What we offer (fixed for both angles):**
> Three commitments that make the speed of improvement, and the depth of support, tangible in practice.

**Features (fixed):**
1. **Client-led roadmap, shipped fast.** A dedicated 15-person product team, with a transparent roadmap influenced by a client council. Co-design sessions run with clients throughout the year, and new features reach everyone on the platform the moment they ship.
2. **Regional community of practice.** Monthly online sessions per region, each focused on a specific topic (e.g. participatory budgeting, representativeness, AI in participation) where clients exchange experience openly. Complemented by an in-product Inspiration Hub, where you can browse how other local governments in your region have run a similar project — so teams don't have to start from scratch.
3. **Dedicated GovSuccess Manager.** A named GovSuccess Manager walks alongside your team: quarterly data and impact reports, help with project design, strategic reviews, and escalation into the product team when needed. We measure ourselves on outcomes, not on feature delivery.

---

## "The bottom line" closing

Two short paragraphs. First acknowledges the competitor as legitimate, second reframes migration as the natural next step.

**Canonical seed:**
> {Competitor} is {a strong open-source project / a credible commercial platform / a legitimate option} and a fair foundation for a participation programme. Go Vocal builds on the same mission and offers a more complete, ready-to-use toolbox: richer engagement methods, in-product analysis and reporting, a modern resident experience, and enterprise-grade security — delivered by a dedicated team of engagement experts.

No italicised tagline by default; only add one if the user explicitly asks for a close-out line.

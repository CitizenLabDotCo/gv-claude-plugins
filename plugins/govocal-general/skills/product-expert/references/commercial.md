# Commercial content (pricing structure, proof points, roadmap, compliance claims)

> Snapshot: Modular Proposal V12 (May 2026), baked 2026-07-03. **Pricing/roadmap are the
> most volatile content in this skill — verify live before quoting in anything a client
> will see.** The proposal references "Annex III. Pricing plans" for full plan contents
> (not in the template itself).

## Pricing structure

- Plans in evidence: **Essential / Standard** and **Premium / Enterprise** (the two
  support tiers pair them). "Enterprise license" = unlimited admin + PM seats, up to two
  managed automations included.
- Proposal table structure: Description / QTY / Price / Discount / Subtotal → Total per
  year; annual, EUR (localize currency!); **multi-year engagement is discounted**
  (NL-BE doc showed 2.5% for two-year). Custom offers: break out extras that could be
  dropped.
- Known add-ons / plan-gated: extra admin & PM seats (per-seat) · custom development
  (hourly, on agreement) · managed automations beyond 2 (non-Enterprise) · new eID
  verification methods · Konveio document annotation (Premium in FR doc) · PowerBI
  (Premium) · Management Feed (Enterprise) · SSO [Enterprise-flagged in NL-BE doc] ·
  advisory-session count license-dependent · MijnBurgerprofiel (BE, paid).

## Proof points ("Our impact in numbers", V10)

**4.7/5** CSAT · **40** countries · **640+** clients · **1,900** monthly active admins ·
**27,100** projects launched · **2,400,000** community members participated ("over 2.5M"
in narrative). Company: founded 2015 Brussels; co-founders Wietse Van Ransbeeck (CEO),
Aline Muylaert, Koen Gremmelprez (CTO); ~50 people, 20+ languages, 50/50 gender balance,
majority-female leadership; offices Brussels, London, Paris, Berlin, Amsterdam, Barcelona,
New York; 4.7/5 Glassdoor, 3+ yr tenure.

Awards: Forbes 30 Under 30 Europe (both co-founders) · ETION Leadership 2023 · Obama
Leader 2025–26 (CEO) · B Corp (2022) · Meaningful Business 100 · World Summit Award
(Government & Citizen Engagement) · **People Powered 2025: #1 on features, 100/100** ·
SDG 16.7 + annual impact report.

References: template has 3 fill-in tables (agency, contact, why-relevant, project
size/scope, dates, URL, case study) — no pre-filled clients. Exec summary name-drops
Copenhagen, Vienna, Seattle. UK doc: Newham, Durham, Wigan. NL doc references (Belgian!):
Lokeren (Denk Mee, burgervoorstellen), Leuven, Gent (wijkbudget). More: govocal.com/case-studies.

## Roadmap & development philosophy (V12 — VERIFY BEFORE CITING)

Philosophy: Shape Up (Basecamp), 8–10-week cycles; 30 major features in 2025; dev team
avg tenure 5+ yrs; public changelog; open roadmap consultable by clients.

Recent (Q1-2026): Perspectives GA · Benchmarks & quality scores · Optional registration ·
360 Input · Common Ground (Beta).

Next 6 months (as of V12): Parallel participation ("most-requested improvement of 2025") ·
SMS authentication & notifications · HTML block (homepage builder) · Assisted project
setup (AI intake→design) · Workflow automation (email commenting, SharePoint/Teams,
routing) · Multi-team management (Spaces, SCIM) · One-click reports.

## Security / compliance / SLA claims (stable, quotable)

- **ISO/IEC 27001** (certified by **BSI**; scope on request) · OWASP Top 10 mitigations ·
  yearly penetration test · TLS 1.2+, encryption at rest · monthly library upgrades,
  immediate high-severity CVE response · centralized logging with anomaly alarms.
- **GDPR**: customer = data controller, Go Vocal = processor; DPA available; full
  data-subject rights table; granular cookie + email consent; data minimization (name +
  email default); audit trail via Management Feed.
- **Accessibility**: WCAG 2.2 AA, certified by AnySurfer, annual third-party audit.
- **Hosting**: SaaS on AWS — Europe (Frankfurt), UK (London), South America (Santiago),
  US (Oregon), Canada (Montreal). Go Vocal handles maintenance, upgrades, DNS + SSL.
- **SLA**: >99.9% availability measured monthly · **RPO 24h / RTO 2h** · nightly encrypted
  backups, 30-day retention · auto-scaling. Support: response <1 working day, ~3h average.
- **Architecture** (for technical evaluators): React SPA + Ruby engine monolith, RabbitMQ,
  Docker Swarm, AWS PostgreSQL w/ **one isolated schema per tenant**, >85% server-side
  test coverage, **source-available on GitHub** (read/audit yes, commercial license to use).
- Data portability: client owns 100% of data; Excel exports; post-contract one-time
  PostgreSQL dump on request.

## Services summary

Implementation: kick-off 90' (participation success plan) → technical setup → training
90' on-site → pre-launch review; 4 weeks standard / 2 expedited. Continuous: 2×/yr
strategy sessions, quarterly check-ins, bi-yearly platform report w/ network benchmarks,
2×90' advisory sessions (menu of 5). Support: Essential/Standard = email+chat 9–18 CET &
CT, FIN AI chatbot 24/7; Premium/Enterprise adds Tue/Thu office hours w/ bookable 15-min
calls.

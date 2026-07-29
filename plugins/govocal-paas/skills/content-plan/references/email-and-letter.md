# Mail to registered audience & physical letter

## Mail to registered audience

The registered audience (platform users who opted in) is the warmest audience the project has — they've participated before. Write to them as returning contributors, not strangers.

One email per calendar entry the matrix marks (typically: launch, one per phase transition / vote open / deadline, results-back). Short-term delivery: the email text goes in the docx and the GSM loads it into the project's email section (clients often lack access at the start). Long term it's sent from the platform — keep each email self-contained (subject + body) so that push is mechanical.

**Anatomy of each email:**
- **Subject line** — ≤ 55 characters, the ask or the news, no "Newsletter #3". Draft 2 options (A/B) for the launch email only.
- **Preheader** — one line extending the subject (most clients' tool supports it; harmless if not used).
- **Opening** — why they're getting this: one line linking to their registration/previous participation.
- **Core** — what's happening in this phase and what they can do, in 2–4 short paragraphs. One idea per paragraph. Match the tone from the setup draft (the scrape rarely covers email; the draft `Tone` is usually the best source here).
- **One button-CTA** — verb + object ("Deel je idee", "Votez maintenant"), pointing at `{{project_url}}` (or deep-link placeholder `{{phase_url}}`).
- **What happens next** — one line: next phase and when they'll hear back.
- **Sign-off** — from the municipality/service, `{{sender_name_service}}`.

**Per moment:**
- *Launch* — the fullest email: why the project, what's open for influence, timeline at a glance, offline option (`{{paper_form_location}}`) if the phase has one.
- *Phase transition* — lead with what the previous phase produced ("{{n_contributions}} ideas came in") before the new ask. Input → visible effect is the retention engine.
- *Deadline reminder* — short, single-purpose, send `{{days_before_deadline}}` days out.
- *Results-back* — what was decided, how input shaped it, what happens now. This email is never optional.

**Statutory overlay:** formal register throughout; the closing email carries the **response-document link** (`{{response_document_url}}`) — that document is the legal proof input was considered, and this email is how registered participants receive it.

## Physical letter

Draft only where the matrix marks it: statutory (often legally required), geo-targeted co-creation (site-adjacent residents), all-households voting legitimacy (devolved), or hard-to-reach groups (issue identification). The letter is expensive per contact — its job is to reach people the digital channels won't.

**Format:**
- Municipal letterhead assumed — start at the address/date block: `{{recipient_address_block}}`, `{{letter_date}}`.
- Salutation per local convention (formal register — a letter from the municipality is never casual).
- **First paragraph = the point.** What is happening and what the recipient can do — assume the letter gets 15 seconds standing at the recycling bin.
- Body: 3–5 short paragraphs, one page maximum. Reading level: accessible to residents who don't read policy — short sentences, no nested clauses.
- **Participation without internet must be possible via the letter alone:** include the offline route (paper form at `{{paper_form_location}}`, phone number `{{contact_phone}}`) alongside the short URL and a QR code note (`QR → {{project_url}}` — flag QR generation for the champion).
- Signature block: `{{signatory_name_title}}` (mayor/alderman as local convention dictates).
- Geo-targeted letters: state plainly why this recipient ("as a resident of {{target_area}}, this affects your street") — relevance is why the letter works.

**Statutory overlay:** where the framework requires it, the letter IS the formal notification — mirror the formal notice content (instrument, window, response channels, response-document commitment), respect `{{minimum_notice_period}}`, and flag legal review in the GSM report. When the framework requires specific wording, placeholder it (`{{legally_required_wording}}`) rather than approximating it.

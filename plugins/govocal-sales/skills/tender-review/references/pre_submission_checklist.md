# Pre-submission checklist (loss-pattern red-team)

Ten areas to check every Go Vocal submission against, each tied to a real win/loss learning. Use the
buyer's scoring grid (from `tender_map.json`) to weight them. For each area decide 🔴 (clear gap, will
lose points / risk DQ), 🟠 (present but under-developed), 🟢 (strong), and size **points-at-stake**.
Always surface mandatory/disqualification risks first, regardless of weight.

## 1. Mandatory compliance & disqualification risks
Check first — a single miss can throw the whole bid out.
- Every mandatory/pass-fail requirement explicitly met and **stated as met**.
- Right legal entity and country rules satisfied (e.g. non-US vendor / EU-entity confirmations — Barrie).
- All required forms/declarations/certificates attached (ISO 27001, insurance, supplier-diversity,
  RGPD/RGAA & IA questionnaires, DC1/DC2 — a missing diversity certificate cost us points at Toronto;
  an incomplete financial annex is an irregular offer).
- Word/character limits respected; formatting rules followed.
- **No reliance on content that "won't be evaluated":** many tenders state cross-referenced attachments,
  external links or demos will NOT be scored — every answer must stand alone, and required diagrams must
  be embedded in the document, not linked (Toronto evaluators couldn't open our demo/links).

## 2. Answer the scoring grid
We lose points by not mirroring what the buyer asked, in their structure.
- Every scored question answered, in the buyer's order and numbering.
- A **requirements-to-answers mapping/overview table** is included — repeatedly a "tender must"; it makes
  the evaluator's job easy and exposes our own gaps.
- Where the buyer states explicit targets (SLA times, uptime, training sessions, signature journey),
  **quote those exact targets back** with committed figures. North Yorkshire handed us their SLA targets
  and we didn't quote them back → "poor". North Vancouver wanted ≥3 live training sessions; we described
  one.
- Each answer reflects the spec's wording, not a generic template answer.

## 3. SLA & support
The single best-evidenced loss factor (Gateshead, Moncton, North Yorkshire, Toronto, Surrey). Check our
SLA section against the **gold-standard facts** below and lead with them.
- **Disaster Recovery / Business Continuity** section present (Gateshead penalised us for omitting it
  though we do it).
- Response/resolution times **not worse** than the spec requires AND not worse than what we deliver
  (Gateshead saw "9 hours" when spec wanted 4h and we do 3h).
- Support hours stated in the **buyer's local time zone**, not GMT-by-default (Moncton misread our hours).
- A **phone / urgent after-hours / on-call path is named** — we do run out-of-hours on-call for critical
  incidents; say so (Moncton penalised "no phone or urgent after-hours support"). "Contact your
  specialist" is not an on-call commitment.
- No "Undefined"/vague resolution commitments; give a real window.
- Service credits and uptime % stated (positives at Hutt City and North Vancouver).
- Named escalation path with response times at each level.

### Go Vocal SLA gold-standard facts (don't undersell — match our copy to these)
- Service availability **99.9%**, measured monthly, with service credits for misses.
- Critical (L1): **3-hour** targeted response, **4-hour** targeted resolution.
- High (L2): response & resolution within **1 business day**.
- Out-of-hours on-call for critical incidents: initial response within **2 hours**, restore/workaround
  within **4 hours**.
- **Daily backups**; failed backups resolved before the next window.
- At least **1 penetration test per contract year**; critical security patches within 3 working days.
- Dedicated Account Manager + dedicated support contact (email + in-platform helpdesk), quarterly
  service reviews.
> If the draft states anything weaker than this, it's a self-inflicted wound — fix it.

## 4. Service descriptions & methodology detail
We consistently describe LESS than we deliver. Spell out:
- **Migration:** owned and led by Go Vocal (not "falls on the client"), with ownership model, timeline,
  API-based approach (Moncton: vague/manual-reading migration lost us the deal on services).
- **Moderation:** full workflow (pre/post-moderation, approval flows, roles) — Toronto judged ours weaker.
- **Unregistered-user / public participation flow** spelled out (Toronto flagged it unclear).
- **Training:** match or exceed the required live sessions; name the full offer (Academy, guides,
  templates). Default ≥3 live sessions unless told otherwise.
- **Delivery team:** named team with CV-style bios AND a **back-up / succession plan** (Toronto, PSoS
  flagged thin CVs / missing continuity).
- **Implementation plan:** roles, responsibilities, timeline, and a **risk/RAID log** by default; match
  the buyer's update cadence; don't schedule work the spec excluded.

## 5. Social Value / RSO (where scored)
A scored category (often ~5–10%) where we have material but don't package it.
- A method statement present and mapped to the buyer's model.
- Commitments specific and ideally **quantified** (local benefit, sustainability, inclusion).
- Pull from Go Vocal's sustainability, pay-transparency and culture material (rated "Excellent" at North
  Vancouver; Gateshead scored us 0.79% vs winner's 2.46% — more than the margin we lost by).

## 6. Hosting & data residency
Template reuse keeps tripping us here.
- Hosting region correct for the buyer and **consistent across the whole document** (CA → AWS Montreal,
  EU → Frankfurt/Paris). Moncton had a stray non-Canadian hosting line contradicting our own answers.
- Data-residency/sovereignty answered explicitly (FR, CA, Chile and others are sensitive).
- Security certifications/standards stated (ISO 27001, WCAG/RGAA level, pen-testing, encryption).

## 7. Pricing & packaging
- Line-item breakdown (licence, onboarding, services, optional modules) — North Vancouver dinged us for
  none; an incomplete unit-price grid can make the offer irregular.
- Price validity period stated.
- Optional modules listed clearly, especially any the buyer referenced (CRM/Power BI).
- **Awareness of the scoring formula:** many tenders score price as lowest÷ours × weight. If we bid
  premium into that, flag whether a leaner number is needed (Barrie, Abbotsford, Boulder, Waterloo).
  Don't assume price is the problem — at Gateshead we won on price and still lost.
- No "hidden extras" perception (Merton).

## 8. References & proof
- Case studies embedded with context and outcomes, not bare hyperlinks (Toronto/North Vancouver links
  weren't read).
- References regionally relevant and at comparable scale (thin local references hurt us in CA and FR).
- Referenced clients briefed and likely to give a strong account (a rocky migration reference hurt Moncton).

## 9. Template hygiene & polish
The most embarrassing, most avoidable losses.
- **No other clients' names left in** (North Yorkshire's plan still named Hutt City + PSoS — "read as a
  lightly edited template"). Note: a person's surname that happens to match a city is fine.
- No off-spec content (don't schedule excluded work; don't argue against mandated artifacts).
- Consistent product naming: **"Go Vocal"** (never "GoVocal"); no leftover "CitizenLab" except where
  legally required (e.g. the literal source-repo URL) — and consider a one-line note so evaluators
  aren't confused.
- Branding/fonts consistent; visuals captioned with what they show.
- Every claim is something we can stand behind live in a demo and a debrief.

## 10. Product framing & honesty
- Are we pitching what they're actually buying? (North Yorkshire bought a survey tool; we pitched an
  engagement platform.) If the fit is wrong, say so — may be a low-probability bid.
- Genuine product gaps (heat-mapping, RIM weighting, planning-doc builder, partial-response handling)
  acknowledged honestly and flagged for Product — never overclaimed.

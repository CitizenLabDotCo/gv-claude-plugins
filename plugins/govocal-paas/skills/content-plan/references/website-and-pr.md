# Website snippet & PR release

## Website snippet

One per project (refresh at results-back if the plan calls for it). This is the anchor: every other channel ultimately routes people here or to the project page directly.

**Format:**
- One paragraph, **max 100 words**, in the website's own tone (Step-2 scrape of the municipality site).
- Structure: what's happening → what the resident can influence → until when → CTA.
- CTA = click through to the project page: `{{project_url}}`.
- **Include a placement recommendation** with the asset: where on the client's site it fits (news section, homepage banner, participation page…), based on what the scrape showed. The champion shouldn't have to figure out where it goes.

**Statutory overlay — the snippet becomes the formal notice.** When `Statutory = true`, the snippet must be legally defensible, not promotional:
- Name the legal instrument (from the draft's `Instrument`) and the formal consultation window: `{{consultation_start_date}}` – `{{consultation_end_date}}` (respect the minimum notice period).
- State how to respond (the platform, plus any legally required alternative channel — writing, in person: `{{formal_response_channels}}`).
- State the commitment: responses will be considered and a response document published (`{{response_document_date}}`).
- Formal register; word limit may stretch to what the notice legally needs. Flag for GSM legal review in every statutory run.

## PR release

Draft only where the matrix marks it — and apply the **newsworthiness test** first: would a local journalist see a story here (money being handed to residents, a first for the municipality, a striking number, a human angle)? If the honest answer is no, recommend skipping in the GSM report rather than producing a release nobody prints.

**Voice:** base it on the tone of the account's previous releases (Step-2 scrape of their news/press section). PR voice is usually more formal than social — don't import the Facebook register.

**Structure (in this order):**
1. **Headline** — the story, not the process ("Residents to decide on €300,000 for their neighbourhoods", not "Municipality launches participation project")
2. **Dateline + lede** — one paragraph answering who / what / when / where / why
3. **Body** — 2–3 short paragraphs: how it works, who can take part, what happens with the input, key dates
4. **Quote** — from the responsible alderman/mayor: `{{official_name_title}}` + `{{official_quote}}`. Draft a *suggested* quote they can approve or rewrite — clearly marked as suggested; never present an invented quote as said.
5. **Practical block** — project page URL, dates, how to participate offline if applicable (`{{paper_form_location}}`)
6. **Boilerplate** — one paragraph about the municipality (pull from a previous release if scraped, else `{{municipality_boilerplate}}`)
7. **Press contact** — `{{press_contact_name_email_phone}}`

**Results-back release** (devolved decision-making especially): winners/outcomes ARE news — lead with the concrete result and a number, include a `{{winning_projects_list}}` placeholder, and a forward line on when implementation starts (`{{implementation_date}}`).

**Statutory:** where the legal framework requires publication in an official gazette or specific outlets, note the obligation in the GSM report (per the draft's `Jurisdiction`/`Instrument`) — the release itself doesn't satisfy it.

# Intake questions — Phase 1, Step 2

Ask in one batch (prefer `AskUserQuestion`). First detect the mode, then ask the matching set. Don't invent answers for blanks — flag them as gaps to resolve in research / validation.

## Step 0 — Mode detection

- Is there an **incumbent or competitor** platform in play (named or implied)?
  - **No** → GREENFIELD (concept note only).
  - **Yes** → COMPETITIVE (concept note + comparison spreadsheet). Also ask the competitive set below.

## GREENFIELD intake (city concept note)

Required:
1. **City name** (+ country). Sets the `{City}` token and the output language (`language_map.md`).
2. **The situation.** Greenfield first platform? Active RFP/tender? Pilot? Who is the note addressed to (e.g. City Manager, head of public participation, an evaluation team)?
3. **Local context.** Departments / regions already doing engagement; the city's resident-service channel name (if the city has one); priority use cases (planning, safety, budgeting, service delivery, informal-settlement upgrading…); demographics & languages spoken; any capacity/budget constraints.
4. **USP emphasis.** Which of the five pillars to lead on, and any **retitling** of the five. Should FormSync and ECHO be split out under USP 1 (yes when there's real paper / in-person engagement)?

Optional but valuable:
5. **City logo** (drop into `assets/brand/` or provide per run) and any preferred hero image.
6. **Anything we should NOT say** (sensitivities, pending procurement rules).

## COMPETITIVE intake (battlecard)

1. **Competitor name** (as referred to internally) — the `{Competitor}` token.
2. **Their home country / primary market** — for output language.
3. **Live deal/client this is for**, and the immediate use case driving the decision (PB, consultation, petitions, planning…).
4. **Primary links** — website, product/features, pricing, knowledge base, docs site.
5. **Internal artefacts** — prior proposal PDFs (theirs/ours), Notion sub-pages, Slack threads, call notes, a migration case study.
6. **Angle to emphasise** and **anything we should NOT say**.

## Always (both modes)

- Confirm **output language** (default from `language_map.md`, but confirm — HQ ≠ primary market).
- Confirm which **product features** to foreground, so the right sections of the product doc (`references/product_doc.md`) get pulled.

## Fallbacks

If the user only gives the city/competitor name: proceed from web + product-doc research, but flag honestly — greenfield local references will need validation; competitive spreadsheets will carry more 🟡/unverified rows.

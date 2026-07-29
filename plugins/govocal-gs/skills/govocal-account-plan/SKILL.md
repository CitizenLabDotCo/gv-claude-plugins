---
name: govocal-account-plan
description: Build a Go Vocal account plan for a named client — diagnoses health tier and risk vector, prescribes a 4–6 week play. Trigger on "account plan for [client]", "prep my 1:1 with [client]", "what play should I run on [client]", "diagnose [client]". Covers all three health tiers (bad → P1–P4, average → A1a/A1c/A2 + reused P2, good → G1–G4) and the competitive-risk branch (Play #7 Tender Defense, runnable for any health tier).
---

# Go Vocal Account Plan

Build an account plan a CSM can scan in 60 seconds before a 1:1. Done = a markdown plan saved to outputs, one Planhat Conversation note proposed, and CSM feedback captured.

Source of truth for the play library and decision trees: [Account Plan Skill — Claude (Notion)](https://www.notion.so/govocal/Account-Plan-Skill-Claude-34a9663b7b2681fb8e8cc2b2e6ecf4ce). Local mermaid copies live in `decision_tree/` and play descriptions in `plays/`.

## Scope

The skill diagnoses across two axes: **health tier** (`h` score) and **risk vector** (why the client might churn even with good health).

Currently covered:
- **Bad-health branch** (`h ≤ 3`) — Plays #1–#4 with sub-variants 4a / 4b / 4c.
- **Average-health branch** (`h ∈ [4, 6]`) — Plays A1a, A1c, A2, plus reused P2 at lower urgency.
- **Good-health branch** (`h ≥ 7`) — Plays G1, G2, G3, G4.
- **Competitive-risk branch** — Play #7 Tender Defense, any health tier.

Not yet co-designed:
- **Governance-risk** — DM change, champion departure, exec sponsor change, M&A, restructure.
- **Commercial-risk** — budget cut, austerity, downgrade pressure, late-payment patterns.

This skill is **not** for: prospect / sales pipeline prep (use `/ai-bdr-campaign-*`), churn-prevention announcements to leadership (use `/churn-prevention`), competitor positioning docs (use `/competitor-battlecard`), internal teammate 1:1s.

## How to run the skill

Run steps in order. Show the CSM what you have at each step and invite correction before moving on. Decision support, not autopilot.

### Step 1 — Identify the client

Ask for the client name. Use `mcp__df61a2d9-0ea0-4e3d-9889-e3bfad6ca18b__search_records`.
- **Multiple matches** — show names + domains, let the CSM pick.
- **Zero matches** — ask the CSM to confirm the exact name or paste the Planhat Company ID. Don't fabricate.

### Step 2 — Pull client state from Planhat

Read the Company record with `get_model_record`. Fields (full mapping in `planhat_signals.md`):

**Contract & lifecycle** — `custom.Lifecycle Phase`, `customerFrom`, `renewalDate`, `renewalDaysFromNow`, `custom.Population Group`, `custom.Region List`, `custom.Account Classification`, `custom.Executive Sponsor(s)`, `owner`.

**Activity signals** — `h`, `hDiff`, active admins 30d (`usage.66f6be9a0f0da01c6acaa338`), published projects (`usage.65451693c1d313d907be6927`), open engagement opportunities (`usage.6545162df0d156d5c359d0ba`), participants 60d (`usage.66f65604343b4dc033418755`), first-project-live timestamp (`usage.69b7cdf6d11490ab4cb9c537`), Company NPS (`usage.671249ff681ded6eaea9773f`).

**Risk-vector signals** — `phase`, `custom.Status Notes` (tender / RFP / competitor / budget / champion-change mentions), `custom.Forecast confidence`.

**Recent context (60 days)** — `custom.Status Notes`, recent Conversations, Comments, Tasks, Documents. Summarise in 3–4 bullets.

If a field is blank, write "no data in Planhat" rather than inferring. Note blanks in the Diagnosis if they affect routing.

### Step 3 — Determine the customer-journey stage

Classify against the Go Vocal customer journey. Contract month is one input — judge with the qualitative signals from Step 2.

| Stage | Success | Goal | KPIs |
|---|---|---|---|
| **Onboarding** | Core team trained, first projects live | 100 participants | registrants, core-team activity |
| **Adoption** | Core team running platform actively | Project rhythm + ≥1 always-on feature | open projects (≥1 continuous), methods used, participation rate |
| **Expansion** | New departments onboarding | Multiple PMs, projects across teams | active PMs, open projects, participants |
| **Flagship** | Strong engagement culture, market reference | LinkedIn, events, referrals | NPS |

S/M clients often stay in centralised Adoption — don't force Expansion. L/XL migrating clients often jump straight to Expansion. State the current stage, note any mismatch with contract month, validate with the CSM.

### Step 4 — Determine health tier + risk vector

#### 4a. Health tier (h score, then qualitative cross-check)

| Tier | `h` range |
|---|---|
| 🔴 Bad | `h ≤ 3` |
| 🟠 Average | `h ∈ [4, 6]` |
| 🟢 Good | `h ≥ 7` |

Cross-check `h` against qualitative signals (Status Notes, recent Conversations, NPS). If they disagree, flag the mismatch to the CSM and take their call.

#### 4b. Risk vector

Even good-health clients can be at churn risk for non-activity reasons. Check Planhat signals and ask the CSM. **The CSM's named risk vector overrides auto-detected signals.**

- **Activity risk** — default if health = Bad. Routes to bad-health tree (Step 5a).
- **Competitive risk** — Status Notes mentions tender / Ausschreibung / appel d'offres / licitación / RFP / procurement / a named competitor (Esri, Cap Collectif, Decidim, Granicus, etc.); OR `phase` = `3. Pre-renewal` in a tender-prone segment. Routes to **Play #7** regardless of health.
- **Governance risk** *(not yet co-designed)* — exec sponsor change, DM change, champion departure, M&A, restructure. Stop, hand back.
- **Commercial risk** *(not yet co-designed)* — budget cut, austerity, downgrade, late payments. Stop, hand back.
- **None of the above** — proceed with the health-tier tree only.

#### Routing rule

| Health | Risk vector | Action |
|---|---|---|
| Bad | any | Step 5a bad-health tree (+ Play #7 in parallel if Competitive). |
| Average | none / Activity | Step 5b average-health tree. |
| Average | Competitive | Step 5d Play #7 (skip the average-health questions). |
| Good | none | Step 5c good-health tree. |
| Good | Competitive | Step 5d Play #7. |
| any | Governance / Commercial | Stop. Return signals + activity summary. Capture as feedback in Step 9. |

State the routing back to the CSM in one line and wait for confirmation before Step 5.

### Step 5 — Walk the relevant decision tree

Each tree is in `decision_tree/{tier}.mmd` and rendered in [the Notion page](https://www.notion.so/govocal/Account-Plan-Skill-Claude-34a9663b7b2681fb8e8cc2b2e6ecf4ce). Walk interactively — read Planhat, form a hypothesis, validate with the CSM at every branch. Don't conclude on inferred evidence alone.

**Ground rule on buy-in.** Contract renewals, license upgrades, or old Planhat annotations are **not** evidence buy-in still exists. Always ask: "When did the decision-maker last actively support this work? How do you know?" Treat buy-in as expired unless the CSM names a concrete recent signal.

#### 5a. Bad-health flow (`h ≤ 3`)

Walk `decision_tree/bad_health.mmd`:
1. **Activity check** — confirm Planhat numbers match what the CSM sees.
2. **Elections / Hibernation** — ask explicitly. → **Play #3**.
3. **DM buy-in** — if no recent active support → **Play #1**.
4. **Cross-department demand** — if only champion's team AND size M/L/XL → **Play #2**. Skip for size S.
5. **Restart capability** — if buy-in + time exist but stuck → **Play #4**:
   - No project plan → **4a Success Plan Session**.
   - Plan + digital-savvy person → **4b Project Design Session**.
   - Plan + no digital-savvy person → **4c Pure Turnkey**.

#### 5b. Average-health flow (`h ∈ [4, 6]`)

Walk `decision_tree/average_health.mmd`:
1. **Continuous open engagement opportunities?** (avg open eng opps 60d ≥ 1)
2. **If no — rhythm gap. Why?**
   - Champion not installing always-on features → **Play A1a** Always-On Setup (community monitor, monthly survey, submit-a-proposal; Essential→Standard upsell trigger).
   - Not enough project inflow from other teams → **Play P2 reused** (lower urgency than bad-health #2).
   - Champion overloaded, needs to decentralise → **Play A1c** Decentralize PMs (activate other PMs; Standard→Premium upsell trigger).
3. **If yes — sufficient participants per segment?**
   - No, demand gap → **Play A2** Participation Boost (registered audience + email leverage).
   - Yes → re-classify as Good health, walk 5c.

#### 5c. Good-health flow (`h ≥ 7`)

Walk `decision_tree/good_health.mmd`. Single question: **What's the biggest opportunity?**
- Project framing weak, residents browse but don't convert → **Play G1** Flagship Projects (Premium→Enterprise).
- Platform looks generic, no flagship feel → **Play G2** Flagship Platform (branding + UX).
- PR / campaign moment available → **Play G3** Flagship Campaigns (Premium→Enterprise).
- Client ready to be a public reference → **Play G4** Become Advocate (events + speaking + flagship features e.g. Perspectives).

#### 5d. Competitive-risk flow (any health tier)

Open `plays/07_tender_defense.md` and run its diagnostic flow:
1. Tender requirements (draft document available?)
2. Scoring criteria (technical vs commercial weight)
3. Decision-maker / buying-committee map
4. Named competitors — invoke `/competitor-battlecard` for each.

Do not run health-tier questions for competitive cases. Play #7 supersedes.

#### Closing Step 5

State the diagnosis back to the CSM in one sentence and wait for "yes, go" before Step 6. If the CSM pushes back, revise — don't argue.

### Step 6 — Apply the parallel-plays rule

Max two plays at once. Secondary play allowed only if it uses **different stakeholders** from the primary AND has **no prerequisite** relationship.

**Whitelisted**: P3+P2 · P1+P4a · P1+P2 (only if champion is strong) · A1a+A2 · A1c+P2 · G1+G2 · G3+G4 · #7+P1 · #7+P2.

**Forbidden**: P1+P4c · A1a+A1c · A2+G3 · G2+G4 · G1→G3 (sequential, not parallel) · #7+any P4 variant.

### Step 7 — Assemble the account plan

Read `account_plan_template.md` and populate four sections: Client context, Diagnosis, Plan forward (primary + optional secondary play with week-by-week steps + this-week's commitments + proposed Planhat note), Your feedback (left blank for Step 9).

If a chosen play maps to an upsell trigger (A1a → Essential→Standard, A1c → Standard→Premium, G1+G3 → Premium→Enterprise, G2/G4 → tier-gated feature unlocks), include one line on it in the Plan forward. CSMs handle upsell themselves — no AE handoff.

Keep it tight. Cut Step 5 validation Q&A, framework tables, v1-vs-v2 comparisons, meta commentary. Rationales are one line; week-by-week steps are bullets. Aim for ~1 screen of reading; cut anything past 2 pages.

Save as `{client_slug}_account_plan_{YYYY-MM-DD}.md`.

### Step 8 — Propose the Planhat write-back

Log **one Conversation record** (type: `note`) summarising the diagnosis, chosen play, and week-1 action.

Do not touch `custom.Status Notes`, `custom.Bad Health Reason`, `custom.Bad health actions`, `custom.Quarterly Action Plan`, or any other field. CSMs own those.

Show the CSM the exact note text and confirm before writing.

**Known limitation**: the Planhat MCP doesn't yet support creating Conversation records. Until it does, output the note text for the CSM to paste manually.

### Step 9 — Capture feedback and log to Notion

**This step has two required parts. The skill is not done until both are complete.**

#### 9a — Ask for feedback

Ask the CSM three direct questions:
1. **What works / what resonates?**
2. **What's off or missing?**
3. **What would you change?**

Don't accept "looks good" as the full answer — try the three questions once. Capture the answers in section 4 of the saved `.md` plan file.

If feedback points at a recurring gap, offer to open a follow-up to iterate on the skill.

#### 9b — Write the log entry to Notion

Immediately after capturing feedback, create a record in the **Generated Plans Log** database. This is not optional — it is how the skill improves over time and the only way the team can track plan quality.

Use `mcp__d8a7daf0-0326-45ff-8d46-6a5247d52297__notion-create-pages` with:
- `parent`: `{ "type": "data_source_id", "data_source_id": "29d1bd9b-250b-40f6-9c86-702aa33f6915" }`

Fields to populate:

| Property | Value |
|---|---|
| `Client + Date` (title) | `{Client name} — {YYYY-MM-DD}` |
| `Client` | Client name |
| `Health tier` | `Bad` / `Average` / `Good` |
| `Primary play` | e.g. `P1`, `A1a`, `G3` |
| `Status` | `Reviewed` |
| `date:Generated on:start` | Today's date (ISO-8601, e.g. `2026-05-11`) |
| `CSM` | Notion user ID of the CSM as a JSON array string, e.g. `["21b6333d-befe-449f-87a8-346dd04a1d97"]` |
| `CSM feedback` | Answers from Step 9a concatenated into one string |

To find a CSM's Notion user ID, call `mcp__d8a7daf0-0326-45ff-8d46-6a5247d52297__notion-get-users` with their name. Known IDs (cache these):
- Sophie Zinn → `21b6333d-befe-449f-87a8-346dd04a1d97`

If the Notion write fails, tell the CSM and ask them to paste the entry manually at: https://www.notion.so/govocal/Account-Plan-Skill-Claude-34a9663b7b2681fb8e8cc2b2e6ecf4ce

## Files in this skill

- `SKILL.md` — this file
- `decision_tree/bad_health.{mmd,dot,svg,png}` — bad-health tree
- `decision_tree/average_health.mmd` — average-health tree
- `decision_tree/good_health.mmd` — good-health tree
- `plays/01_decision_maker.md` — P1
- `plays/02_cross_department.md` — P2
- `plays/03_elections.md` — P3
- `plays/04_turnkey.md` — P4 (4a / 4b / 4c)
- `plays/07_tender_defense.md` — P7 (any health tier)
- `plays/A1a_always_on_setup.md` — A1a Always-On Setup
- `plays/A1c_decentralize_pms.md` — A1c Decentralize PMs
- `plays/A2_participation_boost.md` — A2 Participation Boost
- `plays/G1_flagship_projects.md` — G1 Flagship Projects
- `plays/G2_flagship_platform.md` — G2 Flagship Platform
- `plays/G3_flagship_campaigns.md` — G3 Flagship Campaigns
- `plays/G4_become_advocate.md` — G4 Become Advocate
- `account_plan_template.md` — output template
- `planhat_signals.md` — Planhat field mapping
- `play_library_schema.md` — spec for the Notion play-library database

## Ground rules

- Always validate the diagnosis with the CSM before naming a play.
- Always treat buy-in as expired unless the CSM points to recent evidence.
- Always complete both parts of Step 9 — ask the three feedback questions (9a) AND write the Notion log entry (9b). The skill is not done until the Notion record exists. Never end the session after saving the plan without doing this.
- If a Planhat field is blank, note it in the Diagnosis. Never fabricate.
- If the CSM names a different risk vector or health tier than the signals suggest, take the CSM's answer.
- Do not touch `custom.*` fields except via the single Conversation note in Step 8.
- Do not run more than two plays in parallel.
- Do not use this skill for prospects, churn-prevention announcements, competitor docs, or internal 1:1s.

## Known gaps

- Governance-risk and commercial-risk branches not yet built — see Scope.
- Multi-cause routing is rule-based — CSMs must confirm.
- Elections play depends on the CSM looking up local election windows; no country calendar.
- Tender-defense play (#7) does not auto-fetch the tender document — relies on the champion sharing it.
- Recent-activity summary depends on CSMs logging Conversations / Status Notes in Planhat — garbage in, garbage out.
- Planhat MCP doesn't yet support creating Conversation records (Step 8 outputs paste-ready text).

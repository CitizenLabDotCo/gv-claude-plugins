# Intake questions

Ask in a single batched `AskUserQuestion` (fall back to a numbered list if unavailable). Skip anything
already answered. Don't invent answers for blanks — flag them.

1. **Stage / mode.** "Is this an early/mid-bid **strategic review & price-to-win**, a final
   **pre-submission red-team**, or both? (Default: both if a draft exists and submission is near.)"

2. **Tender documents (Drive).** "What's the Google Drive folder (or files) with the buyer's tender?
   The scoring/award annex and the price form matter most." → folder link or file IDs.

3. **Our draft.** "Where's our draft response — same Drive folder, a Notion page, an upload, or Google
   Docs? Include the SLA, pricing schedule, implementation plan and references if separate."

4. **Competitors & assumed prices.** "Who do you expect to bid, and at what price would each come in? A
   point estimate or a range per competitor is fine — it's what makes the simulation real." (Common:
   TreeCompany, Hoplr, CitizenLab/OSP/Decidim, Cap Collectif, Social Pinpoint, Commonplace, EngagementHQ,
   Granicus, Objective, Consultvox, SmartSurvey.)

5. **Our price boundaries.** "Our list/target forfait and our cost floor (lowest we'd accept)?
   Price-to-win never recommends below the floor or below the abnormally-low threshold."

6. **Notion location.** "Which Notion parent page should I publish the review under?" The review always
   goes to Notion (default: a "Tenders" page, or append to the deal's existing page). Don't offer a
   Google Doc/.docx unless explicitly asked.

7. **Language.** "Confirm output language: proposal rewrites in the tender's language; for FR/DE tenders
   the internal analysis defaults to English. Override?"

If competitor prices are unknown, proceed but state the simulation shows *price-to-win at assumed
competitor quality*, and let the user set prices live in the simulator afterward. If the scoring grid
isn't in the documents, review against the checklist anyway and flag that fixes can't be weighted
precisely.

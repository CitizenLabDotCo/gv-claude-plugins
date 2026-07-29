# Social posts — Facebook, Instagram, X

Read when the calendar includes any social entry. Common rules first, then per-channel specifics.

## Before writing: match the account

The Step-2 scrape of the account's real page beats any generic best practice. From a handful of recent posts, extract and match:
- Typical length (some municipalities write 3 lines, some write 15)
- Formality — "u"/"vous"/"Sie" vs "je"/"tu"/"du"; the choice is loaded in NL/FR/DE and the account has already made it. Never switch registers on them.
- Emoji habits — frequency and placement; mirror, don't exceed
- Hashtag habits — many municipal accounts use none; then you use none
- How they refer to themselves ("the city", "we", the municipality's name)

No account found → the channel is skipped (SKILL.md Step 2); don't use this file for it.

## Rules common to all social posts

- **First line = the hook.** It's all most people see before "see more". Lead with what the resident gets to do or decide, never with institutional framing ("The city council has decided to organise…" ❌ / "300 000 euro. You decide where it goes." ✓)
- **One post, one ask.** Exactly one CTA, pointing at `{{project_url}}` (or the event/registration where the entry says so).
- **Plain language** — the reading level of a local newspaper. No policy jargon, no acronyms.
- **Say the influence honestly** — the ask must match the phase's actual influence level. "Decide" only for devolved decision-making; "shape/co-design" for co-creation; "tell us" for consultation.
- **Accessibility:** every image gets alt text (include `alt:` in the asset); no walls of hashtags; CamelCase multi-word hashtags.
- **Visuals:** describe the intended visual in one line above the copy (`Visual: photo of {{site_photo}}` / the payload's imagery block is the first candidate). You draft copy, not images.
- Results-back posts: lead with a concrete number or outcome ("412 ideas. Here are the 5 moving forward.") and thank participants by name of neighbourhood/group, never generically.

## Facebook

- The default reach channel for 30+ residents; assume this is where most participants come from.
- Length: match the account; default 40–120 words.
- Link posts: put `{{project_url}}` in the post body; note for the champion that FB downranks link posts slightly — a strong visual + link in body is the default; link-in-first-comment only if the account itself does that.
- Reminder/deadline posts: shorter, urgency framing ("3 dagen. {{deadline_date}}."), restate the ask — never assume the reader saw the launch post.
- Event entries: use FB's event framing in copy ("kom langs" / "venez nombreux"), date + venue + registration placeholder.

## Instagram

- The reach channel for under-35 and harder-to-reach voices; the **lead channel** for community engagement archetypes.
- Copy: shorter than FB — default 30–80 words; hook in the first line (feed truncates early).
- No clickable links in captions: CTA is "link in bio" → note for the champion to set the bio link to `{{project_url}}` for the campaign window; mention this once in the asset's placeholder list.
- Visual-first: the `Visual:` line matters more here than the caption. For vote-mobilisation and showcase posts, suggest carousel (multiple contributions/options) vs single image explicitly.
- Hashtags: 2–5 locally relevant ones IF the account uses them (municipality name, neighbourhood, project tag). No generic #participation soup.
- Stories: where the calendar marks a reminder on Instagram, draft it as a story line (1 sentence + sticker suggestion: countdown for deadlines, poll for light engagement, link sticker to `{{project_url}}`).

## X (Twitter)

- Audience here is press, councillors, civil society, stakeholders — not the general public. Write for that reader: sharper, more factual, less warm than FB/IG.
- ≤ 280 characters including the link. One tweet per calendar entry; a thread only for results-back (1 outcome tweet + 2–3 detail tweets).
- Statutory amplification entries: neutral, formal, one line — instrument name, consultation window, link. This is a notice, not marketing.
- Tag the official municipal account and relevant institutional accounts as `{{handles_to_tag}}` — never guess handles.

# Channel × archetype matrix, cadence, and cross-cutting rules

Read this on every run. The matrix encodes what works across the project library — apply it, don't re-derive it.

Legend: **✓** = default on (draft it) · **○** = conditional (draft only if the trigger in the cell applies AND the account uses the channel) · **—** = off.

## Channel × archetype matrix

| Channel | 1. Information & transparency | 2. Issue identification & agenda-setting | 3. Co-creation & design | 4. Devolved decision-making | 5. Community engagement | Statutory overlay (modifier) |
|---|---|---|---|---|---|---|
| **Facebook** | ✓ launch + 1 reminder | ✓ launch, mid-point push, results | ✓ at each phase transition | ✓ heaviest mix — launch, vote open, deadline, winners | ✓ frequent light-touch, share contributions | unchanged |
| **Instagram** | ○ | ✓ reaches younger / harder-to-reach voices | ○ if visual (site, plan, designs) | ✓ vote mobilisation | ✓ **lead channel** — most visual archetype | — |
| **X (Twitter)** | ○ | ○ | ○ press/stakeholder audience | ○ | — | ○ official notice amplification |
| **Website snippet** | ✓ | ✓ | ✓ | ✓ | ○ | ✓ **becomes the formal notice** — legally defensible wording |
| **PR release** | ○ only if newsworthy | ○ launch | ○ launch + results | ✓ launch + winners announcement (results are news) | ○ human-interest angle | per legal framework (official gazette etc.) |
| **Mail to registered audience** | ✓ single announcement | ✓ launch + results-back | ✓ one per phase | ✓ launch, vote open, deadline, results | ○ | ✓ formal tone + response-document link at close |
| **Physical letter** | — unless works/disruption notice | ○ for hard-to-reach groups | ○ site-adjacent residents (geo-targeted) | ✓ all households if budget allows — voting legitimacy | — | ✓ **often legally required** — check framework + minimum notice period |

## Cadence & the moment that matters, per archetype

| Archetype | Default duration | Comms touchpoints | The moment that matters |
|---|---|---|---|
| 1. Information & transparency | 2–4 weeks | 2: launch + reminder | **Launch** — reach is the whole game |
| 2. Issue identification & agenda-setting | 4–8 weeks | 3–4: launch, mid-point push, results-back | **Mid-point push** — fights participation drop-off |
| 3. Co-creation & design | 6–12 weeks | 1 per phase transition + results-back | **Phase transitions** — show how input shaped the next iteration |
| 4. Devolved decision-making | 8–12 weeks | 5+: launch, ideation push, vote open, deadline reminder, winners | **Vote open + winners announcement** |
| 5. Community engagement | 6–12 weeks | Frequent light-touch throughout | **The showcase** — celebrating contributions IS the outcome |
| Statutory (modifier) | 6–8 weeks, respect minimum notice period | Adds: formal opening notice + formal closing response-document publication | **Closing response document** — proof input was considered |

Weight the copy effort toward the moment that matters: it gets the strongest asset, and on 6+ week projects it usually also earns a reminder.

## Cross-cutting rules (from the library data)

1. **Every plan ends with a results-back communication on every active channel.** The closing info phase is worth ~1 full point on the project's Feedback score — the comms plan must support it, never skip it. Even light community projects get a showcase/results moment.
2. **Comms cluster at phase boundaries** — mirrors the `info → engagement → info` bookend pattern that high-scoring projects share. Between boundaries, only archetypes 4 and 5 sustain mid-phase pushes.
3. **No silent gaps longer than 2 weeks** on archetypes running 6+ weeks. If the phase plan creates one, add a light-touch entry (share a contribution, progress stat, event reminder) on the archetype's lead social channel.
4. **○-channels: generate only if the account actually uses the channel** (the Step-2 scrape confirms) AND the cell's trigger applies. A core ✓-channel the account lacks → flag in the GSM report instead of inventing posts.
5. **Events** (project-level, from the payload): announce on the archetype's social channels + the phase email; remind 2–3 days before. Events with `feeds_phase` set get their CTA pointed at that phase's ask.

## Bilingual municipalities (BE and similar)

When the tenant serves two official languages (payload `settings.languages` has two locales, or the scrape shows systematically bilingual comms):

- **Both languages, always:** website snippet, PR release, registered-audience email, physical letter — the formal/owned channels. Draft natively in each language (no mirrored word-for-word translation; same facts, each text idiomatic).
- **Social channels: follow the account's own practice** as observed in the scrape — some accounts alternate languages, some duplicate every post, some run one account per language. Match what they do; if unclear, duplicate the post in both languages.
- Statutory + bilingual: the formal notice and letter must exist in every language the legal framework requires — flag for GSM legal check.

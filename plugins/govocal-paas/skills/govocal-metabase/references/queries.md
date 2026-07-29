# Common Metabase queries - copy-paste reference

Each section shows the recommended approach (card mode first, SQL fallback). MCP tool names are shortened to `execute`, `search`, `retrieve` etc. - the actual prefix is `mcp__Metabase__Unofficial___Community___`.

## Finding things

Find a card by name:
```
search({ query: "active tenants", models: ["card"], max_results: 10 })
```

Grep inside SQL of cards (only when `models=["card"]`):
```
search({ query: "registration_completed_at", models: ["card"], search_native_query: true })
```

List all collections to find the History-Tracked one (id 66) or a team collection:
```
list({ model: "collections", limit: 100 })
```

Inspect a card's SQL/parameters before running it:
```
retrieve({ model: "card", ids: [1311] })
```

## Enumerate the live ⭐ models

In Metabase API terminology, models are `dataset`s. To list everything currently published as a model:

```
search({ query: "", models: ["dataset"], max_results: 50 })
```

To restrict to the curated ⭐ ones, filter results by name on the client side (names start with `⭐`). Cross-check against the table below before assuming an ID is still valid.

You can also visit `https://metabase.hq.govocal.com/browse/models` in a browser for the rendered list.

## ⭐ Model IDs (card mode targets - from Notion guide, verify via `search` first)

| Card | ID |
|---|---|
| ⭐ Visitors | 1310 |
| ⭐ Users | 1311 |
| ⭐ Active users (30 days) | 1312 |
| ⭐ Participants | 1319 |
| ⭐ Tenants | 1322 |
| ⭐ Projects | 1323 |
| ⭐ Folders | 1324 |
| ⭐ Participation contexts | 1333 |
| ⭐ Contributions | 1315 |
| ⭐ Inputs | 1325 |
| ⭐ Sessions | 1314 |
| active_tenants (reference history-tracked card) | 1320 |

## Run a curated model in card mode

Run ⭐ Users with default filters:
```
execute({ card_id: 1311, row_limit: 500 })
```

Run ⭐ Projects, restrict to a parameter the card already exposes - inspect first with `retrieve({ model: "card", ids: [1323] })` to find the parameter `id`, `slug` and `target`, then:
```
execute({
  card_id: 1323,
  card_parameters: [
    { id: "<uuid-from-retrieve>", slug: "tenant", target: ["dimension", ["template-tag", "tenant"]], type: "category", value: ["some-tenant-slug"] }
  ]
})
```

## SQL fallback - count active tenants

If no card fits, do this in `execute` SQL mode. **Always filter to active tenants** unless the user says otherwise.

```sql
-- Count of active tenants (today's snapshot)
SELECT COUNT(*) AS active_tenants
FROM tenants
WHERE lifecycle_stage = 'active';
```

## SQL fallback - users, properly filtered

Counting from the raw `users` table without filters double-counts pending invites and abandoned registrations. Use this template, or just run card 1311 (⭐ Users).

```sql
SELECT COUNT(*) AS real_users
FROM users
WHERE invite_status <> 'pending'
  AND registration_completed_at IS NOT NULL;
```

## SQL fallback - daily contributions, filter yesterday

Metabase data is yesterday's by ~overnight reload. For daily counts, filter on yesterday so the answer is a complete day.

```sql
SELECT DATE(created_at) AS day, COUNT(*) AS contributions
FROM contributions
WHERE created_at::date = CURRENT_DATE - INTERVAL '1 day'
GROUP BY 1;
```

## History-tracked metric template (collection 66)

Pattern any history-tracked question must follow: one row, one column, one number, yesterday's data.

```sql
-- Saved as a question named e.g. `active_tenants` in collection 66
SELECT COUNT(*) AS value
FROM tenants
WHERE lifecycle_stage = 'active';
```

To read the resulting series:

```sql
-- From the historical_data schema
SELECT date, value
FROM historical_data.metrics
WHERE metric = 'active_tenants'
ORDER BY date;
```

## Large exports

Switch to `export` when result set may exceed 500 rows or the user wants a file.

```
export({
  database_id: <id>,
  query: "SELECT ...",
  format: "xlsx",
  filename: "active_users_by_tenant"
})
```

For a saved card:
```
export({ card_id: 1312, format: "csv", filename: "active_users_30d" })
```

## When in doubt

Before writing SQL by hand, do:
1. `search({ query: "<concept>", models: ["card"] })` - does a card exist?
2. If yes: `retrieve({ model: "card", ids: [<id>] })` - check its SQL/parameters.
3. If still not a fit: write SQL, but reuse the filter logic from the closest existing card.

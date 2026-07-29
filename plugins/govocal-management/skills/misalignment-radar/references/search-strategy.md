# Misalignment Radar — Search Strategy

This document contains the structured search queries to run when scanning Go Vocal's Slack for cross-functional misalignment. Run all searches with `after:YYYY-MM-DD` set to 7 days ago.

## Go Vocal team structure (for reference)

| Team | Primary channel | Channel ID |
|------|----------------|------------|
| Development | #team-development | C65GX921W |
| Sales | #team-sales | CE2BHKY22 |
| Product | #team-product | C036GLX6X1D |
| Marketing | #team-marketing | C83NU56AG |
| Operations | #team-operations | C02HGEUS47M |
| GovSuccess | #team-govsuccess | C98UFE3S8 |
| North America | #team-northam | C0646ELH31U |

### Key cross-functional channels

| Channel | ID | Purpose |
|---------|-----|---------|
| #cross-team-operations | C0514L06SGG | Team leads + ops coordination |
| #product-marketing | C02HN06ALDB | Product ↔ Marketing alignment |
| #general | C09457NG3 | Company-wide announcements |
| #operations | CN2N7N5RU | Cross-company ops requests |

### Report target

| Channel | ID |
|---------|-----|
| Team leads (private) | CNTBVJLE4 |

## Search campaign

Run these searches in order. Use `slack_search_public` for all. Set `include_context: true` and `limit: 20` for each.

### Round 1: Blocker and dependency language

These surface situations where one team is waiting on another.

```
query: "blocked after:YYYY-MM-DD"
query: "waiting on after:YYYY-MM-DD"
query: "blocker after:YYYY-MM-DD"
query: "dependency after:YYYY-MM-DD"
query: "need from after:YYYY-MM-DD"
query: "still waiting after:YYYY-MM-DD"
query: "when will after:YYYY-MM-DD"
query: "who owns after:YYYY-MM-DD"
```

### Round 2: Priority and timeline shifts

These surface situations where plans are changing in ways that might not be communicated.

```
query: "reprioritize after:YYYY-MM-DD"
query: "deprioritize after:YYYY-MM-DD"
query: "pushed back after:YYYY-MM-DD"
query: "timeline change after:YYYY-MM-DD"
query: "scope change after:YYYY-MM-DD"
query: "moved to next after:YYYY-MM-DD"
query: "postpone after:YYYY-MM-DD"
query: "delay after:YYYY-MM-DD"
```

### Round 3: Cross-team friction indicators

These surface moments where teams are confused about ownership or direction.

```
query: "who is responsible after:YYYY-MM-DD"
query: "whose call after:YYYY-MM-DD"
query: "not aligned after:YYYY-MM-DD"
query: "misaligned after:YYYY-MM-DD"
query: "conflicting after:YYYY-MM-DD"
query: "confused about after:YYYY-MM-DD"
query: "didn't know after:YYYY-MM-DD"
query: "already working on after:YYYY-MM-DD"
```

### Round 4: Escalation and urgency

These surface situations where normal coordination has broken down.

```
query: "escalate after:YYYY-MM-DD"
query: "urgent after:YYYY-MM-DD"
query: "critical after:YYYY-MM-DD"
query: "asap after:YYYY-MM-DD"
query: "need help after:YYYY-MM-DD"
query: "dropping the ball after:YYYY-MM-DD"
```

### Round 5: Cross-team channel reads

After the keyword searches, read the last 7 days of messages from these cross-functional channels to catch misalignment that doesn't use obvious keywords:

1. `#cross-team-operations` (C0514L06SGG) — team leads coordination
2. `#product-marketing` (C02HN06ALDB) — product ↔ marketing
3. `#operations` (CN2N7N5RU) — cross-company requests

Use `slack_read_channel` with `oldest` set to the Unix timestamp of 7 days ago.

## Analysis guidance

After collecting all search results, group them by theme rather than by search query. A single misalignment issue might show up across multiple searches — e.g., a blocked handoff might appear in both "waiting on" and "escalate" searches.

Cross-reference findings: if a blocker mentioned in #team-development is also discussed in #team-product, that's stronger evidence than a single mention. If a priority change in one channel has no corresponding update in the dependent team's channel, that's a signal.

Pay attention to what's *missing* as much as what's present. If Team A announces a major scope change and Team B (who depends on that work) shows no awareness of it, that silence is the signal.

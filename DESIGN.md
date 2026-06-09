# Viewer Design Rules

This file defines design rules for the HAKARI-Bench leaderboard viewer. Keep
viewer-specific design guidance here instead of spreading it through
`AGENTS.md`, implementation comments, or ad hoc notes.

## Review Viewports

- Treat the desktop/PC view as the standard design target. The viewer is
  primarily used for inspecting dense benchmark tables, filters, and comparison
  controls on a PC-sized screen.
- When checking design changes, verify the desktop/PC view first. Use it as the
  baseline for layout density, column behavior, spacing, and interaction
  affordances.
- Keep mobile support sufficient for basic reading and navigation. Mobile does
  not need to be the primary optimization target, but users should still be able
  to load the page, read the headline and controls, scroll the leaderboard, and
  avoid broken or overlapping UI.

## Design Scope

- Put reusable viewer design rules in this file.
- Keep `AGENTS.md` focused on repository-wide workflow and engineering rules.
- If a viewer design decision changes expected behavior, update tests and any
  relevant viewer documentation at the same time.

## Interface Priorities

- Favor scannable, data-dense layouts over marketing-style presentation.
- Preserve clear hierarchy for benchmark selection, filters, score controls,
  and the leaderboard table.
- Avoid adding panels or explanatory sections unless they directly improve the
  benchmark inspection workflow.
- Prefer compact controls with stable dimensions so labels, loading states, and
  hover states do not shift the layout.

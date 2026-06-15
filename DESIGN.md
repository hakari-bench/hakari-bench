---
version: alpha
name: HAKARI-Bench-viewer-design
description: >-
  A dense benchmark management interface for comparing retrieval, reranking,
  BM25, sparse, late-interaction, compression, and language/task trade-offs. The
  UI should feel quiet, technical, and trustworthy: compact controls, high
  information density, rounded low-border surfaces, light/dark parity, and
  subtle cyan interaction cues. The table is the product.
colors:
  light:
    bg: "#f7fdff"
    surface: "#ffffff"
    surface-muted: "#e0f1f5"
    surface-faint: "#edf8fb"
    border: "#a9ccd6"
    border-strong: "#85bdcc"
    text: "#243036"
    text-muted: "#52626b"
    text-faint: "#6f7f87"
    accent: "#0077aa"
    accent-strong: "#005f88"
    accent-soft: "rgb(0 119 170 / 0.10)"
    control-bg: "#e3f2f6"
    control-hover: "#d5eaf0"
    control-active: "#c3e0e9"
    warn-bg: "#fff6df"
    warn-text: "#a96b00"
    danger: "#ff5888"
    variant: "#765aa8"
  dark:
    bg: "#202628"
    surface: "#2b3133"
    surface-muted: "#343d40"
    surface-faint: "#252c2e"
    border: "#435358"
    border-strong: "#5b7880"
    text: "#f1fbff"
    text-muted: "#abb9bd"
    text-faint: "#768589"
    accent: "#00d0ff"
    accent-strong: "#a8f0ff"
    accent-soft: "rgb(0 208 255 / 0.11)"
    control-bg: "#30383a"
    control-hover: "#344044"
    control-active: "#30454b"
    warn-bg: "rgb(239 208 106 / 0.11)"
    warn-text: "#efd06a"
    danger: "#ff5888"
    variant: "#b99cff"
typography:
  family: >-
    "JetBrains Mono", "Fira Code", "SFMono-Regular", "Cascadia Code",
    "Roboto Mono", "Noto Sans Mono", "Yu Gothic UI", "Meiryo",
    ui-monospace, monospace
  base:
    fontSize: current viewer default
    lineHeight: current viewer default
    letterSpacing: 0
  control:
    fontSize: inherit
    fontWeight: 500
    lineHeight: 1.2
  label:
    fontSize: inherit
    fontWeight: 600
    lineHeight: 1.2
  table-number:
    fontSize: inherit
    fontWeight: 400
    lineHeight: 1.2
    fontVariantNumeric: tabular-nums
rounded:
  sm: 4px
  md: 6px
  lg: 8px
  pill: 9999px
spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
components:
  app-header:
    purpose: Brand, repository link, docs, and theme toggle.
    treatment: Compact horizontal row; title and right-side controls share the
      same vertical center line. The title uses the same body-scale typography,
      color, weight, and font family as the short product description below it.
      The brand mark is a single-color inline SVG that follows the same
      stroke-based icon style as header actions.
  leaderboard-configuration:
    purpose: Select evaluation mode, benchmark scope, metrics, task facets, display,
      variants, and filters.
    treatment: One integrated workspace above the table; no marketing panels.
  control-button:
    purpose: Any clickable selection chip, including mode, scope, metric, language,
      and advanced filter disclosure controls.
    treatment: Rounded low-contrast fill by default; subtle hover; clearer active fill.
  help-modal:
    purpose: Explain technical controls without adding permanent copy to the page.
    treatment: Modal header uses the target concept name, not generic "Help".
  leaderboard-table:
    purpose: The primary product surface.
    treatment: Dense, sticky model-name column, compact row heights, borders only where
      they improve scanning.
  model-score-bar:
    purpose: Show relative Borda strength behind the sticky model name.
    treatment: Subtle background bar scaled by visible max score; never competes with text.
  score-cell:
    purpose: Show score, optional task rank, z-score, and variant deltas.
    treatment: Numeric alignment and compact heat color; rank decoration is minimal.
  footer:
    purpose: Metadata such as latest update and database source.
    treatment: Small, low-margin, no redundant product title.
---

# HAKARI-Bench Viewer Design

This file defines the design system for the HAKARI-Bench leaderboard viewer.
Keep viewer-specific design guidance here instead of spreading it through
`AGENTS.md`, implementation comments, or ad hoc notes.

The viewer is not a landing page. It is a benchmark inspection tool for people
who need to compare many models, tasks, languages, and efficiency variants at
once. The design should make comparison faster, reduce ambiguity, and preserve
trust in the numbers.

## Product Intent

HAKARI-Bench compares retrieval and reranking systems across multilingual and
domain-specific Nano suites. The UI therefore has two competing jobs:

- Keep the control surface understandable for first-time readers.
- Keep the table dense enough for repeated expert comparison.

The current visual direction uses a quiet technical palette, rounded surfaces,
subtle cyan action cues, and a monospaced numeric feel. This makes the viewer
read as an analytical instrument rather than a general-purpose dashboard.

## Primary Viewport

- Standard review target: desktop/PC.
- Primary width: 1280px, because this should fit a MacBook 13-inch class
  display.
- Verify desktop first for layout density, control grouping, sticky columns,
  horizontal scrolling, hover states, and table readability.
- Mobile support is secondary but must not break. Users should be able to load
  the page, read the title and key controls, open help/docs, and horizontally
  scroll the table without overlapping UI.

## Theme Strategy

- Default theme follows the OS preference.
- Light and dark themes must be maintained together. A design change is not
  complete until both themes look intentional.
- Do not let one theme become the source of truth and the other become a
  mechanical inversion. Contrast, active states, heat colors, and muted text
  often need separate tuning.
- The theme toggle belongs in the header action cluster near the docs link.

## Color Principles

- Use cyan as the primary interaction signal: selected state, links, icons,
  score bars, focus, and loading indicators.
- Keep clickable-but-secondary controls visible without shouting. Default
  button fills should read as actionable, while active state should be clearly
  stronger.
- Light-mode controls need a distinct visual step from panel backgrounds:
  default controls should be visibly clickable, and active controls should read
  one level stronger without adding hard borders.
- Prefer surface color and background tint over hard borders. Borders are useful
  for the table and precision controls, but panel chrome should stay quiet.
- Use green/emerald heat colors for strong positive score cells and rose/red for
  weak or negative deltas. Keep these colors balanced in light mode so they do
  not overpower model names and controls.
- Use purple only for variant metadata where it distinguishes a model variant
  from a base model.

## Typography

- Preserve the current font sizes unless the user explicitly asks for a sizing
  change. The table density depends on predictable text metrics.
- Use the monospaced stack for model names, task names, scores, labels, and
  compact controls. This supports scanning and numeric comparison.
- Table headers use a compact 11px regular weight. Standard columns and
  multi-line task columns should keep the same size, color, and weight so
  benchmark/task or benchmark/language labels scan as one label.
- Use `font-variant-numeric: tabular-nums` for ranks, scores, z-scores, counts,
  dimensions, dates, and parameter values.
- Keep letter spacing at 0. Do not use negative tracking for this viewer.
- Avoid hero-scale text. The page title should match the product description's
  compact text treatment because the leaderboard table is the main content.

## Layout Principles

- The first screen should be the usable leaderboard, not explanatory content.
- Group controls by workflow:
  - Evaluation mode: Retrieval or Reranking.
  - Benchmark scope: All, Core, Group, and Nano suite selection.
  - Table shape: Metric, task facets, task scores, ranks, z-scores, and visible
    aggregation.
  - Efficiency variants: Dims, Quant, Rescore, Sparse pruning.
  - Refinement: language, model/task text filters, advanced runtime/model facets.
- Keep most groups single-column. Use two columns only when the groups are
  parallel and compact, such as Table display and Efficiency variants.
- Benchmark scope should keep all Nano suite choices visible on desktop.
  Collapsing them hides the primary navigation model.
- Use help modals rather than permanent explanatory copy for technical controls.
  The control area should remain compact.
- Avoid nested cards. Sections should be low-border surfaces or full-width
  bands; repeated item cards and modals are acceptable.

## Controls

- Any clickable label should look clickable before hover. Use a low-contrast
  background fill, rounded radius, and enough padding to create a stable target.
- Active controls should use the stronger active surface and accent text or
  border.
- Non-clickable labels such as "Benchmark scope", "Task facets", and "Metric"
  should not adopt button styling.
- Help icons belong inside the control they explain when the scope is local,
  such as All/Core/Group or Safeguard positives.
- Use icons where they shorten recognition: table, calendar, docs, language,
  filters, metric, retrieval, and reranking.
- In Refine results, Params sits above Length and uses compact numeric inputs
  in millions for Active Params and Total Params bounds.
- Keep the HAKARI-Bench brand mark as a simple single-color balance icon with
  `currentColor` stroke so it can inherit the viewer accent color in both
  themes.
- Use a separate white SVG for the browser favicon, while keeping the in-page
  brand mark theme-aware.
- Loading indicators should be animated but small. Initial page loading can be
  centered and spacious; incremental loading should stay in the corner or near
  the affected control.
- Initial page loading should reserve a tall, stable leaderboard area so the
  first viewport does not feel collapsed while data is fetched.

## Help And Documentation

- Tooltip-style hover text is only for very short labels.
- Detailed explanations belong in modals, especially for controls that affect
  ranking semantics or filtering.
- Modal headers should be the concept being explained, such as "Task facets",
  "Dims", or "NanoRTEB", not generic labels like "Help".
- Help copy should start with a short explanation, then describe what the
  feature changes, what it filters or displays, and give examples when helpful.
- Model and task text filters should document multi-keyword matching. For
  example, `jina bge` matches rows containing either `jina` or `bge`; task
  filters work similarly, and short task names such as `nq` must be supported.

## Leaderboard Table

- The table is the primary interface. Optimize it before optimizing surrounding
  chrome.
- Keep model name sticky and readable during horizontal scroll.
- Keep task columns compact. Repeated suite prefixes may be removed from the
  subtask line when the remaining label is non-empty.
- When a task label has a suite and subtask, use a two-line header treatment
  rather than `Suite::Task`.
- Documentation icons should sit beside the specific task or suite label they
  explain.
- Model-name hover and row hover backgrounds should match, including sticky
  columns.
- Use Borda background bars as context, not as chart decoration. Bars should be
  subtle, use the accent color, and scale relative to the visible maximum Borda
  score so the top visible row reaches 100% without moving the minimum score to
  zero.
- If there is only one visible row, the bar can fill to 100%; if there are no
  visible rows, no bar should render.

## Score Cells

- Score cells must remain compact and numerically aligned.
- Rank columns such as Borda and Mean should stay narrow; they are comparison
  anchors, not score detail columns.
- Do not show the Tasks column in the leaderboard table. Keep task counts
  available in CSV export.
- When only task ranks are shown, render ranks plainly like Borda rank values.
- When z-score and task rank are both shown, keep rank and score inside the same
  cell without changing the score's perceived font size. The z-score should stay
  visually subordinate and aligned consistently.
- Use `[rank] score` only when both rank and z-score/score context are present
  and it improves comparison. Avoid decorative rank badges.
- Positive z-score in light mode should read as green but not saturated enough
  to dominate the table.
- Light-mode z-score colors should be dark enough to remain legible at compact
  table font sizes because STD uses text color without a filled background.
- STD/z-score display should not use filled backgrounds or borders. Preserve a
  stable numeric width, and express positive/negative strength through the text
  color of the score and sigma string.

## Variant Labels

- Keep row metadata short. Prefer `Dims`, `Quant`, `Rescore`, and
  `Sparse pruning` over longer technical labels when the displayed values are
  compact.
- Model type, dimension, variant, and quantization labels use the same
  semi-transparent active-control background so light-mode labels stay visible
  against both white and faint-cyan table rows. Dimension and variant labels
  keep the accent-blue text treatment, and all of these labels stay borderless
  so they read as metadata rather than separate controls.
- Sparse active-dimension variants should use short labels such as `q16d` and
  `d256d`, with the full setting and explanation in help or model detail UI.
- CSV export may include longer descriptive fields such as Variant Label and
  Variant Category because spreadsheet users benefit from explicit metadata.

## Footer And Metadata

- The footer is for provenance, not branding repetition.
- Include latest update with a calendar-style icon.
- Include database source:
  - Remote cache: `database: remote / <sha1-prefix>`.
  - Local path: `database: local / <path>`, wrapping cleanly when long.
- Keep footer font size, padding, and margin smaller than the main UI.
- Do not repeat "HAKARI-Bench leaderboard" in the footer.

## Do

- Review desktop at 1280px before considering the change done.
- Check both light and dark themes after visual changes.
- Keep density high and copy short.
- Prefer modals for detailed help.
- Use icons to clarify control meaning.
- Use background color, radius, and low-contrast fills to replace unnecessary
  borders.
- Update this file when a design decision changes.

## Don't

- Do not add marketing-style hero sections, decorative gradients, or ornamental
  background imagery.
- Do not add explanatory paragraphs directly into the control area when a modal
  can carry the explanation.
- Do not change font sizes casually.
- Do not create one-note color palettes or let cyan dominate every surface.
- Do not hide core benchmark suite choices on desktop.
- Do not make active/hover states shift layout.
- Do not use hard borders everywhere; reserve them for table readability and
  controls that need precise separation.

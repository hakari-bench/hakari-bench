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
      The in-page title reads `HAKARI-Bench - A Leaderboard for Information
      Retrieval Models Across Diverse Tasks`; the browser document title
      remains the shorter `HAKARI-Bench leaderboard`.
      The brand mark uses the square HAKARI-Bench app icon at 28px with a 22%
      CSS border radius for an iOS-style rounded shape. The brand/title target
      links to `/` so users can refresh back to the default leaderboard state.
  leaderboard-configuration:
    purpose: Select evaluation mode, benchmark scope, metrics, task facets, display,
      variants, and filters.
    treatment: One integrated workspace above the table; no marketing panels.
      Model family filters expose BM25 separately from Sparse so lexical
      baselines can be compared or hidden independently from learned sparse
      retrievers. License filters include commercial-use buckets derived from
      model-card license metadata; BM25 rows follow the bm25s MIT license and
      appear in the commercial bucket. License filters show the bucket
      checkboxes directly, matching Model family rather than adding a redundant
      subheading or hiding them inside a secondary disclosure. Filter results is
      closed on the unfiltered initial view and opens automatically when a text,
      facet, parameter, length, or rank-recalculation filter is active.
      Efficiency filters expose expanded Dims and Quantization controls directly
      without nested disclosure widgets whenever Filter results is open.
      Dims and Quantization sit on the same compact row as inline controls.
      Efficiency variants toggles preserve the active Filter results state,
      including Dims and Quantization selections, so toggling additional variant
      rows does not clear visible filters.
      Rescore is an additive refinement of Quantization, not an independent row
      category: Quantization + Rescore shows full-dimension compressed-first-pass
      rescore rows, and adding Dims also shows truncated-dimension rescore rows.
      Rescore alone, or Dims + Rescore without Quantization, intentionally adds
      no rows when restored from a URL. To avoid an apparently inert first click,
      turning on Rescore while both prerequisites are off also turns on Dims and
      Quantization; turning Rescore off never changes them. If either prerequisite
      is already on, preserve that explicit selection. Explain this behavior from
      a dedicated question-mark help trigger beside Rescore. Keep that trigger
      inside the Rescore chip's visual boundary, matching the integrated help
      treatment used by benchmark-scope buttons.
      Rescore rows must retain a visible `rescore` badge in addition to their
      dimension and quantization badges; never expose internal names such as
      `binary_rescore` or `int8_rescore`. Use the
      purple variant-metadata token for the Rescore badge's text and tint in
      both light and dark themes so it does not read like the cyan dimension
      badge or amber quantization badge. Keep it borderless like the other
      compact metadata badges.
      M-BEIR(task) and M-BEIR(lang) are mutually exclusive representations of
      one benchmark scope and share the same integrated `or` selector treatment
      used by Task columns and Grouped columns.
      Benchmark scope and Task facets are two cuts over the same task population,
      so they share one bordered panel. Preserve their existing labels and controls,
      and separate Task facets from the scope controls with only a horizontal border.
      The main filter controls are arranged as two aligned flex lanes: left lane
      Model, Dims, Active params (M), and Query length; right lane Task,
      Quantization, Total params (M), and Document length.
      Dims uses explicit min/max numeric bounds in the form `Dims [min] - [max]`;
      an empty maximum means no upper bound, and Dims inputs do not use browser
      datalist suggestions. Dims, Params, and Length numeric inputs update their
      pending hidden form values while typing, but only submit the filter when
      the user presses Enter or otherwise submits the form. Quantization uses
      checkboxes with Original, int8, binary, and any additional recorded formats
      selected by default.
      Params and Length do not use parent group labels; expose Active params (M),
      Total params (M), Query length, and Document length as separate inline
      range controls with their own icon and help trigger so the different axes
      are visible without adding vertical section space.
  control-button:
    purpose: Any clickable selection chip, including mode, scope, metric, language,
      and advanced filter disclosure controls.
    treatment: Rounded low-contrast fill by default; subtle hover; clearer active fill.
  help-modal:
    purpose: Explain technical controls without adding permanent copy to the page.
    treatment: Shared `.hakari-modal` shell on surface color with a strong border,
      soft shadow, and a blurred dimmed backdrop. The dialog is a column flex box
      capped at 85vh: the header stays fixed while only the body scrolls, so long
      explanations never push the close control off screen. The header sits on the
      faint surface tint and pairs a small accent icon with the target concept
      name (not generic "Help"); the close control is a quiet icon-only ghost
      button with an accessible "Close" label. The header name stays short, so a
      group name that a short title genuinely needs ("Benchmark scope",
      "Getting started") rides above the lead line as a small uppercase accent
      chip instead of being pushed into the title; do not add a chip that merely
      restates where the trigger sits. The lead line answers "in one sentence,
      what is this?" and is set as a GitHub-style tip callout - accent left rule,
      accent-soft fill, and a lightbulb "In short" label - so a reader who only
      looks at one thing looks at the right one. Explanatory copy is the point of
      these dialogs, so the body is near-primary text color rather than the muted
      metadata tone. The dialog is roughly 44rem wide and its own padding sets
      the reading measure: capping paragraphs narrower than the dialog only
      leaves a ragged right gutter, which reads as broken rather than as
      breathing room. viewer.js splits help
      copy into real paragraphs instead of relying on `white-space: pre-wrap`, so
      the gap between paragraphs is a deliberate margin rather than a full blank
      line at body line height. A follow-through link
      out of a dialog uses the `.hakari-modal-action` chip, not bare underlined
      body copy. Help, benchmark-doc summary, count-breakdown, and model-detail
      dialogs all reuse this shell.
  docs-page:
    purpose: Standalone benchmark and task documentation rendered from Markdown.
    treatment: Shares the leaderboard chrome (brand mark linking home, GitHub link,
      theme toggle) and loads viewer.js so theme choice persists. Article sits on a
      surface card beside a sticky "On this page" outline; tables get a header row,
      light row striping, and a rounded border; inline code reads as a subtle chip.
      The index leads with its own title, carries the paper reference in an accent
      card below it, and lists groups as a responsive grid of compact link cards.
  leaderboard-table:
    purpose: The primary product surface.
    treatment: Dense, sticky model-name column, compact row heights, borders only where
      they improve scanning. Table display includes an optional Others toggle
      for low-frequency metadata columns such as License and Model Type,
      appended at the far right so the core score columns remain stable. These
      cells must stay one line using short labels such as Apache, CC BY-NC,
      OpenAI, and Late int.; expose the full label through hover tooltip and
      Model Details. Task columns and Grouped columns form one visibly connected,
      mutually exclusive choice. Task columns uses Micro scoring and shows raw
      task units for ordinary benchmarks; Grouped columns uses Macro scoring and
      shows one column per selected benchmark group. M-BEIR is the deliberate
      exception because its 13-task x 14-language matrix must never become 182
      visible columns. Both table modes expand M-BEIR only
      along its selected inner axis: task mode uses 13 columns such as
      `M-BEIR-arguana`, while language mode uses 14 columns such as `M-BEIR-ar`.
      The inner columns are display breakdowns. Micro still weights all 182 raw
      result cells, while Macro averages M-BEIR into one benchmark contribution.
      Every Grouped column uses its benchmark-group documentation tooltip and
      wraps its complete label within the column instead of ellipsizing it. When
      a Task or Grouped metric header is selected for sorting, move that metric
      column to the front of the metric-column region so the sorted values stay
      visible beside the fixed summary columns.
  model-details:
    purpose: Modal metadata for a single result row.
    treatment: Prefer model-card metadata when present. Order fields as Language,
      Model type, Ranking label, parameter counts, max tokens, truncate dims,
      license, Hugging Face, GitHub, papers, then runtime and variant details.
      GitHub links should show the `owner/repo` label instead of generic copy.
      Prompt metadata should use Query Prompt and Doc Prompt labels. Optional
      model-card notices are short user-facing caveats and render as the final
      Model Details row.
  leaderboard-plot:
    purpose: Optional visual comparison surface for score, scale, dimension, and
      compression trade-offs using the same scoped and filtered rows as the table.
    treatment: Available as icon-labeled Table / Chart tabs at the start of the
      result status line before the current scope and evaluation mode. The chart
      uses compact Y axis, X axis, and Color selectors positioned in the graph
      area's top-right corner, muted grid lines, fixed-size circles, and
      hover-only tooltips for row metadata. Color defaults to Dims and uses a
      high-contrast violet-to-cyan-to-amber scale that remains distinguishable
      on both light and dark backgrounds. The tooltip preserves line breaks so
      score/rank and model metadata scan as separate groups. The right-side color
      legend label is vertical and sits
      to the right of the gradient bar and tick labels. It must preserve the current
      benchmark scope and filters, quantization axes must automatically include
      quantization variants, sparse/BM25 rows use a representative average
      regular dense dimension for plotting, late-interaction rows use their
      token-interaction dimension for Dims-driven plot size/color and label it
      as Token dim in tooltips,
      Dims on the X axis should render grid/tick marks on 128-dimension
      boundaries through 1024, then only show major high-dimension markers such
      as 2048 and the visible maximum to avoid label collisions. Dims X-axis
      spacing should compress the low-dimension 0-256 range so small dimensions
      do not consume the same visual width as the more important mid/high range,
      nonnegative measures must not render negative axis or legend labels, quantization
      channels use a fixed 1-16 scale where none is 16,
      int8 is 8, and binary is 1. Active Params and Total Params default to
      explicit log-scale channels and also offer linear channels; log-scale
      labels should include "(log scale)" in the plotted axis or legend title.
      Dims and token channels use logarithmic scaling where they drive position
      or color, the Color selector may use None to render one constant color
      without extra encoding, and all leaderboard controls must preserve the
      current chart view state. Mobile-width viewports should hide the chart and
      chart controls and show a concise message that chart view requires a wider
      device.
      BM25-style baselines and static embeddings should remain visible at 0
      params in active/total-parameter plot channels because they do not have
      model weights in the same sense as neural models. Other rows with unknown
      active/total params, such as hosted API models, should use the visible
      maximum param value for plotting so unknown scale is not confused with
      zero-weight baselines. Log-scaled parameter axes that include 0-param rows
      should reserve a small left bucket for zero so the smallest positive
      neural model is not drawn on top of the zero baseline. Rows without
      max-token metadata should use the
      visible maximum max-token value for plotting so they are not dropped
      solely because color or another plot channel uses Max Tokens. Borda Score
      uses a fixed 0-100 Y axis, while Task Mean scores use the visible score
      minimum and maximum as the Y-axis bounds.
    status-line: The current benchmark scope sits directly after the Table / Chart
      switch with the same database icon used by the Benchmark scope control;
      avoid a bare slash before the scope label.
  model-score-bar:
    purpose: Show the active score-sort target behind the sticky model name.
    treatment: Use Borda, Mean, Macro, Micro, or the selected Task/Grouped raw
      metric score when that score column controls sorting. Fall back to Borda
      for non-score sorts. Scale against the visible maximum and never compete
      with text.
  score-cell:
    purpose: Show score, optional task rank, z-score, and variant deltas.
    treatment: Numeric alignment and compact heat color; rank decoration is minimal.
  footer:
    purpose: Metadata such as latest update and database source.
    treatment: Small, low-margin, no redundant product title. During the first
      leaderboard load, keep the footer top border hidden so the centered loading
      state remains visually quiet; the loaded footer may use the normal divider.
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
  change. The table density depends on predictable text metrics. The standalone
  documentation pages are the deliberate exception; see Documentation Pages.
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
  - Benchmark scope: Overall, Overall (EN), Clear, and Nano suite selection.
  - Table shape: Metric, task facets, task scores, ranks, z-scores, and visible
    aggregation.
  - Efficiency variants: Dims, Quant, Rescore, Sparse pruning.
  - Refinement: language, model/task text filters, advanced runtime/model facets.
- Keep most groups single-column. Use two columns only when the groups are
  parallel and compact, such as Table display and Efficiency variants.
- Benchmark scope should keep all Nano suite choices visible on desktop.
  Collapsing them hides the primary navigation model.
- Keep the configuration panel vertically tight so the leaderboard reaches the
  first screen. Prefer small, consistent section padding and gaps over generous
  spacing; do not buy compactness by hiding suite choices or shrinking control
  hit targets below a comfortable size.
- Keep the page top chrome tight: the brand row should sit close to the viewport
  top, and intro/status copy should use compact margins and padding so the
  leaderboard remains the first meaningful surface.
- The Table / Chart switch belongs directly above the result surface. Chart is an
  inspection mode for the current table rows, not a separate dashboard; it should
  not duplicate the main benchmark, filter, or variant controls.
- Use help modals rather than permanent explanatory copy for technical controls.
  The control area should remain compact.
- Avoid nested cards. Sections should be low-border surfaces or full-width
  bands; repeated item cards and modals are acceptable.

## Controls

- Any clickable label should look clickable before hover. Use a low-contrast
  background fill, rounded radius, and enough padding to create a stable target.
- Active controls should use the stronger active surface and accent text or
  border.
- Boolean display and variant toggles (STD, Task ranks, Dims,
  Quantization, Rescore, Sparse pruning) use the `.toggle-chip` style: a control
  chip whose checked state adopts the active surface and accent text, matching the
  selection chips rather than a raw native checkbox. Keep the real checkbox for
  form submission and focus, visually hidden, with a visible focus ring on the
  chip.
- Task columns and Grouped columns use the same chip treatment inside one
  bordered choice group with a short `or` separator. Selecting either clears
  the other; selecting the active chip again may return to the summary table.
  While either mode is active, the incompatible Score choice is visibly
  disabled because Task columns is always Micro and Grouped columns is always
  Macro.
- Non-clickable labels such as "Benchmark scope", "Task facets", and "Metric"
  should not adopt button styling.
- Help icons belong inside the control they explain when the scope is local,
  such as Overall/Overall (EN) or Safeguard positives. A section label such as
  "Benchmark scope" also carries its own help for the section as a whole, since
  the per-button help cannot explain what the group of buttons is.
- The header question mark uses the same icon-button shell as the GitHub, docs,
  and theme controls and sits first among them.
- Use icons where they shorten recognition: table, calendar, docs, language,
  filters, metric, retrieval, and reranking.
- In Filter results, Params sits above Length and uses compact numeric inputs
  narrow enough not to dominate the filter row
  in millions for Active Params and Total Params bounds.
- Keep the HAKARI-Bench brand mark at 28px with the same 22% rounded app-icon
  treatment in the leaderboard and documentation headers.
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
- Modal headers should be the short name of the concept being explained, such
  as "Task facets", "Dims", "Overall", or "Borda Score" - not generic labels
  like "Help", and not a descriptive sentence. When the short name would be
  ambiguous on its own, put the group name in the eyebrow chip ("Benchmark
  scope: Overall" becomes an "Overall" header under a "Benchmark scope" chip)
  and let the lead callout carry the description. The trigger's `aria-label`
  keeps both parts. A chip is for disambiguation only; a title that already
  matches the column or control it opens from does not get one.
- Help copy should start with a short explanation, then describe what the
  feature changes, what it filters or displays, and give examples when helpful.
- Write help copy for someone who has never seen a retrieval leaderboard. Every
  modal is read on its own, so explain the vocabulary it uses (nDCG@10, Borda,
  Micro/Macro, RRF, quantization) inside that modal instead of assuming an
  earlier one was read. Prefer a concrete example and a "when to use this" line
  over exhaustive mechanics, and keep internal identifiers such as
  `reranking_hybrid` to a single aside rather than the main explanation.
- Help copy lives in `hakari_bench/viewer/help_text.py` as `HelpCopy` values, not
  inline in the render functions, so the whole explanation set can be read and
  edited as one document.
- Each rendered response serializes its used help copy once in a deduplicated
  page-local JSON registry. Help triggers carry only a compact registry key plus
  their accessible label; do not repeat long help text in every trigger or add a
  network request when a dialog opens.
- Three help surfaces exist, and each answers a different question. The header
  question mark explains the page itself: what a row is, what a score means, and
  in which order the controls apply. Control help explains one control. Score
  column headers (Borda Score, Macro Mean, Micro Mean, Mean Score, Δ vs Base)
  carry their own help, as do the model metadata columns (Active Params, Total
  Params, Max Tokens, Dims), because those values are what a reader looks at
  first and none of them is self-explanatory. A column header with a help icon
  stops filling its cell so the icon stays beside its own label.
- Model and task text filters should document multi-keyword matching. For
  example, `jina bge` matches rows containing either `jina` or `bge`; task
  filters work similarly, and short task names such as `nq` must be supported.
- All in-page dialogs (help, benchmark-doc summary, model detail) share the
  `.hakari-modal` shell so they read as one component family in both themes. Use
  surface background, a strong border, a soft shadow, and a blurred dimmed
  backdrop. Keep an accent icon beside the header concept name and a quiet ghost
  close chip. Because viewer.js sets dialog text with `textContent`, keep the
  scripted id on an inner `<span>` so the static header icon survives updates.

## Documentation Pages

- The standalone `/docs` pages are part of the product, not a separate site:
  reuse the leaderboard chrome so they feel continuous.
- Give every docs page the same header: brand mark linking back to the
  leaderboard, GitHub link, and theme toggle. Load viewer.js so the stored theme
  applies and the toggle works; do not rely on inline scripts because the page
  CSP forbids them.
- Keep both themes intentional here too. Docs colors come from the same tokens as
  the leaderboard; never let docs fall back to a fixed light palette.
- Documentation body copy, list items, and table data use the primary text token
  in each theme. Reserve muted text for card summaries, captions, and secondary
  notes so long-form docs keep strong contrast in both light and dark themes.
- Docs are the one place that departs from the leaderboard's compact type scale.
  These pages are read, not scanned: body copy is 15px at 1.65 line height.
  Keep leading tighter here than typical prose guidance suggests: that guidance
  assumes a proportional face, and the monospaced stack fits fewer characters
  per line and already tracks well, so 1.7-1.8 reads as loose rather than airy.
- The article column itself carries the reading measure, so body copy fills the
  card from edge to edge. Do not cap individual paragraphs inside a wider card:
  a card visibly wider than its own text reads as broken, not as breathing room.
  Extra width at large viewports goes to the outline rail, not to the card.
- Do not set label text in all caps. Small uppercase labels with letter spacing
  fight the monospaced stack and read as shouting at this size; use sentence
  case at a small size and muted color instead.
- Keep the heading levels visibly distinct. h2 opens a section with a rule above
  it and generous space; h3 is close to body size, so it carries a short accent
  bar on its left edge instead of relying on weight alone.
- h2 and h3 headings carry anchor ids and reveal a `#` link on hover so sections
  can be linked directly.
- Group and task pages are long. Give any article with three or more sections an
  "On this page" outline: a sticky rail on the right from 1180px up, and a
  wrapping jump-link card above the article below that width. The outline marks
  the section currently in view.
- Render documentation tables with a distinct header row, light row striping, and
  a rounded border so dense metadata stays scannable. Inline code should read as a
  subtle bordered chip, and code blocks use the faint code background.
- Table cells stay on one line and numeric columns are right-aligned with
  tabular figures, so scores and counts compare down the column. Only columns
  holding long text such as titles or URLs wrap. Never let a short label wrap
  onto five lines to avoid horizontal scrolling.
- The values are what these tables are read for, so headers give up width
  first: header cells set at 11px, wrap freely over several lines, and align to
  the bottom of the row so short and tall labels share one baseline. Do not widen
  a numeric column just to keep `Reranking hybrid nDCG@10` on one line.
- Task identifiers must not break mid-token. Columns wrap only when their
  content exceeds the wrap threshold, which is set above the longest task
  identifier so `legal_bench_corporate_lobbying` stays on one line.
- Tables may reclaim part of the card's horizontal padding. A reading-width
  column cannot hold a nine-column metadata table, and the numbers matter more
  than the card's inner margin.
- Tables that exceed the column pan inside their own `.doc-table-scroll`
  wrapper. Because overlay scrollbars give no hint that columns continue,
  viewer.js sets `data-overflow` on the wrapper and the side that still has
  hidden content fades. Do not rely on the scrollbar alone.
- The docs index leads with its own heading, then the paper reference, then the
  suite list as a responsive grid of compact link cards. Do not show summaries on
  the index; keep longer explanations on the group pages so the index stays fast
  to scan and fits within roughly one screen.

## Leaderboard Table

- The table is the primary interface. Optimize it before optimizing surrounding
  chrome.
- The first column is a leading display-order rank (1, 2, 3 ...) shown before the
  model name, with an empty header. It numbers the visible rows in the current
  sort order. Because this leading rank already communicates standing, the table
  does not carry separate Borda or Mean rank columns; the default sort is Borda
  Score (descending) and that column is the visible sort anchor. The rank index
  pins to the left alongside the model column; hidden/filtered rows are skipped so
  the numbers stay contiguous.
- The Model Name header is a search affordance, not a sort control: it carries a
  small magnifier, opens Filter results when that panel is collapsed, and puts
  the caret in the Model input with its text selected. Alphabetical order answers
  nothing on a leaderboard, while "where is this model?" is a constant question.
  Because the caret can land off-screen or in a panel that just opened, the
  focused filter input takes a clearly visible accent ring, not the default
  hairline focus border.
- Scroll axes are split: vertical scrolling is the browser/page, horizontal
  scrolling stays inside the table via an `overflow-x: auto` wrapper. This keeps
  the surrounding chrome (config panel, footer) fixed while only the table pans
  horizontally. The rank-index and model columns pin to the left during that
  horizontal scroll.
- On page scroll, a JS-driven floating header (viewer.js) pins a copy of the
  column-header row to the viewport top. It mirrors the table's internal
  horizontal scroll and column widths and keeps the rank-index and model columns
  pinned left; it is read-only (`pointer-events: none`) to avoid duplicate
  controls. This is necessary because the horizontal `overflow` wrapper also
  becomes the vertical scroll context, so pure CSS sticky cannot pin the header on
  page scroll. Do not "fix" this by removing the horizontal wrapper — that makes a
  wide table scroll the whole page and drags the footer/chrome off-screen.
- Keep model name sticky and readable during horizontal scroll.
- Keep task columns narrow, but allow Task and Grouped headers to grow vertically
  and wrap long names. Never replace part of a metric label with an ellipsis.
  Repeated suite prefixes may be removed from the subtask line when the remaining
  label is non-empty.
- When a task label has a suite and subtask, use a two-line header treatment
  rather than `Suite::Task`. Treat both lines as one sort button so clicking the
  suite/dataset line or the task line performs the same column sort.
- Documentation icons should sit beside the specific task or suite label they
  explain and remain a separate control from the two-line sort button.
- Model-name hover and row hover backgrounds should match, including sticky
  columns.
- Use model-name background bars as context, not as chart decoration. When a
  score column controls sorting, bars use that Borda, Mean, Macro, Micro, Task,
  or Grouped raw score; non-score sorts fall back to Borda. Bars should be
  subtle, use the accent color, and scale relative to the visible maximum score
  so the top visible score reaches 100% without moving the minimum score to zero.
- If there is only one visible row, the bar can fill to 100%; if there are no
  visible rows, no bar should render.

## Score Cells

- Score cells must remain compact and numerically aligned.
- Standing is shown only by the leading rank-index column, not by dedicated Borda
  or Mean rank columns. Keep Borda Score as the visible, default-sorted aggregate.
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
- The light-mode heat ramp must keep a clear green (positive) or red (negative)
  hue across its whole range. Increase darkness with magnitude for emphasis, but
  the strongest cells must still read as colored, not collapse to near-black —
  otherwise the best and worst results lose their signal exactly where it matters.
- Light-mode z-score colors should be dark enough to remain legible at compact
  table font sizes because STD uses text color without a filled background.
- STD/z-score display should not use filled backgrounds or borders. Preserve a
  stable numeric width, and express positive/negative strength through the text
  color of the score and sigma string.

## Variant Labels

- Keep row metadata short. Prefer `Dims`, `Quant`, `Rescore`, and
  `Sparse pruning` over longer technical labels when the displayed values are
  compact.
- Show a `Rescore` table column immediately after `Quant` only while the Rescore
  efficiency-variant toggle is active. Put `rescore` in that column for rescore
  variants and leave ordinary rows empty so mixed result sets remain scannable.
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

# EaseStore — Amazon.de Seller Analytics (private)

Product repository: the seller workbook, its manuals, and the browser-based
analysis tools for easestore.de.

## Structure

| Path | What it is |
|---|---|
| `tools/seasonality/index.html` | Seasonality Analyzer — drop a Helium 10 search-volume export, get amplitude / ramp month / YoY direction / verdicts. 100% client-side, single file, no backend. |
| `workbook/` | Amazon.de Seller Workbook v3 (xlsx) — 11 sheets: seasonality, order timing, unit economics, selection gates, niche scorecard, order size (newsvendor), PPC planner, cash flow, monthly P&L, money recovery, review themes. |
| `manuals/` | Sheet 1 user manual (EN md/pdf + RU pdf) — future in-app help content. |
| `build/` | Python sources that generate the workbook and PDF manuals. Edit these, not the artifacts. |

## Deploying the tool (Squarespace main site)

Squarespace can't host raw HTML files, so the tool lives on a free static host
connected to this repo (Netlify or Cloudflare Pages, both support private
repos), on a subdomain: `tools.easestore.de` via a CNAME record in the
Squarespace domain panel. Main site links to it. Auto-deploys on every push.

## Rules

- Formulas in the workbook are verified against independent calculations
  before every release (see build scripts).
- No Amazon fee tables are hardcoded anywhere — fees change every Dec/Jan.
- The analyzer must stay fully client-side: "your file never leaves your
  browser" is a product promise.

© EaseStore 2026. All rights reserved. Not financial advice.

# Sheet 1 — Seasonality: User Manual

**What this sheet answers:** Is demand for this niche seasonal, when does it ramp, and is the category growing or dying? You run it **before** any profit math — it takes 10 minutes per niche and kills more bad candidates than any other check.

---

## 1. Pick the right keyword (this decides everything)

Measure the **parent keyword** — the product category, phrased the way a buyer types it when they know *what* they want but not *which one*.

**The satisfaction test.** Imagine the person who typed the keyword. Would they be happy landing on your product?

| Their answer | What the keyword is | Use it for |
|---|---|---|
| Mostly no (they wanted something else from that department) | Too broad ("küche", "küchenzubehör") | Nothing |
| Yes — now choosing between brands | **Parent** ("schubladen organizer küche") | **This sheet** |
| Yes — and the phrase already names your exact variant | Child ("besteckkasten bambus 30cm") | Listing title & PPC, later |

Two rules that follow:

- **Children inherit the parent's curve** unless the extra word changes *why* people buy (gift sets, "kinder", seasonal use). If you plan to target such a child, check its curve separately — it may need its own stock timing.
- **Never measure a listing younger than 18 months.** A young listing's chart is launch curve + season, inseparable. Measure the category on data that existed before the listing did.

## 2. Get the data (Helium 10 Cerebro)

1. Open Cerebro → tab **Analyze Keywords** (not *Find Keywords* — that's for discovering terms later).
2. **Switch the marketplace flag to Amazon.de.** The default is often Amazon.com — US data is useless here.
3. Enter the parent **plus its 2–3 biggest children in one query, comma-separated.** One query = one search credit regardless of how many keywords it holds — batch per niche to protect your monthly credits.
4. Click the chart icon next to the search volume → set the period to 2 years / all time → export via the hamburger menu, or read the values off the chart.

## 3. Convert weekly points to months

The history gives ~4 data points per month. Each point is a weekly *sample of the monthly volume* at that date — so **average the points inside each calendar month. Never sum.**

- Summing counts the same demand 4× — and inflates 5-point months by ~25%, creating fake spikes and a false amplitude.
- Self-check: one recent point should be in the same ballpark as the keyword's current search volume in Cerebro's main table. Same ballpark → average is correct.

## 4. Enter the data (yellow cells only)

- Your data window can start in **any month** — the sheet is a calendar profile, not a calendar year. The only rule: **each value goes into its calendar-month row.** August 2024 belongs in the Aug row of "Volume yr 1", January 2025 in the Jan row of yr 1, August 2025 in Aug of yr 2.
- "Year 1" = the older 12 months, "Year 2" = the newer 12.
- A 25-month window (e.g. Aug 2024 – Aug 2026) has one month too many: **drop the current, unfinished month.**
- Alignment smell test: does the peak land in a month that makes real-world sense for this product? Organizers peak in January (New Year decluttering), cycling peaks in summer. A peak in a nonsense month usually means the rows are shifted.

## 5. Read the results

| Output | Meaning | Bands |
|---|---|---|
| **Amplitude** | Best month ÷ worst month — the shape of the year | <1.5 flat · 1.5–2.5 moderate · 2.5–4 strong · >4 single-season (capital trap for a first product) |
| **Top-4 share** | How concentrated the year is | >60% = a four-month business carrying twelve months of costs |
| **Ramp month** | First month the index crosses 1.00 upward (Dec→Jan wrap handled) | Stock must land ~4 weeks earlier → feeds Sheet 2. If the ramp is Jan, the on-stock date falls in early December — Q4 congestion — so target mid-November instead |
| **YoY / Demand direction** | Is the category growing? | >+5% growing · −5…+5% flat · −5…−15% cooling → verify on Trends · <−15% declining → drop |
| **Months with data** | Guard | The verdict refuses to fire until all 12 months are filled. A true zero-demand month = extreme single-season warning |

Amplitude and YoY answer **different questions**: amplitude is the shape of the year; YoY is whether the tide rises or falls. A niche can pass one and fail the other — the küche example below passed amplitude (2.04) and failed direction (−8.9%).

## 6. Verify with Google Trends (2 minutes, free)

Trends is the independent second opinion on **shape and direction** — never on volume (its values are relative, 0–100 to the window's peak).

- **Use a broader term than on Amazon.** Trends samples all of Google; a 3-word niche phrase sits at its noise floor and draws a jagged, unreliable line. Drop the qualifier: "schubladen organizer", not "schubladen organizer küche". Region Germany, 5 years.
- **Ignore the "+X% vs previous period" badge** — it compares against years when the term barely existed.
- **Read the peaks across years.** Same peak month as your Cerebro data = shape confirmed. Peak heights stepping down year after year = genuine decline; a boom settling onto a plateau above the pre-boom level = normalization, acceptable.
- **Vocabulary check.** German product vocabulary shifts (besteckkasten → organizer). Use Trends' *compare* mode with the traditional synonym. Both sliding together = the category is cooling. One holds while the other falls = a naming shift, not lost demand — recheck via Xray page-1 revenue (the money view, not the words view).

## 7. Decide

| Situation | Action |
|---|---|
| Flat/moderate amplitude + flat/growing direction | Pass. → Sheet 3 (unit economics) |
| Strong amplitude, ramp still reachable | → Sheet 2: is the order-by date in the future? |
| Single-season, or zero-demand months | Drop as a first product |
| Cooling direction | Trends + vocabulary check decide; enter only with a strong differentiation angle |
| Declining direction | Drop unless Trends shows a clearly temporary dip |

Enter amplitude, top-4 share and the direction verdict into the niche's column on Sheet 5 (scorecard).

## Worked example (real run)

*schubladen organizer küche*, Amazon.de, 24 months to Aug 2026: amplitude **2.04** (moderate ✓), top-4 share **41.6%** (✓), peak **Jan** / trough **Jun** (New-Year decluttering — plausible, alignment confirmed), ramp **Jan** → stock by mid-November → order by ~September. But YoY **−8.9%**, negative in 10 of 12 months → COOLING. Trends 5y ("schubladen organizer"): January peaks 73 → 100 (2023) → 92 → 68 → 55 — a boom peaking in early 2023 and stepping down since, now at pre-boom levels. Pending the vocabulary check (vs "besteckkasten"), the niche **fails the flat-or-rising rule** despite its friendly seasonality. That is the sheet doing its job: the amplitude said "fine", the direction said "no".

## Common mistakes (each one produces confident wrong answers)

1. Measuring a department term ("küchenzubehör") — meaningless demand, competition and curve.
2. Measuring your exact variant — too thin, noise reads as seasonality.
3. **Summing** weekly points instead of averaging.
4. Typing the export in row order instead of calendar-month rows (shifts the whole curve).
5. Trusting a jagged Trends line on a 3-word term instead of broadening it.
6. Reading the "+X%" Trends badge as growth.
7. Using BSR for amplitude — ranks are relative and systematically understate seasonal swings.
8. Measuring a listing under 18 months old instead of the category.

---

*v1 · 2026-08-19 · internal draft — future in-app help content for the easestore.de tool. Educational material, not financial advice.*

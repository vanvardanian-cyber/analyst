#!/usr/bin/env python3
"""Sheet 1 Seasonality user manual -> styled PDF (reportlab platypus)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether)

ACCENT = colors.HexColor("#1F4E79")
GREY   = colors.HexColor("#666666")
LIGHT  = colors.HexColor("#EDF2F8")
BORDER = colors.HexColor("#C9D6E4")

st_title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=ACCENT)
st_sub   = ParagraphStyle("s", fontName="Helvetica", fontSize=9.5, leading=13, textColor=GREY)
st_h     = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=ACCENT, spaceBefore=12, spaceAfter=4)
st_b     = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=13.5, alignment=TA_LEFT, spaceAfter=5)
st_bul   = ParagraphStyle("u", parent=st_b, leftIndent=10, bulletIndent=2, spaceAfter=3)
st_cell  = ParagraphStyle("c", fontName="Helvetica", fontSize=8.5, leading=11.5)
st_cellb = ParagraphStyle("cb", parent=st_cell, fontName="Helvetica-Bold")
st_note  = ParagraphStyle("n", parent=st_b, textColor=GREY, fontSize=8.5, leading=11.5)

doc = SimpleDocTemplate("/home/claude/manual-sheet1-seasonality.pdf", pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm,
                        title="Sheet 1 - Seasonality: User Manual", author="easestore.de")
S = []
def h(t): S.append(Paragraph(t, st_h))
def p(t): S.append(Paragraph(t, st_b))
def bul(t): S.append(Paragraph(t, st_bul, bulletText="•"))
def tbl(header, rows, widths):
    data = [[Paragraph(x, st_cellb) for x in header]] + \
           [[Paragraph(x, st_cell) for x in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    S.append(t); S.append(Spacer(1, 6))

S.append(Paragraph("Sheet 1 — Seasonality: User Manual", st_title))
S.append(Spacer(1, 3))
S.append(Paragraph("Amazon.de Seller Workbook · internal v1 · 2026-08-19 · future in-app help content, easestore.de", st_sub))
S.append(Spacer(1, 6))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
S.append(Spacer(1, 6))
p("<b>What this sheet answers:</b> Is demand for this niche seasonal, when does it ramp, and is the category growing or dying? "
  "Run it <b>before</b> any profit math — it takes 10 minutes per niche and kills more bad candidates than any other check.")

h("1. Pick the right keyword (this decides everything)")
p("Measure the <b>parent keyword</b> — the product category, phrased the way a buyer types it when they know <i>what</i> "
  "they want but not <i>which one</i>. Apply the <b>satisfaction test</b>: imagine the person who typed the keyword — "
  "would they be happy landing on your product?")
tbl(["Their answer", "What the keyword is", "Use it for"],
    [["Mostly no — they wanted something else from that department", "Too broad (“kueche”, “kuechenzubehoer”)", "Nothing"],
     ["Yes — now choosing between brands", "<b>Parent</b> (“schubladen organizer kueche”)", "<b>This sheet</b>"],
     ["Yes — and the phrase already names your exact variant", "Child (“besteckkasten bambus 30cm”)", "Listing title &amp; PPC, later"]],
    [62*mm, 62*mm, 50*mm])
bul("<b>Children inherit the parent's curve</b> unless the extra word changes <i>why</i> people buy (gift sets, “kinder”, "
    "seasonal use). A child you plan to target with its own driver needs its own curve check and its own stock timing.")
bul("<b>Never measure a listing younger than 18 months.</b> A young listing's chart is launch curve + season, inseparable. "
    "Measure the category on data that existed before the listing did.")

h("2. Get the data (Helium 10 Cerebro)")
bul("Open Cerebro, tab <b>Analyze Keywords</b> (not <i>Find Keywords</i> — that one discovers new terms, for later).")
bul("<b>Switch the marketplace flag to Amazon.de.</b> The default is often Amazon.com — US data is useless here.")
bul("Enter the parent <b>plus its 2–3 biggest children in one query</b>, comma-separated. One query = one search credit "
    "regardless of how many keywords it holds — batch per niche to protect your monthly credits.")
bul("Click the chart icon next to the search volume, set the period to 2 years / all time, export via the hamburger menu.")

h("3. Convert weekly points to months")
p("The history gives ~4 data points per month. Each point is a weekly <i>sample of the monthly volume</i> at that date — "
  "so <b>average the points inside each calendar month. Never sum.</b> Summing counts the same demand 4x and inflates "
  "5-point months by ~25%, creating fake spikes and a false amplitude.")
p("<b>Self-check:</b> one recent point should be in the same ballpark as the keyword's current search volume in Cerebro's "
  "main table. Same ballpark = average is correct.")

h("4. Enter the data (yellow cells only)")
bul("Your data window can start in <b>any month</b> — the sheet is a calendar profile, not a calendar year. The only rule: "
    "<b>each value goes into its calendar-month row.</b> Aug 2024 belongs in the Aug row of Year 1; Jan 2025 in the Jan row of Year 1; Aug 2025 in Aug of Year 2.")
bul("“Year 1” = the older 12 months, “Year 2” = the newer 12. A 25-month window has one month too many: "
    "<b>drop the current, unfinished month.</b>")
bul("<b>Alignment smell test:</b> does the peak land in a month that makes real-world sense? Organizers peak in January "
    "(New Year decluttering), cycling peaks in summer. A peak in a nonsense month usually means the rows are shifted.")

h("5. Read the results")
tbl(["Output", "Meaning", "Bands / rule"],
    [["<b>Amplitude</b>", "Best month / worst month — the shape of the year",
      "&lt;1.5 flat · 1.5–2.5 moderate · 2.5–4 strong · &gt;4 single-season (capital trap for a first product)"],
     ["<b>Top-4 share</b>", "How concentrated the year is",
      "&gt;60% = a four-month business carrying twelve months of costs"],
     ["<b>Ramp month</b>", "First month the index crosses 1.00 upward (Dec-to-Jan wrap handled)",
      "Stock lands ~4 weeks earlier — feeds Sheet 2. A January ramp puts the on-stock date in early December (Q4 congestion): target mid-November instead"],
     ["<b>YoY / direction</b>", "Is the category growing?",
      "&gt;+5% growing · −5…+5% flat · −5…−15% cooling (verify on Trends) · &lt;−15% declining (drop)"],
     ["<b>Months with data</b>", "Guard",
      "The verdict refuses to fire until all 12 months are filled; a true zero-demand month = extreme single-season warning"]],
    [30*mm, 58*mm, 86*mm])
p("Amplitude and YoY answer <b>different questions</b>: amplitude is the shape of the year, YoY is whether the tide rises "
  "or falls. A niche can pass one and fail the other — the worked example below passed amplitude (2.04) and failed direction (−8.9%).")

h("6. Verify with Google Trends (2 minutes, free)")
p("Trends is the independent second opinion on <b>shape and direction</b> — never on volume (its values are relative, 0–100 to the window's peak).")
bul("<b>Use a broader term than on Amazon.</b> Trends samples all of Google; a 3-word niche phrase sits at its noise floor "
    "and draws a jagged, unreliable line. Drop the qualifier: “schubladen organizer”, not “schubladen organizer kueche”. Region Germany, 5 years.")
bul("<b>Ignore the “+X% vs previous period” badge</b> — it compares against years when the term barely existed.")
bul("<b>Read the peaks across years.</b> Same peak month as Cerebro = shape confirmed. Peak heights stepping down year "
    "after year = genuine decline; a boom settling onto a plateau above pre-boom levels = normalization, acceptable.")
bul("<b>Vocabulary check.</b> German product vocabulary shifts (besteckkasten vs. organizer). Use Trends' compare mode with the "
    "traditional synonym. Both sliding together = the category is cooling. One holds while the other falls = a naming shift, "
    "not lost demand — recheck via Xray page-1 revenue (the money view, not the words view).")

h("7. Decide")
tbl(["Situation", "Action"],
    [["Flat / moderate amplitude + flat or growing direction", "Pass. Continue to Sheet 3 (unit economics)"],
     ["Strong amplitude, ramp still reachable", "Sheet 2: is the order-by date still in the future?"],
     ["Single-season, or zero-demand months", "Drop as a first product"],
     ["Cooling direction", "Trends + vocabulary check decide; enter only with a strong differentiation angle"],
     ["Declining direction", "Drop unless Trends shows a clearly temporary dip"]],
    [95*mm, 79*mm])
p("Enter amplitude, top-4 share and the direction verdict into the niche's column on Sheet 5 (scorecard).")

ex = [Paragraph("Worked example (real run)", st_h),
      Paragraph("<i>schubladen organizer kueche</i>, Amazon.de, 24 months to Aug 2026: amplitude <b>2.04</b> (moderate, pass), "
        "top-4 share <b>41.6%</b> (pass), peak <b>Jan</b> / trough <b>Jun</b> — the New-Year-decluttering pattern, so the row "
        "alignment is confirmed. Ramp <b>Jan</b>: stock by mid-November, order by ~September. But YoY <b>−8.9%</b>, negative in "
        "10 of 12 months: COOLING. Trends 5y (“schubladen organizer”): January peaks 73 → 100 (2023) → 92 → 68 → 55 — "
        "a boom peaking in early 2023 and stepping down since, now at pre-boom levels. Pending the vocabulary check vs. "
        "“besteckkasten”, the niche <b>fails the flat-or-rising rule</b> despite friendly seasonality. That is the sheet "
        "doing its job: amplitude said “fine”, direction said “no”.", st_b)]
S.append(KeepTogether(ex))

h("Common mistakes (each produces confident wrong answers)")
for m in ["Measuring a department term (“kuechenzubehoer”) — meaningless demand, competition and curve.",
          "Measuring your exact variant — too thin; noise reads as seasonality.",
          "<b>Summing</b> weekly points instead of averaging.",
          "Typing the export in row order instead of calendar-month rows (shifts the whole curve).",
          "Trusting a jagged Trends line on a 3-word term instead of broadening it.",
          "Reading the “+X%” Trends badge as growth.",
          "Using BSR for amplitude — ranks are relative and systematically understate seasonal swings.",
          "Measuring a listing under 18 months old instead of the category."]:
    bul(m)

S.append(Spacer(1, 8))
S.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
S.append(Spacer(1, 3))
S.append(Paragraph("Educational material, not financial advice. Data sources: Helium 10 Cerebro (Amazon.de), Google Trends (DE, 5y), "
                   "Amazon Product Opportunity Explorer as cross-check. Method: classical multiplicative decomposition "
                   "(Hyndman &amp; Athanasopoulos, otexts.com/fpp3).", st_note))

doc.build(S)
print("done")

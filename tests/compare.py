#!/usr/bin/env python3
"""Judge the page against the independent mirror.

Reads .out/page.json (what the page displayed) and .out/mirror.json (what the
workbook maths says it should have displayed) and reports every mismatch.
Also checks that the RU page shows numerically identical results to EN.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
page = json.load(open(os.path.join(HERE, ".out", "page.json")))
mir = json.load(open(os.path.join(HERE, ".out", "mirror.json")))

fails, checks = [], []


SPACES = "\u00a0\u202f\u2009 "


def num(s):
    """First number in a displayed string, in either page locale.

    EN renders en-US (€99,240 / 1.92); RU renders ru-RU (€99\u00a0240 / 1,92).
    """
    if s is None:
        return None
    t = s.replace("\u2212", "-")
    for c in SPACES:
        t = t.replace(c, "")
    m = re.search(r"-?\d[\d.,]*", t)
    if not m:
        return None
    tok = m.group(0).rstrip(".,")
    if "." in tok:                       # dot decimal -> commas are thousands separators
        tok = tok.replace(",", "")
    elif "," in tok:                     # comma is a decimal point only if 1-2 digits follow
        head, _, tail = tok.rpartition(",")
        tok = head.replace(",", "") + ("." + tail if len(tail) <= 2 else tail)
    return float(tok)


def eq(label, shown, expected, tol=0.005):
    got = num(shown) if isinstance(shown, str) else shown
    ok = got is not None and expected is not None and abs(got - expected) <= tol
    checks.append((ok, label, shown, expected))
    if not ok:
        fails.append(f"{label}: page shows {shown!r}, mirror says {expected!r}")


def same(label, a, b):
    ok = a == b
    checks.append((ok, label, a, b))
    if not ok:
        fails.append(f"{label}: {a!r} != {b!r}")


en = page["en"]

# ---- Gate 0: the nine Block A rows must be present, in the right groups,
#      and every answer scenario must land on the status the mirror predicts.
g0, m0 = en["gate0"], mir["gate0"]
EXPECTED_ROWS = [("ppe", "q0a"), ("elec", "q0a"), ("kids", "q0a"), ("skin", "q0a"),
                 ("health", "q0a"), ("load", "q0a"), ("ip", "q0a"),
                 ("gpsr", "q0b"), ("epr", "q0b"), ("brand", "q0c")]
same("G0 question count", len(g0["questions"]), len(EXPECTED_ROWS))
same("G0 rows and groups", [(q["id"], q["group"]) for q in g0["questions"]], EXPECTED_ROWS)
same("G0 Block A row count (workbook Sheet 4 C5:C13)",
     sum(1 for q in g0["questions"] if q["group"] in ("q0a", "q0b")), 9)
for name, exp in m0.items():
    run = en["gate0Runs"][name]
    same(f"G0 [{name}] status",   run["status"],   exp["status"])
    same(f"G0 [{name}] tally",    run["progress"], exp["progress"])
    if exp["status"] is None:
        same(f"G0 [{name}] chip stays unrun", run["chip"].lower(), "not run")
        same(f"G0 [{name}] no verdict shown", run["headline"], None)
    else:
        ok = bool(run["headline"])
        checks.append((ok, f"G0 [{name}] verdict shown", run["headline"], "a headline"))
        if not ok:
            fails.append(f"G0 [{name}] verdict shown: nothing rendered")
        # a red gate must still not block: the hint always offers the next gate
        if run["status"] == "red":
            ok2 = "Gate 1" in run["hint"]
            checks.append((ok2, f"G0 [{name}] red does not hard-block", run["hint"], "mentions Gate 1"))
            if not ok2:
                fails.append(f"G0 [{name}] red hint does not point on to Gate 1")

# ---- Gate 1
g1, m1 = en["gate1"], mir["gate1"]
eq("G1 amplitude",        g1["tiles"].get("Amplitude"),         round(m1["amplitude"], 2))
eq("G1 consistency",      g1["tiles"].get("Consistency"),       round(m1["consistency"], 2))
eq("G1 seasonal strength", g1["tiles"].get("Seasonal strength"), round(m1["strength"], 2))
eq("G1 top-4 share %",    g1["tiles"].get("Top-4 share"),       round(m1["top4"] * 100, 1), 0.05)
eq("G1 YoY %",            g1["tiles"].get("YoY"),               round(m1["yoy"] * 100, 1), 0.05)
same("G1 ramp month",     g1["tiles"].get("Ramp month"),        m1["ramp"])
eq("G1 months used",      g1["meta"],                            m1["monthsUsed"])

# ---- Gate 2
g2, m2 = en["gate2"], mir["gate2"]
eq("G2 top-10 revenue",       g2["tiles"].get("Top-10 revenue"),        m2["top10Rev"], 1)
eq("G2 top ASIN share %",     g2["tiles"].get("Top ASIN share"),        round(m2["topShare"] * 100, 1), 0.05)
eq("G2 listings >500 reviews", g2["tiles"].get("Reviews >500"),         m2["over500"])
eq("G2 median top-10 reviews", g2["tiles"].get("Median top-10 reviews"), m2["medTop10Reviews"], 1)
eq("G2 CN+HK share %",        g2["tiles"].get("CN+HK share"),           round(m2["cnhkShare"] * 100), 0.5)
eq("G2 median price",         g2["tiles"].get("Median price"),          m2["medPrice"], 0.005)
# the meta line starts with the file name — count only from after the separator
meta_tail = (g2["meta"] or "").split("·", 1)[-1]
meta_nums = [num(x) for x in re.findall(r"\d[\d.,]*", meta_tail)]
same("G2 unique listings",              meta_nums[0] if meta_nums else None, float(m2["unique"]))
same("G2 sponsored duplicates removed", meta_nums[1] if len(meta_nums) > 1 else None, float(m2["dupes"]))
same("G2 off-niche ads dropped",        meta_nums[2] if len(meta_nums) > 2 else None, float(m2["offNiche"]))

# ---- Gate 3 (workbook Sheet 3, cell for cell)
g3, m3 = en["gate3"], mir["gate3"]
eq("G3 net revenue",        g3["tiles"].get("Net revenue"),         round(m3["net"], 2))
eq("G3 Amazon payout",      g3["tiles"].get("Amazon payout / unit"), round(m3["payout"], 2))
eq("G3 landed cost",        g3["tiles"].get("Landed cost / unit"),  round(m3["landed"], 2))
eq("G3 contribution margin", g3["tiles"].get("Contribution margin"), round(m3["cm"], 2))
eq("G3 margin %",           g3["tiles"].get("Margin % of net"),     round(m3["marginPct"], 1), 0.05)
eq("G3 breakeven ACOS %",   g3["tiles"].get("Breakeven ACOS"),      round(m3["beAcosPct"], 1), 0.05)
eq("G3 max EXW",            g3["tiles"].get("Max EXW at 35%"),      round(m3["maxExw"], 2))

# ---- Gate 4
g4, m4 = en["gate4"], mir["gate4"]
eq("G4 keyword sales total", g4["tiles"].get("Keyword sales, total"), m4["totalSales"], 1)
same("G4 best launch keyword", g4["tiles"].get("Best launch keyword"), m4["best"])
eq("G4 suggested P10",       g4["tiles"].get("Suggested P10"),        round(m4["p10"]), 1)
eq("G4 suggested P90",       g4["tiles"].get("Suggested P90"),        round(m4["p90"]), 1)
same("G4 overall status",    g4["status"],                            m4["overall"])

# ---- Dossier: the Sheet 5 scorecard, driven through the real UI
D, mD = en["dossier"], mir["dossier"]

def drow(table, label, section=None):
    for r in table["rows"]:
        if r["label"].split(" weight")[0].strip() == label and (section is None or r["section"] == section):
            return r["cells"]
    return None

same("D chip after first save",  D["afterA"]["chip"], "1 of 10")
same("D columns after A",        D["afterA"]["columns"], ["nicheA"])
same("D niche A weighted score", drow(D["afterA"], "Weighted score (0–100)"), [str(mD["nicheA"]["score"])])
same("D niche A hard gates",     drow(D["afterA"], "Hard gates"), [mD["nicheA"]["hard"]])
same("D niche A verdict",        drow(D["afterA"], "Verdict"), [mD["nicheA"]["verdict"]])

# every 0-2 band, criterion by criterion, against Sheet 5's bands
SCORE_SECTION = "Scores (0–2 each, Sheet 5 bands)"
DLABELS = ["Page-1 revenue, €/month", "Top ASIN share of page revenue",
           "Page-1 listings above 500 reviews", "Fresh entrants (<12 mo, >€3k/mo)",
           "Weak competitor ≤4.3★ to attack", "China + Hong Kong share of page",
           "Seasonality amplitude", "Top-4 months’ share of the year",
           "Contribution margin, % of net", "First order + compliance cash, €"]
for i, label in enumerate(DLABELS):
    same(f"D band [{label}]", drow(D["afterA"], label, SCORE_SECTION), [str(mD["nicheA"]["scores"][i])])

# niche B: single-season. Blank cash must blank the score (Sheet 5 D32), and once
# the cash is typed the disqualification must still force DROP (D34).
same("D columns after B",         D["afterB"]["columns"], ["nicheA", "nicheB"])
same("D niche B score is blank",  drow(D["afterB"], "Weighted score (0–100)")[1], "—")
same("D niche B hard gates",      drow(D["afterB"], "Hard gates")[1], mD["nicheB"]["hard"])
same("D niche B verdict is blank", drow(D["afterB"], "Verdict")[1], "—")
ok = "cash need" in (D["saveStatusB"] or "")
checks.append((ok, "D blank input is named in the save status", D["saveStatusB"], "mentions cash need"))
if not ok:
    fails.append("D save status did not say which input was blank")
same("D niche B score once cash typed",
     drow(D["afterBcash"], "Weighted score (0–100)")[1], str(mD["nicheB_withCash"]["score"]))
same("D disqualified still DROPs despite score",
     drow(D["afterBcash"], "Verdict")[1], mD["nicheB_withCash"]["verdict"])
same("D re-saving a name overwrites, not duplicates", D["afterBcash"]["columns"], ["nicheA", "nicheB"])

# persistence, cap, removal
same("D survives a reload",          D["afterReload"]["columns"], ["nicheA", "nicheB"])
same("D holds exactly 10",           len(D["atCap"]["columns"]), 10)
same("D refuses the 11th",           len(D["afterOverflow"]["columns"]), 10)
ok = "10" in (D["overflowStatus"] or "")
checks.append((ok, "D says why the 11th was refused", D["overflowStatus"], "mentions the cap"))
if not ok:
    fails.append("D overflow status did not explain the cap")
same("D print export is one page at 10 niches", D["printPages"], 1)
same("D print hides the gates",                D["printHidesGates"], True)
same("D removal drops one column",   len(D["afterDelete"]["columns"]), 9)
same("D removal drops the right one", "nicheA" in D["afterDelete"]["columns"], False)

# ---- RU parity: every tile that holds a number must hold the SAME number
ru = page["ru"]
for gate in ("gate1", "gate2", "gate3", "gate4"):
    en_t, ru_t = en[gate]["tiles"], ru[gate]["tiles"]
    same(f"RU {gate}: tile count", len(ru_t), len(en_t))
    for (ek, ev), (rk, rv) in zip(en_t.items(), ru_t.items()):
        a, b = num(ev), num(rv)
        if a is not None or b is not None:
            same(f"RU {gate}: {ek} value", b, a)
    same(f"RU {gate}: status", ru[gate]["status"], en[gate]["status"])
same("RU gate0: question count", len(ru["gate0"]["questions"]), len(en["gate0"]["questions"]))
same("RU gate0: rows and groups",
     [(q["id"], q["group"]) for q in ru["gate0"]["questions"]],
     [(q["id"], q["group"]) for q in en["gate0"]["questions"]])
for name in mir["gate0"]:
    same(f"RU G0 [{name}] status", ru["gate0Runs"][name]["status"], en["gate0Runs"][name]["status"])
ruD = ru["dossier"]
same("RU dossier columns", ruD["afterA"]["columns"], D["afterA"]["columns"])
same("RU dossier row count", len(ruD["afterA"]["rows"]), len(D["afterA"]["rows"]))
for i, (a, b) in enumerate(zip(D["afterBcash"]["rows"], ruD["afterBcash"]["rows"])):
    an = [num(c) for c in a["cells"]]
    bn = [num(c) for c in b["cells"]]
    if any(v is not None for v in an) or any(v is not None for v in bn):
        same(f"RU dossier row {i} ({a['label'][:38]})", bn, an)
same("RU check-row count (gate 2)", len(ru["gate2"]["checks"]), len(en["gate2"]["checks"]))
same("RU check-row count (gate 4)", len(ru["gate4"]["checks"]), len(en["gate4"]["checks"]))

# ---- Real Helium 10 exports, if present. This is the only lane that proves the
#      PARSING works: real headers ("Price  €"), real thousands separators
#      ("4,806.42"), real dates ("Nov 27, 2025"), a BOM, blank cells and
#      sponsored repeats.
if page.get("real") and mir.get("real"):
    R, mR = page["real"], mir["real"]
    same("REAL gate 1 parsed without error", R["g1error"], None)
    same("REAL gate 2 parsed without error", R["g2error"], None)
    same("REAL no JS errors", R["pageErrors"], [])
    eq("REAL G1 amplitude",         R["g1tiles"].get("Amplitude"),         round(mR["gate1"]["amplitude"], 2))
    eq("REAL G1 consistency",       R["g1tiles"].get("Consistency"),       round(mR["gate1"]["consistency"], 2))
    eq("REAL G1 seasonal strength", R["g1tiles"].get("Seasonal strength"), round(mR["gate1"]["strength"], 2))
    eq("REAL G1 top-4 share %",     R["g1tiles"].get("Top-4 share"),       round(mR["gate1"]["top4"] * 100, 1), 0.05)
    eq("REAL G1 YoY %",             R["g1tiles"].get("YoY"),               round(mR["gate1"]["yoy"] * 100, 1), 0.05)
    same("REAL G1 ramp month",      R["g1tiles"].get("Ramp month"),        mR["gate1"]["ramp"])
    eq("REAL G1 months used",       R["g1meta"],                            mR["gate1"]["monthsUsed"])
    eq("REAL G2 top-10 revenue",       R["g2tiles"].get("Top-10 revenue"),        mR["gate2"]["top10Rev"], 1)
    eq("REAL G2 top ASIN share %",     R["g2tiles"].get("Top ASIN share"),        round(mR["gate2"]["topShare"] * 100, 1), 0.05)
    eq("REAL G2 listings >500 reviews", R["g2tiles"].get("Reviews >500"),         mR["gate2"]["over500"])
    eq("REAL G2 median top-10 reviews", R["g2tiles"].get("Median top-10 reviews"), mR["gate2"]["medTop10Reviews"], 1)
    eq("REAL G2 CN+HK share %",        R["g2tiles"].get("CN+HK share"),           round(mR["gate2"]["cnhkShare"] * 100), 0.5)
    eq("REAL G2 median price",         R["g2tiles"].get("Median price"),          mR["gate2"]["medPrice"], 0.005)
    rmeta = (R["g2meta"] or "").split("·", 1)[-1]
    rnums = [num(x) for x in re.findall(r"\d[\d.,]*", rmeta)]
    same("REAL G2 unique listings",              rnums[0] if rnums else None, float(mR["gate2"]["unique"]))
    same("REAL G2 sponsored duplicates removed", rnums[1] if len(rnums) > 1 else None, float(mR["gate2"]["dupes"]))
    same("REAL G2 off-niche ads dropped",        rnums[2] if len(rnums) > 2 else None, float(mR["gate2"]["offNiche"]))
    # the export DOES carry Seller Age, so the shop-age note must state the truth
    same("REAL G2 export carries Seller Age", mR["gate2"]["hasSellerAgeColumn"], True)
    fresh_note = next((n["note"] for n in R["g2notes"] if n["label"] and "Fresh entrants" in n["label"]), "")
    expect = f"{mR['gate2']['freshOnNewShops']} of them on seller accounts under 18 months"
    ok = expect in fresh_note
    checks.append((ok, "REAL G2 new-shop count matches the data", fresh_note[-70:], expect))
    if not ok:
        fails.append(f"REAL G2 fresh-entrant note does not say '{expect}'")
else:
    print("(real Helium 10 exports absent — parsing lane skipped)\n")

# ---- Partial-block rule, pinned with literal expectations rather than mirror
#      agreement (the mirror moved with the page, so agreement proves nothing).
#      On COMPLETE data the rule must be a no-op; the numbers below are the ones
#      the page produced before the rule existed.
same("G1 complete data still gives 3 full blocks, no part-year",
     "part-year" in (en["gate1"]["meta"] or ""), False)
same("G1 complete-data consistency unchanged by the rule",
     en["gate1"]["tiles"].get("Consistency"), "0.96")
same("G1 complete-data amplitude unchanged by the rule",
     en["gate1"]["tiles"].get("Amplitude"), "1.92")
ok = any("prior year" in v["text"] for v in en["gate1"]["verdicts"])
checks.append((ok, "G1 three full years still report a prior-year YoY",
               [v["text"][:60] for v in en["gate1"]["verdicts"]], "one mentions prior year"))
if not ok:
    fails.append("G1 lost the prior-year YoY on three complete years")

if page.get("real") and mir.get("real"):
    R, mR = page["real"], mir["real"]
    same("REAL G1 keeps the leftover months as a part-year block", mR["gate1"]["blocks"], 3)
    same("REAL G1 part-year is 11 months",   mR["gate1"]["partialMonths"], 11)
    same("REAL G1 only two whole years",     mR["gate1"]["fullBlocks"], 2)
    same("REAL G1 no prior-year YoY off a part-year", mR["gate1"]["yoyPrev"], None)
    ok = "part-year of 11 months" in (R["g1meta"] or "")
    checks.append((ok, "REAL G1 card says the block is a part-year", R["g1meta"], "says part-year of 11 months"))
    if not ok:
        fails.append("REAL G1 card does not disclose the part-year block")
    # a generic export header must not become the dossier's keyword name
    ok = R["g1title"] not in ("Search Volume", "Volume", "SV")
    checks.append((ok, "REAL G1 title is not the generic column header", R["g1title"], "not 'Search Volume'"))
    if not ok:
        fails.append("REAL G1 still titles the card with the generic column header")

# ---- GATE 5. Fed workbook Sheet 6's own inputs, the page must reproduce the
#      workbook's own cached values. These are literals read out of the xlsx,
#      not numbers the mirror computed, so they pin the page to the workbook.
G5, mG5 = page["gate5"], mir["gate5"]
same("G5 no JS errors", G5["pageErrors"], [])
for label, tile, want in [("optimal order (Sheet 6 C22)",   "Optimal order",       1159),
                          ("max affordable (C23)",          "Max affordable",       386),
                          ("recommended order (C24)",       "RECOMMENDED",          386),
                          ("expected lost sales (C26)",     "Expected lost sales",  617),
                          ("expected leftover (C27)",       "Expected leftover",      3)]:
    eq(f"G5 {label}", G5["A"].get(tile), want)
eq("G5 service level (C21)",          G5["A"].get("Service level"),       69.5, 0.05)
eq("G5 season contribution (C28)",    G5["A"].get("Season contribution"), 7763, 1)
eq("G5 PO value (Sheet 8 C8)",        G5["B"].get("PO value"),            4991, 1)
eq("G5 import VAT (Sheet 8 C12)",     G5["B"].get("Import VAT"),           948, 1)
# and the same numbers again from the independent mirror
eq("G5 mirror agrees: recommended",   G5["A"].get("RECOMMENDED"),   mG5["qRec"])
eq("G5 mirror agrees: lost sales",    G5["A"].get("Expected lost sales"), mG5["lost"])
eq("G5 mirror agrees: lowest cash",   G5["B"].get("Lowest cash"),   mG5["lowest"], 1)
eq("G5 mirror agrees: capital need",  G5["B"].get("Capital needed"), mG5["need"], 1)
same("G5 budget-capped warning fires", any("BUDGET CAPS" in v for v in G5["va"]), True)
same("G5 mirror agrees the budget caps it", mG5["budWarn"], True)
same("G5 MOQ warning stays silent",   any("MOQ ABOVE" in v for v in G5["va"]), False)
same("G5 cash plan is funded",        any("FUNDED" in v for v in G5["vb"]), True)
same("G5 chip is CAUTION (Sheet 6 warning, cash still positive)", G5["cls"], "yellow")
# the deliberate divergence from Sheet 8's example: never sell more than the order
same("G5 plans exactly the order, not more", G5["B"].get("Units sold in 12 mo"), "386 u")
same("G5 mirror agrees units sold == order", mG5["sold"], mG5["qRec"])
same("G5 13 month rows", len(G5["rows"]), 13)
# Gate 5 feeds the dossier's cash row
eq("G5 fills the dossier cash need", G5["dossierCash"], mG5["need"], 1)

# ---- The RU page is generated, so English leaking into it is a build-script bug,
#      not a translation opinion. Three of these strings shipped in English until
#      the Gate 5 work; the build scan only caught one of them.
RU_MUST_NOT_CONTAIN = [
    "Gate passed", "You can continue", "failed hard checks", "Save this niche",
    "Print / save", "never leave your browser", "Contribution margin",
    "Optimal order", "Max affordable", "Lowest cash", "Capital needed",
    "Month by month", "Starting cash", "Supplier MOQ", "FUNDED", "not run",
]
ru_text = page["ru"].get("bodyText") or ""
leaked = [w for w in RU_MUST_NOT_CONTAIN if w in ru_text]
checks.append((not leaked, "RU page carries no English UI chrome", leaked or "none",
               "no English strings"))
if leaked:
    fails.append(f"RU page still shows English: {leaked}")

# ---- Translation must not move a number. Same defaults on both pages, so every
#      Gate 5 tile must read identically apart from the language of the label.
en_g5 = page["en"].get("g5values") or []
ru_g5 = page["ru"].get("g5values") or []
checks.append((len(en_g5) == 12, "EN Gate 5 rendered all 12 tiles", len(en_g5), 12))
if len(en_g5) != 12:
    fails.append(f"EN Gate 5 rendered {len(en_g5)} tiles, expected 12")
# The RU page formats numbers with ru-RU separators and writes "ю" for units, both
# deliberate. Compare the digits, which translation must never change.
def digits(xs):
    return [re.sub(r"[^\d.]", "", x.replace("\u00a0", "").replace(",", "")) for x in xs]
same("EN/RU Gate 5 numbers identical", digits(en_g5), digits(ru_g5))

# ---- The weekly -> monthly conversion, pinned with literals worked out by hand
#      from the fixture, not taken from the mirror (the mirror moved with the page).
#      Fixture weekly sales: 32 + 105 + 190 + 1140 + 661 = 2128/week.
#      2128 * 52/12 = 9221/month. P10 = 9221*0.04*12, P90 = 9221*0.15*12.
eq("G4 weekly sales converted to monthly", page["en"]["gate4"]["tiles"].get("Keyword sales, total"), 9221, 1)
eq("G4 P10 off the monthly rate",          page["en"]["gate4"]["tiles"].get("Suggested P10"), 4426, 1)
eq("G4 P90 off the monthly rate",          page["en"]["gate4"]["tiles"].get("Suggested P90"), 16598, 1)
g4rows = " ".join((r.get("label") or "") + " " + (r.get("note") or "")
                  for r in page["en"]["gate4"].get("checks", []))
for wk, mo in [("1,140/wk", "4,940/mo"), ("661/wk", "2,864/mo"), ("32/wk", "139/mo")]:
    ok = wk in g4rows and mo in g4rows
    checks.append((ok, f"G4 row shows {wk} as {mo}", wk in g4rows and mo in g4rows, True))
    if not ok:
        fails.append(f"G4 row does not show {wk} converted to {mo}")
# a keyword that used to read WEAK on the same data must now read STRONG
same("G4 nackenkissen is STRONG once converted",
     "nackenkissen" in g4rows and "14 searches per sale — STRONG" in g4rows, True)

# ---- Gate 4 must never report a verdict it could not compute.
#      Before this, an Xray Keywords export rendered a confident red
#      ("NO REAL DEMAND DOORS") purely because every push cost was null.
M = page["gate4missing"]
xk = M["xrayKeywords"]
checks.append((bool(xk["error"]) and "Xray Keywords" in (xk["error"] or ""),
               "G4 refuses the Xray Keywords export by name", xk["error"], "names the file"))
if not (xk["error"] and "Xray Keywords" in xk["error"]):
    fails.append("G4 did not refuse the Xray Keywords export")
same("G4 refuses it instead of scoring it", xk["rendered"], False)
same("G4 gives it no colour at all", xk["cls"], None)
for word in ("CPR", "WEEK"):
    checks.append((word in (xk["error"] or ""), f"G4 refusal explains '{word}'", word in (xk["error"] or ""), True))

nc = M["noCpr"]
same("G4 no-CPR file is not called a bad niche", "NO REAL DEMAND DOORS" in (nc["verdict"] or ""), False)
same("G4 no-CPR file says it cannot judge", "CANNOT JUDGE" in (nc["verdict"] or ""), True)
same("G4 no-CPR file is not red", nc["cls"], "yellow")

pc = M["partialCpr"]
same("G4 still judges when only some rows have CPR", pc["cls"], "green")
checks.append(("3 without CPR" in (pc["meta"] or ""),
               "G4 says how many rows it left out", pc["meta"], "names the skipped count"))
if "3 without CPR" not in (pc["meta"] or ""):
    fails.append("G4 silently dropped the rows without CPR")
for k, v in M.items():
    same(f"G4 {k}: no JS errors", v["pageErrors"], [])

# ---- no JS errors on either page
same("EN page: no JS errors", en["consoleErrors"], [])
same("RU page: no JS errors", ru["consoleErrors"], [])

# ---- report
width = max(len(c[1]) for c in checks)
for ok, label, shown, expected in checks:
    print(f"{'PASS' if ok else 'FAIL'}  {label.ljust(width)}  {shown!r}" + ("" if ok else f"   expected {expected!r}"))
print()
print(f"{sum(1 for c in checks if c[0])}/{len(checks)} checks passed")
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("Browser:", page["browser"])

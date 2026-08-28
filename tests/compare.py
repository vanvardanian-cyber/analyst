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
same("RU check-row count (gate 2)", len(ru["gate2"]["checks"]), len(en["gate2"]["checks"]))
same("RU check-row count (gate 4)", len(ru["gate4"]["checks"]), len(en["gate4"]["checks"]))

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

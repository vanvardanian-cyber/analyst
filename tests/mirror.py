#!/usr/bin/env python3
"""Independent Python mirror of the Niche Funnel maths.

Written from the workbook + the documented method, NOT by transcribing the
page's JavaScript. Its output is the expected answer; run.mjs scrapes what the
page actually shows; compare.py puts the two side by side.
"""
import csv, json, math, os, re, statistics
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def read_csv(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return [r for r in csv.reader(f)]


def xfloat(x):
    """A numeric cell from any Helium 10 export: '4,806.42', '15.29', '', 'N/A'."""
    x = (x or "").strip()
    if x in ("", "N/A", "n/a", "-"):
        return None
    try:
        return float(x.replace(",", ""))
    except ValueError:
        return None


def xdate(x):
    """A date cell: '2026-08-22 00:00:00' or 'Nov 27, 2025'."""
    x = (x or "").strip()
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", x)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    for f in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(x, f).date()
        except ValueError:
            pass
    return None


def pearson(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = sum((x - ma) ** 2 for x in a)
    db = sum((y - mb) ** 2 for y in b)
    d = math.sqrt(da * db)
    return num / d if d else 0.0


def pvar(a):
    m = statistics.fmean(a)
    return statistics.fmean([(v - m) ** 2 for v in a])


# ------------------------------------------------------------------ Gate 0
# Workbook Sheet 4 Block A is C5:C13 and C32 reads
#   =IF(COUNTIF(C5:C13,"YES")=9,"CLEAN","REJECT")
# so nine rows, all of which must be YES. The page splits them into seven
# product-property rows (red) and two seller-duty rows (yellow); the tally it
# prints must still be the workbook's 0-9.
G0_A = ["ppe", "elec", "kids", "skin", "health", "load", "ip"]   # product properties
G0_B = ["gpsr", "epr"]                                            # seller duties
G0_ALL = G0_A + G0_B + ["brand"]


def gate0(answers):
    """answers: {id: 'yes'|'no'}; ids left out are unanswered."""
    fail_a = [q for q in G0_A if answers.get(q) == "no"]
    fail_b = [q for q in G0_B if answers.get(q) == "no"]
    fail_brand = answers.get("brand") == "no"
    block_a_yes = sum(1 for q in G0_A + G0_B if answers.get(q) == "yes")
    answered = sum(1 for q in G0_ALL if answers.get(q))
    if fail_a:
        status = "red"
    elif answered < len(G0_ALL):
        status = None                       # gate must stay "not run"
    elif fail_b or fail_brand:
        status = "yellow"
    else:
        status = "green"
    tally = "%d/9 YES" % block_a_yes
    if block_a_yes == 9:
        tally += " — CLEAN"
    elif answered == len(G0_ALL):
        tally += " — REJECT"
    return {"status": status, "blockAyes": block_a_yes, "answered": answered,
            "progress": "%d of %d answered · workbook Sheet 4 Block A tally: %s"
                        % (answered, len(G0_ALL), tally)}


G0_SCENARIOS = {
    "all-yes":        {q: "yes" for q in G0_ALL},
    "ppe-no":         {**{q: "yes" for q in G0_ALL}, "ppe": "no"},
    "ip-no":          {**{q: "yes" for q in G0_ALL}, "ip": "no"},
    "gpsr-no":        {**{q: "yes" for q in G0_ALL}, "gpsr": "no"},
    "brand-no":       {**{q: "yes" for q in G0_ALL}, "brand": "no"},
    "epr-and-brand":  {**{q: "yes" for q in G0_ALL}, "epr": "no", "brand": "no"},
    "partial":        {"ppe": "yes", "elec": "yes", "kids": "yes"},
    "partial-kill":   {"ppe": "no"},        # one product-property NO kills it alone
}


# ------------------------------------------------------------------ Gate 1
def gate1(fixture="gate1-search-volume.csv", now=None):
    now = now or date.today()
    cur_key = "%04d-%02d" % (now.year, now.month)
    rows = read_csv(fixture)
    acc = {}
    for r in rows[1:]:
        m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", r[0].strip())
        if not m:
            continue
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        key = "%04d-%02d" % (d.year, d.month)
        if key == cur_key:
            continue
        s, n = acc.get(key, (0, 0))
        acc[key] = (s + int(r[1]), n + 1)
    months = sorted(({"key": k, "m": int(k[5:]), "avg": s / n}
                     for k, (s, n) in acc.items()), key=lambda x: x["key"])[-36:]

    prof = [[0.0, 0] for _ in range(12)]
    for m in months:
        p = prof[m["m"] - 1]
        p[0] += m["avg"]; p[1] += 1
    prof_avg = [p[0] / p[1] if p[1] else None for p in prof]
    filled = [v for v in prof_avg if v is not None]
    grand = statistics.fmean(filled)
    index = [None if v is None else v / grand for v in prof_avg]
    nz = [v for v in index if v is not None and v > 0]
    amp = max(nz) / min(nz)
    top4 = sum(sorted(filled, reverse=True)[:4]) / sum(filled)

    n = len(months)
    k = min(3, n // 12)
    blocks = []
    for j in range(k - 1, -1, -1):
        seg = months[n - 12 * (j + 1): n - 12 * j]
        vec = [None] * 12
        for m in seg:
            vec[m["m"] - 1] = m["avg"]
        blocks.append({"seg": seg, "vec": vec})
    tot = [sum(m["avg"] for m in b["seg"]) for b in blocks]
    yoy = tot[-1] / tot[-2] - 1 if len(blocks) >= 2 and tot[-2] else None

    logs = [[math.log((v or 0) + 1) for v in b["vec"]] for b in blocks]
    rs = [pearson(logs[i], logs[j])
          for i in range(len(logs)) for j in range(i + 1, len(logs))]
    consistency = statistics.fmean(rs) if rs else None

    strength = None
    if len(months) >= 30:
        y = [math.log(m["avg"] + 1) for m in months]
        d, calm = [], []
        for t in range(6, len(y) - 6):
            s = 0.5 * y[t - 6] + 0.5 * y[t + 6] + sum(y[t - 5: t + 6])
            d.append(y[t] - s / 12)
            calm.append(months[t]["m"] - 1)
        sm = [[0.0, 0] for _ in range(12)]
        for v, c in zip(d, calm):
            sm[c][0] += v; sm[c][1] += 1
        smv = [p[0] / p[1] if p[1] else 0.0 for p in sm]
        rem = [v - smv[c] for v, c in zip(d, calm)]
        vd = pvar(d)
        if vd > 1e-12:
            strength = max(0.0, 1 - pvar(rem) / vd)

    ramp = None
    for i in range(12):
        prev, cur = index[i - 1], index[i]
        if prev is not None and cur is not None and prev < 1 <= cur:
            ramp = i
            break

    return {"monthsUsed": len(months), "blocks": len(blocks), "amplitude": amp,
            "consistency": consistency, "strength": strength, "top4": top4,
            "yoy": yoy, "ramp": None if ramp is None else MONTHS[ramp],
            "index": index}


# ------------------------------------------------------------------ Gate 2
def gate2(fixture="gate2-xray.csv"):
    rows = read_csv(fixture)
    h = [c.strip().lower() for c in rows[0]]
    # real exports name these "Price  €" and "Fees  €", so match by prefix
    ix = {"asin": h.index("asin"), "brand": h.index("brand"),
          "price": next(i for i, c in enumerate(h) if c.startswith("price")),
          "cat": h.index("category"),
          "rev": next(i for i, c in enumerate(h) if c.startswith("asin revenue")),
          "rating": next(i for i, c in enumerate(h) if c.startswith("ratings")),
          "reviews": next(i for i, c in enumerate(h) if c.startswith("review count")),
          "fees": next(i for i, c in enumerate(h) if c.startswith("fees")),
          "weight": next(i for i, c in enumerate(h) if c.startswith("weight")),
          "created": next(i for i, c in enumerate(h) if c.startswith("creation date")),
          "country": next(i for i, c in enumerate(h) if c.startswith("seller country")),
          "age": next((i for i, c in enumerate(h) if c.startswith("seller age")), None)}
    seen, dupes = {}, 0
    for r in rows[1:]:
        a = r[ix["asin"]].strip()
        if a in seen:
            dupes += 1
            continue
        seen[a] = {"asin": a, "brand": r[ix["brand"]], "cat": r[ix["cat"]],
                   "rev": xfloat(r[ix["rev"]]) or 0.0, "price": xfloat(r[ix["price"]]),
                   "rating": xfloat(r[ix["rating"]]), "reviews": xfloat(r[ix["reviews"]]) or 0.0,
                   "fees": xfloat(r[ix["fees"]]), "weight": xfloat(r[ix["weight"]]),
                   "created": xdate(r[ix["created"]]),
                   "country": r[ix["country"]].upper(),
                   "age": xfloat(r[ix["age"]]) if ix["age"] is not None else None}
    prods = list(seen.values())
    counts = {}
    for p in prods:
        counts[p["cat"]] = counts.get(p["cat"], 0) + 1
    modal = max(counts.items(), key=lambda kv: kv[1])[0]
    off = 0
    if counts[modal] >= len(prods) * 0.6:
        before = len(prods)
        prods = [p for p in prods if p["cat"] == modal]
        off = before - len(prods)

    total = sum(p["rev"] for p in prods)
    srt = sorted(prods, key=lambda p: -p["rev"])
    top10 = srt[:10]
    top10_rev = sum(p["rev"] for p in top10)
    top_share = srt[0]["rev"] / total
    over500 = sum(1 for p in prods if p["reviews"] > 500)
    med_top10_reviews = statistics.median([p["reviews"] for p in top10])
    wall_months = med_top10_reviews / (300 * 0.015)
    cnhk = sum(p["rev"] for p in prods if p["country"] in ("CN", "HK")) / total
    today = date.today()
    fresh = [p for p in prods if p["created"] and (today - p["created"]).days < 365 and p["rev"] > 3000]
    weak = [p for p in srt if p["rating"] is not None and p["rating"] <= 4.3 and p["rev"] >= 2000]
    low_rev_earners = [p for p in srt if p["reviews"] <= 100 and p["rev"] >= 3000]
    med_price = statistics.median([p["price"] for p in prods if p["price"]])
    med_fee_share = statistics.median([p["fees"] / p["price"] for p in prods
                                       if p["fees"] is not None and p["price"]])
    med_weight = statistics.median([p["weight"] for p in prods if p["weight"]])
    return {"unique": len(prods), "dupes": dupes, "offNiche": off,
            "top10Rev": top10_rev, "totalRev": total, "topShare": top_share,
            "over500": over500, "medTop10Reviews": med_top10_reviews,
            "wallMonths": wall_months, "cnhkShare": cnhk, "fresh": len(fresh),
            "weak": len(weak), "proofOfEntry": len(low_rev_earners),
            "medPrice": med_price, "medFeeShare": med_fee_share,
            "medWeight": med_weight,
            "hasSellerAgeColumn": ix["age"] is not None,
            "sellerAgeFilled": sum(1 for p in prods if p["age"] is not None),
            "proofOnNewShops": sum(1 for p in low_rev_earners
                                   if p["age"] is not None and p["age"] <= 18),
            "freshOnNewShops": sum(1 for p in fresh
                                   if p["age"] is not None and p["age"] <= 18)}


# ------------------------------------------------------------------ Gate 3
def gate3(price=59.99, ref=0.15, fba=4.55, stor=0.62, ret=0.07, retc=0.70,
          exw=10.0, frt=2.20, duty=0.027, prep=0.40, tax=0.01):
    """Workbook Sheet 3, cell by cell."""
    net = price / 1.19                       # C21
    referral = ref * price                   # C22 (charged on the gross price)
    returns = ret * retc * net               # C25
    payout = net - referral - fba - stor - returns          # C26
    landed = exw + frt + (exw + frt) * duty + prep          # C27
    tax_cost = tax * net                                    # C28
    cm = payout - landed - tax_cost                         # C29
    max_landed = payout + (-tax_cost) - 0.35 * net          # C32
    max_exw = (max_landed - prep - frt * (1 + duty)) / (1 + duty)   # C33
    return {"net": net, "payout": payout, "landed": landed, "cm": cm,
            "marginPct": cm / net * 100, "beAcosPct": cm / price * 100,
            "maxExw": max_exw}


# ------------------------------------------------------------------ Gate 4
def gate4(landed=12.93, disc=3.0, spend=24.0, max_push=1000.0):
    rows = read_csv("gate4-cerebro.csv")
    h = [c.strip().lower() for c in rows[0]]
    ix = {"kw": h.index("keyword phrase"), "sales": h.index("keyword sales"),
          "sv": h.index("search volume"), "trend": h.index("search volume trend"),
          "cpr": h.index("cpr"), "td": h.index("title density")}
    out, total_sales = [], 0.0
    for r in rows[1:]:
        sales = float(r[ix["sales"]]); sv = float(r[ix["sv"]])
        trend = float(r[ix["trend"]]); cpr = float(r[ix["cpr"]])
        total_sales += sales
        sps = sv / sales if sales > 0 and sv > 0 else None
        if sps is None:      status = "yellow"
        elif sps <= 20:      status = "green"
        elif sps <= 60:      status = "green"
        elif sps <= 120:     status = "yellow"
        else:                status = "red"
        fad = trend >= 200
        if fad:
            status = "red"
        push = cpr * (landed + disc) + spend * 8
        out.append({"kw": r[ix["kw"]], "sps": sps, "push": push,
                    "status": status, "fad": fad})
    candidates = [k for k in out if k["status"] != "red"]
    affordable = [k for k in candidates if k["push"] <= max_push]
    strong = [k for k in affordable if k["status"] == "green"]
    pool = strong or affordable or candidates
    best = sorted(pool, key=lambda k: k["push"])[0] if pool else None
    overall = "green" if strong else ("yellow" if candidates else "red")
    return {"keywords": out, "totalSales": total_sales,
            "best": best["kw"] if best else None,
            "bestPush": best["push"] if best else None,
            "p10": total_sales * 0.04 * 12, "p90": total_sales * 0.15 * 12,
            "overall": overall}



# ------------------------------------------------------------------ Dossier
# Workbook Sheet 5 rows 21-34. Weights sum to 1.00; score = SUMPRODUCT/2*100
# rounded half-up (Excel ROUND, which is also JS Math.round), blank until all
# ten inputs exist (D32 guards on COUNT(D21:D30)<10).
DCRIT = [
    ("rev",    0.15, lambda v, b: 2 if v >= 40000 else 1 if v >= 20000 else 0),
    ("share",  0.10, lambda v, b: 2 if v < 0.30 else 1 if v <= 0.40 else 0),
    ("moat",   0.10, lambda v, b: 2 if v <= 2 else 1 if v <= 4 else 0),
    ("fresh",  0.10, lambda v, b: 2 if v >= 2 else 1 if v >= 1 else 0),
    ("weak",   0.10, lambda v, b: 2 if v == 1 else 0),
    ("cnhk",   0.05, lambda v, b: 2 if v < 0.40 else 1 if v < 0.60 else 0),
    ("amp",    0.15, lambda v, b: 2 if v < 1.5 else 1 if v < 2.5 else 0),
    ("top4",   0.05, lambda v, b: 2 if v < 0.45 else 1 if v < 0.60 else 0),
    ("margin", 0.15, lambda v, b: 2 if v >= 0.35 else 1 if v >= 0.30 else 0),
    ("cash",   0.05, lambda v, b: 2 if v <= 0.8 * b else 1 if v <= b else 0),
]


def dossier(values, compliance, budget=6500):
    scores = [None if values.get(k) is None else f(values[k], budget) for k, _, f in DCRIT]
    if any(x is None for x in scores):
        score = None
    else:
        acc = 0.0
        for (k, w, _), sc in zip(DCRIT, scores):   # same order as the page sums them
            acc += w * sc
        score = math.floor(acc / 2 * 100 + 0.5)
    if compliance == "NO":
        hard, disq = "DISQUALIFIED: compliance", True
    elif values.get("amp") is None:
        hard, disq = "\u2014", False
    elif values["amp"] >= 4:
        hard, disq = "DISQUALIFIED: single-season", True
    elif compliance is None:
        hard, disq = "OK \u2014 Gate 0 unanswered", False
    else:
        hard, disq = "OK", False
    if score is None:
        verdict = ""
    elif disq:
        verdict = "DROP"
    else:
        verdict = "INVESTIGATE" if score >= 70 else "PARK" if score >= 50 else "DROP"
    return {"scores": scores, "score": score, "hard": hard, "verdict": verdict}


REAL = {"gate1": "real-gate1-chart.csv", "gate2": "real-gate2-xray.csv"}


def real_available():
    return {k: v for k, v in REAL.items() if os.path.exists(os.path.join(FIX, v))}


if __name__ == "__main__":
    g1, g1s, g2, g3 = gate1(), gate1("gate1-seasonal.csv"), gate2(), gate3()
    # niche A: the fixtures as they stand, Gate 0 fully clean, cash need 5000
    a_vals = {"rev": g2["top10Rev"], "share": g2["topShare"], "moat": g2["over500"],
              "fresh": g2["fresh"], "weak": 1 if g2["weak"] else 0, "cnhk": g2["cnhkShare"],
              "amp": g1["amplitude"], "top4": g1["top4"], "margin": g3["cm"] / g3["net"],
              "cash": 5000}
    # niche B: same page, the single-season keyword, and no cash figure typed
    b_vals = dict(a_vals, amp=g1s["amplitude"], top4=g1s["top4"], cash=None)
    have = real_available()
    real = {}
    if "gate1" in have:
        real["gate1"] = gate1(REAL["gate1"])
    if "gate2" in have:
        real["gate2"] = gate2(REAL["gate2"])
    res = {"real": real,
           "gate0": {k: gate0(v) for k, v in G0_SCENARIOS.items()},
           "gate1": g1, "gate1seasonal": g1s, "gate2": g2, "gate3": g3, "gate4": gate4(),
           "dossier": {"nicheA": {"values": a_vals, **dossier(a_vals, "YES")},
                       "nicheB": {"values": b_vals, **dossier(b_vals, "YES")},
                       "nicheB_withCash": {**dossier(dict(b_vals, cash=5000), "YES")},
                       "budget": 6500}}
    # the browser driver replays exactly these answer sets
    with open(os.path.join(FIX, "gate0-scenarios.json"), "w") as f:
        json.dump(G0_SCENARIOS, f, indent=2)
    os.makedirs(os.path.join(HERE, ".out"), exist_ok=True)
    with open(os.path.join(HERE, ".out", "mirror.json"), "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps(res, indent=2, default=str)[:2000])

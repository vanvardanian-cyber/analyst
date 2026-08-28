#!/usr/bin/env python3
"""Independent Python mirror of the Niche Funnel maths.

Written from the workbook + the documented method, NOT by transcribing the
page's JavaScript. Its output is the expected answer; run.mjs scrapes what the
page actually shows; compare.py puts the two side by side.
"""
import csv, json, math, os, statistics
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def read_csv(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return [r for r in csv.reader(f)]


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


# ------------------------------------------------------------------ Gate 1
def gate1(now=None):
    now = now or date.today()
    cur_key = "%04d-%02d" % (now.year, now.month)
    rows = read_csv("gate1-search-volume.csv")
    acc = {}
    for r in rows[1:]:
        d = datetime.strptime(r[0], "%Y-%m-%d").date()
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
def gate2():
    rows = read_csv("gate2-xray.csv")
    h = [c.strip().lower() for c in rows[0]]
    ix = {"asin": h.index("asin"), "brand": h.index("brand"),
          "price": h.index("price"), "cat": h.index("category"),
          "rev": next(i for i, c in enumerate(h) if c.startswith("asin revenue")),
          "rating": next(i for i, c in enumerate(h) if c.startswith("ratings")),
          "reviews": next(i for i, c in enumerate(h) if c.startswith("review count")),
          "fees": next(i for i, c in enumerate(h) if c.startswith("fees")),
          "weight": next(i for i, c in enumerate(h) if c.startswith("weight")),
          "created": next(i for i, c in enumerate(h) if c.startswith("creation date")),
          "country": next(i for i, c in enumerate(h) if c.startswith("seller country"))}
    seen, dupes = {}, 0
    for r in rows[1:]:
        a = r[ix["asin"]].strip()
        if a in seen:
            dupes += 1
            continue
        seen[a] = {"asin": a, "brand": r[ix["brand"]], "cat": r[ix["cat"]],
                   "rev": float(r[ix["rev"]]), "price": float(r[ix["price"]]),
                   "rating": float(r[ix["rating"]]), "reviews": float(r[ix["reviews"]]),
                   "fees": float(r[ix["fees"]]), "weight": float(r[ix["weight"]]),
                   "created": datetime.strptime(r[ix["created"]], "%Y-%m-%d").date(),
                   "country": r[ix["country"]].upper()}
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
    fresh = [p for p in prods if (today - p["created"]).days < 365 and p["rev"] > 3000]
    weak = [p for p in srt if p["rating"] <= 4.3 and p["rev"] >= 2000]
    low_rev_earners = [p for p in srt if p["reviews"] <= 100 and p["rev"] >= 3000]
    med_price = statistics.median([p["price"] for p in prods])
    med_fee_share = statistics.median([p["fees"] / p["price"] for p in prods])
    med_weight = statistics.median([p["weight"] for p in prods])
    return {"unique": len(prods), "dupes": dupes, "offNiche": off,
            "top10Rev": top10_rev, "totalRev": total, "topShare": top_share,
            "over500": over500, "medTop10Reviews": med_top10_reviews,
            "wallMonths": wall_months, "cnhkShare": cnhk, "fresh": len(fresh),
            "weak": len(weak), "proofOfEntry": len(low_rev_earners),
            "medPrice": med_price, "medFeeShare": med_fee_share,
            "medWeight": med_weight,
            "hasSellerAgeColumn": any(c.startswith("seller age") for c in h)}


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


if __name__ == "__main__":
    res = {"gate1": gate1(), "gate2": gate2(), "gate3": gate3(), "gate4": gate4()}
    os.makedirs(os.path.join(HERE, ".out"), exist_ok=True)
    with open(os.path.join(HERE, ".out", "mirror.json"), "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps(res, indent=2, default=str)[:2000])

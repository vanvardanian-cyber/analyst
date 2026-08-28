#!/usr/bin/env python3
"""Generate the synthetic test fixtures.

These are NOT real Helium 10 exports. They use the real column headers and
realistic value shapes so the parsing layer is exercised, but the numbers are
constructed to hit specific threshold bands. Real exports must replace them for
the parsing layer to be genuinely trusted (locale number formats, extra
columns, sponsored repeats in the wild).
"""
import csv, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Gate 1
# 36 months of weekly search-volume points. Same shape as the page's own
# "Try with example data" set (a mildly seasonal kitchen-organiser niche).
Y1CAL = [15408, 15404, 12974, 11777, 9802, 9083, 9830, 10348, 11120, 11735, 11100, 10314]
YR0 = [round(v * 0.94) for v in (Y1CAL[7:] + Y1CAL[:7])]
YR1 = [10348, 11120, 11735, 11100, 10314, 15408, 15404, 12974, 11777, 9802, 9083, 9830]
YR2 = [10198, 9675, 10628, 10244, 9772, 17117, 14402, 12257, 10966, 7284, 6866, 7096]
MONTHLY = YR0 + YR1 + YR2

def gate1():
    start = date(2023, 8, 7)
    rows = [["Date", "schubladen organizer küche"]]
    d = start
    while True:
        mi = (d.year * 12 + d.month) - (start.year * 12 + start.month)
        if mi >= 36:
            break
        rows.append([d.isoformat(), MONTHLY[mi]])
        d += timedelta(days=7)
    return rows

# A single-season niche: amplitude far above 4, which Sheet 5 D33 disqualifies
# outright and Gate 1 calls a working-capital trap.
SEASONAL = [820, 700, 640, 600, 610, 660, 730, 910, 1240, 2280, 6600, 9100]


def gate1_seasonal():
    start = date(2023, 8, 7)
    rows = [["Date", "adventskalender befüllbar"]]
    d = start
    while True:
        mi = (d.year * 12 + d.month) - (start.year * 12 + start.month)
        if mi >= 36:
            break
        # mild year-on-year growth so the years still agree with each other
        rows.append([d.isoformat(), round(SEASONAL[d.month - 1] * (1 + 0.04 * (mi // 12)))])
        d += timedelta(days=7)
    return rows


# ---------------------------------------------------------------- Gate 2
# Helium 10 Xray, search-results view. Column names are the real ones.
# NOTE: a real Xray export has NO "Seller Age" column — that absence is
# deliberate here, it is what the page actually receives.
XRAY_HEADER = ["Product Details", "ASIN", "Brand", "Price", "Category", "BSR",
               "ASIN Sales", "ASIN Revenue", "Ratings", "Review Count", "Images",
               "Review Velocity", "Size Tier", "Fees", "Active Sellers #",
               "Weight", "Creation Date", "Seller Country/Region", "Fulfillment", "URL"]

# brand, price, asin_sales, asin_rev, rating, reviews, fees, weight, created, country, fulfilment, category
XRAY_ROWS = [
    ("OrgaLine",     34.99,  610, 21344.0, 4.6,  1840, 6.10, 0.9, "2019-04-11", "DE", "FBA",  "Home & Kitchen"),
    ("Kesper",       27.95,  480, 13416.0, 4.5,  2310, 5.55, 1.1, "2017-02-03", "DE", "FBA",  "Home & Kitchen"),
    ("mDesign",      29.99,  395, 11846.0, 4.4,   940, 5.70, 0.8, "2020-09-22", "US", "FBA",  "Home & Kitchen"),
    ("Youdoit",      22.49,  430,  9670.0, 4.2,   210, 4.95, 0.7, "2024-11-05", "CN", "FBA",  "Home & Kitchen"),
    ("Relaxdays",    24.99,  330,  8247.0, 4.3,  1520, 5.10, 1.3, "2016-06-14", "DE", "FBA",  "Home & Kitchen"),
    ("HOMCOM",       31.90,  240,  7656.0, 4.1,   660, 5.85, 1.6, "2021-01-19", "CN", "FBA",  "Home & Kitchen"),
    ("Sunhoo",       19.99,  360,  7196.0, 4.4,    62, 4.60, 0.6, "2025-10-02", "CN", "FBA",  "Home & Kitchen"),
    ("Navaris",      26.50,  260,  6890.0, 4.5,   880, 5.30, 0.9, "2018-08-30", "DE", "FBA",  "Home & Kitchen"),
    ("Leifheit",     39.99,  165,  6598.0, 4.6,  1210, 6.40, 1.2, "2015-03-25", "DE", "FBA",  "Home & Kitchen"),
    ("Vinabo",       21.99,  290,  6377.0, 4.3,    48, 4.75, 0.7, "2026-01-16", "CN", "FBA",  "Home & Kitchen"),
    ("KitchenMove",  23.49,  190,  4463.0, 4.0,   340, 4.90, 0.8, "2022-05-09", "DE", "FBM",  "Home & Kitchen"),
    ("Yamazaki",     44.00,   95,  4180.0, 4.7,   520, 6.90, 1.0, "2019-11-28", "JP", "FBA",  "Home & Kitchen"),
    ("Orgabox",      18.99,  205,  3893.0, 4.2,    83, 4.40, 0.6, "2025-07-21", "CN", "FBA",  "Home & Kitchen"),
    ("Songmics",     28.99,  130,  3768.0, 4.4,   730, 5.60, 1.4, "2018-01-12", "CN", "FBA",  "Home & Kitchen"),
    ("Wenko",        25.95,  140,  3633.0, 4.5,   960, 5.20, 1.1, "2016-10-07", "DE", "FBA",  "Home & Kitchen"),
    ("Blumtal",      20.49,  150,  3073.0, 4.1,    95, 4.55, 0.7, "2025-12-03", "DE", "FBA",  "Home & Kitchen"),
    ("iDesign",      33.50,   80,  2680.0, 4.2,   410, 5.95, 0.9, "2020-02-18", "US", "FBA",  "Home & Kitchen"),
    ("Rotho",        16.99,  120,  2039.0, 4.3,   580, 4.20, 0.5, "2017-07-26", "DE", "FBA",  "Home & Kitchen"),
    ("Curver",       15.49,   95,  1472.0, 4.4,   690, 4.05, 0.5, "2015-12-01", "NL", "FBA",  "Home & Kitchen"),
    # off-niche sponsored intruder: different category, must be dropped
    ("FitPro",       49.99,  200,  9998.0, 4.5,   310, 7.20, 3.2, "2021-04-04", "CN", "FBA",  "Sports & Outdoors"),
]

def gate2():
    rows = [XRAY_HEADER]
    for i, (brand, price, sales, rev, rating, reviews, fees, weight, created,
            country, fulfil, cat) in enumerate(XRAY_ROWS):
        asin = "B0%s" % str(10000000 + i * 137)[:8]
        rows.append(["%s drawer organiser" % brand, asin, brand, price, cat,
                     1200 + i * 90, sales, rev, rating, reviews, 7,
                     round(reviews / 40.0, 1), "Standard", fees, 1, weight,
                     created, country, fulfil,
                     "https://www.amazon.de/dp/%s" % asin])
    # sponsored placements repeat the two top ASINs — the page must dedupe them
    rows.append(list(rows[1]))
    rows.append(list(rows[2]))
    rows.append(list(rows[1]))
    return rows

# ---------------------------------------------------------------- Gate 4
CEREBRO_HEADER = ["Keyword Phrase", "Keyword Sales", "Cerebro IQ Score", "Search Volume",
                  "Search Volume Trend", "Sponsored ASINs", "Competing Products",
                  "CPR", "Organic", "Title Density"]
CEREBRO_ROWS = [
    ("bauchschläferkissen",         32, 8302,   3495,    47, 384, ">411",   38, 0, 30),
    ("kopfkissen nackenschmerzen", 105, 6404,   6404,    36, 283, ">1,000", 33, 0,  4),
    ("japanisches kissen",         190, 39599, 12751,  1010, 318, ">315",   39, 0,  0),
    ("nackenkissen",              1140, 17847, 71386,    35, 285, ">4,000",121, 0, 37),
    ("seitenschläferkissen",       661, 41852, 83704,    36, 323, ">2,000",137, 0, 42),
]

def gate4():
    return [CEREBRO_HEADER] + [list(r) for r in CEREBRO_ROWS]

def write(name, rows):
    path = os.path.join(HERE, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print("wrote", name, "(%d rows)" % (len(rows) - 1))

if __name__ == "__main__":
    write("gate1-search-volume.csv", gate1())
    write("gate1-seasonal.csv", gate1_seasonal())
    write("gate2-xray.csv", gate2())
    write("gate4-cerebro.csv", gate4())

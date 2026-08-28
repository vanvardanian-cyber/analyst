// Headless driver: loads the funnel page, feeds the fixtures through the real
// file inputs, and records what the page SHOWS. It makes no claims about
// whether those numbers are right — compare.py judges them against mirror.py.
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const FIX = p => path.join(HERE, "fixtures", p);
const OUT = path.join(HERE, ".out");

const CANDIDATE_BROWSERS = [
  "/opt/pw-browsers/chromium",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
];
function browserPath() {
  for (const p of CANDIDATE_BROWSERS) if (fs.existsSync(p)) return p;
  return null;
}

const scrape = () => {
  const txt = el => (el ? el.textContent.trim() : null);
  const tiles = sel => {
    const o = {};
    document.querySelectorAll(`${sel} .tile`).forEach(t => {
      o[t.querySelector(".k").textContent.trim()] = t.querySelector(".v").textContent.trim();
    });
    return o;
  };
  const chip = n => txt(document.querySelector(`#gate${n} .gchip`));
  const gateClass = n => ["green", "yellow", "red"].find(c => document.querySelector(`#gate${n}`).classList.contains(c)) || null;
  const verdicts = sel => [...document.querySelectorAll(`${sel} .verdict`)].map(v => ({
    headline: txt(v.querySelector("b")),
    color: v.querySelector(".dot").getAttribute("style"),
    text: txt(v).replace(/\s+/g, " "),
  }));
  const checkRows = sel => [...document.querySelectorAll(`${sel} table.checks tr`)].map(tr => ({
    color: tr.querySelector(".ic span")?.getAttribute("style") || null,
    label: txt(tr.querySelector("td:nth-child(2) b")),
    value: txt(tr.querySelector("td.val")),
    note: txt(tr.querySelector("td:nth-child(2) span")),
  }));
  return {
    gate1: { chip: chip(1), status: gateClass(1), meta: txt(document.querySelector("#out .meta")),
             tiles: tiles("#out"), verdicts: verdicts("#out"),
             error: txt(document.querySelector("#status.err")) },
    gate2: { chip: chip(2), status: gateClass(2), meta: txt(document.querySelector("#out2 .meta")),
             tiles: tiles("#out2"), verdicts: verdicts("#out2"), checks: checkRows("#out2"),
             error: txt(document.querySelector("#status2.err")) },
    gate3: { chip: chip(3), status: gateClass(3), tiles: tiles("#gate3"), verdicts: verdicts("#g3v") },
    gate4: { chip: chip(4), status: gateClass(4), meta: txt(document.querySelector("#out4 .meta")),
             tiles: tiles("#out4"), verdicts: verdicts("#out4"), checks: checkRows("#out4"),
             error: txt(document.querySelector("#status4.err")) },
    stepBar: [...document.querySelectorAll(".steps .step")].map(s => s.textContent.replace(/\s+/g, " ").trim()),
  };
};

async function runPage(browser, htmlPath, label) {
  const page = await browser.newPage();
  const consoleErrors = [];
  page.on("pageerror", e => consoleErrors.push(String(e)));
  page.on("console", m => { if (m.type() === "error") consoleErrors.push(m.text()); });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "domcontentloaded" });

  await page.setInputFiles("#file", FIX("gate1-search-volume.csv"));
  await page.waitForSelector("#out .card", { timeout: 10000 });

  await page.setInputFiles("#file2", FIX("gate2-xray.csv"));
  await page.waitForSelector("#out2 .card", { timeout: 10000 });

  // Gate 3 defaults already equal workbook Sheet 3; touch one field so the
  // gate status actually gets set, then restore the value.
  await page.fill("#i_price", "59.98");
  await page.fill("#i_price", "59.99");
  await page.waitForTimeout(50);

  await page.setInputFiles("#file4", FIX("gate4-cerebro.csv"));
  await page.waitForSelector("#out4 .card", { timeout: 10000 });

  const data = await page.evaluate(scrape);
  // ignore the CDN fetch failure that file:// causes for the (unused) xlsx lib
  data.consoleErrors = consoleErrors.filter(e => !/xlsx|cloudflare|ERR_/i.test(e));
  data.label = label;
  await page.close();
  return data;
}

const exe = browserPath();
if (!exe) { console.error("No Chromium/Chrome binary found. Install Chrome, or set one of:\n" + CANDIDATE_BROWSERS.join("\n")); process.exit(2); }
const browser = await chromium.launch({ executablePath: exe, headless: true });
const results = {
  browser: exe,
  en: await runPage(browser, path.join(ROOT, "tools/seasonality/index.html"), "EN"),
  ru: await runPage(browser, path.join(ROOT, "tools/seasonality/ru/index.html"), "RU"),
};
await browser.close();
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "page.json"), JSON.stringify(results, null, 2));
console.log("page.json written · EN gate chips:",
  ["gate1","gate2","gate3","gate4"].map(g => `${g}=${results.en[g].status}`).join(" "));

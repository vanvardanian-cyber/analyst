// Headless driver: loads the funnel page, feeds the fixtures through the real
// file inputs, and records what the page SHOWS. It makes no claims about
// whether those numbers are right — compare.py judges them against mirror.py.
import { chromium } from "playwright-core";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

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
    gate0: { chip: chip(0), status: gateClass(0),
             progress: txt(document.querySelector("#g0prog")),
             verdicts: verdicts("#g0v"),
             questions: [...document.querySelectorAll("#gate0 .q")].map(q => ({
               id: q.dataset.id,
               text: q.querySelector(".qtext").childNodes[0].textContent.trim(),
               group: q.closest(".qgroup").id,
               picked: [...q.querySelectorAll("button")].find(b => b.classList.contains("on"))?.dataset.v || null,
             })) },
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

const dossierTable = () => {
  const t = document.querySelector("#d_out table.dtable");
  if (!t) return null;
  let section = "";
  const rows = [];
  for (const tr of t.querySelectorAll("tbody tr")) {
    if (tr.classList.contains("sect")) { section = tr.textContent.trim(); continue; }
    const tds = [...tr.querySelectorAll("td")];
    rows.push({ section, label: tds[0].textContent.trim(),
                cells: tds.slice(1).map(td => td.textContent.trim()) });
  }
  return {
    chip: document.querySelector("#dossier .gchip").textContent.trim(),
    columns: [...t.querySelectorAll("thead th")].slice(1).map(th => th.textContent.replace("✕", "").trim()),
    rows,
  };
};

async function runPage(browser, htmlPath, label) {
  const page = await browser.newPage();
  const consoleErrors = [];
  page.on("pageerror", e => consoleErrors.push(String(e)));
  page.on("console", m => { if (m.type() === "error") consoleErrors.push(m.text()); });
  await page.goto(BASE + htmlPath, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: "domcontentloaded" });

  // Gate 0 answer scenarios — clicked through the real buttons, one page, reset between.
  const G0_SCENARIOS = JSON.parse(fs.readFileSync(path.join(HERE, "fixtures", "gate0-scenarios.json"), "utf8"));
  const gate0Runs = {};
  for (const [name, answers] of Object.entries(G0_SCENARIOS)) {
    await page.click("#g0reset");
    for (const [id, v] of Object.entries(answers))
      await page.click(`#gate0 .q[data-id="${id}"] .yn button[data-v="${v}"]`);
    gate0Runs[name] = await page.evaluate(() => ({
      status: ["green", "yellow", "red"].find(c => document.querySelector("#gate0").classList.contains(c)) || null,
      chip: document.querySelector("#gate0 .gchip").textContent.trim(),
      progress: document.querySelector("#g0prog").textContent.trim(),
      headline: document.querySelector("#g0v .verdict b")?.textContent.trim() || null,
      hint: document.querySelector("#hint0").textContent.trim(),
    }));
  }
  // leave Gate 0 answered clean for the rest of the funnel
  await page.click("#g0reset");
  for (const id of Object.keys(G0_SCENARIOS["all-yes"]))
    await page.click(`#gate0 .q[data-id="${id}"] .yn button[data-v="yes"]`);

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
  data.gate0Runs = gate0Runs;

  // ---- dossier ----------------------------------------------------------
  const dossier = {};
  await page.fill("#d_cash", "5000");
  await page.fill("#d_name", "nicheA");
  await page.click("#d_save");
  dossier.afterA = await page.evaluate(dossierTable);

  // same page and economics, but the single-season keyword and no cash typed
  await page.setInputFiles("#file", FIX("gate1-seasonal.csv"));
  await page.waitForFunction(() => /adventskalender/.test(document.querySelector("#out .cardtitle").textContent));
  await page.fill("#d_cash", "");
  await page.fill("#d_name", "nicheB");
  await page.click("#d_save");
  dossier.afterB = await page.evaluate(dossierTable);
  dossier.saveStatusB = await page.textContent("#d_status");

  // typing the cash figure and re-saving must overwrite, not duplicate
  await page.fill("#d_cash", "5000");
  await page.fill("#d_name", "nicheB");
  await page.click("#d_save");
  dossier.afterBcash = await page.evaluate(dossierTable);

  // survives a reload
  await page.reload({ waitUntil: "domcontentloaded" });
  dossier.afterReload = await page.evaluate(dossierTable);

  // cap: fill to DMAX, then one more must refuse
  for (let i = 3; i <= 10; i++) {
    await page.fill("#d_name", "filler" + i);
    await page.click("#d_save");
  }
  dossier.atCap = await page.evaluate(dossierTable);
  await page.fill("#d_name", "overflow");
  await page.click("#d_save");
  dossier.overflowStatus = await page.textContent("#d_status");
  dossier.afterOverflow = await page.evaluate(dossierTable);

  // the print export must stay one A4 landscape sheet at a full dossier
  const pdf = await page.pdf({ landscape: true, format: "A4", printBackground: true });
  const body = pdf.toString("latin1");
  dossier.printPages = (body.match(/\/Type\s*\/Page[^s]/g) || []).length;
  dossier.printHidesGates = await page.evaluate(() => {
    const s = [...document.styleSheets[0].cssRules].find(r => r.conditionText && r.conditionText.includes("print"));
    return !!s && /gate\):not\(#dossier\)|\.gate:not\(#dossier\)/.test(s.cssText);
  });

  // removing a column
  await page.click("#d_out .del[data-i='0']");
  dossier.afterDelete = await page.evaluate(dossierTable);
  data.dossier = dossier;
  // ignore the CDN fetch failure that file:// causes for the (unused) xlsx lib
  data.consoleErrors = consoleErrors.filter(e => !/xlsx|cloudflare|ERR_/i.test(e));
  data.label = label;
  await page.close();
  return data;
}

// The dossier writes to localStorage, which needs a real origin, so the pages
// are served over http exactly as Vercel serves them.
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json" };
const server = http.createServer((req, res) => {
  if (req.url === "/favicon.ico") { res.writeHead(204).end(); return; }   // not a page bug
  let rel = decodeURIComponent(req.url.split("?")[0]);
  if (rel.endsWith("/")) rel += "index.html";
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404).end("not found"); return;
  }
  res.writeHead(200, { "content-type": MIME[path.extname(file)] || "application/octet-stream" });
  res.end(fs.readFileSync(file));
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}`;

// Optional lane: if real Helium 10 exports are sitting in fixtures/ (gitignored,
// they identify the niche under research) run them through Gates 1 and 2 too.
// This is the only thing that tests the PARSING of a real export.
const REAL = { gate1: "real-gate1-chart.csv", gate2: "real-gate2-xray.csv" };
const haveReal = Object.values(REAL).every(f => fs.existsSync(FIX(f)));

async function runRealPage(browser) {
  const page = await browser.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  await page.goto(BASE + "/tools/seasonality/", { waitUntil: "domcontentloaded" });
  await page.setInputFiles("#file", FIX(REAL.gate1));
  await page.waitForSelector("#out .card, #status.err");
  await page.setInputFiles("#file2", FIX(REAL.gate2));
  await page.waitForSelector("#out2 .card, #status2.err");
  const data = await page.evaluate(() => {
    const txt = el => (el ? el.textContent.trim() : null);
    const tiles = sel => Object.fromEntries([...document.querySelectorAll(`${sel} .tile`)]
      .map(t => [t.querySelector(".k").textContent.trim(), t.querySelector(".v").textContent.trim()]));
    return {
      g1error: txt(document.querySelector("#status.err")),
      g2error: txt(document.querySelector("#status2.err")),
      g1title: txt(document.querySelector("#out .cardtitle")),
      g1meta: txt(document.querySelector("#out .meta")),
      g1tiles: tiles("#out"),
      g2meta: txt(document.querySelector("#out2 .meta")),
      g2tiles: tiles("#out2"),
      g2notes: [...document.querySelectorAll("#out2 table.checks tr")].map(tr => ({
        label: txt(tr.querySelector("td:nth-child(2) b")),
        note: txt(tr.querySelector("td:nth-child(2)")).replace(/\s+/g, " "),
      })),
    };
  });
  data.pageErrors = errs.filter(e => !/favicon|ERR_/i.test(e));
  await page.close();
  return data;
}

const exe = browserPath();
if (!exe) { console.error("No Chromium/Chrome binary found. Install Chrome, or set one of:\n" + CANDIDATE_BROWSERS.join("\n")); process.exit(2); }
const browser = await chromium.launch({ executablePath: exe, headless: true });
const results = {
  browser: exe,
  en: await runPage(browser, "/tools/seasonality/", "EN"),
  ru: await runPage(browser, "/tools/seasonality/ru/", "RU"),
  real: haveReal ? await runRealPage(browser) : null,
};
await browser.close();
server.close();
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "page.json"), JSON.stringify(results, null, 2));
console.log(haveReal ? "real Helium 10 exports: present, exercised"
                     : "real Helium 10 exports: absent, synthetic fixtures only");
console.log("page.json written · EN gate chips:",
  ["gate1","gate2","gate3","gate4"].map(g => `${g}=${results.en[g].status}`).join(" "));

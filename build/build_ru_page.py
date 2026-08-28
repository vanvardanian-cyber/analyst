#!/usr/bin/env python3
# Generate the Russian funnel page from the English one via exact-string translation.
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "seasonality", "index.html")
DST = os.path.join(ROOT, "tools", "seasonality", "ru", "index.html")

s = open(SRC, encoding="utf-8").read()
P = []  # (old, new, expected_count or None=any>=1)
def t(old, new, n=None): P.append((old, new, n))

# ---------- head / header ----------
t('<html lang="en">', '<html lang="ru">')
t('<title>EaseStore · Niche Funnel</title>', '<title>EaseStore · Воронка ниш</title>')
t('<h1>Niche Funnel <span style="font-size:12px;color:var(--ink-muted);font-weight:400">beta · easestore.de</span> <a href="ru/" style="font-size:12px;font-weight:400;color:var(--series-1);margin-left:8px">RU</a></h1>',
  '<h1>Воронка ниш <span style="font-size:12px;color:var(--ink-muted);font-weight:400">beta · easestore.de</span> <a href="../" style="font-size:12px;font-weight:400;color:var(--series-1);margin-left:8px">EN</a></h1>')
t('<p class="tag">Four gates, in order: is demand real and rising → can you win the page → does a unit earn enough → which keyword opens the door. Drop the Helium&nbsp;10 exports, get honest verdicts. A yellow or red gate never blocks you — it tells you what you are accepting if you continue.</p>',
  '<p class="tag">Четыре этапа по порядку: спрос реален и растёт → можно ли выиграть страницу → зарабатывает ли юнит достаточно → какой ключ открывает дверь. Бросьте экспорты Helium&nbsp;10 — получите честные вердикты. Жёлтый или красный этап никогда не блокирует: он говорит, что именно вы принимаете, если идёте дальше.</p>')
t('<b>Your files never leave your browser.</b> Everything is computed on your device; nothing is uploaded or stored.',
  '<b>Ваши файлы не покидают браузер.</b> Всё считается на вашем устройстве; ничего не загружается и не хранится.')

# ---------- steps ----------
t('<b>1</b>&nbsp;Seasonality &amp; direction', '<b>1</b>&nbsp;Сезонность и направление')
t('<b>2</b>&nbsp;Competition (Xray)', '<b>2</b>&nbsp;Конкуренция (Xray)')
t('<b>3</b>&nbsp;Unit economics', '<b>3</b>&nbsp;Юнит-экономика')
t('<b>4</b>&nbsp;Keywords &amp; launch cost', '<b>4</b>&nbsp;Ключи и цена запуска')

# ---------- gate 1 ----------
t('Gate 1 — Seasonality &amp; direction <span class="gchip">not run</span>',
  'Этап 1 — Сезонность и направление <span class="gchip">не запускался</span>')
t('<p class="gsub">Cerebro → Analyze Keywords → chart icon next to Search Volume → period “All time” → download. Kills more bad niches per minute than any other check.</p>',
  '<p class="gsub">Cerebro → Analyze Keywords → иконка графика рядом с Search Volume → период «All time» → скачать. Убивает больше плохих ниш в минуту, чем любая другая проверка.</p>')
t('Drop the search-volume export ', 'Бросьте экспорт истории поискового объёма ')
t('or click to choose', 'или кликните для выбора')  # x3
t('.csv or .xlsx · one date column + one column per keyword · best with 36 months, minimum 24',
  '.csv или .xlsx · колонка дат + колонка на каждый ключ · лучше всего 36 месяцев, минимум 24')
t('Try with example data', 'Попробовать на примере')  # x2

# ---------- gate 2 ----------
t('Gate 2 — Competition &amp; page economics <span class="gchip">not run</span>',
  'Этап 2 — Конкуренция и экономика страницы <span class="gchip">не запускался</span>')
t('<p class="gsub">Xray on the search results page → export CSV. The tool deduplicates sponsored repeats, drops off-niche ads, and runs the selection gates on what is left.</p>',
  '<p class="gsub">Xray на странице выдачи → Export → CSV. Инструмент убирает повторы спонсорских позиций, отбрасывает случайную рекламу из чужих ниш и прогоняет ворота отбора по тому, что осталось.</p>')
t('Drop the Xray export ', 'Бросьте экспорт Xray ')
t('.csv or .xlsx from Helium&nbsp;10 Xray (search results view, Amazon.de)',
  '.csv или .xlsx из Helium&nbsp;10 Xray (страница выдачи, Amazon.de)')

# ---------- gate 3 ----------
t('Gate 3 — Unit economics <span class="gchip">not run</span>',
  'Этап 3 — Юнит-экономика <span class="gchip">не запускался</span>')
t('<p class="gsub">German deemed-supplier math: VAT never reaches you, referral fee is charged on the VAT-inclusive price, duty on the CIF base. Type your numbers — everything recalculates live.</p>',
  '<p class="gsub">Немецкая математика deemed supplier: VAT до вас не доходит, реферальная комиссия берётся с цены с VAT, пошлина — с базы CIF. Введите свои цифры — всё пересчитывается на лету.</p>')
t('Sale price, gross incl. VAT (€)', 'Цена продажи, брутто с VAT (€)')
t('Referral fee %', 'Реферальная комиссия %')
t('FBA fulfilment fee (€)', 'Комиссия FBA за юнит (€)')
t('Storage per unit sold (€)', 'Хранение на проданный юнит (€)')
t('Returns rate %', 'Доля возвратов %')
t('Return cost, % of net price', 'Стоимость возврата, % от нетто-цены')
t('EXW unit cost (€)', 'Цена EXW за юнит (€)')
t('Freight per unit (€)', 'Фрахт за юнит (€)')
t('Import duty % (on CIF)', 'Импортная пошлина % (на CIF)')
t('Prep / labels / inspection (€)', 'Преп / этикетки / инспекция (€)')
t('Turnover tax % (home country)', 'Налог с оборота % (своя страна)')
t('VAT 19% fixed (DE standard rate). Import VAT is a cash-flow item, not a unit cost — plan it in the workbook, Sheet 8.',
  'VAT 19% фиксирован (стандартная ставка DE). Импортный VAT — статья кэш-флоу, а не юнит-кост: планируйте его в книге, Лист 8.')

# ---------- gate 4 ----------
t('Gate 4 — Keywords &amp; launch cost <span class="gchip">not run</span>',
  'Этап 4 — Ключи и цена запуска <span class="gchip">не запускался</span>')
t('<p class="gsub">Cerebro results table → Export → CSV. Which keywords have real buyers (not just searches), which are fads, and what pushing to page 1 actually costs.</p>',
  '<p class="gsub">Таблица результатов Cerebro → Export → CSV. Какие ключи дают реальных покупателей (а не просто поиски), где хайп-всплески и сколько реально стоит пробиться на страницу 1.</p>')
t('Drop the Cerebro keyword export ', 'Бросьте экспорт ключей из Cerebro ')
t('.csv or .xlsx — the keyword table export (with Keyword Sales, Search Volume, CPR, Title Density)',
  '.csv или .xlsx — экспорт таблицы ключей (с Keyword Sales, Search Volume, CPR, Title Density)')
t('Landed cost per unit (€)', 'Себестоимость с доставкой, за юнит (€)')
t('Launch discount per unit (€)', 'Скидка запуска на юнит (€)')
t('Daily launch ad spend (€)', 'Дневной рекламный бюджет запуска (€)')
t('Max affordable push (€)', 'Максимум на разгон (€)')
t('Landed cost auto-fills from Gate 3 until you type your own. Push cost = CPR units × (landed + discount) + 8 days of launch ads — an order of magnitude, not an invoice.',
  'Себестоимость подтягивается из Этапа 3, пока вы не введёте свою. Цена разгона = юниты CPR × (себестоимость + скидка) + 8 дней рекламы — порядок величины, а не счёт на оплату.')

# ---------- footer ----------
t('<b>How to get the files:</b>', '<b>Где взять файлы:</b>')
t('<li><b>Gate 1:</b> Helium 10 → Cerebro → <i>Analyze Keywords</i> → marketplace <b>Amazon.de</b> → parent keyword (+ 2–3 children, comma-separated — one search credit) → chart icon next to Search Volume → period <b>“All time”</b> → download.</li>',
  '<li><b>Этап 1:</b> Helium 10 → Cerebro → <i>Analyze Keywords</i> → маркетплейс <b>Amazon.de</b> → родительский ключ (+ 2–3 дочерних через запятую — один поисковый кредит) → иконка графика рядом с Search Volume → период <b>«All time»</b> → скачать.</li>')
t('<li><b>Gate 2:</b> search the parent keyword on Amazon.de → run <b>Xray</b> on the results page → Export → CSV. Export the full page; the tool deduplicates and filters.</li>',
  '<li><b>Этап 2:</b> найдите родительский ключ на Amazon.de → запустите <b>Xray</b> на странице выдачи → Export → CSV. Экспортируйте всю страницу; инструмент сам чистит и фильтрует.</li>')
t('<li><b>Gate 3:</b> FBA fee from Xray or the Revenue Calculator; EXW from supplier quotes; freight from your forwarder’s rate × unit volume.</li>',
  '<li><b>Этап 3:</b> комиссия FBA — из Xray или Revenue Calculator; EXW — из котировок поставщиков; фрахт — ставка вашего экспедитора × объём юнита.</li>')
t("<li><b>Gate 4:</b> Cerebro → run the parent + children → export the keyword results table as CSV (not the chart — that file is Gate 1's).</li>",
  '<li><b>Этап 4:</b> Cerebro → прогоните родителя + детей → экспортируйте таблицу ключей как CSV (не график — тот файл для Этапа 1).</li>')
t('<b>Method &amp; thresholds:</b> classical multiplicative decomposition, seasonal strength and year consistency after Hyndman &amp; Athanasopoulos (otexts.com/fpp3); selection gates follow the EaseStore workbook (page revenue, review moat, Amazon presence, CN/HK share, fresh entrants); price corridor and margin floor after common practitioner benchmarks (Freedom Ticket) — tightened for German VAT reality. Review-wall months assume 300 units/month at a 1.5% review rate. All thresholds documented, none hidden. Educational tool, not financial advice. © EaseStore 2026',
  '<b>Метод и пороги:</b> классическая мультипликативная декомпозиция, сезонная сила и согласованность лет — по Hyndman &amp; Athanasopoulos (otexts.com/fpp3); ворота отбора повторяют книгу EaseStore (выручка страницы, стена отзывов, присутствие Amazon, доля CN/HK, свежие входы); ценовой коридор и порог маржи — по распространённым практическим бенчмаркам (Freedom Ticket), ужесточённым под немецкую реальность с VAT. Месяцы «стены отзывов» считаются при 300 юнитах/мес и 1,5% отзывов. Все пороги задокументированы, скрытых нет. Учебный инструмент, не финансовая консультация. © EaseStore 2026')

# ---------- JS: months & locale ----------
t('const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];',
  'const MONTHS = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"];')
t('toLocaleString("en-US"', 'toLocaleString("ru-RU"')

# ---------- JS: gate machinery ----------
t('{ green:"PASS", yellow:"CAUTION", red:"CHANGE NICHE?" }', '{ green:"ПРОЙДЕН", yellow:"ОСТОРОЖНО", red:"СМЕНИТЬ НИШУ?" }')
t('const nxt = n<4 ? ` Next: Gate ${n+1}.` : " Funnel done — continue in the workbook (Sheets 4–8: full checklist, order size, cash plan).";',
  'const nxt = n<4 ? ` Дальше: Этап ${n+1}.` : " Воронка пройдена — продолжайте в книге (Листы 4–8: полный чек-лист, размер заказа, кэш-план).";')
t('"✓ Gate passed."', '"✓ Этап пройден."')
t('"▲ You can continue, but the warnings above are the risks you are accepting."',
  '"▲ Можно идти дальше, но предупреждения выше — это риски, которые вы принимаете."')
t('"✖ This niche failed hard checks. You can still continue to learn the numbers — but for a first product, changing the niche is the recommendation."',
  '"✖ Ниша провалила жёсткие проверки. Можно продолжить ради цифр — но для первого товара рекомендация: сменить нишу."')

# ---------- JS: shared errors ----------
t('"Could not read any rows from the file."', '"Не удалось прочитать строки из файла."')
t('"Excel library failed to load — export as CSV instead."', '"Библиотека Excel не загрузилась — экспортируйте как CSV."')
t('"This is the Xray export — it goes to Gate 2 below. Gate 1 takes the search-volume history file (Cerebro → chart icon → download)."',
  '"Это экспорт Xray — он идёт в Этап 2 ниже. Этап 1 принимает файл ИСТОРИИ поискового объёма (Cerebro → иконка графика → скачать)."')
t('"This is the Cerebro keyword-table export — it goes to Gate 4 below. Gate 1 takes the search-volume HISTORY file (chart icon → download)."',
  '"Это экспорт таблицы ключей Cerebro — он идёт в Этап 4 ниже. Этап 1 принимает файл ИСТОРИИ поискового объёма (иконка графика → скачать)."')
t('"No date column found. This looks like a different export — Gate 1 needs the search-volume history file (Gate 2 takes the Xray file below)."',
  '"Колонка с датами не найдена. Похоже, это другой экспорт — Этапу 1 нужен файл истории поискового объёма (файл Xray идёт в Этап 2 ниже)."')
t('"No keyword columns with numbers found next to the date column."',
  '"Рядом с колонкой дат не найдено числовых колонок ключей."')

# ---------- JS: gate 1 verdicts ----------
t('"INCOMPLETE","Only "+r.calMonths+" of 12 calendar months covered — nothing here is reliable yet."',
  '"НЕПОЛНЫЕ ДАННЫЕ","Покрыто только "+r.calMonths+" из 12 календарных месяцев — пока ничему здесь верить нельзя."')
t('"ONE YEAR ONLY","With under 24 months, season and noise cannot be separated. Re-export with the period set to All time."',
  '"ТОЛЬКО ОДИН ГОД","При менее чем 24 месяцах сезон не отделить от шума. Переэкспортируйте с периодом All time."')
t('"PATTERN IS REAL","The years agree with each other (consistency "+cs+") — trust the shape below."+st',
  '"ПАТТЕРН РЕАЛЕН","Годы согласуются между собой (согласованность "+cs+") — форме ниже можно верить."+st')
t('" Seasonal strength "+r.strength.toFixed(2)+" agrees."', '" Сезонная сила "+r.strength.toFixed(2)+" это подтверждает."')
t('"PATTERN UNCERTAIN","The years only partly agree (consistency "+cs+"). Verify the shape on Google Trends (DE, 5y) and Product Opportunity Explorer before timing an order."',
  '"ПАТТЕРН НЕ ТОЧЕН","Годы согласуются лишь частично (согласованность "+cs+"). Проверьте форму в Google Trends (DE, 5 лет) и Product Opportunity Explorer, прежде чем привязывать заказ к датам."')
t('"NO RELIABLE PATTERN","The years disagree (consistency "+cs+") — the ups and downs are mostly noise, and the amplitude number is not meaningful. Treat demand as flat."',
  '"НАДЁЖНОГО ПАТТЕРНА НЕТ","Годы противоречат друг другу (согласованность "+cs+") — колебания в основном шум, и амплитуда не имеет смысла. Считайте спрос ровным."')
t('"INCOMPLETE","Fill a full year of data first."', '"НЕПОЛНЫЕ ДАННЫЕ","Сначала заполните полный год."')
t('"EXTREME","A zero-demand month: extreme single-season. Avoid as a first product."',
  '"ЭКСТРИМ","Месяц с нулевым спросом: экстремальная односезонность. Не для первого товара."')
t('"FLAT","Essentially flat demand. Order timing is not critical."',
  '"РОВНО","Спрос практически ровный. Тайминг заказа не критичен."')
t('"TREAT AS FLAT","Amplitude "+r.amp.toFixed(2)+"× looks seasonal, but the years disagree — likely noise. Do not time orders on this."',
  '"СЧИТАЙТЕ РОВНЫМ","Амплитуда "+r.amp.toFixed(2)+"× выглядит сезонной, но годы не согласуются — скорее шум. Не привязывайте заказ к этой форме."')
t('"FLAT","Flat demand. Order timing is not critical."',
  '"РОВНО","Ровный спрос. Тайминг заказа не критичен."')
t('"MODERATE","Moderate seasonality. Time the order, but sales run all year."',
  '"УМЕРЕННО","Умеренная сезонность. Заказ по календарю, но продажи идут весь год."')
t('"STRONG","Strong seasonality. Stock must land 4 weeks before the ramp; exit the peak lean."',
  '"СИЛЬНО","Сильная сезонность. Товар должен приземлиться за 4 недели до разгона; из пика выходите с минимальным остатком."')
t('"SINGLE-SEASON","A working-capital trap for a first product."',
  '"ОДИН СЕЗОН","Ловушка оборотного капитала для первого товара."')
t('"NO YoY","Fewer than 24 months — direction unknown. Check Google Trends (DE, 5 years)."',
  '"НЕТ YoY","Меньше 24 месяцев — направление неизвестно. Проверьте Google Trends (DE, 5 лет)."')
t('" (prior year "', '" (годом ранее "')
t('"GROWING","+"+p+prev+". Check it isn’t one viral ASIN: is page-1 revenue spread across many listings?"',
  '"РАСТЁТ","+"+p+prev+". Проверьте, что это не один вирусный ASIN: распределена ли выручка страницы 1 по многим листингам?"')
t('"FLAT",p+prev+". Fine for entry — win by taking share."',
  '"СТАБИЛЬНО",p+prev+". Для входа годится — выигрывайте, забирая долю."')
t('"COOLING",p+prev+". Google Trends DE, 5 years: plateau = ok; steady slide = drop. Compare the traditional synonym too."',
  '"ОСТЫВАЕТ",p+prev+". Google Trends DE, 5 лет: плато = ок; устойчивое сползание = отказ. Сравните и с традиционным синонимом."')
t('"DECLINING",p+prev+". Drop unless Trends shows a clearly temporary dip."',
  '"ПАДАЕТ",p+prev+". Отказ, если Trends не показывает явно временный провал."')

# ---------- JS: gate 1 render ----------
t(' complete months used (', ' полных месяцев (')
t(' year${r.blocks.length>1?"s":""} compared · weekly points averaged per calendar month · current month dropped',
  ' г. в сравнении · недельные точки усреднены по календарным месяцам · текущий месяц отброшен')
t(' average index (bars)', ' средний индекс (столбцы)')
t('${tile("Amplitude", fmt(r.amp), "peak ÷ lowest month")}', '${tile("Амплитуда", fmt(r.amp), "пик ÷ худший месяц")}')
t('${tile("Consistency", r.consistency==null?"—":fmt(r.consistency), "do the years agree? (−1…1)")}',
  '${tile("Согласованность", r.consistency==null?"—":fmt(r.consistency), "согласны ли годы? (−1…1)")}')
t('${tile("Seasonal strength", r.strength==null?"needs 3 yrs":fmt(r.strength), "seasonal share of variation (0–1)")}',
  '${tile("Сезонная сила", r.strength==null?"нужно 3 года":fmt(r.strength), "доля сезонности в колебаниях (0–1)")}')
t('${tile("Top-4 share", r.top4==null?"—":(r.top4*100).toFixed(1)+"%", ">60% = 4-month business")}',
  '${tile("Доля топ-4", r.top4==null?"—":(r.top4*100).toFixed(1)+"%", ">60% = бизнес на 4 месяца")}')
t('${tile("YoY", r.yoy==null?"—":(r.yoy>0?"+":"")+(r.yoy*100).toFixed(1)+"%", "last 12 vs previous 12")}',
  '${tile("YoY", r.yoy==null?"—":(r.yoy>0?"+":"")+(r.yoy*100).toFixed(1)+"%", "последние 12 мес к предыдущим 12")}')
t('${tile("Ramp month", r.ramp==null?"—":MONTHS[r.ramp], "stock lands 4 weeks earlier")}',
  '${tile("Месяц разгона", r.ramp==null?"—":MONTHS[r.ramp], "товар приземляется на 4 недели раньше")}')
t('<h3>Seasonality index by month (1.00 = average month)</h3>', '<h3>Индекс сезонности по месяцам (1.00 = средний месяц)</h3>')
t('<summary>Data table</summary><table><tr><th>Month</th><th>Avg volume</th><th>Index</th></tr>',
  '<summary>Таблица данных</summary><table><tr><th>Месяц</th><th>Средний объём</th><th>Индекс</th></tr>')
t('aria-label="Seasonality index by month for ${r.name}"', 'aria-label="Индекс сезонности по месяцам: ${r.name}"')
t('tip.textContent = `${MONTHS[i]} · index ${r.index[i].toFixed(2)} · avg ${Math.round(r.profAvg[i]).toLocaleString("ru-RU")}`;',
  'tip.textContent = `${MONTHS[i]} · индекс ${r.index[i].toFixed(2)} · сред. ${Math.round(r.profAvg[i]).toLocaleString("ru-RU")}`;')
t('st.textContent = results.length + " keyword" + (results.length>1?"s":"") + " analyzed.";',
  'st.textContent = "Ключей проанализировано: " + results.length + ".";')
t('st.className="status"; st.textContent = "Reading " + file.name', 'st.className="status"; st.textContent = "Читаю " + file.name')
t('(example)', '(пример)')

# ---------- JS: gate 2 parse errors ----------
t('"This is the Cerebro keyword-table export — it goes to Gate 4 below."',
  '"Это экспорт таблицы ключей Cerebro — он идёт в Этап 4 ниже."')
t('"This does not look like an Xray export (no ASIN / ASIN Revenue columns). Gate 2 needs the Xray file; the search-volume history goes to Gate 1 above."',
  '"Не похоже на экспорт Xray (нет колонок ASIN / ASIN Revenue). Этапу 2 нужен файл Xray; история поискового объёма идёт в Этап 1 выше."')
t('"No product rows found in the export."', '"В экспорте не найдено строк с товарами."')

# ---------- JS: gate 2 checks ----------
t('"Page revenue (top-10 listings)", eur(a.top10Rev)+"/mo",\n      "≥ €40k/mo proves a real market. Whole export: "+eur(a.total)+"/mo across "+a.n+" listings.",',
  '"Выручка страницы (топ-10 листингов)", eur(a.top10Rev)+"/мес",\n      "≥ €40k/мес доказывает реальный рынок. Весь экспорт: "+eur(a.total)+"/мес на "+a.n+" листингов.",')
t('"Top ASIN share of page revenue", (a.topShare*100).toFixed(1)+"%",\n      a.topShare>0.40 ? "One listing owns the page — you would fight a monopolist." :\n      "Fragmented enough. Top brand overall: "+a.topBrand[0]+" at "+(a.brandShare*100).toFixed(0)+"% (brands can hold several ASINs)."',
  '"Доля топ-ASIN в выручке страницы", (a.topShare*100).toFixed(1)+"%",\n      a.topShare>0.40 ? "Страницей владеет один листинг — вы будете воевать с монополистом." :\n      "Достаточно фрагментировано. Топ-бренд всего: "+a.topBrand[0]+" с "+(a.brandShare*100).toFixed(0)+"% (у бренда может быть несколько ASIN)."')
t('let moatNote = a.over500+" above 500, "+a.over2000+" above 2,000 · median of top-10 = "+fmt0(a.medTop10Reviews)+\n      " reviews ≈ "+(a.wallMonths==null?"—":fmt0(a.wallMonths))+" months to match at 300 units/mo, 1.5% review rate. The workbook gate allows 0–2.";',
  'let moatNote = a.over500+" выше 500, "+a.over2000+" выше 2 000 · медиана топ-10 = "+fmt0(a.medTop10Reviews)+\n      " отзывов ≈ "+(a.wallMonths==null?"—":fmt0(a.wallMonths))+" мес, чтобы догнать при 300 юнитах/мес и 1,5% отзывов. Ворота книги допускают 0–2.";')
t('" ⚠ ALL proof listings sit on veteran seller accounts (>18 months) — buyers tolerate low reviews here, but so far only experienced operators have exploited it."',
  '" ⚠ ВСЕ листинги-доказательства сидят на аккаунтах-ветеранах (>18 мес) — покупатели терпят малое число отзывов, но пока этим пользовались только опытные операторы."')
t('" of them run on seller accounts under 18 months old ("+a.lowRevNewShops.slice(0,3).map(p=>p.brand).join(", ")+") — the closest signal to a true cold start (account age can still hide a funded operator behind a new storefront)."',
  '" из них — на аккаунтах продавцов младше 18 мес ("+a.lowRevNewShops.slice(0,3).map(p=>p.brand).join(", ")+") — самый близкий сигнал к настоящему холодному старту (возраст аккаунта всё же может прятать опытного оператора за новой витриной)."')
t('" BUT the wall is not binding: "+proof+" listings with ≤100 reviews already earn >€3k/mo ("',
  '" НО стена не держит: "+proof+" листингов с ≤100 отзывами уже зарабатывают >€3k/мес ("')
t('") — buyers here demonstrably purchase from low-review listings. Expensive, not impossible."',
  '") — покупатели здесь доказуемо берут у листингов с малым числом отзывов. Дорого, но не невозможно."')
t('" ≥5 such listings = the Black Box 5×5 proof-of-entry standard."',
  '" ≥5 таких листингов = стандарт доказательства входа Black Box 5×5."')
t('" Proof of entry: "+proof+" listings with ≤100 reviews earn >€3k/mo."',
  '" Доказательство входа: "+proof+" листингов с ≤100 отзывами зарабатывают >€3k/мес."')
t('"Review moat: listings above 500 reviews", String(a.over500), moatNote,',
  '"Стена отзывов: листингов выше 500 отзывов", String(a.over500), moatNote,')
t('"Amazon Retail / Amazon Basics on the page", a.amazon.length===0 ? "none" : a.amazon.length+" listings ("+(a.amazonShare*100).toFixed(0)+"% rev)",',
  '"Amazon Retail / Amazon Basics на странице", a.amazon.length===0 ? "нет" : a.amazon.length+" листингов ("+(a.amazonShare*100).toFixed(0)+"% выручки)",')
t('a.amazon.length===0 ? "Clear." :\n      amzDominant ? "Amazon is DOMINANT here — "+(amzInTop10?"a listing in the top-10 earners":"≥10% of page revenue")+". They sell at any price, forever. Hard NO in the workbook." :\n      "Present but not winning ("+(a.amazonShare*100).toFixed(0)+"% of revenue, none in the top-10). The risk is the PRICE ANCHOR: buyers treat Amazon\'s price as the fair one, capping yours — your differentiation must justify the gap. Watch that their listings stay mid-page.",',
  'a.amazon.length===0 ? "Чисто." :\n      amzDominant ? "Amazon здесь ДОМИНИРУЕТ — "+(amzInTop10?"листинг в топ-10 по выручке":"≥10% выручки страницы")+". Он может продавать по любой цене сколько угодно. Жёсткое НЕТ в книге." :\n      "Присутствует, но не выигрывает ("+(a.amazonShare*100).toFixed(0)+"% выручки, никого в топ-10). Риск — ЦЕНОВОЙ ЯКОРЬ: покупатели считают цену Amazon справедливой, что ограничивает вашу — дифференциация должна оправдывать разницу. Следите, чтобы их листинги оставались в середине страницы.",')
t('"China + Hong Kong revenue share", (a.cnhkShare*100).toFixed(0)+"%",\n      "Above 60% = price-war territory with factory-direct sellers."',
  '"Доля выручки Китая + Гонконга", (a.cnhkShare*100).toFixed(0)+"%",\n      "Выше 60% = территория ценовой войны с продавцами напрямую от фабрик."')
t('let frNote = a.fresh.length+" listings under 12 months old already doing >€3k/mo — entry demonstrably works"+\n    (a.fresh.length && a.freshNewShops ? " ("+a.freshNewShops.length+" of them on seller accounts under 18 months)." : ".");',
  'let frNote = a.fresh.length+" листингов младше 12 месяцев уже делают >€3k/мес — вход доказуемо работает"+\n    (a.fresh.length && a.freshNewShops ? " ("+a.freshNewShops.length+" из них на аккаунтах продавцов младше 18 мес)." : ".");')
t('if (a.freshHeavy.length) frNote += " ⚠ "+a.freshHeavy.length+" of them jumped straight to >€20k/mo ("+\n      a.freshHeavy.slice(0,3).map(p=>p.brand).join(", ")+") — that is relaunch or outside traffic, not a cold start. Don\'t read it as easy entry."',
  'if (a.freshHeavy.length) frNote += " ⚠ "+a.freshHeavy.length+" из них сразу прыгнули выше €20k/мес ("+\n      a.freshHeavy.slice(0,3).map(p=>p.brand).join(", ")+") — это перезапуск или внешний трафик, не холодный старт. Не читайте это как лёгкий вход."')
t('if (!a.fresh.length) frNote = "No successful recent entrants — the page may be locked.";',
  'if (!a.fresh.length) frNote = "Успешных свежих входов нет — страница, возможно, заперта.";')
t('add(fr, "Fresh entrants (<12 months, >€3k/mo)", String(a.fresh.length), frNote);',
  'add(fr, "Свежие входы (<12 мес, >€3k/мес)", String(a.fresh.length), frNote);')
t('"Weak competitor to attack (≤4.3★, ≥€2k/mo)", a.weak.length ? a.weak.length+" found" : "none",\n      a.weak.length ? "Best target: "+a.weak[0].brand+" ("+a.weak[0].rating+"★, "+eur(a.weak[0].rev)+"/mo). Mine its 1–3★ reviews (workbook Sheet 11)." :\n      "A 4.5★+ field gives no obvious point of attack — differentiation must come from elsewhere."',
  '"Слабый конкурент для атаки (≤4.3★, ≥€2k/мес)", a.weak.length ? "найдено: "+a.weak.length : "нет",\n      a.weak.length ? "Лучшая цель: "+a.weak[0].brand+" ("+a.weak[0].rating+"★, "+eur(a.weak[0].rev)+"/мес). Разберите его отзывы 1–3★ (книга, Лист 11)." :\n      "Поле сплошь 4.5★+ — очевидной точки атаки нет, дифференциацию придётся искать в другом."')
t('"Price corridor (median price)", a.medPrice==null?"—":"€"+a.medPrice.toFixed(2),\n      "€20–70 sweet spot: below it Amazon fees eat the margin ("+(a.medFeeShare==null?"—":(a.medFeeShare*100).toFixed(0))+"% of price here already), far above it conversion needs brand trust."',
  '"Ценовой коридор (медианная цена)", a.medPrice==null?"—":"€"+a.medPrice.toFixed(2),\n      "Зона €20–70: ниже комиссии Amazon съедают маржу (здесь уже "+(a.medFeeShare==null?"—":(a.medFeeShare*100).toFixed(0))+"% цены), сильно выше — конверсии нужно доверие к бренду."')
t('"Median shipping weight", a.medWeight==null?"—":a.medWeight.toFixed(1)+" kg",\n      "Heavy products = freight-dominated landed cost, and every return hurts. Above ~4 kg a small budget cannot buy competitive stock."',
  '"Медианный вес отправления", a.medWeight==null?"—":a.medWeight.toFixed(1)+" кг",\n      "Тяжёлый товар = себестоимость, где доминирует фрахт, и каждый возврат бьёт больно. Выше ~4 кг малый бюджет не купит конкурентный сток."')

# ---------- JS: gate 2 render ----------
t('<h3 class="cardtitle">Competition check</h3>', '<h3 class="cardtitle">Проверка конкуренции</h3>')
t(' unique listings after cleaning (', ' уникальных листингов после очистки (')
t('${res.dupes} sponsored duplicates removed', 'убрано спонсорских дублей: ${res.dupes}')
t('+res.offNiche+" off-niche ad"+(res.offNiche>1?"s":"")+" dropped"', '+"убрано чужой рекламы: "+res.offNiche')
t('${tile("Top-10 revenue", "€"+fmt0(a.top10Rev), "per month")}', '${tile("Выручка топ-10", "€"+fmt0(a.top10Rev), "в месяц")}')
t('${tile("Top ASIN share", (a.topShare*100).toFixed(1)+"%", "of whole page")}', '${tile("Доля топ-ASIN", (a.topShare*100).toFixed(1)+"%", "от всей страницы")}')
t('${tile("Reviews >500", String(a.over500), "listings (gate: ≤2)")}', '${tile("Отзывы >500", String(a.over500), "листингов (ворота: ≤2)")}')
t('${tile("Median top-10 reviews", fmt0(a.medTop10Reviews), "≈ "+(a.wallMonths==null?"—":fmt0(a.wallMonths))+" months wall")}',
  '${tile("Медиана отзывов топ-10", fmt0(a.medTop10Reviews), "≈ "+(a.wallMonths==null?"—":fmt0(a.wallMonths))+" мес стены")}')
t('${tile("CN+HK share", (a.cnhkShare*100).toFixed(0)+"%", "of revenue")}', '${tile("Доля CN+HK", (a.cnhkShare*100).toFixed(0)+"%", "от выручки")}')
t('${tile("Median price", a.medPrice==null?"—":"€"+a.medPrice.toFixed(2), (a.medFeeShare==null?"":"fees "+(a.medFeeShare*100).toFixed(0)+"% of price"))}',
  '${tile("Медианная цена", a.medPrice==null?"—":"€"+a.medPrice.toFixed(2), (a.medFeeShare==null?"":"комиссии "+(a.medFeeShare*100).toFixed(0)+"% цены"))}')
t(">HARD GATE</span>", ">ЖЁСТКИЕ ВОРОТА</span>")
t('["good","PAGE IS WINNABLE","No hard gate failed. Take the survivors to Gate 3 and the workbook checklist (Sheet 4)."]',
  '["good","СТРАНИЦУ МОЖНО ВЫИГРАТЬ","Ни одни жёсткие ворота не провалены. Ведите выживших в Этап 3 и чек-лист книги (Лист 4)."]')
t('["warning","WINNABLE WITH CAVEATS","Nothing fatal, but read the yellow rows — each one is a cost or a risk you are choosing to carry."]',
  '["warning","МОЖНО, НО С ОГОВОРКАМИ","Фатального нет, но прочитайте жёлтые строки — каждая из них цена или риск, которые вы берёте на себя."]')
t('["critical","THIS PAGE WILL BE VERY EXPENSIVE TO CRACK","A hard gate failed. Big pages like this reward the already-strong; for a first product with a small budget the recommendation is: find another niche. Continue to Gate 3 if you want the numbers anyway."]',
  '["critical","ВЗЛОМАТЬ ЭТУ СТРАНИЦУ БУДЕТ ОЧЕНЬ ДОРОГО","Провалены жёсткие ворота. Такие большие страницы вознаграждают и без того сильных; для первого товара с малым бюджетом рекомендация — искать другую нишу. Хотите цифры — продолжайте в Этап 3."]')
t('<summary>Top 10 listings by revenue</summary><table>\n      <tr><th>Brand</th><th>ASIN</th><th>Rev €/mo</th><th>Reviews</th><th>★</th><th>From</th></tr>',
  '<summary>Топ-10 листингов по выручке</summary><table>\n      <tr><th>Бренд</th><th>ASIN</th><th>Выручка €/мес</th><th>Отзывы</th><th>★</th><th>Откуда</th></tr>')

# ---------- JS: gate 3 ----------
t('tile("Net revenue", "€"+net.toFixed(2), "price ÷ 1.19 (VAT out)")', 'tile("Нетто-выручка", "€"+net.toFixed(2), "цена ÷ 1,19 (без VAT)")')
t('tile("Amazon payout / unit", "€"+payout.toFixed(2), "after referral, FBA, storage, returns")',
  'tile("Выплата Amazon за юнит", "€"+payout.toFixed(2), "после комиссии, FBA, хранения, возвратов")')
t('tile("Landed cost / unit", "€"+landed.toFixed(2), "EXW + freight + duty(CIF) + prep")',
  'tile("Себестоимость за юнит", "€"+landed.toFixed(2), "EXW + фрахт + пошлина(CIF) + преп")')
t('tile("Contribution margin", "€"+cm.toFixed(2), "per unit, before ads")',
  'tile("Contribution margin", "€"+cm.toFixed(2), "за юнит, до рекламы")')
t('tile("Margin % of net", (margin*100).toFixed(1)+"%", "gate: ≥35% before ads")',
  'tile("Маржа % от нетто", (margin*100).toFixed(1)+"%", "ворота: ≥35% до рекламы")')
t('tile("Breakeven ACOS", (beAcos*100).toFixed(1)+"%", "CM ÷ GROSS price (console basis)")',
  'tile("Порог ACOS", (beAcos*100).toFixed(1)+"%", "CM ÷ БРУТТО-цена (база консоли)")')
t('tile("Max EXW at 35%", "€"+maxExw.toFixed(2), "your ceiling for supplier quotes")',
  'tile("Макс. EXW при 35%", "€"+maxExw.toFixed(2), "ваш потолок для котировок поставщика")')
t('["good","MARGIN OK","≥35% before advertising — there is room for PPC and mistakes. Continue to the workbook: Sheet 4 full checklist, Sheet 6 order size, Sheet 8 cash plan."]',
  '["good","МАРЖА ОК","≥35% до рекламы — есть запас на PPC и ошибки. Дальше в книгу: Лист 4 полный чек-лист, Лист 6 размер заказа, Лист 8 кэш-план."]')
t('["warning","THIN","30–35%: workable only if the launch goes well. Push the supplier below €"+Math.max(0,maxExw).toFixed(2)+" EXW or raise the price."]',
  '["warning","ТОНКО","30–35%: сработает только при удачном запуске. Продавите поставщика ниже €"+Math.max(0,maxExw).toFixed(2)+" EXW или поднимите цену."]')
t('["critical","NOT ENOUGH MARGIN","Below 30% before ads there is no room for PPC, returns spikes, or fee increases. Change the price point, the supplier, or the product."]',
  '["critical","МАРЖИ НЕ ХВАТАЕТ","Ниже 30% до рекламы нет места ни для PPC, ни для всплесков возвратов, ни для роста комиссий. Меняйте цену, поставщика или товар."]')

# ---------- JS: gate 4 ----------
t('"This is the Xray export — it goes to Gate 2 above."', '"Это экспорт Xray — он идёт в Этап 2 выше."')
t('"This does not look like a Cerebro keyword-table export (no Keyword Phrase / Search Volume columns)."',
  '"Не похоже на экспорт таблицы ключей Cerebro (нет колонок Keyword Phrase / Search Volume)."')
t('"No keyword rows found in the export."', '"В экспорте не найдено строк с ключами."')
t('intent="no sales data"', 'intent="нет данных о продажах"')
t('intent="STRONG — buyers, not browsers"', 'intent="СИЛЬНЫЙ — покупатели, не зеваки"')
t('intent="OK"; iStat="green"', 'intent="НОРМАЛЬНЫЙ"; iStat="green"')
t('intent="WEAK — mostly window-shopping"', 'intent="СЛАБЫЙ — в основном разглядывают витрину"')
t('intent="LOOKERS — searches don\'t convert"', 'intent="ЗЕВАКИ — поиски не конвертируются"')
t('<h3 class="cardtitle">Keyword check</h3>', '<h3 class="cardtitle">Проверка ключей</h3>')
t(' keywords · push cost at landed €', ' ключей · цена разгона при себестоимости €')
t(' discount + €', ' скидка + €')
t('/day ads × 8 days', '/день рекламы × 8 дней')
t('${tile("Keyword sales, total", fmt0(totalSales)+"/mo", "overlaps between keywords — upper bound")}',
  '${tile("Продажи по ключам, всего", fmt0(totalSales)+"/мес", "ключи пересекаются — верхняя граница")}')
t('${tile("Best launch keyword", best?best.kw:"—", best?("push ≈ €"+fmt0(best.push)):"no viable candidate")}',
  '${tile("Лучший ключ для запуска", best?best.kw:"—", best?("разгон ≈ €"+fmt0(best.push)):"жизнеспособного кандидата нет")}')
t('${tile("Suggested P10", fmt0(totalSales*0.04*12), "4% share × 12 months → workbook Sheet 6")}',
  '${tile("Рекомендуемый P10", fmt0(totalSales*0.04*12), "доля 4% × 12 мес → книга, Лист 6")}')
t('${tile("Suggested P90", fmt0(totalSales*0.15*12), "15% share × 12 months → workbook Sheet 6")}',
  '${tile("Рекомендуемый P90", fmt0(totalSales*0.15*12), "доля 15% × 12 мес → книга, Лист 6")}')
t(">FAD? +'+fmt0(k.trend)+'% trend</span>", ">ХАЙП? +'+fmt0(k.trend)+'% тренд</span>")
t('SV ${fmt0(k.sv)} · sales ${k.sales==null?"—":fmt0(k.sales)}/mo · ', 'SV ${fmt0(k.sv)} · продажи ${k.sales==null?"—":fmt0(k.sales)}/мес · ')
t('+" searches per sale — "', '+" поисков на продажу — "')
t('" · ⚠ CPR demands "+k.velRatio.toFixed(1)+"× the keyword\'s organic 8-day velocity — expensive to hold"',
  '" · ⚠ CPR требует "+k.velRatio.toFixed(1)+"× органической 8-дневной скорости ключа — дорого удерживать"')
t('" — few optimized titles, an opening"', '" — мало оптимизированных заголовков, есть лазейка"')
t('" — title-saturated"', '" — заголовки перенасыщены"')
t('"CPR "+fmt0(k.cpr)+" · push €"+fmt0(k.push)', '"CPR "+fmt0(k.cpr)+" · разгон €"+fmt0(k.push)')
t('["good","LAUNCHABLE","“"+best.kw+"” is the beachhead: real buyer intent, push ≈ €"+fmt0(best.push)+" inside your budget. Rank there first; attack the bigger keywords from that base. A fad-flagged keyword must pass Gate 1 before you believe its volume."]',
  '["good","МОЖНО ЗАПУСКАТЬСЯ","«"+best.kw+"» — плацдарм: реальное покупательское намерение, разгон ≈ €"+fmt0(best.push)+" внутри бюджета. Сначала ранжируйтесь там; большие ключи атакуйте с этой базы. Ключу с флагом хайпа сначала пройти Этап 1 — только потом верьте его объёму."]')
t('["warning","AFFORDABLE, BUT WEAK INTENT","Cheapest viable door is “"+best.kw+"” (push ≈ €"+fmt0(best.push)+", inside budget) — but its searches mostly window-shop ("+fmt0(best.sps)+" per sale). Expect a lower CVR and a longer grind than the push number implies. Look for a stronger-intent child keyword before committing."]',
  '["warning","ПО ДЕНЬГАМ ПРОХОДИТ, НО НАМЕРЕНИЕ СЛАБОЕ","Самая дешёвая дверь — «"+best.kw+"» (разгон ≈ €"+fmt0(best.push)+", внутри бюджета), но её поиски в основном разглядывают витрину ("+fmt0(best.sps)+" на продажу). Ждите более низкий CVR и более долгий разгон, чем обещает цифра. Прежде чем коммититься, поищите дочерний ключ с более сильным намерением."]')
t('["warning","EXPENSIVE DOORS ONLY","Viable keywords exist but every push exceeds your €"+fmt0(maxPush)+" cap — raise the cap knowingly, or find a cheaper child keyword (longer phrase, Cerebro filter: CPR below 40)."]',
  '["warning","ТОЛЬКО ДОРОГИЕ ДВЕРИ","Жизнеспособные ключи есть, но каждый разгон дороже вашего лимита €"+fmt0(maxPush)+" — поднимайте лимит осознанно или ищите более дешёвый дочерний ключ (длиннее фраза, фильтр Cerebro: CPR ниже 40)."]')
t('["critical","NO REAL DEMAND DOORS","Every keyword is a fad spike or a looker keyword — high searches that don\'t convert to purchases. This niche\'s demand is weaker than its search volume pretends. Re-check with Gate 1 before spending anything."]',
  '["critical","ДВЕРЕЙ С РЕАЛЬНЫМ СПРОСОМ НЕТ","Каждый ключ — либо хайп-всплеск, либо ключ зевак: много поисков, мало покупок. Спрос в нише слабее, чем притворяется её поисковый объём. Перепроверьте Этапом 1, прежде чем тратить что-либо."]')
t('Searches-per-sale = search volume ÷ attributed purchases: ≤20 strong · 20–60 normal · 60–120 weak · >120 lookers. Trend ≥+200% = fad flag → verify the shape in Gate 1. Feed the P10/P90 suggestion into the workbook\'s Sheet 6 after an Xray sanity check.',
  'Поисков на продажу = поисковый объём ÷ атрибутированные покупки: ≤20 сильный · 20–60 нормальный · 60–120 слабый · >120 зеваки. Тренд ≥+200% = флаг хайпа → проверьте форму Этапом 1. Рекомендованные P10/P90 переносите в Лист 6 книги после сверки с Xray.')

# ---------- apply ----------
missing = []
for old, new, n in P:
    c = s.count(old)
    if c == 0:
        missing.append(old[:90])
        continue
    if n is not None and c != n:
        print(f"WARN count {c} != {n}: {old[:70]}")
    s = s.replace(old, new)
if missing:
    print(f"MISSING {len(missing)} strings:")
    for m in missing: print("  -", m)
    sys.exit(1)

os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, "w", encoding="utf-8").write(s)
# leftover-English sanity scan (rough): count suspicious phrases
import re
left = [w for w in ["Drop the", "Gate passed", "workbook (Sheets", "searches per sale", "per month\"", "listings (gate"] if w in s]
print("done ->", DST, "| leftover suspects:", left if left else "none")

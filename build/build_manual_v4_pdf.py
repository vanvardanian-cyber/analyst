#!/usr/bin/env python3
"""Workbook v4 user manual (EN) -> styled PDF. RU variant via LANG env."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether)

RU = len(sys.argv) > 1 and sys.argv[1] == "ru"
if RU:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    FD = "/usr/share/fonts/truetype/dejavu/"
    pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DV-B", FD + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DV-I", FD + "DejaVuSans-Oblique.ttf"))
    pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")
    FN, FB, FI = "DV", "DV-B", "DV-I"
    OUTPDF = "/home/claude/manual-workbook-v4-RU.pdf"
else:
    FN, FB, FI = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    OUTPDF = "/home/claude/manual-workbook-v4-EN.pdf"

ACCENT = colors.HexColor("#1F4E79")
GREY   = colors.HexColor("#666666")
LIGHT  = colors.HexColor("#EDF2F8")
BORDER = colors.HexColor("#C9D6E4")

st_title = ParagraphStyle("t", fontName=FB, fontSize=17, leading=21, textColor=ACCENT)
st_sub   = ParagraphStyle("s", fontName=FN, fontSize=9.5, leading=13, textColor=GREY)
st_h     = ParagraphStyle("h", fontName=FB, fontSize=12, leading=15, textColor=ACCENT, spaceBefore=12, spaceAfter=4)
st_b     = ParagraphStyle("b", fontName=FN, fontSize=9.5, leading=13.5, alignment=TA_LEFT, spaceAfter=5)
st_bul   = ParagraphStyle("u", parent=st_b, leftIndent=10, bulletIndent=2, spaceAfter=3)
st_cell  = ParagraphStyle("c", fontName=FN, fontSize=8.5, leading=11.5)
st_cellb = ParagraphStyle("cb", parent=st_cell, fontName=FB)
st_note  = ParagraphStyle("n", parent=st_b, textColor=GREY, fontSize=8.5, leading=11.5)

doc = SimpleDocTemplate(OUTPDF, pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm,
                        title="Amazon.de Seller Workbook v4 - User Manual", author="easestore.de")
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

# ============================ CONTENT (EN) ============================
if not RU:
    S.append(Paragraph("Amazon.de Seller Workbook v4 — User Manual", st_title))
    S.append(Spacer(1, 3))
    S.append(Paragraph("v4 · 2026-08-25 · internal, future in-app help content for easestore.de · companion to the Sheet 1 (Seasonality) manual", st_sub))
    S.append(Spacer(1, 6)); S.append(HRFlowable(width="100%", thickness=1, color=ACCENT)); S.append(Spacer(1, 6))
    p("<b>What the file is:</b> one workbook that walks a product from idea to funded order to monthly operations. "
      "Sheets are numbered in the order you should use them; every sheet links back to Start, and Start shows a live "
      "one-line status per sheet. Blue text on yellow = you type. Black = formula, never overwrite. Green = pulled from another sheet.")

    h("1. The funnel — which sheet, when")
    tbl(["Phase", "Sheets", "Question each answers"],
        [["Choose the product", "1 → 2 → 3 → 4 (5 to compare niches)",
          "Is demand real and rising? Is the season still reachable? Does a unit earn enough? Does it pass every compliance and competition gate?"],
         ["Fund the launch", "6 → 7 → 8",
          "How many units? What can ads cost, and what does the launch push cost? Does the 12-month cash line stay above zero?"],
         ["Operate", "9 · 10 · 11 monthly, 7 every two weeks",
          "Real monthly profit; money Amazon owes you; the complaint to attack next."],
         ["Plan the business", "12",
          "Do 2–3 staggered launches over 3 years stay funded — or do they collide in a cash crisis?"]],
        [30*mm, 52*mm, 92*mm])
    p("A hard NO in Sheet 4's block A ends the candidate regardless of every other number. That is the point of the order: "
      "the cheap checks (1, 4A) run before the expensive ones.")

    h("2. What is new in v4")
    tbl(["Where", "New block", "What it tells you"],
        [["Sheet 12 (new)", "Multi-year plan, 12 quarters, up to 3 products",
          "Whether the LAUNCH SCHEDULE is funded — not one product, the business."],
         ["Sheet 4, rows 38–44", "Review wall in months",
          "How many months of grinding until you match page-1 median review counts."],
         ["Sheet 4, row 46", "Textile / plant-material reminder",
          "Fibre labelling (EU 1007/2011) and phytosanitary risk for plant fillings — check BEFORE sampling."],
         ["Sheet 6, rows 35–41", "P10 / P90 helper",
          "Turns Cerebro keyword sales + a realistic position share into the two demand inputs the order-size model needs."],
         ["Sheet 7, I5:J10", "CPR launch-push cost",
          "Order-of-magnitude cost of pushing to page 1 on one keyword: units burned + 8 days of ads."],
         ["Sheet 8, rows 37–38", "Cash cycle & cash turns",
          "How long each euro is locked up, and how many times a year it can work."]],
        [32*mm, 52*mm, 90*mm])

    h("3. Sheet 12 — the multi-year plan")
    p("<b>Why it exists.</b> Sheet 8 proves one product survives its first year. But real accounts die at product TWO: "
      "each launch locks ~6 months of cash exactly when the previous product is still ramping. Sheet 12 makes that collision visible before you commit.")
    bul("<b>Global inputs:</b> starting cash (pulled from Sheet 8), fixed costs per quarter (subscriptions, EPR fees, accountant), "
        "and the ramp share — a product sells 40% of its mature rate in its launch quarter, 70% in the second, 100% from the third.")
    bul("<b>Per product (up to 3 columns; leave a column empty to plan fewer):</b> launch quarter (1–12), mature units per QUARTER "
        "(not month), payout per unit after tax (product 1 pulls Sheet 3; for others run Sheet 3 per product and type the result), "
        "landed cost, one-off launch cash, ongoing ads per unit.")
    bul("<b>One-off launch cash</b> is everything spent before the first sale: the first order, GPSR responsible person, LUCID/PPWR, "
        "photos, Vine, launch-phase ads including the CPR push (Sheet 7). It leaves the quarter BEFORE the launch quarter — goods take about a quarter to arrive.")
    bul("<b>Stock is bought one quarter ahead:</b> each quarter pays for the NEXT quarter's units. The first order is not double-counted — it sits inside the one-off.")
    p("<b>Read one number: the lowest cash point (C32).</b> Negative = the schedule as typed is NOT funded — push a launch one or two "
      "quarters later, shrink an order, or add capital. Positive = its size is your real buffer. "
      "<b>The file ships with a deliberate warning:</b> the example launches product 2 in quarter 3 on a €6,500 start and dips to "
      "about −€3,400 in quarter 2 — showing exactly the crisis the sheet exists to catch. Move product 2's launch to quarter 5 and watch the line clear zero.")
    p("The structure follows the integrated model taught in Helium 10's Freedom Ticket financial module (units → cash → minimum cash, "
      "staggered launches); every economic number in it is this file's German reality: deemed-supplier payouts ex-VAT, duty on CIF, 1% Georgian turnover tax.")

    h("4. The five v4 upgrades, in use")
    p("<b>Review wall (Sheet 4, rows 38–44).</b> Enter the MEDIAN review count of page-1's top-10 (median, not average — one "
      "5,000-review giant distorts an average), your expected units/month, and a review rate (1–2% of units is normal organically). "
      "The sheet converts the wall into months. Bands: ≤6 months OK · 6–12 CAUTION (budget PPC above target ACOS for that long) · "
      ">12 FLAG — you need Vine plus a real differentiation angle from Sheet 11, or a lower-wall niche. "
      "Default example: 75 median ÷ (300 × 1.5%) = 16.7 months → FLAG.")
    p("<b>P10/P90 helper (Sheet 6, rows 35–41).</b> The newsvendor model is only as good as its two demand inputs. Feed it Cerebro's "
      "keyword sales per month (parent + main children, don't double-count), the months you're stocking, and a captured share. "
      "The defaults 4–15% come from position economics: positions 1–3 take ~40–60% of clicks, 4–8 take ~15–25%, page-1 bottom under 5% — "
      "a new launch realistically lands mid-page. The helper only SUGGESTS: sanity-check against Xray page-1 unit sales, then copy into C6/C7 by hand.")
    p("<b>CPR launch push (Sheet 7, I5:J10).</b> Cerebro's CPR estimates the units in 8 days needed to reach page 1 for a keyword. "
      "Cost of the push = CPR × (landed cost + launch discount) + 8 days of launch ads. It is a heuristic — read the total as an order "
      "of magnitude. If it exceeds roughly 6 weeks of expected page-1 contribution, attack a cheaper child keyword first. Add the result into Sheet 12's one-off.")
    p("<b>Cash cycle & turns (Sheet 8, rows 37–38).</b> Cycle = full supply lead time (Sheet 2) + ~45 days sell-through + ~14 days payout lag. "
      "At ~190 days that is ~1.9 turns/year: each euro completes the loop about twice — so a 40% per-cycle margin compounds to roughly "
      "76% a year on working capital, and cutting 3 weeks off the supply chain can beat a price increase.")
    p("<b>Textiles & plant fillings (Sheet 4, row 46).</b> Any textile needs fibre-composition labelling per EU Regulation 1007/2011 — "
      "defined fibre names only, marketing names on the label are illegal. Plant fillings (buckwheat, spelt — e.g. japanisches kissen) add "
      "phytosanitary import risk: confirm the filling's import status before paying for samples.")

    h("5. Common mistakes with the new blocks")
    for m in ["Entering monthly units into Sheet 12's 'units per QUARTER' row — everything triples.",
              "Typing P10/P90 straight from the helper without the Xray sanity check — Cerebro keyword sales overlap across keywords.",
              "Treating the CPR total as a precise budget instead of an order of magnitude.",
              "Averaging page-1 review counts instead of taking the median for the review wall.",
              "Leaving the shipped Sheet 12 example untouched and reading its ⚠ as your own verdict — replace the yellow inputs with your plan.",
              "Forgetting that Sheet 12 smooths seasonality: a Q4-heavy product needs Sheet 8's monthly view on top."]:
        bul(m)

    S.append(Spacer(1, 8)); S.append(HRFlowable(width="100%", thickness=0.5, color=BORDER)); S.append(Spacer(1, 3))
    S.append(Paragraph("Educational material, not tax, legal or financial advice. Methods: newsvendor model (operations research standard); "
                       "classical seasonal decomposition (Hyndman &amp; Athanasopoulos, otexts.com/fpp3); integrated multi-period cash model structure "
                       "after Helium 10 Freedom Ticket module 4, re-parameterised for Amazon.de deemed-supplier economics. Amazon fees change every "
                       "Dec/Jan — re-check category rates before big decisions.", st_note))

# ============================ CONTENT (RU) ============================
else:
    S.append(Paragraph("Amazon.de Seller Workbook v4 — руководство пользователя", st_title))
    S.append(Spacer(1, 3))
    S.append(Paragraph("v4 · 25.08.2026 · внутренний документ, будущий help-контент easestore.de · дополнение к руководству по Листу 1 (сезонность)", st_sub))
    S.append(Spacer(1, 6)); S.append(HRFlowable(width="100%", thickness=1, color=ACCENT)); S.append(Spacer(1, 6))
    p("<b>Что это за файл:</b> одна книга проводит товар от идеи до профинансированного заказа и ежемесячной работы. "
      "Листы пронумерованы в порядке использования; каждый лист ссылается на Start, а Start показывает живой статус по каждому листу. "
      "Синий текст на жёлтом = вводите вы. Чёрный = формула, не перезаписывать. Зелёный = подтягивается с другого листа.")

    h("1. Воронка — какой лист и когда")
    tbl(["Этап", "Листы", "Вопрос"],
        [["Выбор товара", "1 → 2 → 3 → 4 (5 — сравнить ниши)",
          "Спрос реален и растёт? Сезон ещё достижим? Юнит зарабатывает достаточно? Проходит все ворота комплаенса и конкуренции?"],
         ["Финансирование запуска", "6 → 7 → 8",
          "Сколько юнитов? Сколько может стоить реклама и во что обойдётся разгон? Держится ли 12-месячная кэш-линия выше нуля?"],
         ["Операционка", "9 · 10 · 11 ежемесячно, 7 — раз в две недели",
          "Реальная месячная прибыль; деньги, которые должен Amazon; жалоба, которую атаковать."],
         ["План бизнеса", "12",
          "Выдержат ли 2–3 запуска за 3 года — или столкнутся в кассовом кризисе?"]],
        [30*mm, 52*mm, 92*mm])
    p("Жёсткое NO в блоке A Листа 4 закрывает кандидата независимо от остальных цифр. В этом смысл порядка: дешёвые проверки (1, 4A) идут раньше дорогих.")

    h("2. Что нового в v4")
    tbl(["Где", "Новый блок", "Что даёт"],
        [["Лист 12 (новый)", "Многолетний план: 12 кварталов, до 3 товаров",
          "Профинансирован ли ГРАФИК ЗАПУСКОВ — не один товар, а бизнес."],
         ["Лист 4, строки 38–44", "«Стена отзывов» в месяцах",
          "Сколько месяцев догонять медианное число отзывов первой страницы."],
         ["Лист 4, строка 46", "Текстиль / растительные наполнители",
          "Маркировка состава (EU 1007/2011) и фитосанитарный риск наполнителей — проверить ДО образцов."],
         ["Лист 6, строки 35–41", "Помощник P10 / P90",
          "Превращает keyword sales из Cerebro + реалистичную долю позиции в два входа модели размера заказа."],
         ["Лист 7, I5:J10", "Стоимость CPR-разгона",
          "Порядок величины: сожжённые юниты + 8 дней рекламы для выхода на страницу 1 по ключу."],
         ["Лист 8, строки 37–38", "Кэш-цикл и обороты денег",
          "Сколько дней заперт каждый евро и сколько раз в год он может работать."]],
        [32*mm, 52*mm, 90*mm])

    h("3. Лист 12 — многолетний план")
    p("<b>Зачем он.</b> Лист 8 доказывает, что один товар переживёт первый год. Но реальные аккаунты умирают на товаре НОМЕР ДВА: "
      "каждый запуск запирает ~6 месяцев кэша ровно тогда, когда предыдущий товар ещё разгоняется. Лист 12 делает это столкновение видимым до того, как вы отправили деньги.")
    bul("<b>Общие входы:</b> стартовый кэш (тянется с Листа 8), фиксированные расходы за квартал (подписки, EPR, бухгалтер) и доля разгона — "
        "товар продаёт 40% зрелого темпа в квартал запуска, 70% во втором, 100% с третьего.")
    bul("<b>По товару (до 3 колонок; пустая колонка = товара нет):</b> квартал запуска (1–12), зрелые продажи в КВАРТАЛ (не месяц!), "
        "выплата за юнит после налога (товар 1 тянется с Листа 3; для остальных прогоните Лист 3 и впишите число), "
        "себестоимость с доставкой, разовый кэш запуска, реклама на юнит.")
    bul("<b>Разовый кэш запуска</b> — всё, что уходит до первой продажи: первая партия, GPSR responsible person, LUCID/PPWR, фото, Vine, "
        "рекламный разгон вместе с CPR-пушем (Лист 7). Он уходит кварталом РАНЬШЕ запуска — товар едет примерно квартал.")
    bul("<b>Товар закупается на квартал вперёд:</b> каждый квартал оплачивает юниты СЛЕДУЮЩЕГО. Первая партия не считается дважды — она внутри разового кэша.")
    p("<b>Читайте одно число — минимум кэша (C32).</b> Отрицательный = график в текущем виде НЕ профинансирован: сдвиньте запуск на "
      "1–2 квартала, уменьшите партию или добавьте капитал. Положительный = его размер и есть ваш реальный буфер. "
      "<b>Файл поставляется с намеренным предупреждением:</b> пример запускает товар 2 в 3-м квартале при старте €6 500 и проваливается "
      "до ≈ −€3 400 во 2-м квартале — ровно тот кризис, ради которого лист существует. Передвиньте запуск товара 2 на 5-й квартал — линия выйдет из минуса.")
    p("Структура повторяет интегрированную модель финансового модуля Freedom Ticket (юниты → кэш → минимум кэша, ступенчатые запуски); "
      "вся экономика внутри — немецкая реальность этого файла: выплаты deemed supplier без VAT, пошлина на базу CIF, грузинский налог 1% с оборота.")

    h("4. Пять обновлений v4 в работе")
    p("<b>Стена отзывов (Лист 4, 38–44).</b> Введите МЕДИАНУ отзывов топ-10 первой страницы (медиану, не среднее — один гигант с 5 000 "
      "отзывов ломает среднее), ожидаемые юниты/месяц и долю отзывов (органика даёт 1–2% от продаж). Лист переводит стену в месяцы. "
      "Пороги: ≤6 мес OK · 6–12 CAUTION (закладывайте PPC выше целевого ACOS на весь срок) · >12 FLAG — нужен Vine плюс реальный угол "
      "дифференциации из Листа 11, либо ниша с более низкой стеной. Пример по умолчанию: 75 ÷ (300 × 1,5%) = 16,7 мес → FLAG.")
    p("<b>Помощник P10/P90 (Лист 6, 35–41).</b> Модель newsvendor хороша ровно настолько, насколько её два входа спроса. Дайте ей "
      "keyword sales из Cerebro (родитель + главные дети, без двойного счёта), число месяцев закупки и захватываемую долю. Дефолт 4–15% — "
      "из экономики позиций: позиции 1–3 берут ~40–60% кликов, 4–8 ~15–25%, низ страницы — меньше 5%; новый запуск реалистично встаёт в середину. "
      "Помощник только ПРЕДЛАГАЕТ: сверьте с юнит-продажами страницы 1 в Xray и перенесите в C6/C7 руками.")
    p("<b>CPR-разгон (Лист 7, I5:J10).</b> CPR в Cerebro — оценка юнитов за 8 дней для выхода на страницу 1. Стоимость = CPR × "
      "(себестоимость + скидка запуска) + 8 дней рекламы. Это эвристика — читайте итог как порядок величины. Если он больше ~6 недель "
      "ожидаемой контрибуции страницы 1 — сначала атакуйте более дешёвый дочерний ключ. Итог добавьте в разовый кэш Листа 12.")
    p("<b>Кэш-цикл и обороты (Лист 8, 37–38).</b> Цикл = полный lead time (Лист 2) + ~45 дней распродажи партии + ~14 дней лага выплат. "
      "При ~190 днях это ~1,9 оборота в год: каждый евро делает круг примерно дважды — маржа 40% за цикл превращается в ~76% годовых "
      "на рабочий капитал, а минус 3 недели в цепочке поставки может дать больше, чем повышение цены.")
    p("<b>Текстиль и наполнители (Лист 4, строка 46).</b> Любой текстиль требует маркировки состава по Регламенту EU 1007/2011 — только "
      "определённые названия волокон, маркетинговые названия на этикетке незаконны. Растительные наполнители (гречиха, полба — например, "
      "japanisches kissen) добавляют фитосанитарный риск импорта: проверьте статус наполнителя до оплаты образцов.")

    h("5. Типовые ошибки с новыми блоками")
    for m in ["Вписать месячные юниты в строку «за КВАРТАЛ» Листа 12 — всё утраивается.",
              "Скопировать P10/P90 из помощника без сверки с Xray — keyword sales в Cerebro пересекаются между ключами.",
              "Читать итог CPR как точный бюджет, а не порядок величины.",
              "Брать среднее число отзывов вместо медианы для стены отзывов.",
              "Оставить пример Листа 12 нетронутым и принять его ⚠ за свой вердикт — замените жёлтые входы своим планом.",
              "Забыть, что Лист 12 сглаживает сезонность: товару с горбом в Q4 нужен ещё и месячный вид Листа 8."]:
        bul(m)

    S.append(Spacer(1, 8)); S.append(HRFlowable(width="100%", thickness=0.5, color=BORDER)); S.append(Spacer(1, 3))
    S.append(Paragraph("Учебный материал, не налоговая, юридическая или финансовая консультация. Методы: модель newsvendor (стандарт исследования операций); "
                       "классическая сезонная декомпозиция (Hyndman &amp; Athanasopoulos, otexts.com/fpp3); структура интегрированной многопериодной кэш-модели — "
                       "по модулю 4 Freedom Ticket (Helium 10), перепараметрирована под экономику deemed supplier на Amazon.de. Комиссии Amazon меняются каждые "
                       "декабрь–январь — перепроверяйте ставки категории перед большими решениями.", st_note))

doc.build(S)
print("done", OUTPDF)

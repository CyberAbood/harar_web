"""Assemble a single self-contained index.html with inlined fonts and a hash-based CSP."""
import base64
import hashlib
import html
import json
import pathlib
import urllib.parse

A = json.load(open("assets.json"))
FONTS = pathlib.Path("node_modules/@fontsource")


def face(family, pkg, subset, weight):
    data = (FONTS / pkg / "files" / f"{pkg}-{subset}-{weight}-normal.woff2").read_bytes()
    b64 = base64.b64encode(data).decode()
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};font-display:swap;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    )


FONT_CSS = "".join(
    [
        face("Markazi Text", "markazi-text", "arabic", 500),
        face("Markazi Text", "markazi-text", "arabic", 700),
        face("Plex Arabic", "ibm-plex-sans-arabic", "arabic", 400),
        face("Plex Arabic", "ibm-plex-sans-arabic", "arabic", 600),
        face("Plex Digits", "ibm-plex-sans-arabic", "latin", 500),
        face("Zilla", "zilla-slab", "latin", 500),
        face("Zilla", "zilla-slab", "latin", 700),
    ]
)

PHONE = "+966549980702"
PHONE_SHOWN = "054 998 0702"
INSTAGRAM = "https://instagram.com/hararcaffe"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote("هرر كافيه ظهرة لبن الرياض")

HOT = [
    ("اسبريسو", "Espresso", 5, 10),
    ("أمريكانو", "Americano", 5, 10),
    ("كورتادو", "Cortado", 55, 13),
    ("فلات وايت", "Flat White", 75, 14),
    ("كابتشينو", "Cappuccino", 90, 14),
    ("لاتيه", "Latte", 150, 15),
    ("سبانيش لاتيه", "Spanish Latte", 210, 16),
    ("شوكولاتة ساخنة", "Hot Chocolate", 263, 17),
]
COLD = [
    ("آيس أمريكانو", "Ice Americano", 5, 12),
    ("آيس ماتشا", "Ice Matcha", 180, 17),
    ("آيس لاتيه", "Ice Latte", 150, 15),
    ("آيس سبانيش لاتيه", "Ice Spanish Latte", 210, 16),
    ("آيس موهيتو", "Ice Mojito", 145, 16),
    ("آيس كركديه", "Ice Roselle", 100, 14),
]
DRIP = [
    ("قهوة اليوم", "Coffee of the Day", 5, (("صغير", 8), ("كبير", 10))),
    ("قهوة مقطرة", "V60", 5, (("حار", 16), ("بارد", 18))),
]


def price(value):
    return f'<span class="num">{value}</span> <span class="sar">ر.س</span>'


def row(ar, en, kcal, p):
    if isinstance(p, tuple):
        cell = "".join(f'<span class="opt"><small>{label}</small> {price(v)}</span>' for label, v in p)
    else:
        cell = price(p)
    return (
        f'<tr><th scope="row"><span class="ar">{ar}</span><span class="en" lang="en" dir="ltr">{en}</span></th>'
        f'<td class="kcal"><span class="num">{kcal}</span></td><td class="price">{cell}</td></tr>'
    )


def group(title, en, items):
    rows = "".join(row(*i) for i in items)
    return (
        f'<table class="group"><caption><span>{title}</span><span class="en" lang="en" dir="ltr">{en}</span></caption>'
        '<thead><tr><th scope="col" class="vh">المشروب</th><th scope="col" class="kcal">سعرة</th>'
        f'<th scope="col" class="price">السعر</th></tr></thead><tbody>{rows}</tbody></table>'
    )


# Quoted exactly as written on Google Maps. "…" marks where the pasted text was cut or a quote stops early.
REVIEWS = [
    ("lead", "ar", "The best staff you would ever meet in any cafe in Riyadh very polite and friendly and you feel home when you get there. I spend days in this spot and travel distance to just be there .. small but very calm and friendly space", "Beem Saad"),
    ("", "ar", "شكر خاص ل شيف عمر وعلى الحلويات الرهيبة اللي يعملها كل صنف يفوز عالتاني، يومياً عندهم ولااوصيكم دوقوا كيكة السينابون 👌🏼♥️ مايحتاج اقول اول زيارة ولا اخر زيارة لانو تقريباً يوميا انا عندهم ♥️…", "Haneen Bukhari"),
    ("", "ar", "السلام عليكم ثاني مره اروح ظهرة لبن و لازم امر الكوفي القهوة اليوم جداً جميل و الكوكيز خرافي…", "Rayan"),
    ("", "ar", "المكان مره حلو والخدمات مشاءالله تبارك الرحمن التعامل والموضفين وكمان البارستا اكرم ولد مشاءالله عليه بتوفيق", "شمسان الجعفري"),
    ("", "ar", "المكان جمييل وهادئ وشغلهم ومنتجاتهم ممتازة…", "Essa Haidar"),
    ("wide", "ar", "اشكر صاحب الكوفي على حسن الضيافة", "محمد الغامدي"),
]


def review(kind, _lang, text, name):
    is_en = text[:3].isascii()
    attrs = ' lang="en" dir="ltr"' if is_en else ""
    return (
        f'<figure class="rev {kind}"><blockquote{attrs}>{html.escape(text)}</blockquote>'
        f'<figcaption dir="auto">{html.escape(name)}</figcaption></figure>'
    )


LOGO = f'<svg viewBox="{A["box"]}" role="img" aria-label="هرر" class="logo"><path d="{A["logo"]}"/></svg>'
ART_OUT = "".join(f'<path pathLength="1" d="{d}"/>' for d in A["outlines"])
ART = (
    f'<svg class="art" viewBox="0 80 1240 410" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
    f'<g class="o">{ART_OUT}</g><path class="h" d="{A["hatches"]}"/></svg>'
)

CSS = FONT_CSS + """
:root{--paper:#e4dcc8;--sheet:#efe9da;--panel:#e3dac5;--ink:#26263f;--ink-2:#55546c;--line:#8483a3;--line-soft:#b5b1bb;--leaf:#2c6a4c;--num:'Zilla','Plex Arabic',serif;--body:'Plex Arabic','Zilla',system-ui,sans-serif;--display:'Markazi Text','Zilla',serif;--art-h:clamp(8.5rem,23vh,14rem)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.0625rem/1.75 var(--body)}
a{color:inherit}
:focus-visible{outline:3px solid var(--leaf);outline-offset:3px;border-radius:2px}
.wrap{width:min(1180px,100% - 2.5rem);margin-inline:auto}
.skip{position:absolute;inset-inline-start:1rem;top:-4rem;background:var(--ink);color:var(--sheet);padding:.5rem 1rem;z-index:5}
.skip:focus{top:1rem}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}

/* hero */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;overflow:hidden}
.nav{display:flex;gap:1.75rem;justify-content:flex-end;padding-block:1.25rem;position:relative;z-index:2}
.nav a{text-decoration:none;font-weight:600;font-size:1rem;padding-block:.35rem;border-bottom:2px solid transparent}
.nav a:hover{border-color:currentColor}
.hero-body{position:relative;z-index:2;flex:1;display:grid;align-content:start;padding-block:clamp(.5rem,2vh,1.5rem) calc(var(--art-h) + 1.5rem)}
h1{margin:0}
.logo{display:block;width:min(100%,108vh);height:auto;fill:var(--ink)}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:clamp(1.5rem,5vw,5rem);align-items:end;margin-top:clamp(1.25rem,3.5vh,2.5rem)}
.claim{margin:0}
.claim blockquote{margin:0;font:700 clamp(2rem,4.6vw,3.6rem)/1.12 var(--display);text-wrap:balance}
.claim figcaption{margin-top:.7rem;font-size:.9375rem;color:var(--ink-2)}
.intro p{margin:0 0 1.15rem;max-width:40ch;text-wrap:pretty}
.btns{display:flex;flex-wrap:wrap;gap:.65rem}
.btn{display:inline-block;padding:.62rem 1.25rem;font-weight:600;text-decoration:none;border:2px solid var(--ink);border-radius:999px 999px 999px 4px;transition:background-color .15s,color .15s}
.btn.fill,.btn:hover{background:var(--ink);color:var(--sheet)}
.btn.fill:hover{background:transparent;color:var(--ink)}
.art{position:absolute;inset-inline:0;bottom:0;width:100%;height:var(--art-h);fill:none;stroke:var(--line);stroke-linecap:round;pointer-events:none}
.art .o path{stroke-width:1.6;vector-effect:non-scaling-stroke}
.art .h{stroke-width:1;vector-effect:non-scaling-stroke}
@media (prefers-reduced-motion:no-preference){
.hero .art .o path{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.5s .15s cubic-bezier(.3,.1,.2,1) forwards}
.hero .art .h{opacity:0;animation:rise 1s 1.1s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes rise{to{opacity:1}}
}

/* menu: the printed tent card, on the ink of its own logo */
.menu{background:var(--ink);padding-block:clamp(3rem,8vw,6rem)}
.sheet{background:var(--sheet);padding:clamp(1.25rem,4vw,3.25rem);border-radius:3px}
.sheet-head{display:flex;flex-wrap:wrap;gap:.25rem 2rem;justify-content:space-between;align-items:baseline;margin-bottom:1.5rem}
h2{margin:0;font:700 clamp(2.4rem,5vw,3.5rem)/1.1 var(--display)}
.sheet-head p{margin:0;color:var(--ink-2);font-size:.9375rem}
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(1rem,2.5vw,2rem);align-items:start}
.stack{display:grid;gap:clamp(1rem,2.5vw,2rem)}
.group{width:100%;border-collapse:collapse;background:var(--panel);border-radius:4px;display:block;padding:.95rem clamp(.9rem,2vw,1.4rem) .55rem}
.group thead,.group tbody{display:block}
.group tr{display:grid;grid-template-columns:minmax(0,1fr) 3.1rem 6.7rem;align-items:center;column-gap:.5rem}
.group caption{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;font:700 1.65rem/1.2 var(--display)}
.group caption .en{font:700 1rem/1 var(--num);letter-spacing:.01em}
.group thead tr{border-bottom:2px solid var(--ink);padding-block:.3rem .35rem;font-size:.8125rem;color:var(--ink-2)}
.group thead th{font-weight:400}
.group tbody tr{padding-block:.56rem;border-bottom:1px solid var(--line-soft)}
.group tbody tr:last-child{border-bottom:0}
.group tbody th{font-weight:600;text-align:start;line-height:1.4}
.group .ar,.group .en{display:block}
.group tbody .en{font:500 .9rem/1.35 var(--num);color:var(--ink-2);text-align:right}
.group .kcal{grid-column:2}
.group .price{grid-column:3}
.kcal{text-align:center;font-size:.875rem;color:var(--ink-2)}
.num,.tel{font-variant-numeric:lining-nums tabular-nums}
.num{font-family:var(--num);font-weight:700}
.kcal .num{font-family:'Plex Digits','Plex Arabic',sans-serif;font-weight:500}
.price{text-align:end;white-space:nowrap}
.price>.num,.opt .num{font-size:1.3rem;line-height:1}
.sar{font-size:.75rem;color:var(--ink-2)}
.opt{display:block}
.opt small{font-size:.75rem;color:var(--ink-2)}
.sheet-foot{margin:1.5rem 0 0;max-width:62ch}

/* reviews */
.people{padding-block:clamp(3.5rem,9vw,7rem)}
.people-head{display:grid;gap:.4rem;margin-bottom:clamp(2rem,5vw,3.5rem);max-width:44ch}
.people-head p{margin:0;color:var(--ink-2)}
.revs{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(2.25rem,5vw,4rem) clamp(1.5rem,4vw,3.5rem)}
.rev{margin:0;grid-column:span 4;border-top:2px solid var(--ink);padding-top:.9rem}
.rev blockquote{margin:0;font:500 1.65rem/1.3 var(--display)}
.rev blockquote[lang=en]{font:500 clamp(1.5rem,2.8vw,2.15rem)/1.32 var(--num)}
.rev figcaption{margin-top:.7rem;font-size:.9375rem;font-weight:600}
.rev.lead{grid-column:span 7}
.rev:nth-child(2){grid-column:span 5}
.rev.lead blockquote{text-align:left}
.rev.lead figcaption{text-align:left}
.rev.wide{grid-column:1/-1}
.rev.wide blockquote{font:700 clamp(2rem,4.4vw,3.4rem)/1.15 var(--display)}
.more{margin:clamp(2rem,5vw,3.5rem) 0 0}

/* visit */
.visit{position:relative;background:var(--panel);overflow:hidden;padding-block:clamp(3.5rem,9vw,6.5rem) clamp(9rem,20vw,15rem)}
.visit .art{height:clamp(8rem,18vw,14rem)}
.visit-in{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(2rem,6vw,5rem);align-items:end}
.hello{margin:0 0 .4rem;font-weight:600}
.heart{color:var(--leaf)}
.visit h2{font-size:clamp(2.6rem,6.4vw,5rem);text-wrap:balance}
address{font-style:normal;margin:0 0 1.2rem}
.tel{font-family:var(--num);font-weight:700}
footer{background:var(--ink);color:var(--sheet);padding-block:1.25rem;font-size:.875rem}
footer .wrap{display:flex;flex-wrap:wrap;gap:.5rem 2rem;justify-content:space-between;align-items:center}
footer .logo{width:4.2rem;fill:var(--sheet)}

@media (max-width:760px){
.hero{min-height:auto}
.hero-grid,.cols,.visit-in{grid-template-columns:minmax(0,1fr)}
.logo{width:100%}
.intro p{max-width:none}
.nav{justify-content:flex-start;gap:1.25rem}
.rev,.rev.lead,.rev:nth-child(2){grid-column:1/-1}
.rev.wide blockquote{font-size:2rem}
.group tr{grid-template-columns:minmax(0,1fr) 2.7rem 6.2rem}
}
@media print{.art,.nav,.btns{display:none}.menu{background:none;padding:0}}
"""

MENU_HTML = (
    f'<div class="cols">{group("المشروبات الساخنة", "Hot Drinks", HOT)}'
    f'<div class="stack">{group("المشروبات الباردة", "Cold Drinks", COLD)}{group("المشروبات المقطرة", "Drip Coffee", DRIP)}</div></div>'
)
REV_HTML = "".join(review(*r) for r in REVIEWS)

LD = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "CafeOrCoffeeShop",
        "name": "هرر",
        "alternateName": "Harar Cafe",
        "telephone": PHONE,
        "priceRange": "SAR 8-18",
        "currenciesAccepted": "SAR",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "شارع مندلي",
            "addressLocality": "ظهرة لبن، الرياض",
            "postalCode": "13751",
            "addressCountry": "SA",
        },
        "sameAs": [INSTAGRAM],
    },
    ensure_ascii=False,
)

FAVICON = "data:image/svg+xml," + urllib.parse.quote(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{A["box"]}"><path fill="#26263f" d="{A["logo"]}"/></svg>'
)

BODY = f"""<a class="skip" href="#menu">انتقل إلى المنيو</a>
<header class="hero">
  <div class="wrap">
    <nav class="nav" aria-label="أقسام الصفحة">
      <a href="#menu">المنيو</a><a href="#people">المراجعات</a><a href="#visit">الموقع</a>
    </nav>
  </div>
  <div class="wrap hero-body">
    <h1>{LOGO}</h1>
    <div class="hero-grid">
      <figure class="claim">
        <blockquote>من افضل الكافيهات في الرياض والأفضل في ظهرة لبن</blockquote>
        <figcaption>عامر يحيى، في مراجعته على خرائط جوجل</figcaption>
      </figure>
      <div class="intro">
        <p>مقهى صغير وهادئ في ظهرة لبن. قهوة مقطرة، مشروبات حارة وباردة، وحلويات يسويها شيف عمر.</p>
        <div class="btns"><a class="btn fill" href="#menu">شوف المنيو والأسعار</a><a class="btn" href="{html.escape(MAPS)}" target="_blank" rel="noopener noreferrer">افتح الموقع على الخرائط</a></div>
      </div>
    </div>
  </div>
  {ART}
</header>
<main>
  <section class="menu" id="menu" aria-labelledby="menu-t">
    <div class="wrap"><div class="sheet">
      <div class="sheet-head"><h2 id="menu-t">المنيو</h2><p>الأسعار بالريال السعودي (ر.س)</p></div>
      {MENU_HTML}
      <p class="sheet-foot">وعندنا بعد كوكيز وكيكة سينابون وحلويات ثانية من شيف عمر. اسأل عن المتوفر اليوم في المقهى.</p>
    </div></div>
  </section>
  <section class="people wrap" id="people" aria-labelledby="people-t">
    <div class="people-head"><h2 id="people-t">بكلام زوار هرر</h2><p>مقتطفات من مراجعات خرائط جوجل، بكلمات أصحابها.</p></div>
    <div class="revs">{REV_HTML}</div>
    <p class="more"><a class="btn" href="{html.escape(MAPS)}" target="_blank" rel="noopener noreferrer">اقرأ كل المراجعات على خرائط جوجل</a></p>
  </section>
  <section class="visit" id="visit" aria-labelledby="visit-t">
    <div class="wrap visit-in">
      <div><p class="hello">يا اهلاً <span class="heart">💚</span></p><h2 id="visit-t">ننتظرك على قهوة ثانية في هرر</h2></div>
      <div>
        <address>شارع مندلي، حي ظهرة لبن، الرياض<br>هاتف: <a class="tel" dir="ltr" href="tel:{PHONE}">{PHONE_SHOWN}</a></address>
        <div class="btns"><a class="btn fill" href="{html.escape(MAPS)}" target="_blank" rel="noopener noreferrer">الاتجاهات على الخرائط</a><a class="btn" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">انستقرام</a></div>
      </div>
    </div>
    {ART}
  </section>
</main>
<footer><div class="wrap">{LOGO}<span>ظهرة لبن، الرياض</span></div></footer>"""

style_hash = base64.b64encode(hashlib.sha256(CSS.encode()).digest()).decode()
CSP = (
    f"default-src 'none'; style-src 'sha256-{style_hash}'; font-src data:; img-src data:; "
    "base-uri 'none'; form-action 'none'"
)
PAGE = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>هرر | مقهى في ظهرة لبن، الرياض</title>
<meta name="description" content="مقهى هرر في ظهرة لبن بالرياض. المنيو والأسعار بالريال السعودي، مراجعات الزوار، والموقع.">
<meta name="theme-color" content="#e4dcc8">
<meta property="og:type" content="website">
<meta property="og:title" content="هرر | مقهى في ظهرة لبن، الرياض">
<meta property="og:description" content="المنيو والأسعار بالريال السعودي، مراجعات الزوار، والموقع.">
<meta property="og:locale" content="ar_SA">
<link rel="icon" href="{html.escape(FAVICON)}">
<style>{CSS}</style>
<script type="application/ld+json">{LD}</script>
</head>
<body>
{BODY}
</body>
</html>
"""
out = pathlib.Path("../index.html")
out.write_text(PAGE, encoding="utf-8")
print("KB", out.stat().st_size // 1024)

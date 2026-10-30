#!/usr/bin/env python3
"""Prüft die Website ohne Abhängigkeiten: python3 tools/pruefen.py

1. Wohlgeformtheit: jedes geöffnete Element wird geschlossen, in der richtigen Reihenfolge (html.parser).
2. Interne Links und Quellen: jedes href/src auf eine eigene Datei existiert, jeder #Anker hat ein Ziel,
   keine nichtssagenden Ankertexte („hier“, „mehr“).
3. SEO-Grundlagen je Seite: lang="de", <title> höchstens 60 Zeichen, Meta-Description 70 bis 155 Zeichen,
   Open Graph und Twitter Card passend zu Titel und Description, genau eine h1, keine übersprungene
   Überschriftenebene, kanonische URL passend zum Pfad, Alt-Text, Breite, Höhe und loading="lazy" an jedem Bild
   (außer dem ersten mit fetchpriority="high"), sichtbares Datum (data-stand) gleich dateModified und gleich
   lastmod in der Sitemap.
4. Strukturierte Daten: JSON-LD gültig, je Typ die Pflichtfelder (schema.org, Google-Richtlinien), alle @id-Verweise
   auflösbar, Brotkrümel bis zur kanonischen URL und sichtbar als Navigation, FAQPage nur mit sichtbaren Fragen und
   Antworten, Artikel-Überschrift gleich h1, keine Bewertungen (aggregateRating, review).
5. Hausregeln: keine Gedankenstriche im sichtbaren Text, „IHK" nie in Titel, Description oder Überschriften,
   Marke klein geschrieben, Pflichthinweis im Fuß jeder Seite, keine externen Skripte, Stile oder Schriften,
   nie die genaue Fragenzahl, auf den neuen Inhaltsseiten keine verbotenen Wörter (offiziell, empfohlen …).
6. Dateien für Crawler: Sitemap vollständig, robots.txt mit Sitemap-Zeile und ohne Sperre für KI-Crawler,
   llms.txt im Format von llmstxt.org mit allen Seiten der Sitemap und dem Pflichthinweis, llms-full.txt aktuell.

Rückgabewert 0, wenn alles grün ist, sonst 1.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://becertain.app"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Wortgleich mit pruefungstrainer-content/pakete/aevo/aevo-1.0.0.json, Feld paket.pflichthinweis.
PFLICHT = ("Für die AEVO-Prüfung bei deiner IHK oder HWK. Jede Aufgabe folgt dem Rahmenplan der AEVO und dem Format "
           "der schriftlichen Prüfung. Jede Lösung nennt die Stelle in Gesetz, Verordnung oder Rahmenplan, aus der sie "
           "folgt. Rechtsstand 26.10.2026. Eigene Übungsfragen, unabhängig von IHK, DIHK und HWK.")
SKIP_DIRS = {".git", "screenshots", "_seo", "tools", "docs"}
TITEL_MAX = 60
DESC_MIN, DESC_MAX = 70, 155

# Inhaltsseiten des AEVO-Hubs (SEO-Ausbau 30.10.2026). Müssen existieren, in der Sitemap stehen und von /aevo/
# verlinkt sein.
NEUE_SEITEN = ["/aevo/pruefung/", "/aevo/fragen/", "/aevo/handlungsfeld-1/", "/aevo/handlungsfeld-2/",
               "/aevo/handlungsfeld-3/", "/aevo/handlungsfeld-4/"]
# Rechtsseiten tragen ihr eigenes „Stand:“ für den Rechtstext statt data-stand.
RECHTSSEITEN = {"/datenschutz/", "/nutzungsbedingungen/", "/impressum/"}
# Wörter, die auf den neuen Inhaltsseiten nie vorkommen dürfen (Textregeln Sergej). Die freigegebenen Bestandstexte
# („Keine Bestehensquoten.“, „Den Preis zeigt dir der App Store“) bleiben, wie sie sind.
VERBOTEN = [r"\boffiziell", r"\bebenbürtig", r"\bgleichwertig", r"prüfungsrelevant", r"\bempfohlen", r"\bzugelassen",
            r"Original-Fragen", r"Bestehensquote", r"\bPreis\b"]
NICHTSSAGEND = {"hier", "mehr", "weiter", "link", "klicken", "hier klicken", "mehr erfahren", "mehr zur app"}
KI_CRAWLER = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot",
              "Google-Extended"]

# Pflichtfelder je @type (Auswahl nach schema.org und den Google-Richtlinien für strukturierte Daten).
PFLICHTFELDER = {
    "WebSite": ["name", "url"],
    "Organization": ["name", "url"],
    "Person": ["name"],
    "WebPage": ["url", "name", "isPartOf", "inLanguage"],
    "BreadcrumbList": ["itemListElement"],
    "Article": ["headline", "author", "publisher", "dateModified", "image", "mainEntityOfPage"],
    "LearningResource": ["learningResourceType", "teaches"],
    "MobileApplication": ["name", "operatingSystem", "applicationCategory", "offers"],
    "SoftwareApplication": ["name", "operatingSystem", "applicationCategory", "offers"],
    "FAQPage": ["mainEntity"],
    "Legislation": ["name", "url"],
    "CreativeWork": ["name"],
}


class Seite(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.fehler = [], []
        self.ids, self.links, self.srcs = set(), [], []
        self.title, self.desc, self.canonical, self.lang = "", None, None, None
        self.h1 = 0
        self.h1_text = ""
        self.headings, self.ld = [], []
        self.ebenen = []
        self.text, self.footer_text = [], []
        self._in = {"title": False, "script_ld": False, "head": False, "footer": 0, "h": 0, "style": False,
                    "script": False, "a": False, "summary": False, "brot": 0}
        self._hbuf, self._ldbuf, self._abuf, self._sbuf = [], [], [], []
        self._htag = None
        self.imgs_ohne_alt = 0
        self.bild_fehler = []
        self.extern = []
        self.meta = {}
        self.stand = []
        self.summaries = []
        self.anker = []
        self.brot_links = []
        self.hat_brot = False
        self.robots = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        if "id" in a:
            if a["id"] in self.ids:
                self.fehler.append(f"doppelte id #{a['id']}")
            self.ids.add(a["id"])
        if "data-stand" in a:
            self.stand.append(a["data-stand"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in["title"] = True
        if tag == "meta":
            if a.get("name") == "description":
                self.desc = a.get("content", "")
            if a.get("name") == "robots":
                self.robots = a.get("content", "")
            schluessel = a.get("property") or a.get("name")
            if schluessel and (schluessel.startswith("og:") or schluessel.startswith("twitter:")):
                self.meta[schluessel] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") in ("stylesheet", "preconnect", "preload") and urlparse(a.get("href", "")).netloc:
            self.extern.append(a.get("href"))
        if tag == "script":
            if a.get("type") == "application/ld+json":
                self._in["script_ld"] = True
                self._ldbuf = []
            else:
                self._in["script"] = True
                if a.get("src") and urlparse(a["src"]).netloc:
                    self.extern.append(a["src"])
        if tag == "style":
            self._in["style"] = True
        if tag == "footer":
            self._in["footer"] += 1
        if tag == "nav" and a.get("aria-label") == "Brotkrümelnavigation":
            self.hat_brot = True
            self._in["brot"] += 1
        elif tag == "nav" and self._in["brot"]:
            self._in["brot"] += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._in["h"] += 1
            self._hbuf = []
            self._htag = tag
            self.ebenen.append(int(tag[1]))
            if tag == "h1":
                self.h1 += 1
        if tag == "summary":
            self._in["summary"] = True
            self._sbuf = []
        if tag == "img":
            if not a.get("alt", "").strip() and a.get("role") != "presentation":
                self.imgs_ohne_alt += 1
            if not (a.get("width") and a.get("height")):
                self.bild_fehler.append(f"Bild ohne width/height: {a.get('src')}")
            if a.get("loading") != "lazy" and a.get("fetchpriority") != "high":
                self.bild_fehler.append(f"Bild ohne loading=\"lazy\": {a.get('src')}")
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            self._in["a"] = True
            self._abuf = []
            self._ahref = a["href"]
            if self._in["brot"]:
                self.brot_links.append(a["href"])
        if tag in ("img", "script", "source") and "src" in a:
            self.srcs.append(a["src"])
        if tag == "link" and "href" in a:
            self.srcs.append(a["href"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.fehler.append(f"</{tag}> ohne Öffnung in Zeile {self.getpos()[0]}")
            return
        offen, pos = self.stack.pop()
        if offen != tag:
            self.fehler.append(f"</{tag}> in Zeile {self.getpos()[0]} schließt <{offen}> aus Zeile {pos[0]}")
        if tag == "title":
            self._in["title"] = False
        if tag == "script":
            if self._in["script_ld"]:
                self.ld.append("".join(self._ldbuf))
            self._in["script_ld"] = self._in["script"] = False
        if tag == "style":
            self._in["style"] = False
        if tag == "footer":
            self._in["footer"] -= 1
        if tag == "nav" and self._in["brot"]:
            self._in["brot"] -= 1
        if tag == "a" and self._in["a"]:
            self._in["a"] = False
            self.anker.append((self._ahref, re.sub(r"\s+", " ", "".join(self._abuf)).strip()))
        if tag == "summary":
            self._in["summary"] = False
            self.summaries.append(re.sub(r"\s+", " ", "".join(self._sbuf)).strip())
        if re.fullmatch(r"h[1-6]", tag):
            self._in["h"] -= 1
            text = "".join(self._hbuf)
            self.headings.append(text)
            if tag == "h1":
                self.h1_text = re.sub(r"\s+", " ", text).strip()

    def handle_data(self, data):
        if self._in["title"]:
            self.title += data
        if self._in["script_ld"]:
            self._ldbuf.append(data)
            return
        if self._in["script"] or self._in["style"]:
            return
        self.text.append(data)
        if self._in["footer"]:
            self.footer_text.append(data)
        if self._in["h"]:
            self._hbuf.append(data)
        if self._in["a"]:
            self._abuf.append(data)
        if self._in["summary"]:
            self._sbuf.append(data)


def seiten():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def pfad_von(datei):
    rel = os.path.relpath(datei, ROOT).replace(os.sep, "/")
    return "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def ziel(url, von_pfad):
    """Lokale Datei und Anker zu einem internen Link, oder None für externe Ziele."""
    u = urlparse(url)
    if u.scheme in ("mailto", "tel") or (u.scheme and u.netloc and u.netloc != "becertain.app"):
        return None
    p = unquote(u.path) if u.path else von_pfad
    if not p.startswith("/"):
        p = os.path.normpath(os.path.join(os.path.dirname(von_pfad), p))
    datei = os.path.join(ROOT, p.lstrip("/"))
    if p.endswith("/"):
        datei = os.path.join(datei, "index.html")
    return datei, u.fragment, p


def norm(t):
    return re.sub(r"\s+", " ", t.replace("\u00a0", " ").replace("\u00ad", "")).strip()


def typen(knoten):
    t = knoten.get("@type", [])
    return t if isinstance(t, list) else [t]


def pruefe_ld(name, pfad, s, bloecke, seitenpfade):
    """Pflichtfelder und Querbezüge der strukturierten Daten einer Seite. Gibt (Fehler, dateModified) zurück."""
    f, knoten = [], []
    for block in bloecke:
        try:
            daten = json.loads(block)
        except ValueError as e:
            f.append(f"{name}: JSON-LD ungültig ({e})")
            continue
        if daten.get("@context") not in ("https://schema.org", "https://schema.org/"):
            f.append(f"{name}: JSON-LD ohne @context https://schema.org")
        knoten += daten.get("@graph", [daten])
    ids = {k["@id"] for k in knoten if "@id" in k}
    datum = None
    sichtbar = norm(" ".join(s.text))

    def verweise(obj):
        if isinstance(obj, dict):
            if set(obj) == {"@id"}:
                yield obj["@id"]
            for v in obj.values():
                yield from verweise(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from verweise(v)

    for k in knoten:
        ts = typen(k)
        for t in ts:
            if t not in PFLICHTFELDER:
                f.append(f"{name}: unbekannter @type {t}")
                continue
            for feld in PFLICHTFELDER[t]:
                if t == "LearningResource":
                    if not any(k.get(x) for x in PFLICHTFELDER[t]):
                        f.append(f"{name}: LearningResource ohne learningResourceType oder teaches")
                    break
                if not k.get(feld):
                    f.append(f"{name}: {t} ohne Pflichtfeld {feld}")
        if "aggregateRating" in k or "review" in k:
            f.append(f"{name}: Bewertungen im JSON-LD ({ts}), es gibt keine echten")
        if "WebPage" in ts:
            if k.get("url") != BASE + pfad:
                f.append(f"{name}: WebPage.url {k.get('url')} statt {BASE + pfad}")
            if k.get("name") != norm(s.title):
                f.append(f"{name}: WebPage.name weicht vom <title> ab")
            if k.get("description") and k["description"] != s.desc:
                f.append(f"{name}: WebPage.description weicht von der Meta-Description ab")
            datum = k.get("dateModified")
            if datum and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", datum):
                f.append(f"{name}: dateModified {datum} ist kein ISO-Datum")
            if "datePublished" in k:
                f.append(f"{name}: datePublished gesetzt; nur dateModified (SEO Blueprint, Diagnose)")
        if "Article" in ts:
            if len(k.get("headline", "")) > 110:
                f.append(f"{name}: Article.headline länger als 110 Zeichen")
            if norm(k.get("headline", "")) != norm(s.h1_text):
                f.append(f"{name}: Article.headline ungleich h1")
            if k.get("dateModified") != datum:
                f.append(f"{name}: Article.dateModified ungleich WebPage.dateModified")
        if "BreadcrumbList" in ts:
            items = k.get("itemListElement", [])
            for i, it in enumerate(items, 1):
                if it.get("position") != i or not it.get("name") or not str(it.get("item", "")).startswith(BASE):
                    f.append(f"{name}: BreadcrumbList Eintrag {i} unvollständig")
            if items and items[-1].get("item") != BASE + pfad:
                f.append(f"{name}: BreadcrumbList endet nicht bei {BASE + pfad}")
            if pfad in NEUE_SEITEN:
                soll = [it["item"].replace(BASE, "") for it in items[:-1]]
                if not s.hat_brot:
                    f.append(f"{name}: keine sichtbare Brotkrümelnavigation")
                elif s.brot_links != soll:
                    f.append(f"{name}: sichtbare Brotkrümel {s.brot_links} statt {soll}")
        if "FAQPage" in ts:
            for frage in k.get("mainEntity", []):
                q = norm(frage.get("name", ""))
                antwort = norm(frage.get("acceptedAnswer", {}).get("text", ""))
                if not q or not antwort:
                    f.append(f"{name}: FAQ-Frage ohne Text oder Antwort")
                    continue
                if q not in [norm(x) for x in s.summaries]:
                    f.append(f"{name}: FAQ-Frage nicht sichtbar: {q!r}")
                if antwort not in sichtbar:
                    f.append(f"{name}: FAQ-Antwort nicht wortgleich sichtbar: {q!r}")
        if any(t in ("MobileApplication", "SoftwareApplication") for t in ts):
            o = k.get("offers", {})
            if str(o.get("price")) != "0" or o.get("priceCurrency") != "EUR":
                f.append(f"{name}: App-Angebot ohne price 0 und priceCurrency EUR (Download gratis)")
            if k.get("applicationCategory") != "EducationalApplication" or k.get("operatingSystem") != "iOS":
                f.append(f"{name}: App ohne EducationalApplication oder iOS")
    for ref in verweise(knoten):
        if ref in ids:
            continue
        u = urlparse(ref)
        if u.netloc == "becertain.app" and (u.path in seitenpfade):
            continue
        f.append(f"{name}: @id-Verweis ohne Ziel: {ref}")
    if not knoten:
        f.append(f"{name}: kein JSON-LD")
    return f, datum


def pruefe_robots():
    f = []
    with open(os.path.join(ROOT, "robots.txt"), encoding="utf-8") as fh:
        text = fh.read()
    if f"Sitemap: {BASE}/sitemap.xml" not in text:
        f.append("robots.txt: Sitemap-Zeile fehlt")
    gruppen, agents, regeln = [], [], []
    for zeile in text.splitlines():
        zeile = zeile.split("#", 1)[0].strip()
        if not zeile:
            continue
        schl, _, wert = zeile.partition(":")
        schl, wert = schl.strip().lower(), wert.strip()
        if schl == "user-agent":
            if regeln:
                gruppen.append((agents, regeln))
                agents, regeln = [], []
            agents.append(wert)
        elif schl in ("allow", "disallow"):
            regeln.append((schl, wert))
    if agents:
        gruppen.append((agents, regeln))
    for agents, regeln in gruppen:
        for schl, wert in regeln:
            if schl == "disallow" and wert in ("/", "/*"):
                f.append(f"robots.txt: {', '.join(agents)} gesperrt")
    genannt = {a for agents, _ in gruppen for a in agents}
    for bot in KI_CRAWLER:
        if bot not in genannt:
            f.append(f"robots.txt: {bot} nicht ausdrücklich erlaubt")
    return f


def pruefe_llms(sitemap_locs):
    f = []
    pfad = os.path.join(ROOT, "llms.txt")
    if not os.path.isfile(pfad):
        return ["llms.txt fehlt"]
    with open(pfad, encoding="utf-8") as fh:
        text = fh.read()
    zeilen = text.splitlines()
    if not zeilen or not zeilen[0].startswith("# "):
        f.append("llms.txt: erste Zeile ist keine H1 (llmstxt.org)")
    if not any(z.startswith("> ") for z in zeilen[1:4]):
        f.append("llms.txt: Kurzbeschreibung als Blockzitat fehlt (llmstxt.org)")
    if PFLICHT not in text:
        f.append("llms.txt: Pflichthinweis fehlt oder weicht ab")
    for loc in sitemap_locs:
        if f"]({loc})" not in text:
            f.append(f"llms.txt: {loc} fehlt")
    if re.search(r"\b853\b", text):
        f.append("llms.txt: genaue Fragenzahl")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import llms_full  # noqa: E402
    if not os.path.isfile(llms_full.ZIEL):
        f.append("llms-full.txt fehlt")
    else:
        with open(llms_full.ZIEL, encoding="utf-8") as fh:
            if fh.read() != llms_full.erzeuge():
                f.append("llms-full.txt passt nicht zum HTML: python3 tools/llms_full.py")
    return f


def main():
    fehler, geprueft, links = [], 0, 0
    geparst = {}
    for datei in sorted(seiten()):
        s = Seite()
        with open(datei, encoding="utf-8") as fh:
            s.feed(fh.read())
        s.close()
        geparst[datei] = s
    seitenpfade = {pfad_von(d) for d in geparst}
    # Sitemap zuerst lesen, für lastmod
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
        sitemap = fh.read()
    eintraege = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sitemap)
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    lastmod = {loc.replace(BASE, "") or "/": lm for loc, lm in eintraege}
    if len(eintraege) != len(locs):
        fehler.append("sitemap.xml: nicht jeder Eintrag hat lastmod")

    for datei, s in geparst.items():
        geprueft += 1
        pfad = pfad_von(datei)
        name = os.path.relpath(datei, ROOT)
        ist_404 = name == "404.html"
        f = [f"{name}: {x}" for x in s.fehler]
        if s.stack:
            f.append(f"{name}: nicht geschlossen: " + ", ".join(f"<{t}> Zeile {p[0]}" for t, p in s.stack))
        if s.lang != "de":
            f.append(f"{name}: lang ist nicht de")
        titel = norm(s.title)
        if not titel:
            f.append(f"{name}: kein <title>")
        elif len(titel) > TITEL_MAX:
            f.append(f"{name}: Titel hat {len(titel)} Zeichen (höchstens {TITEL_MAX})")
        if not s.desc:
            f.append(f"{name}: keine Meta-Description")
        elif not DESC_MIN <= len(s.desc) <= DESC_MAX:
            f.append(f"{name}: Description hat {len(s.desc)} Zeichen ({DESC_MIN} bis {DESC_MAX})")
        if s.meta.get("og:title") != titel or s.meta.get("og:description") != s.desc:
            f.append(f"{name}: og:title oder og:description weicht von Titel oder Description ab")
        for pflicht in ("og:image", "og:image:alt", "twitter:card") + (() if ist_404 else ("og:url",)):
            if not s.meta.get(pflicht):
                f.append(f"{name}: {pflicht} fehlt")
        if s.h1 != 1:
            f.append(f"{name}: {s.h1} h1 statt genau einer")
        if s.ebenen and s.ebenen[0] != 1:
            f.append(f"{name}: erste Überschrift ist h{s.ebenen[0]}, nicht h1")
        for vorher, jetzt in zip(s.ebenen, s.ebenen[1:]):
            if jetzt > vorher + 1:
                f.append(f"{name}: Überschrift springt von h{vorher} auf h{jetzt}")
                break
        if not ist_404 and s.canonical != BASE + pfad:
            f.append(f"{name}: kanonisch {s.canonical} statt {BASE + pfad}")
        if not ist_404 and s.meta.get("og:url") != BASE + pfad:
            f.append(f"{name}: og:url {s.meta.get('og:url')} statt {BASE + pfad}")
        if ist_404 and "noindex" not in (s.robots or ""):
            f.append(f"{name}: 404-Seite ohne noindex")
        ld_fehler, datum = pruefe_ld(name, pfad, s, s.ld, seitenpfade)
        f += ld_fehler
        if not ist_404:
            if pfad in RECHTSSEITEN:
                if not re.search(r"Stand: \d", " ".join(s.text)) and pfad != "/impressum/":
                    f.append(f"{name}: sichtbares „Stand:“ fehlt")
            elif not s.stand:
                f.append(f"{name}: sichtbares Datum (data-stand) fehlt")
            elif s.stand[0] != datum:
                f.append(f"{name}: sichtbares Datum {s.stand[0]} ungleich dateModified {datum}")
            if datum and lastmod.get(pfad) and lastmod[pfad] != datum:
                f.append(f"{name}: lastmod {lastmod[pfad]} in der Sitemap ungleich dateModified {datum}")
        if s.imgs_ohne_alt:
            f.append(f"{name}: {s.imgs_ohne_alt} Bilder ohne Alt-Text")
        f += [f"{name}: {x}" for x in s.bild_fehler]
        if s.extern:
            f.append(f"{name}: externe Ressourcen {s.extern}")
        sichtbar = " ".join(s.text)
        for zeichen in ("–", "—"):
            if zeichen in sichtbar or zeichen in s.title or zeichen in (s.desc or ""):
                f.append(f"{name}: Gedankenstrich {zeichen!r} im Text")
        for h in [s.title, s.desc or ""] + s.headings:
            if re.search(r"\bIHK\b", h):
                f.append(f"{name}: „IHK\" in Titel, Description oder Überschrift: {h.strip()!r}")
        if re.search(r"\bBecertain\b|\bBECERTAIN\b|\bBeCertain\b", sichtbar + s.title):
            f.append(f"{name}: Marke nicht klein geschrieben")
        if re.search(r"\b853\b", sichtbar + (s.desc or "")):
            f.append(f"{name}: genaue Fragenzahl 853 statt „über 800“")
        if pfad in NEUE_SEITEN:
            ohne_fuss = norm(sichtbar.replace(" ".join(s.footer_text), ""))
            for muster in VERBOTEN:
                treffer = re.search(muster, ohne_fuss + " " + s.title + " " + (s.desc or ""), re.I)
                if treffer:
                    f.append(f"{name}: verbotenes Wort {treffer.group(0)!r}")
        fuss = re.sub(r"\s+", " ", " ".join(s.footer_text))
        if PFLICHT not in fuss:
            f.append(f"{name}: Pflichthinweis fehlt im Fuß")
        for href, text in s.anker:
            if norm(text).lower().rstrip(".") in NICHTSSAGEND:
                f.append(f"{name}: nichtssagender Ankertext {text!r} für {href}")
        for url in s.links + s.srcs:
            t = ziel(url, pfad)
            if t is None:
                continue
            links += 1
            d, anker, p = t
            if not os.path.isfile(d):
                f.append(f"{name}: Link ins Leere {url}")
                continue
            if anker:
                ziel_seite = geparst.get(d)
                if ziel_seite is None or anker not in ziel_seite.ids:
                    f.append(f"{name}: Anker fehlt {url}")
        fehler += f
    # Sitemap
    sitemap_pfade = set()
    for loc in locs:
        p = loc.replace(BASE, "") or "/"
        sitemap_pfade.add(p)
        d = os.path.join(ROOT, p.lstrip("/"), "index.html") if p.endswith("/") else os.path.join(ROOT, p.lstrip("/"))
        if not os.path.isfile(d):
            fehler.append(f"sitemap.xml: {loc} hat keine Datei")
    for datei in geparst:
        p = pfad_von(datei)
        if p != "/404.html" and p not in sitemap_pfade:
            fehler.append(f"sitemap.xml: {p} fehlt")
    # Neue Inhaltsseiten: vorhanden und von /aevo/ verlinkt
    aevo = geparst.get(os.path.join(ROOT, "aevo", "index.html"))
    for p in NEUE_SEITEN:
        if p not in seitenpfade:
            fehler.append(f"Inhaltsseite {p} fehlt")
        elif aevo is not None and p not in aevo.links:
            fehler.append(f"aevo/index.html: kein Link auf {p}")
    for pflicht in ("CNAME", ".nojekyll", "robots.txt"):
        if not os.path.isfile(os.path.join(ROOT, pflicht)):
            fehler.append(f"{pflicht} fehlt")
    fehler += pruefe_robots()
    fehler += pruefe_llms(locs)

    print(f"{geprueft} Seiten, {links} interne Links und Quellen, {len(locs)} Sitemap-Einträge geprüft.")
    if fehler:
        print(f"{len(fehler)} Befunde:")
        for x in fehler:
            print("  " + x)
        return 1
    print("Alles grün.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Prüft die Website ohne Abhängigkeiten: python3 tools/pruefen.py

1. Wohlgeformtheit: jedes geöffnete Element wird geschlossen, in der richtigen Reihenfolge (html.parser).
2. Interne Links und Quellen: jedes href/src auf eine eigene Datei existiert, jeder #Anker hat ein Ziel.
3. SEO-Grundlagen je Seite: lang="de", ein <title>, Meta-Description, genau eine h1, kanonische URL passend zum Pfad,
   gültiges JSON-LD, Alt-Text an jedem Bild, Sitemap-Einträge zeigen auf echte Seiten.
4. Hausregeln: keine Gedankenstriche im sichtbaren Text, „IHK" nie in Titel, Description oder Überschriften,
   Marke klein geschrieben, Pflichthinweis im Fuß jeder Seite, keine externen Skripte, Stile oder Schriften.

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
PFLICHT = ("Für die AEVO-Prüfung bei deiner IHK oder HWK. Jede Aufgabe folgt dem Rahmenplan der AEVO und dem Format "
           "der schriftlichen Prüfung. Jede Lösung ist mit Gesetz und Fundstelle belegt, Rechtsstand 22.10.2026. "
           "Eigene Übungsfragen, unabhängig von IHK, DIHK und HWK.")
SKIP_DIRS = {".git", "screenshots", "_seo", "tools"}


class Seite(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.fehler = [], []
        self.ids, self.links, self.srcs = set(), [], []
        self.title, self.desc, self.canonical, self.lang = "", None, None, None
        self.h1 = 0
        self.headings, self.ld = [], []
        self.text, self.footer_text = [], []
        self._in = {"title": False, "script_ld": False, "head": False, "footer": 0, "h": 0, "style": False, "script": False}
        self._hbuf, self._ldbuf = [], []
        self.imgs_ohne_alt = 0
        self.extern = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        if "id" in a:
            if a["id"] in self.ids:
                self.fehler.append(f"doppelte id #{a['id']}")
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in["title"] = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
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
        if re.fullmatch(r"h[1-6]", tag):
            self._in["h"] += 1
            self._hbuf = []
            if tag == "h1":
                self.h1 += 1
        if tag == "img" and not a.get("alt", "").strip() and a.get("role") != "presentation":
            self.imgs_ohne_alt += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
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
        if re.fullmatch(r"h[1-6]", tag):
            self._in["h"] -= 1
            self.headings.append("".join(self._hbuf))

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


def main():
    fehler, geprueft, links = [], 0, 0
    geparst = {}
    for datei in sorted(seiten()):
        s = Seite()
        with open(datei, encoding="utf-8") as fh:
            s.feed(fh.read())
        s.close()
        geparst[datei] = s
    for datei, s in geparst.items():
        geprueft += 1
        pfad = pfad_von(datei)
        name = os.path.relpath(datei, ROOT)
        f = [f"{name}: {x}" for x in s.fehler]
        if s.stack:
            f.append(f"{name}: nicht geschlossen: " + ", ".join(f"<{t}> Zeile {p[0]}" for t, p in s.stack))
        if s.lang != "de":
            f.append(f"{name}: lang ist nicht de")
        if not s.title.strip():
            f.append(f"{name}: kein <title>")
        if not s.desc:
            f.append(f"{name}: keine Meta-Description")
        elif not 70 <= len(s.desc) <= 170:
            f.append(f"{name}: Description hat {len(s.desc)} Zeichen (70 bis 170)")
        if s.h1 != 1:
            f.append(f"{name}: {s.h1} h1 statt genau einer")
        ist_404 = name == "404.html"
        if not ist_404 and s.canonical != BASE + pfad:
            f.append(f"{name}: kanonisch {s.canonical} statt {BASE + pfad}")
        for block in s.ld:
            try:
                json.loads(block)
            except ValueError as e:
                f.append(f"{name}: JSON-LD ungültig ({e})")
        if not s.ld:
            f.append(f"{name}: kein JSON-LD")
        if s.imgs_ohne_alt:
            f.append(f"{name}: {s.imgs_ohne_alt} Bilder ohne Alt-Text")
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
        fuss = re.sub(r"\s+", " ", " ".join(s.footer_text))
        if PFLICHT not in fuss:
            f.append(f"{name}: Pflichthinweis fehlt im Fuß")
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
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
        locs = re.findall(r"<loc>([^<]+)</loc>", fh.read())
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
    for pflicht in ("CNAME", ".nojekyll", "robots.txt"):
        if not os.path.isfile(os.path.join(ROOT, pflicht)):
            fehler.append(f"{pflicht} fehlt")

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

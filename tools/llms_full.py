#!/usr/bin/env python3
"""Erzeugt llms-full.txt: den sichtbaren Text der wichtigsten Seiten als Markdown, für Sprachmodelle.

    python3 tools/llms_full.py          schreibt llms-full.txt neu
    python3 tools/llms_full.py --pruefen  Rückgabewert 1, wenn llms-full.txt nicht zum HTML passt

Gelesen wird nur <main> jeder Seite. Ausgelassen: Skripte, Brotkrümel, versteckte Elemente (hidden, aria-hidden),
Bilder. Die Demo-Frage steht über die Fassung ohne JavaScript drin (Frage und Lösung). Ohne Abhängigkeiten.
"""
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://becertain.app"
ZIEL = os.path.join(ROOT, "llms-full.txt")

# Reihenfolge = Reihenfolge in der Datei. Rechtsseiten fehlen absichtlich (in llms.txt verlinkt).
SEITEN = [
    "/",
    "/aevo/",
    "/aevo/pruefung/",
    "/aevo/fragen/",
    "/aevo/handlungsfeld-1/",
    "/aevo/handlungsfeld-2/",
    "/aevo/handlungsfeld-3/",
    "/aevo/handlungsfeld-4/",
    "/support/",
]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p": "", "h1": "# ", "h2": "## ", "h3": "### ", "li": "- ", "summary": "### ", "dd": ""}
AUSLASSEN = {"script", "style", "svg", "nav", "picture", "button", "template"}


class Markdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = 0
        self.skip = 0
        self.stack = []
        self.bloecke = []
        self.puffer = []
        self.prefix = None
        self.dt = None
        self.link = None
        self.title = ""
        self._in_title = False
        self.stand = None

    def _flush(self):
        text = re.sub(r"\s+", " ", "".join(self.puffer).replace("\u00ad", "")).strip()
        if text and self.prefix is not None:
            self.bloecke.append(self.prefix + text)
        self.puffer, self.prefix = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if a.get("data-stand") and not self.stand:
            self.stand = a["data-stand"]
        if tag == "main":
            self.in_main += 1
        if tag in VOID:
            if tag == "br" and self.in_main and not self.skip:
                self.puffer.append(" ")
            return
        versteckt = "hidden" in a or a.get("aria-hidden") == "true" or tag in AUSLASSEN
        self.stack.append((tag, versteckt))
        if versteckt:
            self.skip += 1
        if not self.in_main or self.skip:
            return
        if tag in BLOCK:
            self._flush()
            self.prefix = BLOCK[tag]
            if tag == "dd" and self.dt:
                self.prefix = f"- **{self.dt}:** "
                self.dt = None
        elif tag == "dt":
            self._flush()
            self.prefix = ""
        elif tag == "a":
            href = a.get("href", "")
            if href.startswith("/"):
                href = BASE + href
            elif href.startswith("#"):
                href = ""
            self.link = href
            self.puffer.append("[" if href else "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in VOID:
            return
        if not self.stack:
            return
        offen, versteckt = self.stack.pop()
        if versteckt:
            self.skip -= 1
            return
        if tag == "main":
            self._flush()
            self.in_main -= 1
        if not self.in_main or self.skip:
            return
        if tag in BLOCK:
            self._flush()
        elif tag == "dt":
            self.dt = re.sub(r"\s+", " ", "".join(self.puffer)).strip()
            self.puffer, self.prefix = [], None
        elif tag == "a":
            if self.link:
                self.puffer.append(f"]({self.link})")
            self.link = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.in_main and not self.skip:
            if self.prefix is None:
                self.prefix = ""
            self.puffer.append(data)


def seite_md(pfad):
    datei = os.path.join(ROOT, pfad.strip("/"), "index.html") if pfad != "/" else os.path.join(ROOT, "index.html")
    with open(datei, encoding="utf-8") as fh:
        p = Markdown()
        p.feed(fh.read())
        p.close()
    kopf = [f"Seite: {BASE}{pfad}", f"Titel: {p.title.strip()}"]
    if p.stand:
        kopf.append(f"Stand: {p.stand}")
    return "\n".join(kopf) + "\n\n" + "\n\n".join(p.bloecke)


def erzeuge():
    teile = [
        "# becertain: Volltext der wichtigsten Seiten",
        "",
        "> Sichtbarer Text von becertain.app als Markdown, erzeugt aus dem HTML mit tools/llms_full.py. "
        "Kurzfassung und Seitenliste: https://becertain.app/llms.txt. Anbieter: Sergej Markwart, mindcom, Rheine.",
    ]
    for pfad in SEITEN:
        teile.append("\n---\n")
        teile.append(seite_md(pfad))
    return "\n".join(teile).rstrip() + "\n"


def main():
    text = erzeuge()
    if "--pruefen" in sys.argv:
        try:
            with open(ZIEL, encoding="utf-8") as fh:
                alt = fh.read()
        except FileNotFoundError:
            alt = ""
        if alt != text:
            print("llms-full.txt passt nicht zum HTML. Neu erzeugen: python3 tools/llms_full.py")
            return 1
        return 0
    with open(ZIEL, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"llms-full.txt geschrieben: {len(text.split())} Wörter, {len(SEITEN)} Seiten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

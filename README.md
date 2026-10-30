# pruefungstrainer-web · becertain.app

Website der App-Familie becertain: Startseite, Produktseite je Prüfung (zuerst `/aevo/`) mit Inhaltsseiten darunter (SEO-Hub, BRIEF Abschnitt 6) und die Seiten, die der App Store verlangt (Datenschutz, Nutzungsbedingungen, Support, Impressum). SEO-Maßnahmen und Quellen: `../docs/store/03-seo-massnahmen.md`. Regeln in `../CLAUDE.md`, Übergabe in `~/Documents/pruefungstrainer-research/BRIEF.md`.

## Stack

- Reines HTML und CSS, kein Framework, kein Build-Schritt. Eine kleine Datei `assets/site.js` (ohne Abhängigkeiten, ohne Netzwerk, ohne Speicher) für das Einblenden beim Scrollen, den Balken „Chance zu bestehen“ und die Demo-Frage auf `/aevo/`. Ohne JavaScript bleibt alles lesbar.
- Schrift: Systemschrift (SF Pro und SF Mono auf Apple, sonst Segoe UI, Roboto oder Inter, falls installiert). Keine externen Schriften, keine Anfragen an andere Server.
- Farben, Raster und Radien aus `../pruefungstrainer-ios/BecertainDesign/README.md` als CSS-Variablen in `assets/site.css`, Light und Dark über `prefers-color-scheme`.
- Keine Cookies, keine Tracker, deshalb kein Cookie-Hinweis.
- Hosting: GitHub Pages mit eigener Domain.

## Struktur

```
.
├── index.html                  Startseite becertain
├── aevo/index.html             Produktseite AEVO Prüfung · becertain, Hub für AEVO
│   ├── pruefung/               AEVO-Prüfung: Ablauf, Dauer, Aufgaben, Bestehen (FAQ)
│   ├── fragen/                 AEVO-Prüfungsfragen: Aufbau und Aufgabentypen
│   └── handlungsfeld-1/ … -4/  Themen je Handlungsfeld und eine Frage zum Ausprobieren
├── datenschutz/index.html      App und Website, App-Teil wortgleich mit Texte.swift
├── nutzungsbedingungen/        wortgleich mit Texte.swift
├── impressum/  support/  404.html
├── assets/                     site.css, site.js, favicon.svg, icon-180.png, icon-512.png, og-*.png
│   └── screens/                App-Screens aus pruefungstrainer-ios/Store/raw/1206x2622, 420 und 840 px, WebP mit PNG-Fallback
├── sitemap.xml  robots.txt  llms.txt  llms-full.txt (aus dem HTML erzeugt)
├── CNAME                       becertain.app
├── .nojekyll                   GitHub liefert alles ohne Jekyll aus
├── tools/pruefen.py            Prüfer (Wohlgeformtheit, Links, SEO, strukturierte Daten, Hausregeln, Crawler-Dateien)
├── tools/llms_full.py          schreibt llms-full.txt aus dem sichtbaren Text der wichtigsten Seiten
├── screenshots/                Prüfbilder 390 px und 1280 px (in .gitignore, nicht veröffentlicht)
└── SEO_CHANGELOG.md            jede SEO-Änderung mit Datum, Grund, Messtermin
```

## Lokal ansehen und prüfen

```bash
cd ~/Documents/pruefungstrainer/pruefungstrainer-web
python3 -m http.server 8000
# im Browser: http://localhost:8000

python3 tools/pruefen.py
# „Alles grün." oder eine Liste der Befunde, Rückgabewert 1
```

Der Prüfer braucht nur Python 3. Er prüft: geschlossene Elemente, interne Links und Anker, nichtssagende Ankertexte, `lang="de"`, Titel (höchstens 60 Zeichen), Description (70 bis 155 Zeichen), Open Graph und Twitter Card, genau eine h1 und keine übersprungene Überschriftenebene, kanonische URL, Bilder mit Alt-Text, Breite, Höhe und `loading="lazy"`, JSON-LD (gültig, Pflichtfelder je Typ, @id-Verweise, FAQ sichtbar, Brotkrümel sichtbar, keine Bewertungen), sichtbares Datum `data-stand` gleich `dateModified` gleich `lastmod`, keine externen Skripte oder Schriften, keine Gedankenstriche, „IHK" nie in Titel, Description oder Überschriften, Marke klein, nie die genaue Fragenzahl, verbotene Wörter auf den Inhaltsseiten, Pflichthinweis im Fuß jeder Seite, Sitemap vollständig, `robots.txt` mit KI-Crawlern, `llms.txt` vollständig, `llms-full.txt` aktuell. Vor jedem Push laufen lassen.

Nach jeder Textänderung an Start, AEVO-Seiten oder Support: `python3 tools/llms_full.py`, sonst meldet der Prüfer eine veraltete `llms-full.txt`. Ändert sich eine Seite, `dateModified`, `data-stand` und `lastmod` in der Sitemap gemeinsam auf das neue Datum setzen.

## Texte ändern

- Datenschutz und Nutzungsbedingungen sind wortgleich mit `pruefungstrainer-ios/Motor/Sources/Motor/Texte/Texte.swift` (Enums `Datenschutz`, `Nutzungsbedingungen`, `Impressum`). Wer einen Satz in der App ändert, ändert ihn hier mit, und umgekehrt. Datum unter „Stand" anpassen.
- Einzige Abweichung: Der Abschnitt „Nutzungsstatistik" steht im Web ohne den Vermerk „[TELEMETRIE: Platzhalter.]", der Inhalt ist gleich.
- Pflichthinweis steht im Fuß jeder Seite und auf `/aevo/` als Hinweis, wortgleich mit dem Paket. Ändert er sich, alle Seiten und `tools/pruefen.py` (Konstante `PFLICHT`) anpassen.
- Kopf und Fuß sind in jeder Seite ausgeschrieben. Eine Änderung dort gilt für alle 13 HTML-Dateien.
- Fragenzahl je Handlungsfeld auf den Inhaltsseiten (über 140, über 180, über 370, über 140) und die Demo-Aufgaben stammen aus `aevo-1.0.0.json` und `STATISTIK.md`. Bei jedem Paket-Update prüfen, ob Zahlen und Aufgaben noch stimmen.

## Erstes Deployment (Sergej)

1. **Repo anlegen:** auf GitHub ein neues Repo, zum Beispiel `becertain-web`, öffentlich (GitHub Pages ist für private Repos nur mit bezahltem Plan möglich).
2. **Code pushen:** Das lokale Repo mit Branch `main` gibt es schon, es fehlt nur das Ziel auf GitHub.
   ```bash
   cd ~/Documents/pruefungstrainer/pruefungstrainer-web
   git status                      # offene Änderungen erst committen
   git remote add origin git@github.com:sergejma/becertain-web.git
   git push -u origin main
   ```
3. **Pages aktivieren:** Repo › Settings › Pages › Source „Deploy from a branch", Branch `main`, Ordner `/ (root)`, Save.
4. **Eigene Domain:** Settings › Pages › Custom domain `becertain.app`, Save. Die Datei `CNAME` liegt schon im Repo. Empfohlen: die Domain vorher unter GitHub › Settings (Konto) › Pages › „Add a domain" verifizieren, dann kann sie niemand anderes auf GitHub Pages nutzen (GitHub legt dafür einen TXT-Record fest, den du beim Registrar einträgst).
5. **DNS beim Registrar von becertain.app:**
   - Apex `becertain.app`, vier A-Records:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Optional für IPv6, vier AAAA-Records:
     ```
     2606:50c0:8000::153
     2606:50c0:8001::153
     2606:50c0:8002::153
     2606:50c0:8003::153
     ```
   - `www.becertain.app`: CNAME auf `sergejma.github.io`
   - Vorhandene A-, AAAA- oder CNAME-Einträge des Registrars (Parkseite, Weiterleitung) vorher löschen.
   - Ausbreitung meist 5 bis 60 Minuten, höchstens 24 Stunden. Prüfen: `dig becertain.app +short`
6. **HTTPS erzwingen:** Settings › Pages › „Enforce HTTPS" anhaken, sobald GitHub das Zertifikat ausgestellt hat (meist nach 10 bis 30 Minuten). Pflicht: `.app` steht auf der HSTS-Preload-Liste, Browser öffnen die Domain nur über HTTPS. Bis das Zertifikat da ist, zeigt der Browser einen Fehler; das ist normal.
7. **Prüfen:** `https://becertain.app/`, `https://www.becertain.app/` (leitet auf die Hauptdomain), `https://becertain.app/datenschutz/` und eine Adresse, die es nicht gibt (zeigt `404.html`).
8. **Google Search Console:** Domain-Property `becertain.app` anlegen (TXT-Record beim Registrar), dann `https://becertain.app/sitemap.xml` einreichen.

## Livegang der App (Sergej)

1. **App Store Connect:** Datenschutz-URL `https://becertain.app/datenschutz/`, Support-URL `https://becertain.app/support/`, Marketing-URL `https://becertain.app/aevo/`. Die Nutzungsbedingungen `https://becertain.app/nutzungsbedingungen/` als eigene Lizenzvereinbarung (EULA) eintragen oder in die Beschreibung verlinken; ohne Eintrag gilt die Standard-Lizenz von Apple.
2. **Store-Badge:** das Badge „Laden im App Store" von Apple (Apple Marketing Tools, deutsch, schwarz und weiß) als SVG nach `assets/` legen. In `index.html` und `aevo/index.html` jeweils den Kommentar `APP-STORE-BADGE` suchen und den Platzhalter `<p class="store-slot" …>Bald im App Store</p>` ersetzen durch einen Link `<a href="https://apps.apple.com/de/app/…/id…">` mit dem Badge als `<img alt="Laden im App Store">`. Auf der Startseite zusätzlich den Chip „Bald im App Store" entfernen.
3. **Strukturierte Daten:** in `aevo/index.html` im Block `MobileApplication` `"downloadUrl"` und `"sameAs"` mit der App-Store-URL ergänzen. Keine Bewertungen eintragen, solange es keine echten gibt.
4. **Screenshots:** stehen schon in `assets/screens/`. Kommen neue Rohbilder, neu erzeugen: `sips --resampleWidth <420|840>` für PNG, `cwebp -q 80 -m 6 -resize <420|840> 0` für WebP, Dateinamen gleich lassen, Alt-Texte in `aevo/index.html` prüfen.
5. `llms.txt` (Status „bald im App Store“ ändern) und `SEO_CHANGELOG.md` nachziehen, `python3 tools/llms_full.py`, `python3 tools/pruefen.py`, pushen.

## Updates

```bash
python3 tools/pruefen.py && git add -A && git commit -m "<was sich für Besucher ändert>" && git push
```

GitHub Pages baut in ein bis zwei Minuten neu. Jede Änderung an Titeln, Descriptions, URLs oder neuen Seiten kommt mit Datum in `SEO_CHANGELOG.md`.

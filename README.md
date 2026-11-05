# pruefungstrainer-web · becertain.app

Website der App-Familie becertain: Startseite, Produktseite je Prüfung (zuerst `/aevo/`) mit Inhaltsseiten darunter (SEO-Hub, BRIEF Abschnitt 6) und die Seiten, die der App Store verlangt (Datenschutz, Nutzungsbedingungen, Support, Impressum). SEO-Maßnahmen und Quellen: `../docs/store/03-seo-massnahmen.md`. Regeln in `../CLAUDE.md`, Übergabe in `~/Documents/pruefungstrainer-research/BRIEF.md`.

## Stack

- Reines HTML und CSS, kein Framework, kein Build-Schritt. Eine kleine Datei `assets/site.js` (ohne Abhängigkeiten, ohne Netzwerk, ohne Speicher) für das Einblenden beim Scrollen, den Balken „Chance zu bestehen“ und die Demo-Frage auf `/aevo/`, `/34a/` und den Inhaltsseiten. Dazu ein Einzeiler im `<head>` der Seiten mit Skript, der entscheidet, ob der Kopf seinen Einstieg zeigt. Ohne JavaScript bleibt alles sichtbar und lesbar.
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
├── screenshots/                Prüfbilder (in .gitignore, nicht veröffentlicht): vorher/, nachher/ (dazu 320/ und reduziert/), vergleich/
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

## Bewegung und Verhalten

Gebaut nach den Skills von Emil Kowalski (emil-design-eng, animate, choreograph, apple-design, mobile-native, review-animations, break-ui). Grundsatz: Bewegung nur, wo sie etwas erklärt oder bestätigt, und nie auf etwas, das du oft tust. Alles steckt in `assets/site.css`; `assets/site.js` setzt nur Zustände.

### Token

| Token | Wert | Wofür |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | alles, was eintritt, auf Druck antwortet oder den Zustand wechselt |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | Bewegung auf der Fläche, zurzeit ungenutzt |
| `--d-press` / `--d-release` | 100 / 160 ms | Druck auf Knöpfe und Antworten, Loslassen |
| `--d-select` | 140 ms | Antwort wählen (wie `Motion.select` in der App) |
| `--d-check` | 150 ms | Karte färbt sich beim Prüfen (`Motion.checkCardFill`) |
| `--d-state` | 200 ms | Aufklapp-Pfeil, Symbol im Antwortkreis |
| `--d-result` | 240 ms | Rückmeldung und Erklärung erscheinen |
| `--d-reveal` | 500 ms | Einblenden beim Scrollen (Werbefläche, einmal je Element) |
| `--d-fill` | 600 ms, linear | Balken „Chance zu bestehen“ |

Bewegt werden nur `transform`, `opacity` und `clip-path`, nie `transition: all`. Zustände, die Farbe wechseln (gewählt, richtig, falsch), liegen als eigene Ebenen (`::before`, `::after`) über der Karte und blenden über Opazität.

### Wo sich etwas bewegt und warum

- **Kopf der Startseite, `/aevo/` und `/34a/`:** ein Einstieg je Besuch. Das Skript im `<head>` setzt die Klasse `einstieg` nur, wenn du von außen kommst (Suchmaschine, Link, direkt); wechselst du innerhalb der Seite, steht der Kopf sofort. CSS-Keyframes mit `animation-fill-mode: both`, weil einmalig.

  | Element | Rolle | Start | Dauer | Bewegung | Beziehung |
  |---|---|---|---|---|---|
  | Überschrift `h1` | führt | 0 ms | 560 ms | Opazität, 12 px hoch | |
  | Rubrik `.label` | Dekoration | 0 ms | 400 ms | nur Opazität | zusammen mit der Überschrift |
  | Gerät `.hero__device` | stützt, weich | 80 ms | 520 ms | Opazität, 16 px hoch | überlappt die Überschrift |
  | Unterzeile `.lead` und Liste `.checks` | stützt | 110 ms | 480 ms | Opazität, 8 px hoch | ein Takt, überlappt |
  | Knöpfe `.actions` | stützt | 200 ms | 420 ms | Opazität, 6 px hoch | überlappt die Unterzeile |
  | Beruhigung `.reassure` | Dekoration | 280 ms | 320 ms | nur Opazität | kommt mit den Knöpfen an |
  | Kopfzeile, Hintergrund | still | | | | |

  Stufen 110, 90 und 80 ms, kürzer werdend, damit es als Welle liest und nicht im Takt. Nach rund 600 ms ist alles da, nichts ist währenddessen gesperrt.
- **Einblenden beim Scrollen:** nur Schaufenster, die du einmal siehst: App-Karten auf der Startseite, Galerie, die drei Beweise, Gratis und Pro. Opazität und 8 px, 500 ms ease-out, Staffel 0, 70, 120 ms. Nur Elemente, die beim Laden unter dem sichtbaren Bereich liegen; was schon im Bild ist, steht. Den Startzustand setzt erst `site.js`, ohne Skript ist alles sichtbar.
- **Balken „Chance zu bestehen“:** füllt sich einmal, wenn er ganz zu sehen ist, linear (es ist ein Fortschritt), 300 ms nach dem Sichtbarwerden, damit die Karte vorher ankommt.
- **Probier eine Frage:** Druck `scale(0.97)` in 100 ms, Loslassen 160 ms. Wählen blendet die Auswahl-Ebene in 140 ms ein; schnelles Umentscheiden setzt am aktuellen Wert an (Transitions, keine Keyframes). Beim Prüfen blendet die Ergebnis-Ebene über die Auswahl (150 ms), das Symbol im Kreis kommt mit Opazität und `scale(0.85)` auf 1. Rückmeldung und Erklärung treten über `@starting-style` ein, Rückmeldung zuerst, Erklärung 60 ms später, je 240 ms. Ein Weichzeichner war nicht nötig, weil nichts an derselben Stelle überblendet. „Noch einmal versuchen“ setzt ohne Bewegung zurück.
- **Aufklapp-Pfeile** (Quelle, FAQ, „So rechnen wir“): Drehung 200 ms als Zustandsanzeige, der Inhalt erscheint sofort.
- **Knöpfe und Zeilen:** `:active` auf jedem Knopf (`scale(0.97)`), auf der Quellenzeile `scale(0.985)`; Verweislisten (`.toc`) dunkeln beim Druck ab, ohne Bewegung.

### Bewusst ohne Bewegung

- Navigation, Kopfzeile, Seitenwechsel und Sprünge zu Ankern (`scroll-behavior` bleibt `auto`): oft benutzt, Bewegung wäre nur Warten.
- Seitenköpfe der Inhalts- und Rechtsseiten: Wer von Google kommt, will lesen.
- Abschnittsköpfe, Einleitungen, Listen, FAQ, Hinweis mit Pflichttext, Fuß: kein Einblenden, Text wartet nicht.
- Die Demo-Karte selbst: Sie ist Bedienung, kein Schaufenster, und Ziel von „Frage ausprobieren“.
- Hover: nur Farbe, sofort, nur mit Maus. Karten haben kein Hover mehr, sie sind keine Links.
- Aufklappen mit Höhen-Animation: würde Layout pro Bild kosten.

### Bewegung reduzieren

Unter `prefers-reduced-motion: reduce` fällt die Choreografie zusammen: Der Kopf blendet als Ganzes in 200 ms ein, ohne Weg und ohne Verzögerung. Einblenden beim Scrollen nur Opazität, ohne Staffel. Der Balken steht gleich auf seinem Wert, Pfeile springen, Rückmeldung und Erklärung blenden nur. Der Druck auf Knöpfe bleibt, er ist Rückmeldung ohne Weg.

### Tiefe, Material, Typografie

- Ebene 1 (`.card`, FAQ, Quelle, Verweisliste): Fläche mit halbtransparenter Kante (`--edge`), kein Schatten. Ebene 2 nur im Schaufenster (App-Karten, Demo, Beweise, Gratis und Pro, Geräte): dazu ein weicher Schatten (`--lift`). In Dark trägt die hellere Fläche die Tiefe.
- Kopfzeile: `position: sticky`, durchscheinend (`backdrop-filter: saturate(180%) blur(20px)`), unten ein Verlauf mit 16 Zwischenstufen (Scrim-Kurve) statt einer Linie. Über leerem Hintergrund unsichtbar, über Inhalt eine weiche Kante. `prefers-reduced-transparency` und `prefers-contrast: more`: deckend mit einer Linie, bei mehr Kontrast in der Farbe der Bedienelemente; alle Kanten werden dann deckend.
- Schriftgrößen in `rem`, damit die Schriftgröße des Browsers mitwächst. Überschriften mit `clamp()`, enger Zeilenhöhe und `letter-spacing: -0.02em`, Fließtext 17 px mit 1,5 und höchstens 65 Zeichen breit, Zahlen mit `tabular-nums`. Lange Wörter trennen auf schmalen Bildschirmen an Silbengrenzen, erst ab 10 Buchstaben.

### Mobile Basis

- `viewport-fit=cover` mit `env(safe-area-inset-*)` an Kopfzeile, Seitenrand und Fuß; `theme-color` je Farbschema in der Farbe des Hintergrunds, weil die Kopfzeile durchscheint.
- `-webkit-tap-highlight-color: transparent`, `-webkit-text-size-adjust: 100%`. `touch-action: manipulation` und `user-select: none` nur auf Bedienelementen, Fließtext bleibt markierbar.
- Jedes `:hover` steht hinter `@media (hover: hover) and (pointer: fine)`. Druck-Rückmeldung über `:active` für alle.
- Eingabefelder mindestens 16 px (zurzeit gibt es keine). Kein `overscroll-behavior: none`, die Seite ist ein Dokument. Kein `100svh`, kein Kopf braucht die volle Höhe.
- Kopfzeile auf schmalen Telefonen: bis 28,75em rückt die Navigation zusammen, mit drei Punkten zeigt die Marke nur ihr Zeichen. Unter 22,5em (320 px oder sehr große Schrift) steht die Navigation unter der Marke und die Kopfzeile scrollt mit. Die Grenzen stehen in `em`, damit eine größere Standardschrift wie ein schmalerer Bildschirm zählt.

### Prüfen

Bildschirmfotos, Bewegung und Grenzfälle prüft ein Chrome ohne Fenster, gesteuert über `--remote-debugging-pipe` (Skripte liegen nicht im Repo). Was es dabei nicht sieht und nur ein echtes iPhone zeigt: wie sich Druck, Wischen in der Galerie und Scroll-Kante anfühlen, Safe Areas im Querformat, das Verhalten von `backdrop-filter` beim Scrollen in Safari und die Silbentrennung von Safari.

## Texte ändern

- Datenschutz und Nutzungsbedingungen sind wortgleich mit `pruefungstrainer-ios/Motor/Sources/Motor/Texte/Texte.swift` (Enums `Datenschutz`, `Nutzungsbedingungen`, `Impressum`). Wer einen Satz in der App ändert, ändert ihn hier mit, und umgekehrt. Datum unter „Stand" anpassen.
- Einzige Abweichung: Der Abschnitt „Nutzungsstatistik" steht im Web ohne den Vermerk „[TELEMETRIE: Platzhalter.]", der Inhalt ist gleich.
- Pflichthinweis steht im Fuß jeder Seite und auf `/aevo/` als Hinweis, wortgleich mit dem Paket. Ändert er sich, alle Seiten und `tools/pruefen.py` (Konstante `PFLICHT`) anpassen.
- Kopf und Fuß sind in jeder Seite ausgeschrieben. Eine Änderung dort gilt für alle 23 HTML-Dateien.
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

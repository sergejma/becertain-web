# SEO-Änderungslog becertain.app

Regel (SEO Blueprint, Muster aus getfaceit.com): Was rankt, wird nicht angefasst. Änderungen klein halten, datieren, Wirkung messen, bevor die nächste kommt. Jeder Eintrag nennt Seite, Änderung, Grund, Erwartung und Messtermin.

## Baseline 26.10.2026

- Domain neu, noch nicht live, keine Search-Console-Daten, kein Sistrix-Wert. Erste Messung erst nach Livegang und Einreichen der Sitemap.
- Suchvolumen laut BRIEF Abschnitt 6 (Google-Daten): „aevo prüfung" 1.650 Suchen (CPC 5,80 €), „ausbilderschein" 6.200, „sachkundeprüfung 34a" 9.100, „34a sachkundeprüfung" 1.900.

## Änderungen

### 26.10.2026: Erster Stand

- Neue Seiten: `/` (Marke becertain), `/aevo/` (Produktseite), `/support/`, `/datenschutz/`, `/nutzungsbedingungen/`, `/impressum/`, `/404.html` (noindex). Alle außer 404 in `sitemap.xml`, `robots.txt` erlaubt alles, `llms.txt` beschreibt Marke und App.
- Titel:
  - `/`: „becertain: Prüfungstrainer mit Erklärung und Fundstelle"
  - `/aevo/`: „AEVO Prüfung üben: App für den Ausbilderschein · becertain" (beide Hauptbegriffe vorn, Marke hinten wie im App-Namen)
  - Rechtsseiten: „<Seite> · becertain"
- H1 `/aevo/`: „AEVO Prüfung üben, mit Fundstelle für jede Antwort."
- Strukturierte Daten als `@graph`: `WebSite`, `Organization` (becertain, Anbieter Sergej Markwart, Kontakt), `WebPage` und `BreadcrumbList` je Unterseite, auf `/aevo/` zusätzlich `MobileApplication` (Preis 0 € für den Download, Pro als Einmalkauf ohne Preisangabe, keine Bewertungen) und `FAQPage` mit fünf Fragen.
- Open Graph je Seite mit eigenem Bild (`og-becertain.png`, `og-aevo.png`, 1200 × 630), kanonische URL je Seite.
- Keine externen Schriften, kein JavaScript, keine Tracker: schnelle Seiten ohne Consent-Banner.
- Grund: App-Store-Einreichung braucht Datenschutz- und Support-URL; `/aevo/` ist der Startpunkt für den SEO-Hub nach BRIEF Abschnitt 6.
- Erwartung: Indexierung aller sechs Seiten innerhalb von zwei Wochen nach Einreichen der Sitemap; erste Impressionen für „aevo prüfung app" und Markensuchen.

### 28.10.2026: Wörter aus der Textprüfung, Pflichthinweis, Rechtsstand

- Grundlage: `docs/texte/01-textpruefung.md` Abschnitt 4, Freigabe Sergej 28.10.2026. Begriffe wie in der App: Fundstelle wird im Werbetext „Paragraf“, in Bedienhinweisen „Quelle“; Proberunde wird Einstiegstest; Simulation wird Probeprüfung; Bestehenswahrscheinlichkeit wird Chance zu bestehen; Prognose mit offenem Rechenweg wird „wie wir rechnen“.
- Titel `/`: „becertain: Prüfungs-Apps mit Erklärung und Paragraf“ (vorher „… Prüfungstrainer mit Erklärung und Fundstelle“). Description `/` und `/aevo/` neu, ohne Fundstelle und Simulation.
- H1 `/`: „Prüfungsfragen mit Erklärung und Paragraf.“ H1 `/aevo/`: „AEVO-Prüfung üben, mit Paragraf zu jeder Antwort.“ Titel `/aevo/` unverändert. Die Regel „bis zur ersten Messung nicht anfassen“ greift noch nicht, die Seite war nicht live.
- `/aevo/`: Abschnitte „Was die App kann“ und „Was anders ist“ statt „Lernen, simulieren, wiederholen“ und „Drei Gründe“, Karte Einstiegstest, FAQ und JSON-LD (`FAQPage`, `MobileApplication`) wortgleich nachgezogen.
- Pflichthinweis auf allen sieben Seiten wortgleich mit `aevo-1.0.0.json` (`paket.pflichthinweis`), dritter Satz „Jede Lösung nennt die Stelle in Gesetz, Verordnung oder Rahmenplan, aus der sie folgt.“, Rechtsstand 26.10.2026 statt 22.10.2026. `tools/pruefen.py` (Konstante `PFLICHT`) und `llms.txt` angepasst.
- `/support/`: Fehlerart „Die Quelle passt nicht“ wie in der App.
- `/nutzungsbedingungen/`: nur die Begriffe (Einstiegstest, volle Probeprüfung, Quelle, Chance zu bestehen), Rechtstext sonst gleich.
- `sitemap.xml` `lastmod` und `dateModified` 2026-10-28.
- Grund: Texte klangen nach Berater- und Juristensprache; die Konkurrenz und die Bücher sagen „Probeprüfung“, „Auswertung“, „Paragraf“. Store, App und Website sagen jetzt dasselbe.
- Erwartung: keine messbare Wirkung vor dem Livegang. Danach prüfen, ob „aevo probeprüfung“ und „aevo prüfung app“ Impressionen bringen.
- Messtermin: mit dem ersten Vergleich vier Wochen nach Livegang.

### 28.10.2026: Produktseite mit App-Screens, Demo-Frage und Beweisen (Entwurf, nicht veröffentlicht)

- `/aevo/`: neue Reihenfolge Kopf mit App-Screen, Galerie mit fünf Screens (Bildtexte aus `docs/store/aevo-screenshot-plan.md`), „Probier eine Frage“ (Aufgabe `aevo-hf3.6-007` aus `aevo-1.0.0.json`, § 21 Abs. 2 BBiG), drei Beweise, Gratis und Pro, Hinweis, FAQ. Abschnitte „Was die App kann“ und „So sieht es aus“ (Platzhalter) entfallen, ihr Inhalt steckt in Galerie und Beweisen. H2 `#gruende` jetzt „Drei Dinge, die du in der App nachprüfen kannst“.
- Titel, Description, H1-Text, Canonical, FAQ und `FAQPage` unverändert; H1 bekommt nur einen Zeilenumbruch für breite Fenster. `MobileApplication` um `screenshot` (fünf PNG, 840 px) ergänzt. `og:image` bleibt `og-aevo.png`.
- `/`: AEVO-Karte mit Screen, neue Karte „Sachkunde § 34a, Bald“ ohne Termin.
- Neu: `assets/screens/` (WebP und PNG, lazy, mit Breite und Höhe), `assets/site.js` (eigene Datei, kein externes Skript).
- Grund: Beweis vor Angebot (Hormozi), echte Screens statt Platzhalter. Erwartung: längere Verweildauer und mehr Klicks auf den Store-Link nach Livegang; vorher nicht messbar.
- Messtermin: mit dem ersten Vergleich vier Wochen nach Livegang.

### 28.10.2026: Fragenzahl „über 800“ (Entwurf, nicht veröffentlicht)

- Freigabe Sergej 28.10.2026: Die Fragenzahl heißt „über 800 Fragen“, nie die genaue Zahl. Gilt, solange das Paket über 800 Aufgaben hat; bei jedem Paket-Update prüfen (heute `aevo-1.0.0.json`: 853).
- `/aevo/` Kopf, Unterzeile: „Über 800 eigene Fragen nach dem Rahmenplan, Probeprüfungen über 180 Minuten, und du siehst, wo dir noch Punkte fehlen.“
- `/aevo/` Gratis und Pro: „40 von über 800 Fragen in zwei Teilen, …“ und „Über 800 Fragen, mit Erklärung und Paragraf.“
- `/` AEVO-Karte: „Über 800 Fragen, jede mit Erklärung und Paragraf. Der Einstiegstest mit 40 davon ist gratis, …“
- Titel, Description, H1, JSON-LD und FAQ unverändert (nennen keine Fragenzahl).
- Grund: Zahl statt Adjektiv; Umfang ist ein Kaufgrund für Pro. Messtermin wie oben.

### 30.10.2026: AEVO-Hub mit sechs Inhaltsseiten, Audit, strukturierte Daten, KI-Suche (Entwurf, nicht veröffentlicht)

Grundlage: SEO Blueprint der Knowledge Base (Keyword Research, On-Page-Elemente, Technischer Audit, Diagnose, Usability), CXL „SEO Prozess“ und „Bottom-of-funnel SEO“, Local SEO Phase 2 (llms.txt, KI-Crawler). Ausführlich mit Quelle je Maßnahme: `../docs/store/03-seo-massnahmen.md`.

- Neue Seiten (je ein Hauptbegriff, Breadcrumb sichtbar und als `BreadcrumbList`, `Article`, auf Handlungsfeld- und Fragen-Seite zusätzlich `LearningResource`):
  - `/aevo/pruefung/` „AEVO-Prüfung: Ablauf, Dauer, Aufgaben, Bestehen · becertain“, Hauptbegriff „aevo prüfung“ mit Info-Zusatz (Ablauf, Dauer, Bestehen); fünf FAQ mit `FAQPage`.
  - `/aevo/fragen/` „AEVO Prüfungsfragen: Aufbau und Aufgabentypen · becertain“, Hauptbegriff „aevo prüfungsfragen“ (100 Suchen), Nebenbegriffe „ada schein prüfungsfragen“, „ausbildereignungsprüfung fragen“.
  - `/aevo/handlungsfeld-1/` bis `-4/` „AEVO Handlungsfeld n: … · becertain“, Themen des Rahmenplans in eigenen Worten, je eine echte Aufgabe zum Ausprobieren (aevo-hf1.5-001, aevo-hf2.5-007, aevo-hf3.2-003, aevo-hf4.3-002; Einfachauswahl, mittel, mit BBiG-Paragraf), Fragenzahl je Feld gerundet (über 140, über 180, über 370, über 140). Suchvolumen für „aevo handlungsfeld“ ist nicht gemessen.
- `/aevo/`: Titel und H1 unverändert. Description 167 auf 154 Zeichen, mit „Starte gratis mit dem Einstiegstest“. Neuer Abschnitt „Mehr zur AEVO-Prüfung“ mit Links auf alle sechs Seiten (vor dem Hinweis). JSON-LD: `Legislation` AEVO (sameAs Wikipedia, gesetze-im-internet.de), `MobileApplication` mit `featureList`, `audience`, `about`, `isAccessibleForFree`; keine Bewertungen.
- `/`: Description mit Handlungsaufforderung, Lead nennt Sergej Markwart (mindcom) in Rheine, Ankertext „Mehr zur App“ wird „Mehr zur AEVO-App“.
- `/datenschutz/`: Description 160 auf 140 Zeichen. Rechtstext unverändert.
- Alle Seiten: `Organization` becertain mit `founder` (Person Sergej Markwart) und `parentOrganization` (mindcom, mindcom.io), `dateModified` 2026-10-30. Auf `/`, `/aevo/`, `/support/` sichtbar „Stand dieser Seite: 30. Oktober 2026“ im Fuß (`data-stand`), auf den neuen Seiten im Kopf.
- `robots.txt`: KI-Crawler ausdrücklich erlaubt (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, CCBot). `llms.txt` nach llmstxt.org mit Kernfakten, Seitenliste, Pflichthinweis, Kontakt; neu `llms-full.txt` (aus dem HTML erzeugt mit `tools/llms_full.py`).
- `sitemap.xml`: zwölf Seiten, `lastmod` 2026-10-30.
- `tools/pruefen.py`: Titel höchstens 60, Description 70 bis 155, Überschriften ohne Sprung, OG passend, Bilder mit Maßen und lazy, Pflichtfelder je Schema-Typ, @id-Verweise, FAQ sichtbar, Brotkrümel sichtbar, Datum sichtbar gleich `dateModified` gleich `lastmod`, verbotene Wörter auf neuen Seiten, nie 853, robots.txt, llms.txt, llms-full.txt aktuell.
- Erwartung: Indexierung der sechs Seiten innerhalb von vier Wochen nach Einreichen; erste Impressionen für „aevo prüfung ablauf“, „aevo prüfungsfragen“, „aevo handlungsfeld 3“. Risiko: `/aevo/` und `/aevo/pruefung/` teilen „aevo prüfung“; in der Search Console auf Wechsel der URL je Suchanfrage achten.
- Messtermin: vier Wochen nach Livegang, dann acht Wochen. Bis dahin Titel und H1 der neuen Seiten nicht anfassen.

## Messung

- Erster Vergleich: vier Wochen nach Livegang in der Search Console (Indexierung, Impressionen und Position für „aevo prüfung", „aevo prüfung app", „ausbilderschein app", „becertain").
- Bis dahin nicht anfassen: Titel und H1 von `/aevo/`, URL-Struktur (`/aevo/` bleibt die Wurzel aller AEVO-Seiten, Inhaltsseiten darunter).
- Search Console: zuerst `/aevo/`, `/aevo/pruefung/`, `/aevo/fragen/`, `/aevo/handlungsfeld-3/` per URL-Prüfung zur Indexierung anmelden, danach die übrigen über die Sitemap.

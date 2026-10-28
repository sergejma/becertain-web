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

## Messung

- Erster Vergleich: vier Wochen nach Livegang in der Search Console (Indexierung, Impressionen und Position für „aevo prüfung", „aevo prüfung app", „ausbilderschein app", „becertain").
- Bis dahin nicht anfassen: Titel und H1 von `/aevo/`, URL-Struktur (`/aevo/` bleibt die Wurzel aller AEVO-Seiten).

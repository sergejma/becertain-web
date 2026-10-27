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

## Messung

- Erster Vergleich: vier Wochen nach Livegang in der Search Console (Indexierung, Impressionen und Position für „aevo prüfung", „aevo prüfung app", „ausbilderschein app", „becertain").
- Bis dahin nicht anfassen: Titel und H1 von `/aevo/`, URL-Struktur (`/aevo/` bleibt die Wurzel aller AEVO-Seiten).
